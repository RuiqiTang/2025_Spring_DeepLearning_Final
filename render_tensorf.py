'''
    渲染环绕视频
'''
import os
from nerf_accel.tensorf import TensorfRenderer
from utils.camera_path import generate_spiral_path

def main():
    ckpt_path = 'pretrained/final_model.pth'
    out_dir = 'renderings/output_video'
    os.makedirs(out_dir, exist_ok=True)

    renderer = TensorfRenderer(model_path=ckpt_path)

    render_poses = generate_spiral_path(renderer.cameras, n_frames=120)
    renderer.render_video(render_poses, output_dir=out_dir, save_fps=30)

if __name__ == '__main__':
    main()
