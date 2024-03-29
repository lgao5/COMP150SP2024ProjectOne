from project_code.src.Statistic import *
#this is abdul testing


class Character:

    def init(self, name, level=1, experience=0, stats=None):
        """
        Core Stats: Everyone has these
        - Strength: How much you can lift. How strong you are. How hard you punch, etc.
        - Dexterity: How quick your limbs can perform intricate tasks. How adept you are at avoiding blows you anticipate. Impacts speed.
        - Constitution: The bodies natural armor. Characters may have unique positive or negative constitutions that provide additional capabilities
        - vitality: A measure of how lively you feel. How many Hit Points you have. An indirect measure of age.
        - Endurance: How fast you recover from injuries. How quickly you recover from fatigue.
        - Intelligence: How smart you are. How quickly you can connect the dots to solve problems. How fast you can think.
        - Wisdom: How effectively you can make choices under pressure. Generally low in younger people.
        - Knowledge: How much you know? This is a raw score for all knowledge. Characters may have specific areas of expertise with a bonus or deficit in some areas.
        - Willpower: How quickly or effectively the character can overcome natural urges. How susceptible they are to mind control.
        - Spirit: Catchall for ability to perform otherworldly acts. High spirit is rare. Different skills have different resource pools they might use like mana, stamina, etc. These are unaffected by spirit. Instead spirit is a measure of how hard it is to learn new otherworldly skills and/or master general skills.
         """
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

    def add_capacities(self, capacities):
        """Add a capacity to the character."""
        self.capacity.append(capacities)
    """
    The add_capacity function in the Character 
    class is designed to manage different types of 
    "capacities" that a character might possess.
    """
    def _generate_name(self):
        return "Bob"

    def __str__(self):
        stats_info = ', '.join(str(stat) for stat in self.stats.values())
        stats_return = f"Character: {self.name}, Stats: {stats_info}, Level: {self.level}, Experience: {self.experience}"
        capacity_info = ', '.join(f"{key}: {value}" for key, value in self.capacity.items())
        capacity_return = f"{super().__str__()}, Capacity: {capacity_info}"
        return stats_return + capacity_return
    
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
                self.stats[stat_name].value = max(self.stats[stat_name].value - reduction, 0)  # Prevent stats from going below 0