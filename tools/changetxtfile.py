import os
import shutil
from pathlib import Path


def process_files(sequence_names, groundtruth_dir, backup_dir=None):
    """
    处理指定序列的文本文件，只保留每行的前六个字段

    Args:
        sequence_names: 需要处理的序列名列表
        groundtruth_dir: 所有序列的 groundtruth 文件夹的父路径
        backup_dir: 备份文件的父路径 (可选)
    """
    # 如果提供了备份目录，先进行备份
    if backup_dir:
        for seq_name in sequence_names:
            seq_groundtruth_path = os.path.join(groundtruth_dir, seq_name, 'groundtruth')
            if os.path.exists(seq_groundtruth_path):
                backup_seq_dir = os.path.join(backup_dir, seq_name)
                os.makedirs(backup_seq_dir, exist_ok=True)

                # 复制整个 groundtruth 文件夹
                dst_path = os.path.join(backup_seq_dir, 'groundtruth')
                shutil.copytree(seq_groundtruth_path, dst_path, dirs_exist_ok=True)

        print(f"Backup completed: {backup_dir}")

    # 遍历每个序列
    for seq_name in sequence_names:
        # 构建序列的 groundtruth 文件夹路径
        seq_groundtruth_path = os.path.join(groundtruth_dir, seq_name, 'groundtruth')

        # 检查序列的 groundtruth 文件夹是否存在
        if not os.path.exists(seq_groundtruth_path):
            print(f"Groundtruth folder not found for sequence: {seq_name}")
            continue

        # 只处理 ir_frame 和 rgb_frame 子文件夹
        for folder in ['ir_frame', 'rgb_frame']:
            folder_path = os.path.join(seq_groundtruth_path, folder)

            # 检查子文件夹是否存在
            if not os.path.exists(folder_path):
                print(f"{folder} folder not found for sequence: {seq_name}")
                continue

            # 遍历子文件夹中的所有文本文件
            for filename in os.listdir(folder_path):
                if filename.endswith('.txt'):
                    file_path = os.path.join(folder_path, filename)

                    # 读取文件内容
                    with open(file_path, 'r') as file:
                        lines = file.readlines()

                    # 处理每一行，只保留前六个字段
                    processed_lines = []
                    for line in lines:
                        parts = line.strip().split(',')
                        if len(parts) >= 6:
                            processed_line = ','.join(parts[:6]) + '\n'
                            processed_lines.append(processed_line)
                        else:
                            # 如果行的字段少于6个，保持原样
                            processed_lines.append(line)

                    # 将处理后的内容写回文件
                    with open(file_path, 'w') as file:
                        file.writelines(processed_lines)

                    print(f"Processed file: {file_path}")


def main():
    # 读取序列名 (直接定义路径)
    sequence_file = r"C:\Users\23570\Desktop\switch-seqs-train-to-test.txt"  # 修改为您的文件路径
    if not os.path.exists(sequence_file):
        print(f"Error: {sequence_file} not found")
        return

    try:
        with open(sequence_file, 'r') as file:
            sequence_names = [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Error reading {sequence_file}: {e}")
        return

    if not sequence_names:
        print(f"No sequences found in {sequence_file}")
        return

    # 设置 groundtruth 目录路径 (直接定义路径)
    groundtruth_dir = r"C:\Users\23570\Desktop"  # 修改为您的 groundtruth 目录路径

    # 设置备份目录路径 (可选)
    backup_dir = r"your_backup_directory"  # 修改为您的备份目录路径
    # 如果不需要备份，将 backup_dir 设置为 None
    # backup_dir = None

    # 处理文件
    process_files(sequence_names, groundtruth_dir, backup_dir)


if __name__ == "__main__":
    main()