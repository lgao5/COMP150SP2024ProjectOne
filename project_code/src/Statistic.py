import random


class Statistic:
    def __init__(self, legacy_points: int):
        self.value = self._generate_starting_value(legacy_points)
        self.description = None
        self.min_value = 0
        self.max_value = 100

    def __str__(self):
        return f"{self.value}"

    def increase(self, amount):
        self.value += amount
        if self.value > self.max_value:
            self.value = self.max_value

    def decrease(self, amount):
        self.value -= amount
        if self.value < self.min_value:
            self.value = self.min_value

    def _generate_starting_value(self, legacy_points: int):
        """Generate a starting value for the statistic based on random number and user properties."""
        """This is just a placeholder for now. Perhaps some statistics will be based on user properties, and others 
        will be random."""
        return legacy_points % 100 + random.randint(1, 3)


class Strength(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Strength is a measure of physical power."

class Dexterity(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Dexterity is a measure of physical speed."

class Constitution(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Constitution is a measure of physical resistance."

class Vitality(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Vitality is a measure of physical health."

class Endurance(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Endurance is a measure of healing speed."

class Intelligence(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Intelligence is a measure of how fast one can solve problems."

class Wisdom(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Wisdom is a measure of effective decision making under pressure."

class Knowledge(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Knowledge is a measure of how much one knows."

class Willpower(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Willpower is a measure of how much resistance to natural urges one has."

class Spirit(Statistic):

    def __init__(self, value):
        super().__init__(value)
        self.description = "Spirit is a measure of how difficult it is to learn new skills."


class Capacity(Statistic):
    def __init__(self, legacy_points: int, capacity_type: str):
        super().__init__(legacy_points)
        self.capacity_type = capacity_type
        self.associated_ability = None
        self.description = f"{capacity_type} capacity is a measure of how much {capacity_type} a character can hold."

    def associate_ability(self, ability_name: str):
        """Associate a specific ability with this capacity."""
        self.associated_ability = ability_name

    def __str__(self):
        if self.associated_ability:
            return f"{self.capacity_type} Capacity for {self.associated_ability}: {self.value}"
        return f"{self.capacity_type} Capacity: {self.value}"

""" 
Example using capacity:
mana_capacity = Capacity(10, 'Mana')
mana_capacity.associate_ability('Fireball')
print(mana_capacity)
"""
