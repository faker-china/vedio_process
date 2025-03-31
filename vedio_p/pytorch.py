# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : xff
# @FILE     : pytorch.py
# @Time     : 2024/8/29 下午12:04
#
# @Software : PyCharm
import torch
import torch.nn as nn
import torch.optim as optim


# 定义模型
class LinearModel(nn.Module):
    def __init__(self):
        super(LinearModel, self).__init__()
        self.linear = nn.Linear(in_features=1, out_features=1)

    def forward(self, x):
        return self.linear(x)

    # 创建模型实例


model = LinearModel()

# 定义损失函数和优化器
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# 输入和目标数据
inputs = torch.tensor([[1.0], [2.0], [3.0]], dtype=torch.float32)
targets = torch.tensor([[2.0], [4.0], [6.0]], dtype=torch.float32)

# 训练模型
for epoch in range(100):
    # 前向传播
    outputs = model(inputs)
    loss = criterion(outputs, targets)

    # 反向传播和优化
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/100], Loss: {loss.item():.4f}')