# circles = [1, 2, 3, 4, 5, 6]
# board_config = [
#     ["a", "b"],
#     ["c", "d"],
#     ["e", "f"],
# ]
# from itertools import chain


# for circle, x in zip(circles, chain(*board_config)):
#     print(circle, x)

# for circle in circles:
#     print(circle)

# for x in chain(*board_config):
#     print(x)


def hey(x, y):
    print(x, y)


t = (1, 2)
hey(*t)
