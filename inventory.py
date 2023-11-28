from typing import Iterable, Iterator
from vegetable import *
import pickle

class ItemAlreadyExists(Exception):
    pass

class ItemNotFound(Exception):
    pass

class ItemIterable(Iterable):
    def __init__(self, item_list):
        self._item_list = item_list

    def __iter__(self) -> Iterator:
        return ItemIterator(self._item_list)
    
def load_pickle(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

def dump_pickle(filename, item):
    with open(filename, 'wb') as file:
        pickle.dump(item, file)

class ItemIterator(Iterator):
    def __init__(self, item_list):
        self._items = [(item._name, item._price, item._stock) for item in item_list]
        self._index = 0

    def __next__(self):
        if self._index == len(self._items):
            raise StopIteration()
        
        item = self._items[self._index]
        self._index += 1
        return item

class Inventory:
    def __init__(self):
        self._all_items = dump_pickle('all_items.pkl', [])
        self._items_available = []

    def view_all_items(self):
        iterable = ItemIterable(self._all_items)
        return list(iterable)

    def add_item(self, item):
        self._all_items = load_pickle('all_items.pkl')
        if item._name.lower() not in [items._name.lower() for items in self._all_items]:
            self._all_items.append(item)
        else:
            raise ItemAlreadyExists("The item already exists in the inventory.")
        dump_pickle('all_items.pkl', self._all_items)
        
    def update_item(self, item = None, type = None, price = None, stock = None):
        self._all_items = load_pickle('all_items.pkl')
        item_address = None
        for c_item in self._all_items:
            if c_item._name.lower() == item.lower():
                item_address = c_item
                break
        if item_address:
            item_address.update(item, type, price, stock)
        dump_pickle('all_items.pkl', self._all_items)
    
    def update_today_picks(self, item):
        for i in self._all_items:
            if item.lower() == i._name.lower():
                self._items_available.append(i)
                break  # You need to exit the loop when the item is found.
        else:
            raise ItemNotFound("Item not found.")
    
    def view_available_items(self):
        iterable = ItemIterable(self._items_available)
        return list(iterable)

# Example usage:
if __name__ == "__main__":
    # Driver code

    # Create items
    item1 = Vegetable("Carrot", "Vegetable", 1.5, 100)
    item2 = Vegetable("Broccoli", "Vegetable", 2.0, 50)
    item3 = Vegetable("Spinach", "Greens", 1.0, 75)

    # Create an inventory
    inventory = Inventory()

    # Add items to the inventory
    try:
        inventory.add_item(item1)
        inventory.add_item(item2)
        print("Items added to the inventory.")
    except ItemAlreadyExists as e:
        print(f"Error: {e}")

    # View all items in the inventory
    all_items = inventory.view_all_items()
    print("\nAll items in the inventory:")
    print(all_items)

    # Update item information
    try:
        inventory.update_item(item="Carrot", price=1.8, stock=120)
        print("\nItem information updated.")
    except ItemNotFound as e:
        print(f"Error: {e}")

    # View updated item list
    all_items = inventory.view_all_items()
    print("\nUpdated items in the inventory:")
    print(all_items)

    # Try to update today's picks (assuming 'Spinach' is picked today)
    try:
        inventory.update_today_picks('carrot')
        print("\nToday's picks updated.")
    except ItemNotFound as e:
        print(f"Error: {e}")

    # View available items
    available_items = inventory.view_available_items()
    print("\nAvailable items for today:")
    print(available_items)

    try:
        inventory.update_item(item="Carrot", price=2.0, stock=120)
        print("\nItem information updated.")
    except ItemNotFound as e:
        print(f"Error: {e}")

    available_items = inventory.view_available_items()
    print("\nAvailable items for today:")
    print(available_items)
