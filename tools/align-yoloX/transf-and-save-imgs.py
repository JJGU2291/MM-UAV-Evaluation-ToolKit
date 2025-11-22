import cv2
import numpy as np
import os

def preproc(img, input_size, swap=(2, 0, 1)):
    if len(img.shape) == 3:
        padded_img = np.ones((input_size[0], input_size[1], 3), dtype=np.uint8) * 114
    else:
        padded_img = np.ones(input_size, dtype=np.uint8) * 114

    r = min(input_size[0] / img.shape[0], input_size[1] / img.shape[1])
    resized_img = cv2.resize(
        img,
        (int(img.shape[1] * r), int(img.shape[0] * r)),
        interpolation=cv2.INTER_LINEAR,
    ).astype(np.uint8)
    padded_img[: int(img.shape[0] * r), : int(img.shape[1] * r)] = resized_img

    padded_img = padded_img.transpose(swap)
    padded_img = np.ascontiguousarray(padded_img, dtype=np.float32)
    return padded_img, r

# 指定输入图片路径和输出图片路径
input_image_path = "0001_rgb.jpg"  # 替换为你的输入图片路径
output_image_path = "0001_rgb_after_transf.png"  # 指定输出图片路径

# 加载输入图片
img = cv2.imread(input_image_path)

# 检查图片是否加载成功
if img is None:
    print(f"未能加载图片：{input_image_path}")
else:
    # 指定目标输入尺寸
    input_size = (640, 640)  # 例如目标尺寸为 640x640

    # 执行预处理变换
    padded_img, r = preproc(img, input_size)

    # 将处理后的图像从 CHW 格式转换回 HWC 格式以便保存
    padded_img_hwc = padded_img.transpose((1, 2, 0)).astype(np.uint8)

    # 保存处理后的图像到本地
    cv2.imwrite(output_image_path, padded_img_hwc)
    print(f"处理后的图像已保存到：{output_image_path}")