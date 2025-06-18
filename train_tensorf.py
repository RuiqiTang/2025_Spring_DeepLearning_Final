'''
主训练脚本
'''
import os
from tensorboardX import SummaryWriter
from nerf_accel.tensorf import TensorfTrainer
from utils.config import load_config

def main():
    config = load_config('configs/tensorf_example.yaml')
    writer = SummaryWriter(log_dir=config['log_dir'])

    trainer = TensorfTrainer(config=config, writer=writer)
    trainer.train()

    # 保存模型
    os.makedirs(config['ckpt_dir'], exist_ok=True)
    trainer.save_model(os.path.join(config['ckpt_dir'], 'final_model.pth'))

if __name__ == '__main__':
    main()
