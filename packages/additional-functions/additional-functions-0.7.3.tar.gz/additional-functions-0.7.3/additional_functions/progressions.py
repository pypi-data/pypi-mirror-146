class ArithmeticProgression:

    d = 0
    a = []

    def __init__(self, start, d):
        self.a.append(start)
        self.d = d

    def get_nth(self, n):
        return self.a[0] + (n - 1) * self.d
    
    def count_to_nth(self, n):
        for _ in range(len(self.a), n):
            self.a.append(self.a[-1] + self.d)

    def get_to_nth(self, n):
        self.count_to_nth(n)
        return self.a

    def get_sum_to_nth(self, n):
        return n * (self.a[0] + self.get_nth(n)) // 2

class GeometricProgression:

    q = 1
    b = []

    def __init__(self, start, q):
        if start == 0 or q == 0:
            print("b0 or q can't be 0")
            return 
        self.b.append(start)
        self.q = q

    def get_nth(self, n):
        return self.b[0] * (self.q ** (n - 1))
    
    def count_to_nth(self, n):
        for _ in range(len(self.b), n):
            self.b.append(self.b[-1] * self.q)

    def get_to_nth(self, n):
        self.count_to_nth(n)
        return self.b

    def get_sum_to_nth(self, n):
        if self.q == 1: return n * self.b[0]
        return (self.b[0] * ((self.q ** n) - 1)) // (self.q - 1)

    def get_prod_to_nth(self, n):
        return int((self.b[0] * self.get_nth(n)) ** (n / 2))

class HarmonicProgression:

    d = 0
    c = []

    def __init__(self, start, d):
        self.c.append(start)
        self.d = d
    
    def get_nth(self, n):
        return ((self.c[0] ** -1) + (n - 1) * self.d) ** -1

    def count_to_nth(self, n):
        for _ in range(len(self.c), n):
            self.c.append(((self.c[-1] ** -1) + self.d) ** -1)

    def get_to_nth(self, n):
        self.count_to_nth(n)
        return self.c
