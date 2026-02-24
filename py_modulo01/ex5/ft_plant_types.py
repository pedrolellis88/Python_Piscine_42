class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age


class Flower(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)
        self.color = color

    def bloom(self):
        print(f"{self.name} is blooming beautifully!\n")


class Tree(Plant):
    def __init__(self, name, height, age, trunk):
        super().__init__(name, height, age)
        self.trunk = trunk

    def produce_shade(self, shade):
        print(f"{self.name} provides {shade} square meters of shade\n")


class Vegetable(Plant):
    def __init__(self, name, height, age, season, nutritional_value):
        super().__init__(name, height, age)
        self.season = season
        self.nutritional_value = nutritional_value

    def nutrients(self):
        print(f"{self.name} is rich in {self.nutritional_value}")


if __name__ == "__main__":
    print("== Garden Plant Types ===\n")
    r = Flower("Rose", 25, 30, "red")
    s = Flower("Sunflower", 20, 15, "yellow")
    o = Tree("Oak", 500, 1825, "50cm diameter")
    p = Tree("Pine", 300, 900, "40cm diameter")
    t = Vegetable("Tomato", 80, 90,  "summer harvest", "vitamin C")
    c = Vegetable("Carrot", 30, 70, "winter", "beta carotene")
    print(f"{r.name} (Flower) : {r.height}cm, {r.age} days, {r.color} color")
    r.bloom()
    print(f"{s.name} (Flower) : {s.height}cm, {s.age} days, {s.color} color")
    s.bloom()
    print(f"{o.name} (Tree) : {o.height}cm, {o.age} days, {o.trunk}")
    o.produce_shade(78)
    print(f"{p.name} (Tree) : {p.height}cm, {p.age} days, {p.trunk}")
    p.produce_shade(59)
    print(f"{t.name} (Vegetable): {t.height}cm, {t.age} days, {t.season}")
    t.nutrients()
    print("")
    print(f"{c.name} (Vegetable): {c.height}cm, {c.age} days, {c.season}")
    c.nutrients()
