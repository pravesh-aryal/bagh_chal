start_point = (0, 0)

length = 100
matrix = []
add_value = int(length / 4)
x = start_point[0]
y = start_point[1]
row = []
for i in range(0, 5):

    for i in range(0, 5):
        row.append((x, y))
        y += add_value
        
	matrix.append(row)