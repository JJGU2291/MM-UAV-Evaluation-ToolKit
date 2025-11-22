#将每一个序列中的id整体换一下

import os


def replace_id_in_files(directory):
    # 遍历指定目录下的所有文件
    for filename in os.listdir(directory):
        # 只处理.txt文件
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)

            # 读取并修改内容
            modified_lines = []
            with open(filepath, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) >= 2 and parts[1] == '1':
                        parts[1] = '4'
                    modified_lines.append(','.join(parts))

            # 写回原文件
            with open(filepath, 'w') as f:
                f.write('\n'.join(modified_lines))


if __name__ == '__main__':
    # 使用示例（请替换为实际目录路径）
    target_directory = r'C:\Users\23570\Desktop\TrackEval-master\data\trackers\demo\MMMUAVir-test-one-seq\Test\data'
    replace_id_in_files(target_directory)
    print("ID替换完成！")