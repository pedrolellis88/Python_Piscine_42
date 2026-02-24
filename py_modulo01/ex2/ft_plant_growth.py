class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age

    def grow(self):
        self.height += 1

    def age_one_day(self):
        self.age += 1

    def get_info(self):
        return f"{self.name}: {self.height}cm, {self.age} days old"


def simulate_days(plant, days_left):
    if days_left == 0:
        return
    plant.grow()
    plant.age_one_day()
    simulate_days(plant, days_left - 1)


if __name__ == "__main__":
    days_passed = 6
    rose = Plant("Rose", 25, 30)
    print("=== Day 1 ===")
    print(rose.get_info())
    simulate_days(rose, days_passed)
    print(f"=== Day {days_passed + 1} ===")
    print(rose.get_info())
    print(f"Growth this week: +{days_passed}cm")
