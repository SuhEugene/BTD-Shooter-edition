class Map:
    def __init__(self):
        pass

    def get(self, pos):
        if (pos[0] < 100 and pos[1] < 100):
            return (1, 1)
        else:
            return (0, 0)