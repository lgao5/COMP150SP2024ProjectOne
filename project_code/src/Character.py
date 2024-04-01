from project_code.src.Statistic import *
import random


class Character:
    def __init__(self, name, level=1, experience=0, stats=None):
        legacy_points = random.randint(0, 50)
        self.name = name
        self.level = level
        self.experience = experience
        self.attempted_quests = set()
        self.successful_quests = set()

        if stats:
            self.stats = stats
        else:
            self.stats = {
                "Strength": Statistic("Strength", legacy_points),
                "Dexterity": Statistic("Dexterity", legacy_points),
                "Constitution": Statistic("Constitution", legacy_points),
                "Vitality": Statistic("Vitality", legacy_points),
                "Endurance": Statistic("Endurance", legacy_points),
                "Intelligence": Statistic("Intelligence", legacy_points),
                "Wisdom": Statistic("Wisdom", legacy_points),
                "Knowledge": Statistic("Knowledge", legacy_points),
                "Willpower": Statistic("Willpower", legacy_points),
                "Spirit": Statistic("Spirit", legacy_points)
            }

        self.capacity = {
            "Mana": random.randint(10, 20),
            "Stamina": random.randint(10, 20),
            "Psy": random.randint(10, 20)
        }

    def __str__(self):
        stats_info = ', '.join(str(stat) for stat in self.stats.values())
        capacity_info = ', '.join(f"{key}: {value}" for key, value in self.capacity.items())
        return f"Character: {self.name}, Stats: {stats_info}, Capacity: {capacity_info}, Level: {self.level}, Experience: {self.experience}"

    def add_experience(self, amount):
        self.experience += amount
        if self.experience >= 10:  # Arbitrary value for leveling up
            self.experience -= 10
            self.level_up()

    def level_up(self):
        self.level += 1
        print(f"{self.name} has reached level {self.level}!")

    def rest(self):
        for stat in self.stats.values():
            stat.value += random.randint(1, 3)
        print(f"{self.name} has rested and gained strength.")

    def reduce_stats(self, stats_to_reduce):
        for stat_name, reduction in stats_to_reduce.items():
            if stat_name in self.stats:
                self.stats[stat_name].value = max(self.stats[stat_name].value - reduction, 0)

    def has_completed_all_quests(self):
        return len(self.successful_quests) == 3

    def to_dict(self):
        """Convert character data to a dictionary for saving."""
        return {
            "Name": self.name,
            "Level": self.level,
            "Experience": self.experience,
            "AttemptedQuests": ','.join(self.attempted_quests),
            "SuccessfulQuests": ','.join(self.successful_quests),
            "Strength": self.stats["Strength"].value,
            "Dexterity": self.stats["Dexterity"].value,
            "Constitution": self.stats["Constitution"].value,
            "Vitality": self.stats["Vitality"].value,
            "Endurance": self.stats["Endurance"].value,
            "Intelligence": self.stats["Intelligence"].value,
            "Wisdom": self.stats["Wisdom"].value,
            "Knowledge": self.stats["Knowledge"].value,
            "Willpower": self.stats["Willpower"].value,
            "Spirit": self.stats["Spirit"].value,
            "Mana": self.capacity["Mana"],
            "Stamina": self.capacity["Stamina"],
            "Psy": self.capacity["Psy"]
        }

    @staticmethod
    def from_dict(data):
        """Create a Character object from a dictionary."""
        character = Character(
            name=data["Name"],
            level=int(data["Level"]),
            experience=int(data["Experience"]),
            stats={
                "Strength": Statistic("Strength", int(data["Strength"])),
                "Dexterity": Statistic("Dexterity", int(data["Dexterity"])),
                "Constitution": Statistic("Constitution", int(data["Constitution"])),
                "Vitality": Statistic("Vitality", int(data["Vitality"])),
                "Endurance": Statistic("Endurance", int(data["Endurance"])),
                "Intelligence": Statistic("Intelligence", int(data["Intelligence"])),
                "Wisdom": Statistic("Wisdom", int(data["Wisdom"])),
                "Knowledge": Statistic("Knowledge", int(data["Knowledge"])),
                "Willpower": Statistic("Willpower", int(data["Willpower"])),
                "Spirit": Statistic("Spirit", int(data["Spirit"]))
            },
            # capacities are not saved in the example provided but can be added if needed
        )
        character.attempted_quests = set(data["AttemptedQuests"].split(',')) if data["AttemptedQuests"] else set()
        character.successful_quests = set(data["SuccessfulQuests"].split(',')) if data["SuccessfulQuests"] else set()
        return character