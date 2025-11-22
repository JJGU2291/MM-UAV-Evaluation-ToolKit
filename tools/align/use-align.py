import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取图片 a 和 b
img_a = cv2.imread('transformed_image2.jpg')
img_a = cv2.resize(img_a, (80, 80))
img_b = cv2.imread('transformed_image1.jpg')
img_b = cv2.resize(img_b, (80, 80))

# 将BGR图像转换为RGB（供matplotlib显示）
img_a_rgb = cv2.cvtColor(img_a, cv2.COLOR_BGR2RGB)
img_b_rgb = cv2.cvtColor(img_b, cv2.COLOR_BGR2RGB)

# 定义仿射变换矩阵
affine_matrix = np.float32([
    [8.07382900e-01, 1.83380107e-02, 7.37903474e+01 / 8],
    [-1.83380107e-02, 8.07382900e-01, 7.88069744e+01 / 8]
])

# 对图片 a 进行仿射变换
height, width = img_a.shape[:2]
transformed_img_a = cv2.warpAffine(img_a, affine_matrix, (width, height))

# 转换为RGB格式
transformed_img_a_rgb = cv2.cvtColor(transformed_img_a, cv2.COLOR_BGR2RGB)

# 使用matplotlib显示图像
plt.figure(figsize=(12, 4))

# 显示原始图像A
plt.subplot(1, 3, 1)
plt.imshow(img_a_rgb)
plt.title('Original Image A')
plt.axis('off')

# 显示变换后的图像A
plt.subplot(1, 3, 2)
plt.imshow(transformed_img_a_rgb)
plt.title('Transformed Image A')
plt.axis('off')

# 显示目标图像B
plt.subplot(1, 3, 3)
plt.imshow(img_b_rgb)
plt.title('Image B')
plt.axis('off')

# 保存整个对比图到本地
plt.savefig('comparison_result.png', bbox_inches='tight', dpi=300)

# 单独保存变换后的图像A到本地
cv2.imwrite('transformed_image_a.jpg', transformed_img_a)

# 显示图像窗口
plt.show()