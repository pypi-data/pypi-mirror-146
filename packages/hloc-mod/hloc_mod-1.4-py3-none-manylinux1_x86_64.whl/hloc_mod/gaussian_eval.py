from pathlib import Path
import argparse
import numpy as np
import os

from hloc_mod.utils.read_write_model import Image, write_model, Camera
from hloc_mod.utils.read_write_model import qvec2rotmat, rotmat2qvec
from hloc_mod import extract_features, match_features, triangulation, logger, pairs_from_poses


def get_gaussian_camera(id_):
    model_name = 'OPENCV_FISHEYE'
    params = [177.181061, 176.755334, 318.378062, 184.260543, 0.19439516092645015, -0.006566455902626316,
              -0.017857643795486215, 0.004027909384714204]
    camera = Camera(
        id=id_, model=model_name,
        width=int(640), height=int(480), params=params)
    return camera


def parse_poses(path, colmap=False):
    """Parse a list of poses in COLMAP or MLAD quaternion convention."""
    names = []
    poses = []
    with open(path) as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            if line[0] == '#' or line == '':
                continue
            data = line.replace(',', ' ').split()
            ts, p = data[0], np.array(data[1:], float)
            # ts = str(int(float(ts) * 10)).zfill(4)
            # name = 'frame' + ts + '.jpg'
            ts = str(round(float(ts), 1))
            name = ts + '.png'
            # frame0000.jpg
            if colmap:
                q, t = np.split(p, [4])
            else:
                t, q = np.split(p, [3])
                q = q[[3, 0, 1, 2]]  # xyzw to wxyz
            R = qvec2rotmat(q)
            poses.append((ts, R, t))
            names.append(name)
    return names, poses


def build_empty_colmap_model(pose_file_path, sfm_dir):
    """Build a COLMAP model with images and cameras only."""
    cam0 = get_gaussian_camera(0)
    cameras = {0: cam0}

    names, poses = parse_poses(pose_file_path)
    images = {}
    id_ = 0
    for name, (ts, R_cam_to_w, t_cam_to_w) in zip(names, poses):
        R_w_to_cam = R_cam_to_w.T
        t_w_to_cam = -(R_w_to_cam @ t_cam_to_w)

        image = Image(
            id=id_,
            qvec=rotmat2qvec(R_w_to_cam),
            tvec=t_w_to_cam,
            camera_id=0,
            name=name,
            xys=np.zeros((0, 2), float),
            point3D_ids=np.full(0, -1, int))
        images[id_] = image
        id_ += 1

    sfm_dir.mkdir(exist_ok=True, parents=True)
    write_model(cameras, images, {}, path=str(sfm_dir), ext='.bin')


def delete_unused_images(img_dir, pose_file_path):
    """Delete all images in root if they are not contained in timestamps."""
    images = list(img_dir.glob('*.png'))

    names, poses = parse_poses(pose_file_path)
    names = set(names)

    deleted = 0
    for image in images:
        if image.name not in names:
            os.remove(image)
            deleted += 1
    logger.info(f'Deleted {deleted} images in {img_dir}.')


import shutil


def eval_data(model, data_dir):
    data_dir = Path(data_dir)

    ref_images = data_dir / 'img'
    pose_path = data_dir / 'pose.txt'
    output_dir = data_dir / 'output_eval'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    ref_sfm_empty = output_dir / 'sfm_reference_empty'
    ref_sfm = output_dir / 'sfm_superpoint+superglue'

    fconf = extract_features.confs['superpoint_xin']
    mconf = match_features.confs['superglue-fast']

    num_ref_pairs = 20
    ref_pairs = output_dir / f'pairs-db-dist{num_ref_pairs}.txt'

    # Build an empty COLMAP model containing only camera and images
    # from the provided poses and intrinsics.
    build_empty_colmap_model(pose_path, ref_sfm_empty)

    # Match reference images that are spatially close.
    pairs_from_poses.main(ref_sfm_empty, ref_pairs, num_ref_pairs)

    # Extract, match, and triangulate the reference SfM model.
    ffile = extract_features.gaussian_main(model, fconf, ref_images, output_dir)
    mfile = match_features.main(mconf, ref_pairs, fconf['output'], output_dir)
    recon = triangulation.main(ref_sfm, ref_sfm_empty, ref_images, ref_pairs, ffile, mfile)

    return recon.compute_mean_track_length(), \
           recon.compute_mean_observations_per_reg_image(), \
           recon.compute_mean_reprojection_error()


if __name__ == '__main__':
    model = None
    mean_track_length, mean_observations_per_image, mean_reprojection_error = eval_data(model, '/home/xin/Downloads/mono_20220310')