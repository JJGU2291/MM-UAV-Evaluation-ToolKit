import cv2
import numpy as np
import matplotlib.pyplot as plt


def align_images(image_a_path, image_b_path):
    # 读取图片
    image_a = cv2.imread(image_a_path, cv2.IMREAD_GRAYSCALE)
    image_b = cv2.imread(image_b_path, cv2.IMREAD_GRAYSCALE)

    if image_a is None or image_b is None:
        raise ValueError("无法读取图像文件")

    # 初始化ORB检测器
    orb = cv2.ORB_create(nfeatures=5000)

    # 检测关键点和描述子
    key_points_a, descriptors_a = orb.detectAndCompute(image_a, None)
    key_points_b, descriptors_b = orb.detectAndCompute(image_b, None)

    # 使用BFMatcher进行匹配
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors_a, descriptors_b)

    # 按距离排序，保留最佳匹配
    matches = sorted(matches, key=lambda x: x.distance)

    # 获取匹配点
    src_pts = np.float32([key_points_a[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([key_points_b[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # 计算仿射变换矩阵
    affine_matrix, _ = cv2.estimateAffinePartial2D(src_pts, dst_pts)

    # 应用仿射变换到image_a
    aligned_image = cv2.warpAffine(image_a, affine_matrix, (image_b.shape[1], image_b.shape[0]))

    # 可视化结果
    visualize_alignment(image_a, image_b, aligned_image, affine_matrix)

    return affine_matrix


def visualize_alignment(image_a, image_b, aligned_image, affine_matrix):
    # 创建可视化窗口
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # 显示原始图像a
    axes[0].imshow(image_a, cmap='gray')
    axes[0].set_title('a')
    axes[0].axis('off')

    # 显示目标图像b
    axes[1].imshow(image_b, cmap='gray')
    axes[1].set_title('b')
    axes[1].axis('off')

    # 显示对齐后的图像a
    axes[2].imshow(aligned_image, cmap='gray')
    axes[2].set_title('a-to-b_after_align')
    axes[2].axis('off')

    plt.tight_layout()
    plt.show()

    # 打印仿射变换矩阵
    print("\n从图像a到图像b的仿射变换矩阵:")
    print(affine_matrix)


# 使用示例
if __name__ == "__main__":
    # 替换为您的图像路径
    image_a_path = 'ir_after_transf.png'
    image_b_path = 'rgb_after_transf.png'



    affine_matrix = align_images(image_a_path, image_b_path)

    affine_matrix = align_images(image_b_path, image_a_path)
