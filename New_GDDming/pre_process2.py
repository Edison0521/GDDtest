index_to_delete = [2, 3]
outfile = open('produce_Table1\'\'\'.txt', 'w', encoding='utf-8')
with open('produce_Table1\'\'.txt', 'r', encoding='utf-8')as f:
    for line in f:
        line = line.strip().split(";;")
        line = [line[i] for i in range(0, len(line), 1) if i not in index_to_delete]
        for i in range(0, len(line)):
            if i != len(line) - 1:
                outfile.write(line[i] + ";;")
            else:
                outfile.write(line[i])
        outfile.write('\n')
outfile.close()
