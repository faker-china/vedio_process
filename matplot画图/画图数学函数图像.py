import matplotlib.pyplot as plt
import numpy as np

#0.生成数据
x=np.linspace(-10,10,1000)
y=np.sin(x)

#1.创建画布
plt.figure(figsize=(20,8),dpi=100)

#2.绘制图像
plt.plot(x,y)
plt.grid()

#3.显示图像
plt.show()