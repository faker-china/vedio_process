import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from sklearn.model_selection import train_test_split
from tqdm import tqdm


# 定义Dataset类，用于加载图片数据
class WatermarkDataset(Dataset):
    def __init__(self, image_paths, watermark_paths, transform=None):
        """
        Args:
            image_paths (list): 原始图像文件路径列表
            watermark_paths (list): 水印图像文件路径列表
            transform (callable, optional): 图像预处理操作
        """
        self.image_paths = image_paths
        self.watermark_paths = watermark_paths
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)  # 数据集的大小

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        watermark_path = self.watermark_paths[idx % len(self.watermark_paths)]  # 水印素材是循环使用的

        image = Image.open(image_path).convert('RGB')  # 打开原始图像
        watermark = Image.open(watermark_path).convert('RGBA')  # 打开水印图像

        # 如果有transform，则对图像进行预处理
        if self.transform:
            image = self.transform(image)
            watermark = self.transform(watermark)

        return image, watermark


# 定义数据预处理操作（包括归一化和数据增强）
transform = transforms.Compose([
    transforms.Resize((256, 256)),  # 调整图像大小为256x256
    transforms.RandomHorizontalFlip(),  # 随机水平翻转
    transforms.RandomRotation(30),  # 随机旋转30度
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.2),  # 随机调整图像颜色
    transforms.ToTensor(),  # 将PIL图像转换为Tensor并归一化到[0, 1]
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # 标准化
])


# 获取文件夹下所有图像路径的辅助函数
def get_image_files_from_folder(folder_path, extensions=('.jpg', '.jpeg', '.png')):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(extensions)]


# 假设你已经有了带水印和不带水印的图像路径
image_folder = r"D:\test\UNet\data\image"  # 存放原始图像的文件夹
watermark_folder = r"D:\test\UNet\data\watermarks"  # 存放水印图像的文件夹

image_paths = get_image_files_from_folder(image_folder)
watermark_paths = get_image_files_from_folder(watermark_folder)

# 分割数据集为训练集和验证集
train_image_paths, val_image_paths = train_test_split(image_paths, test_size=0.2, random_state=42)
train_watermark_paths, val_watermark_paths = train_test_split(watermark_paths, test_size=0.2, random_state=42)

# 创建Dataset实例
train_dataset = WatermarkDataset(image_paths=train_image_paths, watermark_paths=train_watermark_paths,
                                 transform=transform)
val_dataset = WatermarkDataset(image_paths=val_image_paths, watermark_paths=val_watermark_paths, transform=transform)

# 创建DataLoader实例，用于批量加载数据
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=4)

# 打印加载的数据形状
data_iter = iter(train_loader)
images, watermarks = next(data_iter)
print(images.shape, watermarks.shape)  # 查看加载的图像和水印的大小

# 示例：训练模型的一个循环
for epoch in range(10):  # 假设训练10个epoch
    model.train()  # 切换到训练模式
    for batch_idx, (image, watermark) in enumerate(tqdm(train_loader, desc=f"Epoch {epoch + 1}", unit="batch")):
        # 假设你的模型是UNet，这里用model进行训练
        # output = model(image)  # 假设这里是模型输出
        # loss = loss_function(output, watermark)  # 假设你有一个损失函数
        # optimizer.zero_grad()
        # loss.backward()
        # optimizer.step()

        # 打印每个batch的输出形状
        print(f"Batch {batch_idx + 1}, Image shape: {image.shape}, Watermark shape: {watermark.shape}")
