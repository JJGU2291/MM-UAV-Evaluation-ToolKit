import os
import shutil

# 指定目录路径
directory = r'C:\Users\23570\Desktop\MOT_train_labels_ir'

# 遍历目录下的所有文件
for filename in os.listdir(directory):
    # 检查文件是否为txt文件
    if filename.endswith('.txt'):
        # 获取文件名（不带扩展名）
        file_basename = os.path.splitext(filename)[0]

        # 创建新的文件夹路径
        new_folder = os.path.join(directory, file_basename)
        gt_folder = os.path.join(new_folder, 'gt')

        # 创建文件夹
        os.makedirs(gt_folder, exist_ok=True)

        # 移动文件到新的路径
        old_file_path = os.path.join(directory, filename)
        new_file_path = os.path.join(gt_folder, 'gt.txt')
        shutil.move(old_file_path, new_file_path)

        print(f'Moved {filename} to {new_file_path}')