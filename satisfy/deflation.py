# 打开a.txt文件和b.txt文件
with open('PIPO.txt', 'r') as infile, open('processed_PIPO.txt', 'w') as outfile:
    # 逐行读取txt文件中的数据
    for line in infile:
        temp = eval(line.strip())
        if temp <= 6:
            data = temp * 0.25
        elif temp <= 9:
            data = (temp - 6) * 2 + 1.5
        else:
            data = (temp - 9) * 0.25 + 7.5
        # 将处理后的数据写入txt文件中，并加上换行符
        outfile.write(str(data) + '\n')
