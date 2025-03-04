```python
import argparse
# 是 Python 标准库中的一个模块，用于命令行参数的解析

from easydict import EasyDict as edict
# EasyDict 是一个将字典转换为对象类型的工具，使得通过点操作符 (.) 来访问字典的键更为方便

import yaml
# yaml 用于读取 YAML 格式的配置文件，这些文件通常用于存储配置信息

import torch
import torch.backends.cudnn as cudnn
# torch：PyTorch 库，是深度学习框架。
# cudnn：用于优化 GPU 加速的选项

from torch.utils.data import DataLoader
# DataLoader：PyTorch 中的一个工具，用于处理数据集，支持批处理、打乱数据等

from tensorboardX import SummaryWriter
# SummaryWriter 是 TensorBoardX 提供的一个接口，用于将训练日志写入到 TensorBoard 中，便于可视化
```