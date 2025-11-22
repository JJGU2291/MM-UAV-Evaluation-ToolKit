import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 设置字体大小
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 18  # 调整图例字体大小

# 设置基础路径
base_path = r"C:\Users\23570\Desktop\TrackEval-master\data\trackers\MMMUAV"

# 定义挑战属性及其缩写
challenge_attributes = [
    "Extremetarget",
    "Fastmotion",
    "Lowillumination",
    "Objectoverlap",
    "Scalevariation",
    "Similarityclutter",
    "Tinytarget"
]
challenge_abbreviations = [
    "ET",
    "FM",
    "LI",
    "OO",
    "SV",
    "SC",
    "TT"
]

# 初始化数据字典
trackers_data_ir = {}
trackers_data_rgb = {}

# 遍历所有跟踪器
for tracker in os.listdir(base_path):
    tracker_path = os.path.join(base_path, tracker)

    if not os.path.isdir(tracker_path):
        continue

    # 遍历每个跟踪器的挑战属性结果
    for attr, abbrev in zip(challenge_attributes, challenge_abbreviations):
        # 处理IR模态
        result_folder_ir = f"eval_results_ir_{attr}"
        result_path_ir = os.path.join(tracker_path, result_folder_ir, "drone_summary_light.txt")

        if os.path.exists(result_path_ir):
            # 读取文件并提取HOTA值
            df = pd.read_csv(result_path_ir, delim_whitespace=True)  # 使用whitespace分隔读取
            hota_value = df['HOTA'].values[0]  # 假设HOTA值在第二行

            # 收集数据
            if tracker not in trackers_data_ir:
                trackers_data_ir[tracker] = {}
            trackers_data_ir[tracker][abbrev] = hota_value

        # 处理RGB模态
        result_folder_rgb = f"eval_results_rgb_{attr}"
        result_path_rgb = os.path.join(tracker_path, result_folder_rgb, "drone_summary_light.txt")

        if os.path.exists(result_path_rgb):
            # 读取文件并提取HOTA值
            df = pd.read_csv(result_path_rgb, delim_whitespace=True)  # 使用whitespace分隔读取
            hota_value = df['HOTA'].values[0]  # 假设HOTA值在第二行

            # 收集数据
            if tracker not in trackers_data_rgb:
                trackers_data_rgb[tracker] = {}
            trackers_data_rgb[tracker][abbrev] = hota_value

# 获取所有跟踪器名称（去重）
all_trackers = list(set(trackers_data_ir.keys()).union(trackers_data_rgb.keys()))

# ==== 重要修改1：按LI属性排序 ====
# 获取每个跟踪器的LI值（优先使用IR模态的值）
def get_li_value(tracker):
    """获取跟踪器的LI属性值（优先使用IR模态的值）"""
    if tracker in trackers_data_ir and "LI" in trackers_data_ir[tracker]:
        return trackers_data_ir[tracker]["LI"]
    elif tracker in trackers_data_rgb and "LI" in trackers_data_rgb[tracker]:
        return trackers_data_rgb[tracker]["LI"]
    return 0  # 如果没有数据则返回0

# 按LI值降序排列跟踪器
sorted_trackers = sorted(all_trackers, key=lambda x: get_li_value(x), reverse=True)

# 绘制雷达图
num_attributes = len(challenge_abbreviations)
angles = np.linspace(0, 2 * np.pi, num_attributes, endpoint=False).tolist()

# 计算需要的图例行数
num_rows_legend = len(sorted_trackers)
legend_height = num_rows_legend * 0.05  # 每个图例项占用的空间比例

# 创建图形和坐标轴
fig = plt.figure(figsize=(12, 8 + num_rows_legend * 0.3))  # 根据图例数量调整高度
# fig.suptitle('HOTA Values Across Challenge Attributes')  # 总标题

# 创建IR模态子图
ax1 = fig.add_subplot(121, polar=True)
ax1.set_title('IR Modality HOTA')

# 计算IR模态HOTA值的最大值
if trackers_data_ir:
    max_hota_ir = max(max(data.values()) for data in trackers_data_ir.values())
else:
    max_hota_ir = 0

# 绘制每个跟踪器的IR雷达图
for i, tracker in enumerate(sorted_trackers):
    if tracker in trackers_data_ir:
        data = trackers_data_ir[tracker]
        values = [data[abbrev] for abbrev in challenge_abbreviations]
        values += values[:1]  # 闭合图形
        angles_line = angles + angles[:1]

        # 获取颜色和线条样式
        color = ['b', 'orange', 'g', 'r', 'c', 'm', 'y', 'k'][i % 8]
        line_style = ['-', '--', '-.', ':'][i % 4]

        # 绘制线条，线条变粗
        ax1.plot(angles_line, values, label=tracker, color=color, linestyle=line_style, linewidth=3)

ax1.set_ylim(0, max_hota_ir * 1.1 if max_hota_ir > 0 else 1)  # 设置Y轴范围
ax1.set_thetagrids(range(0, int(360 / num_attributes) * num_attributes, int(360 / num_attributes)), challenge_abbreviations)

# 创建RGB模态子图
ax2 = fig.add_subplot(122, polar=True)
ax2.set_title('RGB Modality HOTA')

# 计算RGB模态HOTA值的最大值
if trackers_data_rgb:
    max_hota_rgb = max(max(data.values()) for data in trackers_data_rgb.values())
else:
    max_hota_rgb = 0

# 绘制每个跟踪器的RGB雷达图
for i, tracker in enumerate(sorted_trackers):
    if tracker in trackers_data_rgb:
        data = trackers_data_rgb[tracker]
        values = [data[abbrev] for abbrev in challenge_abbreviations]
        values += values[:1]  # 闭合图形
        angles_line = angles + angles[:1]

        # 获取颜色和线条样式
        color = ['b', 'orange', 'g', 'r', 'c', 'm', 'y', 'k'][i % 8]
        line_style = ['-', '--', '-.', ':'][i % 4]

        # 绘制线条，线条变粗
        ax2.plot(angles_line, values, label=tracker, color=color, linestyle=line_style, linewidth=3)

ax2.set_ylim(0, max_hota_rgb * 1.1 if max_hota_rgb > 0 else 1)  # 设置Y轴范围
ax2.set_thetagrids(range(0, int(360 / num_attributes) * num_attributes, int(360 / num_attributes)), challenge_abbreviations)

# 创建统一的图例，位置上移，每行一个
handles = []
labels = []
for i, tracker in enumerate(sorted_trackers):
    color = ['b', 'orange', 'g', 'r', 'c', 'm', 'y', 'k'][i % 8]
    line_style = ['-', '--', '-.', ':'][i % 4]
    handles.append(plt.Line2D([0], [0], color=color, linestyle=line_style, linewidth=3))
    labels.append(tracker)

fig.legend(handles, labels, loc='lower center', ncol=1, bbox_to_anchor=(0.5, 0.05))  # 每行一个图例

# 调整图形布局，根据图例数量调整底部留白
bottom_margin = -0.2 + num_rows_legend * 0.05  # 底部留白比例
plt.subplots_adjust(bottom=bottom_margin, wspace=0.4)

# 显示图形
plt.show()