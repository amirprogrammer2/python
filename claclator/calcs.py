class Calc:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y

    def add (self):
        return self.x + self.y
    def minus (self):
        return self.x - self.y
    def multi (self):
        return self.x * self.y
    def division (self):
        if self.y == 0:
            return "the number does not become zero"
        return self.x / self.y
    