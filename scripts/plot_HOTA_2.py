import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.font_manager import FontProperties

# 设置字体大小
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['font.family'] = 'Times New Roman'  # 设置全局字体为Times New Roman

# 设置基础路径
base_path = r"../data/trackers/MMMUAV-for-plot"

# 定义挑战属性及其缩写
challenge_attributes = [
    "Extremetarget", "Fastmotion", "Lowillumination",
    "Objectoverlap", "Scalevariation", "Similarityclutter", "Tinytarget"
]
challenge_abbreviations = ["ET", "FM", "LI", "OO", "SV", "SC", "TT"]

# 初始化数据字典
trackers_data_ir = {}
trackers_data_rgb = {}
trackers_overall_ir = {}
trackers_overall_rgb = {}

# 遍历所有跟踪器，收集基础数据
for tracker in os.listdir(base_path):
    tracker_path = os.path.join(base_path, tracker)
    if not os.path.isdir(tracker_path):
        continue

    # 读取整体IR模态HOTA值
    overall_file_ir = os.path.join(tracker_path, "eval_results_ir", "drone_summary_light.txt")
    if os.path.exists(overall_file_ir):
        df = pd.read_csv(overall_file_ir, delim_whitespace=True)
        trackers_overall_ir[tracker] = df['HOTA'].values[0]

    # 读取整体RGB模态HOTA值
    overall_file_rgb = os.path.join(tracker_path, "eval_results_rgb", "drone_summary_light.txt")
    if os.path.exists(overall_file_rgb):
        df = pd.read_csv(overall_file_rgb, delim_whitespace=True)
        trackers_overall_rgb[tracker] = df['HOTA'].values[0]

    # 遍历每个跟踪器的挑战属性结果
    for attr, abbrev in zip(challenge_attributes, challenge_abbreviations):
        # 处理IR模态
        result_folder_ir = f"eval_results_ir_{attr}"
        result_path_ir = os.path.join(tracker_path, result_folder_ir, "drone_summary_light.txt")
        if os.path.exists(result_path_ir):
            df = pd.read_csv(result_path_ir, delim_whitespace=True)
            if tracker not in trackers_data_ir:
                trackers_data_ir[tracker] = {}
            trackers_data_ir[tracker][abbrev] = df['HOTA'].values[0]

        # 处理RGB模态
        result_folder_rgb = f"eval_results_rgb_{attr}"
        result_path_rgb = os.path.join(tracker_path, result_folder_rgb, "drone_summary_light.txt")
        if os.path.exists(result_path_rgb):
            df = pd.read_csv(result_path_rgb, delim_whitespace=True)
            if tracker not in trackers_data_rgb:
                trackers_data_rgb[tracker] = {}
            trackers_data_rgb[tracker][abbrev] = df['HOTA'].values[0]

# ---------------------- 关键修改：统一跟踪器的颜色和线条样式 ----------------------
all_trackers = list(set(trackers_data_ir.keys()).union(set(trackers_data_rgb.keys())))
all_trackers.sort()  # 按名称排序，确保分配稳定

colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
    '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5'
]
line_styles = ['-', '--', '-.', ':']

tracker_color = {tracker: colors[i % len(colors)] for i, tracker in enumerate(all_trackers)}
tracker_linestyle = {tracker: line_styles[i % len(line_styles)] for i, tracker in enumerate(all_trackers)}
# ------------------------------------------------------------------------------

# 按各自HOTA值排序跟踪器
sorted_trackers_ir = sorted(trackers_data_ir.keys(),
                            key=lambda x: trackers_overall_ir.get(x, 0),
                            reverse=True)
sorted_trackers_rgb = sorted(trackers_data_rgb.keys(),
                             key=lambda x: trackers_overall_rgb.get(x, 0),
                             reverse=True)

# 绘制雷达图
num_attributes = len(challenge_abbreviations)
angles = np.linspace(0, 2 * np.pi, num_attributes, endpoint=False).tolist()

# 计算图例所需空间
num_rows_legend = max(len(sorted_trackers_ir), len(sorted_trackers_rgb))
legend_height = num_rows_legend * 0.05
fig = plt.figure(figsize=(12, 8 + num_rows_legend * 0.4))

