starting_point = (50, 100)

length = 100
matrix = []
add_value = int(length / 4)
x = starting_point[0]
y = starting_point[1]

for i in range(0, 5):
    row = []
    for i in range(0, 5):
        row.append((x, y))
        y += add_value

    print(row)
    matrix.append(row)
    x += add_value
    y = starting_point[1]
print("this is", matrix)
