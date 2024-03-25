from matplotlib import pyplot as plt

st_max_provide = [42.31, 0.1, 55.72, 73.94, 32.89, 20.06, 48.11, 44.62, 49.03, 8.2, 17.81, 7.47]
st_true0_provide = [42.31, 0.1, 55.72, 73.94, 32.89, 20.06, 48.11, 44.62, 49.03, 8.2, 17.81, 7.47]
st_max_demand = [94.01, 64.5, 91.58, 45.16, 24.56, 19.81, 3.2, 57.44]
st_true0_demand = [94.01, 64.5, 91.58, 45.16, 24.56, 19.81, 3.2, 57.44]
a = 8


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
    plt.xlabel('供能用户ID', fontsize=20, fontweight='medium')  # 添加横轴标签\n",
    plt.ylabel('能源量(kW·h)', fontsize=20, fontweight='medium')  # 添加y轴名称\n",
    # 画柱状图
    plt.bar(x1, st_max_provide, width=width, label="最大能源供应量")
    x11 = [i + 1 + width for i in range(b)]
    plt.bar(x11, st_true0_provide, width=width, label="实际能源供应量")
    plt.xticks(x1, fontsize=15)
    plt.yticks(fontsize=15)
    plt.legend(fontsize=15)
    # plt.savefig('7.pdf')
    plt.savefig('3_5.svg', format='svg', dpi=800)
    # foo_fig = plt.gcf()  # 'get current figure'
    # foo_fig.savefig('7.eps', format='eps', dpi=800)
    # ax3 = fig.add_subplot(2, 2, 3)
    # plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei显示中文\n",
    # plt.savefig('3.eps',  dpi=600)  # 输出
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
    plt.legend(fontsize=15)
    # 显示柱状图
    # plt.savefig('8.pdf')
    plt.savefig('3_6.svg', format='svg', dpi=800)
    # foo_fig = plt.gcf()  # 'get current figure'
    # foo_fig.savefig('8.eps', format='eps', dpi=800)
    # plt.savefig('4.eps',  dpi=600)  # 输出
    plt.show()


f1(a, st_max_provide, st_true0_provide, st_max_demand, st_true0_demand)
