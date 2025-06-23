import os
import shutil
import json

SPLIT="val"

# 路径设置
base_dir = "/root/autodl-tmp/myproject/nerf_data"
target_base_dir = f"/root/autodl-tmp/myproject/nerf_train_test_val_split/{SPLIT}"

# 确保目标文件夹存在
os.makedirs(os.path.join(target_base_dir, "images"), exist_ok=True)

# 1. 移动 transforms_train.json 文件
src_json_path = os.path.join(base_dir, f"transforms_{SPLIT}.json")
dst_json_path = os.path.join(target_base_dir, f"transforms_{SPLIT}.json")
shutil.move(src_json_path, dst_json_path)
print(f"Moved JSON: {src_json_path} -> {dst_json_path}")

# 2. 读取 json，移动对应图片
with open(dst_json_path, 'r') as f:
    data = json.load(f)

for frame in data["frames"]:
    img_rel_path = frame["file_path"]           # 例："images/DSC02888.JPG"
    img_name = os.path.basename(img_rel_path)   # 例："DSC02888.JPG"
    src_img_path = os.path.join(base_dir, img_rel_path)
    dst_img_path = os.path.join(target_base_dir, "images", img_name)

    if os.path.exists(src_img_path):
        shutil.move(src_img_path, dst_img_path)
        print(f"Moved image: {src_img_path} -> {dst_img_path}")
    else:
        print(f"Warning: source image not found: {src_img_path}")
