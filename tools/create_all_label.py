import os

# 定义数据集目录
# dataset_dir = '/mnt/sda/Disk_D/Anti-UAV-VET-train'
dataset_dir = r'C:\Users\23570\Desktop'

# 读取train.txt文件获取所有序列文件夹名
# with open(os.path.join(dataset_dir, 'train.txt'), 'r') as f:
#     train_seqs = [line.strip() for line in f.readlines() if line.strip()]

# 读取train.txt文件获取所有序列文件夹名
with open(os.path.join(dataset_dir, 'switch-seqs-train-to-test.txt'), 'r') as f:
    train_seqs = [line.strip() for line in f.readlines() if line.strip()]


# 遍历所有序列文件夹
for seq in train_seqs:
    print(seq)
    seq_path = os.path.join(dataset_dir, seq)
    # groundtruth_dir = os.path.join(seq_path, 'groundtruth', 'rgb_frame')
    groundtruth_dir = os.path.join(seq_path, 'groundtruth', 'ir_frame')
    # 初始化一个列表来存储所有标注
    all_annotations = []

    # 遍历groundtruth目录下的所有标注文件
    for label_file in sorted(os.listdir(groundtruth_dir)):
        # print(label_file)
        if label_file.startswith('groundtruth_') and label_file.endswith('.txt'):
            label_path = os.path.join(groundtruth_dir, label_file)
            with open(label_path, 'r') as file:
                labels = [line.strip() for line in file.readlines() if line.strip()]

            # 提取目标ID
            target_id = int(label_file.split('_')[-1].split('.')[0])

            # 遍历标注文件中的每一行
            for label in labels:
                label_parts = label.split(',')
                frame_name = label_parts[0]
                x1, y1, x2, y2, is_missing = map(int, label_parts[1:])

                # # 检查是否缺失
                # if is_missing == 0:
                all_annotations.append(f"{frame_name},{target_id},{x1},{y1},{x2},{y2},{is_missing}")

    # 将合并后的标注写入groundtruth_all.txt
    groundtruth_all_path = os.path.join(groundtruth_dir, 'groundtruth_all.txt')
    with open(groundtruth_all_path, 'w') as file:
        for annotation in sorted(all_annotations):
            file.write(annotation + '\n')

print('Merged annotations for all sequences.')