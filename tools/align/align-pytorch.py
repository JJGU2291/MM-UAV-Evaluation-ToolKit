import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
from PIL import Image
import torchvision.transforms as T

# 1. 定义仿射变换矩阵（针对80x80输入设计）
# theta_ir_to_rgb = torch.tensor([
#     [1/(8.07382900e-01), 1.83380107e-02, 7.37903474e+01 / 8 / 40],
#     [-1.83380107e-02, 1/(8.07382900e-01), 7.88069744e+01 / 8 / 40]
# ], dtype=torch.float)

theta_rgb_to_ir = torch.tensor([[ 0.8271,  0.0119,  0.0615],
                                [-0.0119,  0.8271, -0.2396]])

# theta_ir_to_rgb = torch.tensor([[ 1.2033, -0.0204, -0.0739],
#                                 [ 0.0204,  1.2033, -0.0386]])


# 2. 图像加载与预处理函数
def load_and_preprocess(img_path, target_size=(80, 80)):
    img = Image.open(img_path).convert('RGB')
    transform = T.Compose([
        T.Resize(target_size),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(img).unsqueeze(0)  # 添加batch维度


# 3. 加载示例图像（替换为你的图片路径）
rgb_tensor = load_and_preprocess(".jpg")
ir_tensor = load_and_preprocess("transformed_image2.jpg")


# 4. 执行仿射变换
def apply_affine_transform(input_tensor, theta):
    # 生成仿射网格 (需要与输入tensor的batch size匹配)
    grid = F.affine_grid(theta.unsqueeze(0), input_tensor.size(), align_corners=False)

    # 应用网格采样
    output = F.grid_sample(
        input_tensor,
        grid,
        mode='bilinear',
        padding_mode='zeros',
        align_corners=False
    )
    return output


transformed_ir = apply_affine_transform(rgb_tensor, theta_rgb_to_ir)


# 5. 反归一化并转换回PIL图像
def tensor_to_pil(tensor):
    inv_normalize = T.Normalize(
        mean=[-0.485 / 0.229, -0.456 / 0.224, -0.406 / 0.225],
        std=[1 / 0.229, 1 / 0.224, 1 / 0.225]
    )
    return T.ToPILImage()(inv_normalize(tensor.squeeze()))


# 6. 可视化对比
plt.figure(figsize=(12, 6))

plt.subplot(131)
plt.title("Original IR")
plt.imshow(tensor_to_pil(ir_tensor))
plt.axis('off')

plt.subplot(132)
plt.title("Transformed IR->RGB")
plt.imshow(tensor_to_pil(transformed_ir))
plt.axis('off')

plt.subplot(133)
plt.title("Original RGB")
plt.imshow(tensor_to_pil(rgb_tensor))
plt.axis('off')

plt.tight_layout()
plt.show()