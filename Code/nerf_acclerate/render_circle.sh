#!/bin/bash

# 设置动态链接库路径（必要）
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH

# 渲染命令（你可以修改参数）
python render_imgs_circle.py \
  /root/autodl-tmp/myproject/output/myscene/ckpt.npz \
  /root/autodl-tmp/myproject/nerf_data \
  --dataset_type nerf \
  --traj_type circle \
  --num_views 300 \
  --fps 30 \
  --width 256 \
  --height 256 \
  --radius 7.1206 \
  --offset "0,0.25,0.05"\
  --vec_up  "  -0.2427,0.7714,0.5882"

