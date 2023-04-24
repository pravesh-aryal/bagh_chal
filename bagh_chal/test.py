from itertools import chain

a = [[i * 5 + j + 1 for j in range(5)] for i in range(5)]
print(a)
x = chain(*a)

print((x))
for each in x:
    print(each)
