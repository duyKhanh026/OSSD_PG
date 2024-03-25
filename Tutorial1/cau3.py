def capDS(lst):
    for i in lst:
        for j in lst:
            yield i, j

# Kiểm tra kiểu của generator
print(type(capDS([3, 4, 5])))

# In tất cả các cặp phần tử từ danh sách
for x, y in capDS([3, 4, 5]):
    print(x, y)
