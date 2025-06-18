# 2025_Spring_DeepLearning_Final

## 使用docker配置环境
1. 确保当前目录有dockerfile以及requirement.txt

```bash
docker build -t tensorf-cpu .
```

2. 运行容器并挂载本地

```bash
docker run -it --rm -v $(pwd):/app tensorf-cpu /bin/bash
```
容器内的`/app` 路径就是你本地当前目录，代码修改实时生效

3. 在容器内运行，例如：

```bash
python train.py --config configs/tensorf.yaml
```

## B分锅的文件架构
主要开发branch：
- dev_tensoRF
- dev_plenoxels

```
project_root/
├── data/                  # 存放 COLMAP 重建后的图片/pose 数据
├── configs/               # 超参数配置文件
├── logs/                  # TensorBoard 输出等日志
├── renderings/            # 渲染输出视频和图片
├── pretrained/            # 模型保存目录
├── nerf_accel/            # NeRF 加速版本实现代码（如 TensoRF）
├── utils/                 # PSNR、轨迹等辅助工具
├── train_tensorf.py       # 主训练脚本
├── render_tensorf.py      # 渲染新轨迹视频
└── compute_metrics.py     # PSNR 等评价指标计算

```
