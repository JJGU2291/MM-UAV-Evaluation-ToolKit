import os

# 定义需要检查的目录
base_dir = r'C:\Users\23570\Desktop'

# 读取train.txt文件中的所有序列文件夹名
with open(os.path.join(base_dir, "switch-seqs-train-to-test.txt"), "r") as file:
    sequence_folders = file.read().splitlines()

# 遍历每个序列文件夹
for folder in sequence_folders:
    print(folder)
    folder_path = os.path.join(base_dir, folder)
    gt_dir = os.path.join(folder_path, "groundtruth", "rgb_frame")

    # 检查groundtruth目录是否存在
    if os.path.exists(gt_dir):
        # 遍历groundtruth目录下的所有标注文件
        for filename in os.listdir(gt_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(gt_dir, filename)

                # 读取并处理每个标注文件
                with open(file_path, "r+") as file:
                    lines = file.readlines()
                    file.seek(0)
                    file.truncate()

                    for line in lines:
                        # 分割行内容
                        parts = line.strip().split(',')
                        if len(parts) == 6:
                            frame, x1, y1, x2, y2, label = parts
                            # 确保坐标满足条件
                            x1, x2 = int(x1), int(x2)
                            y1, y2 = int(y1), int(y2)

                            # 检查并修正坐标
                            if x1 > x2:
                                print('x1 > x2')
                                x1, x2 = x2, x1
                            if y1 > y2:
                                print('y1 > y2')
                                y1, y2 = y2, y1

                            if x1 == 0 and x2 == 0 and y1 == 0 and y2 == 0 and label == 0:
                                print('no label')
                                label = 1

                            if x1 > 0 or x2 > 0 or y1 > 0 or y2 > 0:
                                if label == 1:
                                    print('label')
                                    label = 0

                            # 写回文件
                            file.write(f"{frame},{x1},{y1},{x2},{y2},{label}\n")
                    file.truncate()  # 确保文件大小正确
    print("Done")

print("所有标注文件已检查并修正。")
