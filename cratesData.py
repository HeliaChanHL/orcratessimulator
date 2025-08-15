import random
from copy import deepcopy
# Finishes
finishes = {
    "Rainbow":"#ee39ac",
    "Molten":"#eb2f00",
    "Bubble":"#1b83ff",
    "Floral":"#fa9efd",
    "Matrix":"#023a19",
    "Gold":"#fdc761",
    "Chrome":"#4a6180",
    "Glitch":"#eeb5d6",
    "Galaxy":"#54256b"
}
rarity_color_map = {
    "Common": "grey",
    "Rare": "#0097d8",
    "Epic": "#895bf3",
    "Legendary": "#f19c0b"
}
modalText="hi"

# Crate and Item Classes
class Item:
    def __init__(self, name, rarity, item_type):
        self.display_name = name  # Store the name without rarity for display in the output table
        self.rarity = rarity
        self.item_type = item_type
        self.has_finish = False
        self.finish_type = None

    def apply_finish(self, finish):
        self.display_name = f"{finish} {self.display_name}"  # Prepend the finish to the item name
        self.has_finish = True
        self.finish_type = finish

    def __repr__(self):
        return f"Item(name={self.display_name}, rarity={self.rarity}, type={self.item_type})"

    def __str__(self):
        return self.display_name

class Crate:
    def __init__(self, crate_name):
        self.crate_name = crate_name
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def open_crate(self,finish_chance,rarity_probabilities):
        selected_items = []
        for _ in range(3):  # Three rolls per crate
            rarity = self.roll_for_rarity(rarity_probabilities)  # Determine the rarity of the item
            possible_items = [item for item in self.items if item.rarity == rarity]
            selected_item = random.choice(possible_items)
            selected_items.append(selected_item)
        
        # Clone items to avoid modifying originals and apply finishes
        cloned_items = [deepcopy(item) for item in selected_items]
        for item in cloned_items:
            if item.item_type.lower() == "cosmetic" and random.random() <= finish_chance:
                random_finish = random.choice(list(finishes.keys()))
                item.apply_finish(random_finish)

        return cloned_items

    def roll_for_rarity(self,rarity_probabilities):
        roll = random.random()
        cumulative_probability = 0.0
        for rarity, probability in rarity_probabilities.items():
            cumulative_probability += probability
            if roll < cumulative_probability:
                return rarity
        return "Common"  # Default to Common if no other match
