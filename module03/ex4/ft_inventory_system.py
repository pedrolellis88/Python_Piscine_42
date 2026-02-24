def ft_inventory_system():
    """Manages player inventories using nested dictionaries and prints analytics.""" # noqa
    print("=== Player Inventory System ===\n")

    inventories = dict()

    inventories["alice"] = dict()
    inventories["alice"]["sword"] = {"category": "weapon", "rarity": "rare", "qty": 1, "value": 500} # noqa
    inventories["alice"]["potion"] = {"category": "consumable", "rarity": "common", "qty": 5, "value": 50} # noqa
    inventories["alice"]["shield"] = {"category": "armor", "rarity": "uncommon", "qty": 1, "value": 200}# noqa

    inventories["bob"] = dict()
    inventories["bob"]["potion"] = {"category": "consumable", "rarity": "common", "qty": 0, "value": 50} # noqa
    inventories["bob"]["magic_ring"] = {"category": "accessory", "rarity": "rare", "qty": 1, "value": 700}# noqa

    inventories["charlie"] = dict()
    inventories["charlie"]["dagger"] = {"category": "weapon", "rarity": "common", "qty": 2, "value": 120} # noqa

    return inventories


def inventory_value(player_inv):
    """Calculates the total gold value of a player's inventory."""
    total = 0
    for _, info in player_inv.items():
        total += info["qty"] * info["value"]
    return total


def inventory_item_count(player_inv):
    """Calculates the total quantity of items in a player's inventory."""
    count = 0
    for _, info in player_inv.items():
        count += info["qty"]
    return count


def category_counts(player_inv):
    """Counts total item quantities grouped by category."""
    counts = dict()
    for _, info in player_inv.items():
        cat = info["category"]
        counts[cat] = counts.get(cat, 0) + info["qty"]
    return counts


def print_inventory(inventories, player_name):
    """Prints a player's inventory and summary statistics."""
    print(f"=== {player_name.capitalize()}'s Inventory ===")
    inv = inventories.get(player_name)
    if inv is None:
        print("Player not found.")
        return

    for item_name, info in inv.items():
        qty = info["qty"]
        value = info["value"]
        cat = info["category"]
        rarity = info["rarity"]
        total_item_value = qty * value
        print(f"{item_name} ({cat}, {rarity}): {qty}x @ {value} gold each = {total_item_value} gold") # noqa

    total_value = inventory_value(inv)
    total_items = inventory_item_count(inv)
    cats = category_counts(inv)

    print(f"\nInventory value: {total_value} gold")
    print(f"Item count: {total_items} items")

    line = "Categories: "
    first = True
    for cat, qty in cats.items():
        if not first:
            line += ", "
        line += f"{cat}({qty})"
        first = False
    print(line)


def transfer_item(inventories, giver, receiver, item_name, qty):
    """Transfers qty of item_name from giver to receiver, if possible."""
    giver_inv = inventories.get(giver)
    receiver_inv = inventories.get(receiver)

    if qty <= 0:
        print("Transaction failed: invalid quantity.")
        return

    if giver_inv is None or receiver_inv is None:
        print("Transaction failed: invalid player name.")
        return

    giver_item = giver_inv.get(item_name)
    if giver_item is None:
        print("Transaction failed: item not found in giver inventory.")
        return

    if giver_item["qty"] < qty:
        print("Transaction failed: not enough quantity to transfer.")
        return

    receiver_item = receiver_inv.get(item_name)

    if receiver_item is None:
        receiver_inv[item_name] = {
            "category": giver_item["category"],
            "rarity": giver_item["rarity"],
            "qty": 0,
            "value": giver_item["value"],
        }
        receiver_item = receiver_inv[item_name]

    giver_item.update({"qty": giver_item["qty"] - qty})
    receiver_item.update({"qty": receiver_item["qty"] + qty})

    print("Transaction successful!")


def rarest_items(inventories):
    """
    Returns a list of item names that have the highest rarity level
    found across all inventories.
    """
    rarity_rank = {"common": 1, "uncommon": 2, "rare": 3}

    best_rank = 0
    rarest = []

    for _, inv in inventories.items():
        for item_name, info in inv.items():
            rank = rarity_rank.get(info.get("rarity", "common"), 1)
            if rank > best_rank:
                best_rank = rank
                rarest = [item_name]
            elif rank == best_rank and item_name not in rarest:
                rarest.append(item_name)

    return rarest


def print_inventory_analytics(inventories):
    """Prints global analytics across all players."""
    print("\n=== Inventory Analytics ===")

    most_valuable_name = None
    most_valuable_value = -1

    most_items_name = None
    most_items_qty = -1

    for player_name, inv in inventories.items():
        total_value = inventory_value(inv)
        total_qty = inventory_item_count(inv)

        if total_value > most_valuable_value:
            most_valuable_value = total_value
            most_valuable_name = player_name

        if total_qty > most_items_qty:
            most_items_qty = total_qty
            most_items_name = player_name

    rarest = rarest_items(inventories)

    print(f"Most valuable player: {most_valuable_name.capitalize()} ({most_valuable_value} gold)")  # noqa
    print(f"Most items: {most_items_name.capitalize()} ({most_items_qty} items)")  # noqa
    line = "Rarest items: "
    first = True
    for item in rarest:
        if not first:
            line += ", "
        line += item
        first = False
    print(line)


inventories = ft_inventory_system()
print_inventory(inventories, "alice")

print("\n=== Transaction: Alice gives Bob 2 potions ===")
transfer_item(inventories, "alice", "bob", "potion", 2)
print("\n=== Updated Inventories ===")
print(f"Alice potions: {inventories['alice']['potion']['qty']}")
print(f"Bob potions: {inventories['bob']['potion']['qty']}")

print_inventory_analytics(inventories)
