starting_point = (0, 0)
# length = game_settings.BOARD_WIDTH
length = 600

coordinates = []
JUMP_VALUE = int(length / 4)
x, y = starting_point
# Creating 5 * 5 matrix
for i in range(0, 5):
    row = []
    for j in range(0, 5):
        row.append((x, y))
        x += JUMP_VALUE

    coordinates.append(row)
    x = starting_point[1]
    y += JUMP_VALUE
print(coordinates)
for row in coordinates:
    print(row)
