import os
import shutil

# === 设置路径 ===
base_dir = os.path.abspath(os.path.join(os.getcwd(), "nerf_data"))
images_dir = os.path.join(base_dir, "images")
images_8_dir = os.path.join(base_dir, "images_8")
backup_dir = os.path.join(base_dir, "images_8_backup")

# === 步骤 1: 备份 images_8 到 images_8_backup ===
if not os.path.exists(backup_dir):
    shutil.copytree(images_8_dir, backup_dir)
    print(f"[✓] 已备份 images_8 到 {backup_dir}")
else:
    print(f"[!] 备份目录 {backup_dir} 已存在，跳过备份")

# === 步骤 2: 获取 images 中的文件名（不含路径）===
valid_names = set(os.listdir(images_dir))
print(f"[i] images 中共找到 {len(valid_names)} 个文件")

# === 步骤 3: 过滤 images_8 中无效文件 ===
deleted = 0
for fname in os.listdir(images_8_dir):
    if fname not in valid_names:
        path_to_delete = os.path.join(images_8_dir, fname)
        os.remove(path_to_delete)
        deleted += 1

print(f"[✓] 删除了 images_8 中 {deleted} 个多余文件，保留 {len(valid_names) - deleted} 个文件")