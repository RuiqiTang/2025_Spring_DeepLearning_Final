'''
    PSNR等评价指标
'''
import os
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from glob import glob
from PIL import Image

def evaluate_psnr(rendered_dir, gt_dir):
    rendered_images = sorted(glob(os.path.join(rendered_dir, '*.png')))
    gt_images = sorted(glob(os.path.join(gt_dir, '*.png')))
    
    psnr_list = []
    for r, g in zip(rendered_images, gt_images):
        img_r = np.array(Image.open(r)) / 255.0
        img_g = np.array(Image.open(g)) / 255.0
        psnr_val = psnr(img_g, img_r, data_range=1.0)
        psnr_list.append(psnr_val)

    print(f"Average PSNR: {np.mean(psnr_list):.2f} dB")

if __name__ == '__main__':
    evaluate_psnr('renderings/output_video', 'data/test_gt')
