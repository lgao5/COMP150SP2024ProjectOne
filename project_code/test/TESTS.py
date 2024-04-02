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
# Test rest method in Character Class
def test_rest_method():
    char = Character("Test")
    initial_stats = {stat.name: stat.value for stat in char.stats.values()}
    char.rest()
    for stat_name, initial_value in initial_stats.items():
        assert char.stats[stat_name].value > initial_value, "Stat values should increase after resting"

# Test reduce_stats method in Character Class
def test_reduce_stats_method():
    char = Character("Test")
    reduction = {"Strength": 2, "Dexterity": 3}
    initial_strength = char.stats["Strength"].value
    initial_dexterity = char.stats["Dexterity"].value
    char.reduce_stats(reduction)
    assert char.stats["Strength"].value == initial_strength - reduction["Strength"], "Strength should be reduced by 2"
    assert char.stats["Dexterity"].value == initial_dexterity - reduction["Dexterity"], "Dexterity should be reduced by 3"

# Test has_completed_all_quests method in Character Class
def test_completed_all_quests():
    char = Character("Test")
    char.successful_quests = {"Quest1", "Quest2", "Quest3"}
    assert char.has_completed_all_quests() is True, "Should return True when all quests are completed"

# Test Location Class
def test_location_initialization():
    loc = Location("TestLocation", "A test location", [])
    assert loc.name == "TestLocation", "Location name should be 'TestLocation'"
    assert loc.description == "A test location", "Location description should be 'A test location'"

# Test SaveUser.load_characters and SaveUser.save_characters methods
def test_save_load_characters():
    char = Character("Test")
    SaveUser.save_characters([char], filename="test_save.csv")
    loaded_chars = SaveUser.load_characters("test_save.csv")
    assert len(loaded_chars) == 1, "Should load one character"
    loaded_char = loaded_chars[0]
    assert loaded_char.name == char.name, "Loaded character name should match"
    assert loaded_char.level == char.level, "Loaded character level should match"
    assert loaded_char.experience == char.experience, "Loaded character experience should match"

# Running additional tests
test_rest_method()
test_reduce_stats_method()
test_completed_all_quests()
test_location_initialization()
test_save_load_characters()

print("All additional tests passed!")

