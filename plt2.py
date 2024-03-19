from matplotlib import pyplot as plt

st_max_provide = [70.05, 58.92, 28.96, 20.56, 83.01, 47.08, 5.82, 64.71, 27.93, 58.98]
st_true0_provide = [67.31, 55.93, 18.59, 8.4, 79.91, 40.67, 0, 60.23, 16.95, 58.46]
st_max_demand = [2.28, 87.46, 15.84, 35.99, 50.08, 9.32, 28.18, 76.76, 74.34, 26.2]
st_true0_demand = [2.28, 87.46, 15.84, 35.99, 50.08, 9.32, 28.18, 76.76, 74.34, 26.2]
a = 10


def f1(a, st_max_provide, st_true0_provide, st_max_demand, st_true0_demand):
    b = 20 - a
    x = [i + 1 for i in range(a)]
    # x轴坐标, a=5, 返回[0, 1, 2, 3, 4]
    # x1 = np.arange(1, 1 + b)
    x1 = [i + 1 for i in range(b)]
    # fig = plt.figure(figsize=(10, 9))
    # plt.subplots_adjust(left=None, bottom=0.15, right=None, top=None, wspace=0.3, hspace=0.5)
    # ax1 = fig.add_subplot(2, 2, 1)
    # plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei显示中文\n",
    # ax2 = fig.add_subplot(2, 1, 1)
    plt.rcParams['font.sans-serif'] = ['SimSun']
    total_width, n = 0.8, 2
    # 每种类型的柱状图宽度
    width = total_width / n

    # plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei显示中文\n",
    # plt.title(title2)  # 添加标题\n",
    plt.xlabel('供能用户ID', fontsize=20, fontweight='medium')  # 添加横轴标签\n",
    plt.ylabel('能源量(kW·h)', fontsize=20, fontweight='medium')  # 添加y轴名称\n",
    # 画柱状图
    plt.bar(x1, st_max_provide, width=width, label="最大能源供应量")
    x11 = [i + 1 + width for i in range(b)]
    plt.bar(x11, st_true0_provide, width=width, label="实际能源供应量")
    plt.xticks(x1, fontsize=15)
    plt.yticks(fontsize=15)
    plt.legend(fontsize=15)
    # plt.savefig('5.pdf')
    # ax3 = fig.add_subplot(2, 2, 3)
    # plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei显示中文\n",
    plt.savefig('3_3.svg', format='svg',  dpi=800)  # 输出
    # foo_fig = plt.gcf()  # 'get current figure'
    # foo_fig.savefig('5.eps', format='eps', dpi=800)
    plt.show()
    #
    # ax4 = fig.add_subplot(2, 1, 2)

    total_width, n = 0.8, 2
    # 每种类型的柱状图宽度
    width = total_width / n
    plt.rcParams['font.sans-serif'] = 'SimSun'  # 设置字体为SimHei显示中文\n",
    # plt.title(title4)  # 添加标题\n",
    plt.xlabel('需能用户ID', fontsize=20, fontweight='medium')  # 添加横轴标签\n",
    plt.ylabel('能源量(kW·h)', fontsize=20, fontweight='medium')  # 添加y轴名称\n",
    # 画柱状图
    plt.bar(x, st_max_demand, width=width, label="能源需求量")
    x2 = [i + 1 + width for i in range(a)]

    plt.bar(x2, st_true0_demand, width=width, label="实际获得能源供应量")
    plt.xticks(x, fontsize=15)
    plt.yticks(fontsize=15)
    # 显示图例
    plt.ylim(0, 100)
    plt.legend(fontsize=15,loc='upper right')
    # 显示柱状图
    plt.savefig('3_4.svg', format='svg', dpi=800)
    # plt.savefig('6.pdf')
    # foo_fig = plt.gcf()  # 'get current figure'
    # foo_fig.savefig('6.eps', format='eps', dpi=800)
    # plt.savefig('4.eps',  dpi=600)  # 输出
    plt.show()


f1(a, st_max_provide, st_true0_provide, st_max_demand, st_true0_demand)
