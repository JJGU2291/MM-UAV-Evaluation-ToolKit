import matplotlib.pyplot as plt

# 横坐标数据
buffer = [30, 60, 90, 120, 150, 180, 210, 240, 360, 480, 640]

# RGB 对应的 IDF1 值
idf1_rgb = [50.5, 54.72, 56.69, 58.42, 59.39, 59.67, 59.65, 59.80, 59.95, 59.77, 60.00]

# IR 对应的 IDF1 值
idf1_ir = [60.28, 65.23, 66.93, 68.10, 69.12, 69.51,70.08, 70.28, 70.18, 70.29, 70.11]

# 创建图形
plt.figure(figsize=(10, 6))

# 绘制 RGB 折线
plt.plot(buffer, idf1_rgb, label='RGB', marker='o', color='blue')  # 使用蓝色线条和圆形标记点

# 绘制 IR 折线
plt.plot(buffer, idf1_ir, label='IR', marker='o', color='red')  # 使用红色线条和圆形标记点

# 添加图例
plt.legend()

# 添加标题
plt.title('IDF1 Values for RGB and IR vs Buffer Size')

# 添加横纵坐标标签
plt.xlabel('Buffer Size')
plt.ylabel('IDF1 Value (%)')

# 添加网格
plt.grid(True)
plt.savefig('idf1_vs_buffer.png', dpi=300)
# 显示图形
plt.show()