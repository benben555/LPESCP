# 打开a.txt文件和b.txt文件
with open('LPESCP.txt', 'r') as infile, open('processed_LPESCP.txt', 'w') as outfile:
    # 逐行读取a.txt文件中的数据
    for line in infile:
        # 将每行的数据转换成整数并加上2
        temp = eval(line.strip())
        if temp <= 6:
            data = temp * 0.25
        elif temp <= 9:
            data = (temp - 6) * 2 + 1.5
        else:
            data = (temp - 9) * 0.25 + 7.5
        # 将处理后的数据写入b.txt文件中，并加上换行符
        outfile.write(str(data) + '\n')
