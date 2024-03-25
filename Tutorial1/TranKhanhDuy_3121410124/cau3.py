def capDS(lst):
	for i in lst:
		for j in lst:
			yield i, j

# Kiểm tra kiểu của generator
print(type(capDS([3, 4, 5])))

print("____Q1____")
# In tất cả các cặp phần tử từ danh sách
for x, y in capDS([3, 4, 5]):
	print(x, y)


# Q1
def chiaHet(iterable, k):
	for item in iterable:
		if item % k == 0:
			yield item

# Kiểm tra kiểu của generator
s = chiaHet([1, 5, 2], 5)
print(type(s))

# In danh sách các phần tử từ generator
print(list(s))

# Kiểm tra generator với số tự nhiên
def naturals():
	n = 1
	while True:
		yield n
		n += 1

m = chiaHet(naturals(), 2)
print([next(m) for _ in range(5)])


print("____Q2____")

def Box(s, k):
    it = iter(s)
    for _ in range(k):
        yield next(it)
    raise ValueError("ValueError")


# Ví dụ
try:
    t = Box([5, 9, 4], 2)
    print(next(t))  # In ra: [3, 2]
    print(next(t))
    print(next(t))
except ValueError as e:
    print(e)  # In ra: Not enough values in the iterable.

try:
	print(list(Box(range(6), 6)))
except ValueError as e:
	print(e)


try:
    t2 = Box(map(abs, reversed(range(-3, -1))), 2)
    print(next(t2))  # In ra: [3, 2]
    print(next(t2))
    print(next(t2))
except ValueError as e:
    print(e)  # In ra: Not enough values in the iterable.
