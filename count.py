def count_word_occurrences(file_path, word):
    count = 0

    # 打开文件
    with open(file_path, 'r') as file:
        # 逐行读取文件内容
        for line in file:
            # 将每一行按照空格分隔成单词列表
            if word in line:
                # 统计匹配到的单词数量
                count += 1
    return count


# 测试代码
file_path = "d.txt"
target_word = "False"

try:
    result = count_word_occurrences(file_path, target_word)
    print(f"The word '{target_word}' occurs {result} times in the file.")
except FileNotFoundError:
    print("File not found.")
