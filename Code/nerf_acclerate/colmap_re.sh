#!/bin/bash

# Exit on error
set -e

# Prevent Qt errors
export QT_QPA_PLATFORM=offscreen

# Prevent XDG errors
export XDG_RUNTIME_DIR=/tmp/runtime-root

# Data paths
DATASET_DIR="$PWD/colmap"
IMAGE_DIR="$PWD/nerf_data/images"
DB_PATH="$DATASET_DIR/database.db"
SPARSE_DIR="$DATASET_DIR/sparse/0"

# Check if directories exist
if [ ! -d "$IMAGE_DIR" ]; then
    echo "Error: Image directory $IMAGE_DIR does not exist"
    exit 1
fi

# Create output directory
mkdir -p "$SPARSE_DIR"

echo "Starting COLMAP reconstruction..."
echo "Images: $IMAGE_DIR"
echo "Database: $DB_PATH"
echo "Output: $SPARSE_DIR"

# Feature extraction (CPU only)
echo "1/3 Extracting features..."
COLMAP_PATH=$(which colmap)
if [ -z "$COLMAP_PATH" ]; then
    echo "Error: COLMAP is not installed or not in PATH"
    echo "Please run setup_env.sh first"
    exit 1
fi

$COLMAP_PATH feature_extractor \
    --database_path "$DB_PATH" \
    --image_path "$IMAGE_DIR" \
    --ImageReader.single_camera 1 \
    --ImageReader.camera_model SIMPLE_RADIAL \
    --SiftExtraction.use_gpu 0

# Feature matching (CPU only)
echo "2/3 Matching features..."
$COLMAP_PATH exhaustive_matcher \
    --database_path "$DB_PATH" \
    --SiftMatching.use_gpu 0

# Sparse reconstruction
echo "3/3 Running sparse reconstruction..."
$COLMAP_PATH mapper \
    --database_path "$DB_PATH" \
    --image_path "$IMAGE_DIR" \
    --output_path "$SPARSE_DIR"

echo "✅ COLMAP reconstruction completed successfully!"



