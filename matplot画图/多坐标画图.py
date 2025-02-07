import matplotlib.pyplot as plt
import random

#0.生成数据
x=range(60)
y_beijing=[random.uniform(10,15) for i in x]
y_shanghai=[random.uniform(15,25) for i in x]

#1.创建画布
fig, axes = plt.subplots(nrows=1,ncols=2,figsize=(20,8),dpi=100)

#2.绘制图像
axes[0].plot(x,y_beijing,color='r',linestyle='--',label="北京")
axes[1].plot(x,y_shanghai,label="上海")

#2.1添加x，y轴刻度
y_ticks=range(40)
x_ticks_label=["11点{}分".format(i) for i in x]
# plt.yticks(y_ticks[::5])
# plt.xticks(x[::5],x_ticks_label[::5])
# #plt.xticks(x_ticks_label[::5])#必须最开始传进去的是数字
#
axes[0].set_xticks(x[::5])
axes[0].set_yticks(y_ticks[::5])
axes[0].set_xticklabels(x_ticks_label[::5])
axes[1].set_xticks(x[::5])
axes[1].set_yticks(y_ticks[::5])
axes[1].set_xticklabels(x_ticks_label[::5])

# #2.2添加网格
# plt.grid(True,linestyle='--',alpha=0.7)
axes[0].grid(True,linestyle='--',alpha=0.7)
axes[1].grid(True,linestyle='--',alpha=0.7)
#
plt.rcParams['font.sans-serif']=['SimHei']#添加如下语句 —设置字体为：SimHei（黑体）画图显示中文黑体
#
# plt.savefig("./test.png")#保存图像
#
# #2.3添加描述
# plt.xlabel("时间")
# plt.ylabel("温度")
# plt.title("一小时温度变化图",fontsize=20)
axes[0].set_xlabel("时间")
axes[0].set_ylabel("温度")
axes[0].set_title("北京一小时温度变化图",fontsize=20)
axes[1].set_xlabel("时间")
axes[1].set_ylabel("温度")
axes[1].set_title("上海一小时温度变化图",fontsize=20)
#显示图例
# plt.legend()
axes[0].legend()
axes[1].legend()
#3.显示图像
plt.show()