# 字体设置
normal_font = FontProperties()
bold_font = FontProperties(weight='bold', size=18)

# ---------------------- IR模态子图 ----------------------
ax1 = fig.add_subplot(121, polar=True)
ax1.set_title('HOTA (IR)', y=1.1)

max_hota_ir = max(max(data.values()) for data in trackers_data_ir.values()) if trackers_data_ir else 0
ax1.set_ylim(0, max_hota_ir * 1.1 if max_hota_ir > 0 else 1)
ax1.set_thetagrids(range(0, int(360 / num_attributes) * num_attributes, int(360 / num_attributes)),
                   challenge_abbreviations)

handles_ir = []
labels_ir = []
highlighted_trackers = ["DeepSORT", "BoT-SORT", "Deep OC-SORT", "BoostTrack","BoostTrack++",]  # 需要加*的Tracker

for tracker in sorted_trackers_ir:
    if tracker in trackers_data_ir:
        data = trackers_data_ir[tracker]
        values = [data[abbrev] for abbrev in challenge_abbreviations] + [data[challenge_abbreviations[0]]]
        angles_line = angles + angles[:1]

        color = tracker_color[tracker]
        linestyle = tracker_linestyle[tracker]
        line_width = 3 if sorted_trackers_ir.index(tracker) < 2 else 3

        line, = ax1.plot(angles_line, values, color=color, linestyle=linestyle, linewidth=line_width)
        handles_ir.append(line)

        overall_value = trackers_overall_ir.get(tracker, 0)
        name_label = tracker + '*' if tracker in highlighted_trackers else tracker
        labels_ir.append(f"{name_label} ({overall_value:.2f})")

leg1 = ax1.legend(handles_ir, labels_ir, loc='lower center', bbox_to_anchor=(0.5, -1.3),
                  ncol=1, columnspacing=1.0, handlelength=2.0)
for i, text in enumerate(leg1.get_texts()):
    if i < 2:
        text.set_fontproperties(bold_font)

# ---------------------- RGB模态子图 ----------------------
ax2 = fig.add_subplot(122, polar=True)
ax2.set_title('HOTA (RGB)', y=1.1)

max_hota_rgb = max(max(data.values()) for data in trackers_data_rgb.values()) if trackers_data_rgb else 0
ax2.set_ylim(0, max_hota_rgb * 1.1 if max_hota_rgb > 0 else 1)
ax2.set_thetagrids(range(0, int(360 / num_attributes) * num_attributes, int(360 / num_attributes)),
                   challenge_abbreviations)

handles_rgb = []
labels_rgb = []

for tracker in sorted_trackers_rgb:
    if tracker in trackers_data_rgb:
        data = trackers_data_rgb[tracker]
        values = [data[abbrev] for abbrev in challenge_abbreviations] + [data[challenge_abbreviations[0]]]
        angles_line = angles + angles[:1]

        color = tracker_color[tracker]
        linestyle = tracker_linestyle[tracker]
        line_width = 3 if sorted_trackers_rgb.index(tracker) < 2 else 3

        line, = ax2.plot(angles_line, values, color=color, linestyle=linestyle, linewidth=line_width)
        handles_rgb.append(line)

        overall_value = trackers_overall_rgb.get(tracker, 0)
        name_label = tracker + '*' if tracker in highlighted_trackers else tracker
        labels_rgb.append(f"{name_label} ({overall_value:.2f})")

leg2 = ax2.legend(handles_rgb, labels_rgb, loc='lower center', bbox_to_anchor=(0.5, -1.3),
                  ncol=1, columnspacing=1.0, handlelength=2.0)
for i, text in enumerate(leg2.get_texts()):
    if i < 2:
        text.set_fontproperties(bold_font)

plt.subplots_adjust(bottom=0.10 + num_rows_legend * 0.03, wspace=0.2)
plt.savefig('plot.png', dpi=300)
plt.savefig('plot.pdf', bbox_inches='tight', pad_inches=0.05)
plt.show()
