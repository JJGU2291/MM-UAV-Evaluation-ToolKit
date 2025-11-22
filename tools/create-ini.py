import os

# 根目录路径
root_directory = r'C:\Users\23570\Desktop\TrackEval-master\data\gt\demo\MMMUAVrgb-train'
# 存储 seqLength 的 txt 文件路径
seq_length_file = r'C:\Users\23570\Desktop\TrackEval-master\data\gt\demo\seq-length\train.txt'  # 替换为实际路径

# 读取 txt 文件到字典 {folder_name: seqLength}
seq_length_dict = {}
with open(seq_length_file, 'r') as f:
    for line in f:
        line = line.strip()
        if line and ':' in line:
            folder, length = line.split(':', 1)
            seq_length_dict[folder] = length

# 遍历根目录下的所有子文件夹
for folder_name in os.listdir(root_directory):
    folder_path = os.path.join(root_directory, folder_name)

    if os.path.isdir(folder_path):
        # 从字典获取 seqLength，若不存在则设为 0
        seq_length = seq_length_dict.get(folder_name, '0')

        # 创建 seqinfo.ini 文件内容
        ini_content = f"""[Sequence]
name={folder_name}
imDir=rgb_frame
frameRate=30
seqLength={seq_length}
imWidth=640
imHeight=360
imExt=.jpg
"""
        # 检查并删除旧文件
        ini_file_path = os.path.join(folder_path, 'seqinfo.ini')
        if os.path.exists(ini_file_path):
            os.remove(ini_file_path)
            print(f'Deleted existing {ini_file_path}')

        # 写入新文件
        with open(ini_file_path, 'w') as f:
            f.write(ini_content)

        print(f'{ini_file_path} : seqLength={seq_length}')