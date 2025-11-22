import torch
import numpy as np

def convert_opencv_to_pytorch_corrected(opencv_matrix, src_size):
    W, H = src_size

    # 构建OpenCV的3x3仿射矩阵
    a, b, tx = opencv_matrix[0]
    c, d, ty = opencv_matrix[1]
    M_opencv = np.array([
        [a, b, tx],
        [c, d, ty],
        [0, 0, 1]
    ], dtype=np.float32)

    # 坐标系转换矩阵
    T1 = np.array([
        [W/2, 0,    W/2],
        [0,   H/2,  H/2],
        [0,    0,    1]
    ], dtype=np.float32)

    T2_inv = np.array([
        [2/W, 0,    -1],
        [0,   2/H,  -1],
        [0,   0,    1]
    ], dtype=np.float32)

    # 计算组合矩阵
    M_combined = T2_inv @ M_opencv @ T1

    # 提取前两行前三列作为PyTorch的仿射矩阵
    pytorch_matrix = torch.tensor([
        [M_combined[0,0], M_combined[0,1], M_combined[0,2]],
        [M_combined[1,0], M_combined[1,1], M_combined[1,2]]
    ], dtype=torch.float32)

    return pytorch_matrix

# ir-rgb
opencv_mat = np.float32(
    [[ 8.27052483e-01,  1.19444060e-02,  7.12148035e+01/8],
     [-1.19444060e-02,  8.27052483e-01, -1.75122477e+01/8]])

#rgb-ir
# opencv_mat = np.float32(
#     [[1.21608358e+00, - 3.50641825e-02, - 8.43251122e+01],
#      [3.50641825e-02,  1.21608358e+00,  1.32566340e+01]])

src_size = (80, 80)

theta = convert_opencv_to_pytorch_corrected(opencv_mat, src_size)

print(theta)