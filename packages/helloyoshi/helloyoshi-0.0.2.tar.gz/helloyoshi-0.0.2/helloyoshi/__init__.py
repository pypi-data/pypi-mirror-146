from hello import sayhello


class hy:
    def __init__(self):
        print("Constructer success build")

    def working(self, b):
        print(sayhello(5))
        # print(f'{b} is working')
        return "Hello"
