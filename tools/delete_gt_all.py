import os

# 定义数据集目录
dataset_dir = r'C:\Users\23570\Desktop'

# 读取train.txt文件获取所有序列文件夹名
with open(os.path.join(dataset_dir, 'switch-seqs-train-to-test.txt'), 'r') as f:
    train_seqs = [line.strip() for line in f.readlines()]

# 遍历所有序列文件夹
for seq in train_seqs:
    seq_path = os.path.join(dataset_dir, seq)
    groundtruth_all_path = os.path.join(seq_path, 'groundtruth', 'rgb_frame', 'groundtruth_all.txt')

    # 检查文件是否存在，如果存在则删除
    if os.path.isfile(groundtruth_all_path):
        os.remove(groundtruth_all_path)
        print(f"已删除文件：{groundtruth_all_path}")
    else:
        print(f"文件不存在：{groundtruth_all_path}")

print("所有groundtruth_all.txt文件已被删除。")