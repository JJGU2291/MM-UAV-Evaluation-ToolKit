import os


def compare_groundtruth_line_counts(base_dir, train_file):
    """
    比较每个序列中 groundtruth/ir_frame/groundtruth_all.txt 和 groundtruth/rgb_frame/groundtruth_all.txt 的行数是否一致。

    参数:
        base_dir (str): 包含序列文件夹的根目录路径。
        train_file (str): 包含序列名称的文件路径。
    """
    # 读取 train.txt 文件中的序列名称
    with open(train_file, 'r') as f:
        sequences = [line.strip() for line in f.readlines()]

    inconsistent_sequences = []  # 用于存储行数不一致的序列名称

    for sequence in sequences:
        sequence_dir = os.path.join(base_dir, sequence)

        # 检查序列文件夹是否存在
        if not os.path.exists(sequence_dir):
            print(f"序列文件夹 {sequence_dir} 不存在，跳过...")
            continue

        # 构建 groundtruth 文件路径
        ir_gt_path = os.path.join(sequence_dir, "groundtruth", "ir_frame", "groundtruth_all.txt")
        rgb_gt_path = os.path.join(sequence_dir, "groundtruth", "rgb_frame", "groundtruth_all.txt")

        # 检查文件是否存在
        if not os.path.exists(ir_gt_path) or not os.path.exists(rgb_gt_path):
            print(f"序列 {sequence} 中缺少必要的 groundtruth 文件，跳过...")
            continue

        # # 读取文件行数
        # try:
        #     with open(ir_gt_path, 'r') as ir_file:
        #         ir_line_count = sum(1 for line in ir_file)
        #
        #     with open(rgb_gt_path, 'r') as rgb_file:
        #         rgb_line_count = sum(1 for line in rgb_file)
        # except Exception as e:
        #     print(f"读取序列 {sequence} 的 groundtruth 文件时出错：{e}")
        #     continue

        try:
            with open(ir_gt_path, 'r') as ir_file:
                ir_line_count = sum(1 for line in ir_file if line.strip())  # 读取非空行

            with open(rgb_gt_path, 'r') as rgb_file:
                rgb_line_count = sum(1 for line in rgb_file if line.strip())  # 读取非空行
        except Exception as e:
            print(f"读取序列 {sequence} 的 groundtruth 文件时出错：{e}")
            continue

        # 比较行数
        if ir_line_count != rgb_line_count:
            inconsistent_sequences.append(sequence)
            print(
                f"序列 {sequence} 的 groundtruth 文件行数不一致: ir_frame={ir_line_count}, rgb_frame={rgb_line_count}")

    # 打印所有行数不一致的序列名称
    if inconsistent_sequences:
        print("\n行数不一致的序列名称如下：")
        for seq in inconsistent_sequences:
            print(seq)
    else:
        print("所有序列的 groundtruth 文件行数一致。")


# 设置目录和文件路径
base_dir = r'C:\Users\23570\Desktop'
train_file = os.path.join(base_dir, "switch-seqs-train-to-test.txt")

# 调用函数
compare_groundtruth_line_counts(base_dir, train_file)