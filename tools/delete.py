import os


def keep_first_line_only(directory):
    """
    将指定目录下的所有 .txt 文件内容替换为仅保留第一行
    :param directory: 目标目录路径
    """
    # 遍历目录下所有文件
    for filename in os.listdir(directory):
        # 筛选 .txt 文件
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)

            try:
                # 读取第一行内容
                with open(filepath, 'r', encoding='utf-8') as f:
                    first_line = f.readline()

                # 将第一行写回文件（覆盖原内容）
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(first_line)

                print(f"已处理: {filename}")

            except PermissionError:
                print(f"权限不足无法处理: {filename}")
            except UnicodeDecodeError:
                print(f"编码错误文件: {filename} (尝试其他编码)")
            except Exception as e:
                print(f"处理 {filename} 时出错: {str(e)}")


if __name__ == "__main__":
    # 使用示例
    target_dir = r"C:\Users\23570\Desktop\TrackEval-master\data\trackers\demo\MMMUAVir-train\MOT-ir-train\data"  # 替换为你的实际路径
    keep_first_line_only(target_dir)