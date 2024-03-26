# Assuming the existing classes and functions are defined above...
import main.py
# Test Statistic Class
def test_statistic_initialization():
    stat = Statistic("Strength", 10)
    assert 1 <= stat.value <= 20, "Value should be in the range of 1 to 20"
    assert stat.name == "Strength", "Name should be 'Strength'"

# Test Character Class
def test_character_initialization():
    char = Character("Test")
    assert char.name == "Test", "Character name should be 'Test'"
    assert 1 <= char.level == 1, "Initial level should be 1"
    assert 0 <= char.experience == 0, "Initial experience should be 0"
    assert "Strength" in char.stats, "Character should have a 'Strength' stat"
    assert isinstance(char.stats["Strength"], Statistic), "'Strength' should be an instance of Statistic"

# Test add_experience and level_up methods
def test_experience_and_level_up():
    char = Character("Test")
    initial_level = char.level
    char.add_experience(10)
    assert char.experience == 0, "Experience should reset to 0 after leveling up"
    assert char.level == initial_level + 1, "Character should have leveled up"

# Running tests
test_statistic_initialization()
test_character_initialization()
test_experience_and_level_up()

print("All tests passed!")
