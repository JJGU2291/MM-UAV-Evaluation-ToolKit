import os
import shutil

# 设置基础路径
base_path = r"C:\Users\23570\Desktop\TrackEval-master\data\gt\MMMUAV"
seqmaps_path = os.path.join(base_path, "seqmaps")

# 获取所有挑战属性文件
challenge_files = [f for f in os.listdir(seqmaps_path) if f.startswith("MMMUAV") and f.endswith("-test.txt")]

# 处理每个挑战属性文件
for challenge_file in challenge_files:
    # 提取模态和挑战属性
    parts = challenge_file.split("-")
    modal = parts[0]  # 如 MMMUAVir 或 MMUAVrgb
    challenge = parts[1]  # 挑战属性名
    split = parts[2].split(".")[0]  # 分割类型，如 test

    challenge_dir_name = f"{modal}-{challenge}-{split}"

    # 创建目标文件夹路径
    target_dir = os.path.join(base_path, challenge_dir_name)
    os.makedirs(target_dir, exist_ok=True)

    # 获取该挑战属性的序列号
    seq_file_path = os.path.join(seqmaps_path, challenge_file)
    with open(seq_file_path, 'r') as f:
        lines = f.readlines()
        seq_names = [line.strip() for line in lines if not line.startswith('names')]

    # 复制整个序列文件夹到新创建的挑战属性文件夹
    for seq_name in seq_names:
        for src_modal in ['MMMUAVir-test', 'MMMUAVrgb-test']:
            # 源文件夹路径
            src_folder = os.path.join(base_path, src_modal, seq_name)

            # 目标文件夹路径
            dst_folder = os.path.join(target_dir, seq_name)

            # 如果目标文件夹已存在，先删除
            if os.path.exists(dst_folder):
                shutil.rmtree(dst_folder)

            # 复制整个序列文件夹
            if os.path.exists(src_folder):
                shutil.copytree(src_folder, dst_folder)

    print(f"Created {challenge_dir_name} folder with sequences: {seq_names}")