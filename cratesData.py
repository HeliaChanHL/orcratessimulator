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

modalText="""
## 1. Adjust Rarity Probabilities
Controls the likelihood of obtaining items of different rarities.
Use the sliders to set the probabilities for each rarity:
- Legendary: 5% (default)
- Epic: 13% (default)
- Rare: 27% (default)
- Common: 55% (default)
The total of all probabilities will automatically normalize to 100%.
## 2. Select Crate Type
From the dropdown menu, choose the crate you want to open. The first crate is selected by default.
## 3. Set Finish Chance
Adjust the chance of receiving a "finish" item when opening a crate. 
Use the slider to set a value between 0.0 and 1.0 (default is 1%).
## 4. Specify Number of Crates to Open
Use the number input to select how many crates you want to open at once (minimum of 1).
## 5. Display Odds
Choose whether to display the odds of getting each rarity by default.
Use the dropdown menu to select either True (show odds) or False (hide odds).
## 6. Roll Crates
Click the "Roll Crates" button to simulate opening the selected number of crates.

---

## 7. Track Your Progress
The simulator will process your selections and display the results, including the items you received and their rarities.
The simulator keeps track of:
- Total crates opened.
- OR-Bucks spent.
- Counts of each rarity and item type received.
- Counts of how many times each crate has been opened."""