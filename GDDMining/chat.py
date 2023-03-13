my_list = ['(4842:Human2).birthDate', '(4842:Human2).name', '(4842:Human1).birthDate', '(4842:Human3).deathDate', '(4842:Human2).id', '(4842:Human3).id', '(4842:Human0).name', '(4842:Human0).birthDate', '(4842:Human0).deathDate', '(4842:Human1).deathDate', '(4842:Human1).name', '(4842:Human1).id', '(4842:Human3).name', '(4842:Human2).deathDate', '(4842:Human0).id', '(4842:Human3).birthDate']

result_dict = {}
for item in my_list:
    keyword = item.split(".")[1]  # 提取关键字
    print(item)
    if keyword not in result_dict:
        result_dict[keyword] = []
    result_dict[keyword].append(item)  # 把元素添加到相应的关键字列表中

# 打印结果
for keyword, items in result_dict.items():
    print(keyword, items)
