from dnd_character import Character
from dnd_character.SRD import SRD_classes
from dnd_character.equipment import SRD_equipment
from ast import literal_eval


def test_keys_values():
    char = Character(experience=200)
    for key, val in zip(char.keys(), char.values()):
        assert char[key] == val
    assert dict(zip(char.keys(), char.values())) == dict(char)


def test_save_and_load_lvl1_character():
    player = Character()
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_save_and_load_lvl3_character():
    player = Character(level=3)
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_save_and_load_lvl1_bard():
    player = Character(classs=SRD_classes["bard"])
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_save_and_load_lvl3_bard():
    player = Character(level=3, classs=SRD_classes["bard"])
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_save_and_load_custom_lvl_character():
    player = Character(level=3, experience=100, constitution=10)
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_save_and_load_experience():
    player = Character(experience=100)
    clone = Character(**dict(player))
    assert player._experience._experience == clone._experience._experience
    assert player.experience.to_next_level == clone.experience.to_next_level


def test_save_and_load_leveled_up_character():
    player = Character(classs=SRD_classes["bard"])
    for i in range(900):
        player.experience += 1
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_literal_eval_constructs_valid_dict():
    char = Character(experience=200)
    str_keys = str(char.keys())
    str_vals = str(char.values())
    assert dict(zip(literal_eval(str_keys), literal_eval(str_vals))) == dict(char)


def test_property_decorated_methods_serialize():
    player = Character(experience=200, dexterity=15)
    clone = Character(**dict(player))
    assert dict(player) == dict(clone)


def test_rolled_stats_serialize():
    player = Character(experience=200)
    serialized_char = Character(**dict(zip(player.keys(), player.values())))
    assert serialized_char.dexterity == player.dexterity


def test_rolled_stats_serialize_after_literal_eval():
    player = Character(experience=200)
    str_keys = str(player.keys())
    str_vals = str(player.values())
    assert (
        Character(**dict(zip(literal_eval(str_keys), literal_eval(str_vals)))).dexterity
        == player.dexterity
    )


def test_save_and_load_hitpoints():
    player = Character()
    player.hp = 6
    assert dict(Character(**dict(player))) == dict(player)


def test_save_and_load_equipment():
    player = Character()
    player.giveItem(SRD_equipment["bagpipes"])
    assert dict(Character(**dict(player))) == dict(player)


def test_save_and_load_armour_class():
    player = Character(dexterity=14)
    assert dict(Character(**dict(player))) == dict(player)


def test_save_and_load_light_armour_class():
    player = Character(classs=SRD_classes["bard"], dexterity=14)
    assert dict(Character(**dict(player))) == dict(player)


def test_save_and_load_heavy_armour_class():
    player = Character(classs=SRD_classes["paladin"], dexterity=14)
    assert dict(Character(**dict(player))) == dict(player)


def test_str_repr():
    player = Character(classs=SRD_classes["fighter"])
    player.giveItem(SRD_equipment["flute"])
    player.experience += 50
    character_repr = str(player)
    mandatory_attrs = [
        "name",
        "age",
        "gender",
        "description",
    ]
    assert sum([f"{attr.title()}: {str(player.__dict__[attr])}" in character_repr for attr in mandatory_attrs]) == len(mandatory_attrs)
    assert f"Biography:\n{str(player.biography)}" in character_repr
    assert f"Class: {str(player.class_name)}" in character_repr
    assert f"Level: {str(player.level)}" in character_repr
    assert f"Experience: {str(player.experience)}" in character_repr
    assert f"to next level: {str(player.experience.to_next_level)}" in character_repr.lower()
    assert sum([value['name'] in character_repr for value in player.proficiencies.values()]) == len(player.proficiencies)
    assert sum([value['name'] in character_repr for value in player.inventory]) == len(player.inventory)
    assert sum([value['name'] in character_repr for value in player.class_features.values()]) == len(player.class_features)
