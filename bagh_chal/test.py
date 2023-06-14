class Circle:
    def __init__(self, x, y) -> None:
        self.x = 90
        self.y = 100


class Tiger(Circle):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)

    # def __init__(self):
    #     self.name = "tiger"


t = Tiger()
print(t.x)
