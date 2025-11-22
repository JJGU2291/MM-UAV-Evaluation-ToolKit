import cv2
import os

# 指定输入图片路径和输出图片路径
input_image_path = "ir_after_transf.png"  # 替换为你的输入图片路径
output_image_path = "ir_after_transf_80.png"  # 指定输出图片路径

# 加载输入图片
img = cv2.imread(input_image_path)

# 检查图片是否加载成功
if img is None:
    print(f"未能加载图片：{input_image_path}")
else:
    # 指定目标尺寸为 80x80
    target_size = (80, 80)

    # 调整图片大小
    resized_img = cv2.resize(img, target_size, interpolation=cv2.INTER_LINEAR)

    # 保存处理后的图片
    cv2.imwrite(output_image_path, resized_img)
    print(f"处理后的图片已保存到：{output_image_path}")

# 显示原始图片和处理后的图片（可选）
if img is not None:
    cv2.imshow("Original Image", img)
    cv2.imshow("Resized Image", resized_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()