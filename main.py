import matplotlib.pyplot as plt
with open('PIPO.txt', 'r') as f1, open('WMMF.txt', 'r') as f2, open('LPESCP.txt', 'r') as f3:
    data1 = [float(line.strip()) for line in f1]
    data2 = [float(line.strip()) for line in f2]
    data3 = [float(line.strip()) for line in f3]
x = range(len(data1))  # x轴数据，可以根据具体情况调整
plt.plot(x, data1, label='Data 1')
plt.plot(x, data2, label='Data 2')
plt.plot(x, data3, label='Data 3')

# 添加标题和标签
plt.title('Line Chart')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# 添加图例
plt.legend()
plt.savefig('5.svg', format='svg', dpi=150)  # 输出
plt.show()