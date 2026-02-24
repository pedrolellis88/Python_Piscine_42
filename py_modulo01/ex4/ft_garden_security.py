class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age


class SecurePlant:
    def __init__(self, plant):
        self.plant = plant

    def set_height(self, new_h):
        if new_h < 0:
            print(f"Invalid operation attempted: height {new_h}cm [REJECTED]")
            print("Security: Negative height rejected")
            return
        self.plant.height = new_h
        print(f"Height updated: {new_h}cm [OK]")

    def set_age(self, new_a):
        if new_a < 0:
            print(f"Invalid operation attempted: age {new_a} days [REJECTED]")
            print("Security: Negative age rejected")
            return
        self.plant.age = new_a
        print(f"Age updated: {new_a} days [OK]")

    def get_height(self):
        return self.plant.height

    def get_age(self):
        return self.plant.age


if __name__ == "__main__":
    print("=== Garden Security System ===")
    rose = Plant("Rose", 0, 0)
    secure_rose = SecurePlant(rose)
    print("Plant created:", secure_rose.plant.name)
    secure_rose.set_height(25)
    secure_rose.set_age(30)
    print("")
    secure_rose.set_height(-5)
    new_height = secure_rose.get_height()
    new_age = secure_rose.get_age()
    print(f"\nCurrent plant {rose.name} ({new_height}cm, {new_age} days)")
