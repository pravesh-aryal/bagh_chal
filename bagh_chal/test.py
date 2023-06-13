# class Animal:
#     def __init__(self) -> None:
#         self.name = "ANIMAL IS MY NAME"


# dog = Animal()
# print(dog)

# dog.breed = "Husky"
# print(dog)
# print(dog.breed)
# print(Animal.name)


def is_valid_move(func):
    def inner(x):
        if func() == 5:
            return True

    return inner


@is_valid_move
def move(destination):
    print("VALID MOVE IS MADE")


move(5)
