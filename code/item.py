class Item:
    def __init__(self, name, description, icon, effectFunc, stackable=True):
        self.name = name
        self.description = description
        self.icon = icon  # Load an image or None
        self.effectFunc = effectFunc  # Function to call when used
        self.stackable = stackable
