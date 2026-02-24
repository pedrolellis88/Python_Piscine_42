class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age

    def get_info(self):
        return f"{self.name} ({self.height}cm, {self.age} days)"


class PlantFactory:
    def create_rose():
        return Plant("Rose", 25, 30)

    def create_oak():
        return Plant("Oak", 200, 365)

    def create_cactus():
        return Plant("Cactus", 5, 90)

    def create_sunflower():
        return Plant("Sunflower", 80, 45)

    def create_fern():
        return Plant("Fern", 15, 120)


if __name__ == "__main__":
    print("=== Plant Factory Output ===")
    rose = PlantFactory.create_rose()
    oak = PlantFactory.create_oak()
    cactus = PlantFactory.create_cactus()
    sunflower = PlantFactory.create_sunflower()
    fern = PlantFactory.create_fern()
    print("Created :", rose.get_info())
    print("Created :", oak.get_info())
    print("Created :", cactus.get_info())
    print("Created :", sunflower.get_info())
    print("Created :", fern.get_info())
    print("\nTotal plants created: 5")
