class Plant:
    def __init__(self, name, height, age):
        self.n = name
        self.h = height
        self.a = age

    def grow(self, new_height):
        self.h += new_height

    def age_days(self, days):
        self.a += days

    def get_info(self):
        return f"{self.n}: {self.h}cm, {self.a} days old"


class FloweringPlant(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)
        self.color = color

    def bloom(self):
        return f"{self.n} is blooming with {self.color} flowers"

    def get_info(self):
        first = f"{self.n}: {self.h}cm, {self.a} days old, "
        second = f"{self.color} flowers (blooming)"
        return first + second


class PrizeFlower(FloweringPlant):
    def __init__(self, name, height, age, color,  points):
        super().__init__(name, height, age, color)
        self.points = points

    def get_info(self):
        base = super().get_info()
        return f"{base}, Prize points: {self.points}"


class Garden:
    def __init__(self, owner):
        self.owner = owner
        self.plants = []
        self.total_growth = 0

    def add_plant(self, plant):
        self.plants.append(plant)
        print(f"Added {plant.n} to {self.owner}'s garden")

    def grow_all(self, amount):
        print(f"{self.owner} is helping all plants grow...")
        for plant in self.plants:
            plant.grow(amount)
            plant.age_days(amount)
            self.total_growth += amount
            print(f"{plant.n} grew {amount}cm and {amount} day(s)")
        print("")

    def report(self):
        print(f"=== {self.owner}'s Garden Report ===")
        print("Plants in garden:")
        for p in self.plants:
            print(f"- {p.get_info()}")
        r = 0
        f = 0
        pr = 0
        for p in self.plants:
            if isinstance(p, PrizeFlower):
                pr += 1
            elif isinstance(p, FloweringPlant):
                f += 1
            elif isinstance(p, Plant):
                r += 1
        g = self.total_growth
        nbr = len(self.plants)
        print(f"\nPlants added: {nbr}, Total growth: {g}cm and {g} day(s)")
        print(f"Plant types: {r} regular, {f} flowering, {pr} prize flowers\n")


class GardenManager:

    class GardenStats:

        @staticmethod
        def average_height(garden):
            if not garden.plants:
                return 0
            return sum(p.h for p in garden.plants) / len(garden.plants)

        @staticmethod
        def average_age(garden):
            if not garden.plants:
                return 0
            return sum(p.a for p in garden.plants) / len(garden.plants)

        @staticmethod
        def count_prize_flowers(garden):
            return sum(isinstance(p, PrizeFlower) for p in garden.plants)

        @staticmethod
        def validate_height(plant):
            return plant.h >= 0

        @staticmethod
        def validate_age(plant):
            return plant.a >= 0

    def __init__(self):
        self.gardens = {}

    def add_garden(self, garden):
        self.gardens[garden.owner] = garden

    @classmethod
    def create_garden_network(cls, owners):
        mgr = cls()
        for owner in owners:
            mgr.add_garden(Garden(owner))
        return mgr

    def score_gardens(self):
        scores = {}
        for owner, garden in self.gardens.items():
            stats = self.GardenStats
            avg_height = stats.average_height(garden)
            avg_age = stats.average_age(garden)
            prize_count = stats.count_prize_flowers(garden)
            score = int(avg_height * 2 + avg_age * 2 + prize_count * 50)
            scores[owner] = score
        return scores


if __name__ == "__main__":
    print("=== Garden Management System Demo ===\n")
    manager = GardenManager.create_garden_network(["Alice", "Bob"])
    alice = manager.gardens["Alice"]
    bob = manager.gardens["Bob"]
    oak = Plant("Oak Tree", 100, 125)
    rose = FloweringPlant("Rose", 25, 30,  "red")
    sunflower = PrizeFlower("Sunflower", 50, 70, "yellow", 10)
    alice.add_plant(oak)
    alice.add_plant(rose)
    alice.add_plant(sunflower)
    print("")
    alice.grow_all(10)
    alice.report()
    val_h_oak = GardenManager.GardenStats.validate_height(oak)
    val_a_oak = GardenManager.GardenStats.validate_age(oak)
    print("Height validation test:", val_h_oak)
    print("Age validation test:", val_a_oak)
    print("")
    bob.add_plant(Plant("Basil", 20, 25))
    print("")
    scores = manager.score_gardens()
    bob.grow_all(5)
    bob.report()
    print("Garden scores - Alice:", scores["Alice"], ", Bob:", scores["Bob"])
    print("Total gardens managed:", len(manager.gardens))
