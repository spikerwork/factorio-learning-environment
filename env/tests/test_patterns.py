import unittest
import sys
sys.path.append(r"C:\Users\martb\Documents\paperpclip_max\PaperclipMaximiser")
sys.path.append(r"C:\Users\martb\Documents\paperpclip_max\PaperclipMaximiser\env")
sys.path.append(r"C:\Users\martb\Documents\paperpclip_max\PaperclipMaximiser\env\src")

from env.src.instance import FactorioInstance
from env.src.utils.achievements import eval_program_with_achievements
from env.src.models.game_state import GameState
def test_achievements():
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27000,
                                fast=True,
                                #cache_scripts=False,
                                inventory={})
        instance.speed(10)

        test_string_1 = "pos = nearest(Resource.Stone)\nmove_to(pos)\nharvest_resource(pos, 10)\ncraft_item(Prototype.StoneFurnace, 1)\npos = nearest(Resource.Coal)\nmove_to(pos)\nharvest_resource(pos, 10)\npos = nearest(Resource.IronOre)\nmove_to(pos)\nharvest_resource(pos, 10)\npos = Position(x = 0, y = 0)\nmove_to(pos)\nfurnace = place_entity(Prototype.StoneFurnace, position = pos)\ninsert_item(Prototype.IronOre, furnace, 5)\ninsert_item(Prototype.Coal, furnace, 5)\nsleep(16)\nextract_item(Prototype.IronPlate, furnace.position, 10)"
        _, _, _, achievements = eval_program_with_achievements(instance, test_string_1)
        ground_truth_achievement = {'static': {'stone-furnace': 1, 'coal': 10, 'stone': 10, 'iron-ore': 10}, 'dynamic': {'iron-plate': 5}}
       
        assert achievements == ground_truth_achievement
        test_string = "pos = nearest(Resource.Stone)\nmove_to(pos)\nharvest_resource(pos, 10)\ncraft_item(Prototype.StoneFurnace, 1)\npos = nearest(Resource.Coal)\nmove_to(pos)\nharvest_resource(pos, 10)\npos = nearest(Resource.CopperOre)\nmove_to(pos)\nharvest_resource(pos, 10)\npos = Position(x = 0, y = 0)\nmove_to(pos)\nfurnace = place_entity(Prototype.StoneFurnace, position = pos)\ninsert_item(Prototype.CopperOre, furnace, 5)\ninsert_item(Prototype.Coal, furnace, 5)\nsleep(16)"
        _, _, _, achievements = eval_program_with_achievements(instance, test_string)
        ground_truth_achievement = {'static': {'stone-furnace': 1, 'coal': 10, 'stone': 10, 'copper-ore': 10}, 'dynamic': {'copper-plate': 5}}
        assert achievements == ground_truth_achievement
        test_string = "pos = nearest(Resource.Stone)\nmove_to(pos)\nharvest_resource(pos, 10)\ncraft_item(Prototype.StoneFurnace, 1)\npos = nearest(Resource.Coal)\nmove_to(pos)\nharvest_resource(pos, 10)\npos = nearest(Resource.CopperOre)\nmove_to(pos)\nharvest_resource(pos, 10)\npos = Position(x = 0, y = 0)\nmove_to(pos)\nfurnace = place_entity(Prototype.StoneFurnace, position = pos)\ninsert_item(Prototype.CopperOre, furnace, 5)\ninsert_item(Prototype.Coal, furnace, 5)\nsleep(16)"
        _, _, _, achievements = eval_program_with_achievements(instance, test_string)
        ground_truth_achievement = {'static': {'stone-furnace': 1, 'coal': 10, 'stone': 10, 'copper-ore': 10}, 'dynamic': {'copper-plate': 5}}
        assert achievements == ground_truth_achievement






def test_achievements_1():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY)
        instance.speed(10)
        

        test_string_1 = 'move_to(Position(x=10, y=10))\n \n# Place offshore pump near water\nwater_position = nearest(Resource.Water)\nassert water_position, "No water source found nearby"\nmove_to(water_position)\noffshore_pump = place_entity(Prototype.OffshorePump, Direction.DOWN, water_position)\nassert offshore_pump, "Failed to place offshore pump"\n# Place boiler next to offshore pump\n# Important: The boiler needs to be placed with a spacing of 2 to allow for pipe connections\nboiler = place_entity_next_to(Prototype.Boiler, offshore_pump.position, Direction.DOWN, spacing=2)\nassert boiler, "Failed to place boiler"\n# add coal to the boiler\n# need to update the boiler var after insert\nboiler = insert_item(Prototype.Coal, boiler, quantity=5)\n# Connect offshore pump to boiler with pipes\npipes = connect_entities(offshore_pump, boiler, Prototype.Pipe)\nassert pipes, "Failed to connect offshore pump to boiler"\n# Place steam engine next to boiler\n# Important: The steam engine needs to be placed with a spacing of 2 to allow for pipe connections\nsteam_engine = place_entity_next_to(Prototype.SteamEngine, boiler.position, Direction.LEFT, spacing=2)\nassert steam_engine, "Failed to place steam engine"\n# Connect boiler to steam engine with pipes\npipes = connect_entities(boiler, steam_engine, Prototype.Pipe)\nassert pipes, "Failed to connect boiler to steam engine"\n# check if the boiler is receiving electricity\n# if it says not connected to power network, then it is working\n# it just isnt connected to any power poles\nmove_to(Position(x=0, y=0))\nass_machine = place_entity(Prototype.AssemblingMachine1, Direction.UP, Position(x=0, y=0))\nconnect_entities(ass_machine, steam_engine, Prototype.SmallElectricPole)'
        _, _, _, achievements = eval_program_with_achievements(instance, test_string_1)

        test_string_1 = '"""\nLet\'s analyze what we need for an iron gear wheel factory:\n\n1. Recipe check for iron gear wheel:\n- 2 iron plates per iron gear wheel\n- For 1 iron gear wheel per minute, need 2 iron plates per minute\n- Stone furnace can produce 18 plates/min, so 1 furnace is enough\n- Need iron ore mining to feed the furnace\n- Burner mining drill (15/min) is sufficient for ore\n\n2. Steps:\na) Set up iron ore mining with burner drill\nb) Connect ore to furnace with inserter/belt\nc) Connect plates to assembling machine\nd) Power the assembling machine\ne) Set up output collection\n\nLet\'s implement step by step:\n"""\n\n# First find iron ore patch\niron_pos = nearest(Resource.IronOre)\nmove_to(iron_pos)\n\n# Place burner mining drill\ndrill = place_entity(Prototype.BurnerMiningDrill, position=iron_pos)\n# Add initial fuel\ninsert_item(Prototype.Coal, drill, quantity=5)\n\n# Place furnace with some spacing for belts\nfurnace = place_entity_next_to(\n    Prototype.StoneFurnace,\n    reference_position=drill.position,\n    direction=Direction.RIGHT,\n    spacing=5\n)\n# Add fuel to furnace\ninsert_item(Prototype.Coal, furnace, quantity=5)\n\n# Add inserter to move ore from belt to furnace\nfurnace_input = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace.position,\n    direction=Direction.LEFT\n)\nfurnace_input = rotate_entity(furnace_input, Direction.RIGHT)\n# Fuel the inserter\ninsert_item(Prototype.Coal, furnace_input, quantity=1)\n\n# Connect drill to furnace with belt\nbelt = connect_entities(drill.drop_position, furnace_input.pickup_position, Prototype.TransportBelt)\n\nprint("Initial mining and smelting setup complete. Will check production after a few seconds.")\nsleep(10)\nass_macine = get_entity(Prototype.AssemblingMachine1, position=Position(x=0, y=0))\n# place inserter to move plates to assembling machine\nfurn_out = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position  = furnace.position,\n    direction = Direction.RIGHT)\nass_in = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position  = ass_macine.position,\n    direction = Direction.RIGHT)\nass_in = rotate_entity(ass_in, Direction.LEFT)\nset_entity_recipe(ass_macine, Prototype.IronGearWheel)\nconnect_entities( furn_out,ass_in, Prototype.TransportBelt)\nsleep(60)'
        _, _, _, achievements = eval_program_with_achievements(instance, test_string_1)

        print(achievements)

def test_achievements_3():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY)
        test_string_1 = 'connect_entities(Position(x = -4.5, y = -1.5), Position(x = -11.5, y = 22.5), Prototype.SmallElectricPole)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print("asda")


def test_achievements_4():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY)

        #test_string_1 = '# Find copper ore patch\ncopper_pos = nearest(Resource.CopperOre)\nprint(f"Found copper ore at {copper_pos}")\n\n# Move there and place first drill\nmove_to(copper_pos)\ndrill1 = place_entity(Prototype.BurnerMiningDrill, position=copper_pos)\ndrill1 = insert_item(Prototype.Coal, drill1, quantity=5)\nprint(f"Placed first drill at {drill1.position}")\n\n# Place second drill\ndrill2_pos = Position(x=drill1.position.x + 3, y=drill1.position.y)\nmove_to(drill2_pos)\ndrill2 = place_entity(Prototype.BurnerMiningDrill, position=drill2_pos)\ndrill2 = insert_item(Prototype.Coal, drill2, quantity=5)\nprint(f"Placed second drill at {drill2.position}")\n\n# Place third drill\ndrill3_pos = Position(x=drill2.position.x + 3, y=drill2.position.y)\nmove_to(drill3_pos)\ndrill3 = place_entity(Prototype.BurnerMiningDrill, position=drill3_pos)\ndrill3 = insert_item(Prototype.Coal, drill3, quantity=5)\nprint(f"Placed third drill at {drill3.position}")\n\n# Log the positions for next step\nprint(f"Drill positions: {drill1.position}, {drill2.position}, {drill3.position}")\n# Place first furnace north of middle drill\nfurnace1_pos = Position(x=22.0, y=10.0)\nmove_to(furnace1_pos)\nfurnace1 = place_entity(Prototype.StoneFurnace, position=furnace1_pos)\nfurnace1 = insert_item(Prototype.Coal, furnace1, quantity=5)\nprint(f"Placed first furnace at {furnace1.position}")\n\n# Place second furnace next to first\nfurnace2_pos = Position(x=24.0, y=10.0)\nmove_to(furnace2_pos)\nfurnace2 = place_entity(Prototype.StoneFurnace, position=furnace2_pos)\nfurnace2 = insert_item(Prototype.Coal, furnace2, quantity=5)\nprint(f"Placed second furnace at {furnace2.position}")\n\n# Get the drill entities again to ensure fresh state\ndrill1 = get_entity(Prototype.BurnerMiningDrill, Position(x=20.0, y=20.0))\ndrill2 = get_entity(Prototype.BurnerMiningDrill, Position(x=23.0, y=20.0))\ndrill3 = get_entity(Prototype.BurnerMiningDrill, Position(x=26.0, y=20.0))\n\n# Connect drills with transport belts to create a collection line\nbelts1 = connect_entities(drill1.drop_position, drill2.drop_position, Prototype.TransportBelt)\nbelts2 = connect_entities(drill2.drop_position, drill3.drop_position, Prototype.TransportBelt)\n\n# Connect the collection line to both furnaces using inserters\n# Place inserter for first furnace\ninserter1 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace1.position,\n    direction=Direction.DOWN,\n    spacing=0\n)\ninserter1 = insert_item(Prototype.Coal, inserter1, quantity=1)\nprint(f"Placed first inserter at {inserter1.position}")\n\n# Place inserter for second furnace\ninserter2 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace2.position,\n    direction=Direction.DOWN,\n    spacing=0\n)\ninserter2 = insert_item(Prototype.Coal, inserter2, quantity=1)\nprint(f"Placed second inserter at {inserter2.position}")\n\n# Connect collection line to furnace inserters\nconnect_entities(drill2.drop_position, inserter1.pickup_position, Prototype.TransportBelt)\nconnect_entities(drill3.drop_position, inserter2.pickup_position, Prototype.TransportBelt)\n\n# Log current state\n# Get existing inserters\ninserter1 = get_entity(Prototype.BurnerInserter, Position(x=22.5, y=11.5))\ninserter2 = get_entity(Prototype.BurnerInserter, Position(x=24.5, y=11.5))\n\n# Rotate input inserters to pick up from belts and insert into furnaces\ninserter1 = rotate_entity(inserter1, Direction.UP)\ninserter2 = rotate_entity(inserter2, Direction.UP)\n\n# Add output inserters for furnaces\n# First furnace output inserter\noutput_inserter1 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=Position(x=22.0, y=16.0),  # first furnace position\n    direction=Direction.RIGHT,\n    spacing=0\n)\noutput_inserter1 = insert_item(Prototype.Coal, output_inserter1, quantity=1)\nprint(f"Placed first output inserter at {output_inserter1.position}")\n\n# Second furnace output inserter\noutput_inserter2 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=Position(x=24.0, y=16.0),  # second furnace position\n    direction=Direction.RIGHT,\n    spacing=0\n)\noutput_inserter2 = insert_item(Prototype.Coal, output_inserter2, quantity=1)\nprint(f"Placed second output inserter at {output_inserter2.position}")\n\n# Place a chest to collect copper plates\ncollection_chest = place_entity(\n    Prototype.WoodenChest,\n    position=Position(x=26.0, y=16.0)  # Right of second furnace\n)\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Connect output inserters to chest with belts\nconnect_entities(output_inserter1.drop_position, collection_chest.position, Prototype.TransportBelt)\nconnect_entities(output_inserter2.drop_position, collection_chest.position, Prototype.TransportBelt)\n\n# Log current state'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print("asda")
        test_string_1 = '# Find copper ore patch\ncopper_pos = nearest(Resource.CopperOre)\nprint(f"Found copper ore at {copper_pos}")\n\n# Move there and place first drill\nmove_to(copper_pos)\ndrill1 = place_entity(Prototype.BurnerMiningDrill, position=copper_pos)\ndrill1 = insert_item(Prototype.Coal, drill1, quantity=5)\nprint(f"Placed first drill at {drill1.position}")\n\n# Place second drill\ndrill2_pos = Position(x=drill1.position.x + 3, y=drill1.position.y)\nmove_to(drill2_pos)\ndrill2 = place_entity(Prototype.BurnerMiningDrill, position=drill2_pos)\ndrill2 = insert_item(Prototype.Coal, drill2, quantity=5)\nprint(f"Placed second drill at {drill2.position}")\n\n# Place third drill\ndrill3_pos = Position(x=drill2.position.x + 3, y=drill2.position.y)\nmove_to(drill3_pos)\ndrill3 = place_entity(Prototype.BurnerMiningDrill, position=drill3_pos)\ndrill3 = insert_item(Prototype.Coal, drill3, quantity=5)\nprint(f"Placed third drill at {drill3.position}")\n\n# Log the positions for next step\nprint(f"Drill positions: {drill1.position}, {drill2.position}, {drill3.position}")\nprint(f"Current inventory: {inspect_inventory()}")\nprint(f"Updated entities on the map: {get_entities()}")\n'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        test_string_1 = '# Place first furnace north of middle drill\nfurnace1_pos = Position(x=22.0, y=10.0)\nmove_to(furnace1_pos)\nfurnace1 = place_entity(Prototype.StoneFurnace, position=furnace1_pos)\nfurnace1 = insert_item(Prototype.Coal, furnace1, quantity=5)\nprint(f"Placed first furnace at {furnace1.position}")\n\n# Place second furnace next to first\nfurnace2_pos = Position(x=24.0, y=10.0)\nmove_to(furnace2_pos)\nfurnace2 = place_entity(Prototype.StoneFurnace, position=furnace2_pos)\nfurnace2 = insert_item(Prototype.Coal, furnace2, quantity=5)\nprint(f"Placed second furnace at {furnace2.position}")\n\n# Get the drill entities again to ensure fresh state\ndrill1 = get_entity(Prototype.BurnerMiningDrill, Position(x=20.0, y=20.0))\ndrill2 = get_entity(Prototype.BurnerMiningDrill, Position(x=23.0, y=20.0))\ndrill3 = get_entity(Prototype.BurnerMiningDrill, Position(x=26.0, y=20.0))\n\n# Connect drills with transport belts to create a collection line\nbelts1 = connect_entities(drill1.drop_position, drill2.drop_position, Prototype.TransportBelt)\nbelts2 = connect_entities(drill2.drop_position, drill3.drop_position, Prototype.TransportBelt)\n\n# Connect the collection line to both furnaces using inserters\n# Place inserter for first furnace\ninserter1 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace1.position,\n    direction=Direction.DOWN,\n    spacing=0\n)\ninserter1 = insert_item(Prototype.Coal, inserter1, quantity=1)\nprint(f"Placed first inserter at {inserter1.position}")\n\n# Place inserter for second furnace\ninserter2 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace2.position,\n    direction=Direction.DOWN,\n    spacing=0\n)\ninserter2 = insert_item(Prototype.Coal, inserter2, quantity=1)\nprint(f"Placed second inserter at {inserter2.position}")\n\n# Connect collection line to furnace inserters\nconnect_entities(drill2.drop_position, inserter1.pickup_position, Prototype.TransportBelt)\nconnect_entities(drill3.drop_position, inserter2.pickup_position, Prototype.TransportBelt)\n\n# Log current state\nprint(f"Current inventory: {inspect_inventory()}")\nprint(f"Updated entities: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        test_string_1 = '# Get existing inserters\ninserter1 = get_entity(Prototype.BurnerInserter, Position(x=22.5, y=11.5))\ninserter2 = get_entity(Prototype.BurnerInserter, Position(x=24.5, y=11.5))\n\n# Rotate input inserters to pick up from belts and insert into furnaces\ninserter1 = rotate_entity(inserter1, Direction.UP)\ninserter2 = rotate_entity(inserter2, Direction.UP)\n\n# Add output inserters for furnaces\n# First furnace output inserter\noutput_inserter1 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=Position(x=22.0, y=16.0),  # first furnace position\n    direction=Direction.RIGHT,\n    spacing=0\n)\noutput_inserter1 = insert_item(Prototype.Coal, output_inserter1, quantity=1)\nprint(f"Placed first output inserter at {output_inserter1.position}")\n\n# Second furnace output inserter\noutput_inserter2 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=Position(x=24.0, y=16.0),  # second furnace position\n    direction=Direction.RIGHT,\n    spacing=0\n)\noutput_inserter2 = insert_item(Prototype.Coal, output_inserter2, quantity=1)\nprint(f"Placed second output inserter at {output_inserter2.position}")\n\n# Place a chest to collect copper plates\ncollection_chest = place_entity(\n    Prototype.WoodenChest,\n    position=Position(x=26.0, y=16.0)  # Right of second furnace\n)\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Connect output inserters to chest with belts\nconnect_entities(output_inserter1.drop_position, collection_chest.position, Prototype.TransportBelt)\nconnect_entities(output_inserter2.drop_position, collection_chest.position, Prototype.TransportBelt)\n\n# Log current state\nprint(f"Current inventory: {inspect_inventory()}")\nprint(f"Updated entities: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        
        print("asda")


def test_achievements_5():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY)

        #test_string_1 = '# Find copper ore patch\ncopper_pos = nearest(Resource.CopperOre)\nprint(f"Found copper ore at {copper_pos}")\n\n# Move there and place first drill\nmove_to(copper_pos)\ndrill1 = place_entity(Prototype.BurnerMiningDrill, position=copper_pos)\ndrill1 = insert_item(Prototype.Coal, drill1, quantity=5)\nprint(f"Placed first drill at {drill1.position}")\n\n# Place second drill\ndrill2_pos = Position(x=drill1.position.x + 3, y=drill1.position.y)\nmove_to(drill2_pos)\ndrill2 = place_entity(Prototype.BurnerMiningDrill, position=drill2_pos)\ndrill2 = insert_item(Prototype.Coal, drill2, quantity=5)\nprint(f"Placed second drill at {drill2.position}")\n\n# Place third drill\ndrill3_pos = Position(x=drill2.position.x + 3, y=drill2.position.y)\nmove_to(drill3_pos)\ndrill3 = place_entity(Prototype.BurnerMiningDrill, position=drill3_pos)\ndrill3 = insert_item(Prototype.Coal, drill3, quantity=5)\nprint(f"Placed third drill at {drill3.position}")\n\n# Log the positions for next step\nprint(f"Drill positions: {drill1.position}, {drill2.position}, {drill3.position}")\n# Place first furnace north of middle drill\nfurnace1_pos = Position(x=22.0, y=10.0)\nmove_to(furnace1_pos)\nfurnace1 = place_entity(Prototype.StoneFurnace, position=furnace1_pos)\nfurnace1 = insert_item(Prototype.Coal, furnace1, quantity=5)\nprint(f"Placed first furnace at {furnace1.position}")\n\n# Place second furnace next to first\nfurnace2_pos = Position(x=24.0, y=10.0)\nmove_to(furnace2_pos)\nfurnace2 = place_entity(Prototype.StoneFurnace, position=furnace2_pos)\nfurnace2 = insert_item(Prototype.Coal, furnace2, quantity=5)\nprint(f"Placed second furnace at {furnace2.position}")\n\n# Get the drill entities again to ensure fresh state\ndrill1 = get_entity(Prototype.BurnerMiningDrill, Position(x=20.0, y=20.0))\ndrill2 = get_entity(Prototype.BurnerMiningDrill, Position(x=23.0, y=20.0))\ndrill3 = get_entity(Prototype.BurnerMiningDrill, Position(x=26.0, y=20.0))\n\n# Connect drills with transport belts to create a collection line\nbelts1 = connect_entities(drill1.drop_position, drill2.drop_position, Prototype.TransportBelt)\nbelts2 = connect_entities(drill2.drop_position, drill3.drop_position, Prototype.TransportBelt)\n\n# Connect the collection line to both furnaces using inserters\n# Place inserter for first furnace\ninserter1 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace1.position,\n    direction=Direction.DOWN,\n    spacing=0\n)\ninserter1 = insert_item(Prototype.Coal, inserter1, quantity=1)\nprint(f"Placed first inserter at {inserter1.position}")\n\n# Place inserter for second furnace\ninserter2 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace2.position,\n    direction=Direction.DOWN,\n    spacing=0\n)\ninserter2 = insert_item(Prototype.Coal, inserter2, quantity=1)\nprint(f"Placed second inserter at {inserter2.position}")\n\n# Connect collection line to furnace inserters\nconnect_entities(drill2.drop_position, inserter1.pickup_position, Prototype.TransportBelt)\nconnect_entities(drill3.drop_position, inserter2.pickup_position, Prototype.TransportBelt)\n\n# Log current state\n# Get existing inserters\ninserter1 = get_entity(Prototype.BurnerInserter, Position(x=22.5, y=11.5))\ninserter2 = get_entity(Prototype.BurnerInserter, Position(x=24.5, y=11.5))\n\n# Rotate input inserters to pick up from belts and insert into furnaces\ninserter1 = rotate_entity(inserter1, Direction.UP)\ninserter2 = rotate_entity(inserter2, Direction.UP)\n\n# Add output inserters for furnaces\n# First furnace output inserter\noutput_inserter1 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=Position(x=22.0, y=16.0),  # first furnace position\n    direction=Direction.RIGHT,\n    spacing=0\n)\noutput_inserter1 = insert_item(Prototype.Coal, output_inserter1, quantity=1)\nprint(f"Placed first output inserter at {output_inserter1.position}")\n\n# Second furnace output inserter\noutput_inserter2 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=Position(x=24.0, y=16.0),  # second furnace position\n    direction=Direction.RIGHT,\n    spacing=0\n)\noutput_inserter2 = insert_item(Prototype.Coal, output_inserter2, quantity=1)\nprint(f"Placed second output inserter at {output_inserter2.position}")\n\n# Place a chest to collect copper plates\ncollection_chest = place_entity(\n    Prototype.WoodenChest,\n    position=Position(x=26.0, y=16.0)  # Right of second furnace\n)\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Connect output inserters to chest with belts\nconnect_entities(output_inserter1.drop_position, collection_chest.position, Prototype.TransportBelt)\nconnect_entities(output_inserter2.drop_position, collection_chest.position, Prototype.TransportBelt)\n\n# Log current state'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print("asda")
        test_string_1 = '# Find copper patch\ncopper_pos = nearest(Resource.CopperOre)\nprint(f"Found copper at {copper_pos}")\n\n# Find water for power\nwater_pos = nearest(Resource.Water) \nprint(f"Found water at {water_pos}")\n\n# Place power infrastructure\nmove_to(water_pos)\npump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed pump at {pump.position}")\n\n# Place boiler with spacing for pipes\nboiler = place_entity_next_to(\n    Prototype.Boiler,\n    reference_position=pump.position,\n    direction=Direction.RIGHT,\n    spacing=3\n)\nprint(f"Placed boiler at {boiler.position}")\n\n# Add steam engine with spacing\nsteam_engine = place_entity_next_to(\n    Prototype.SteamEngine,\n    reference_position=boiler.position,\n    direction=Direction.RIGHT,\n    spacing=3\n)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect with pipes\nconnect_entities(pump, boiler, Prototype.Pipe)\nconnect_entities(boiler, steam_engine, Prototype.Pipe)\n\n# Add fuel to boiler\nboiler = insert_item(Prototype.Coal, boiler, quantity=50)\n\n# Place first electric mining drill\nmove_to(copper_pos)\ndrill1 = place_entity(Prototype.ElectricMiningDrill, position=copper_pos)\nprint(f"Placed first drill at {drill1.position}")\n\n# Connect power to drill\nconnect_entities(steam_engine.position, drill1.position, Prototype.SmallElectricPole)\n\n# Log key positions for next steps\nprint(f"Steam engine at: {steam_engine.position}")\nprint(f"First drill at: {drill1.position}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        test_string_1 = '# Get updated drill1 entity\ndrill1 = get_entity(Prototype.ElectricMiningDrill, Position(x=19.5, y=19.5))\n\n# Place first furnace ~10 spaces away from drill1\'s drop position\nfurnace_pos = Position(x=drill1.position.x + 10, y=drill1.position.y)\nmove_to(furnace_pos)\nfurnace1 = place_entity(Prototype.StoneFurnace, position=furnace_pos)\nprint(f"Placed first furnace at {furnace1.position}")\n\n# Place inserter next to furnace\n# Always use 0 spacing for inserters\nfurnace1_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace1.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\nprint(f"Placed furnace inserter at {furnace1_inserter.position}")\n\n# Rotate inserter to put items into furnace (180 degrees from default)\nfurnace1_inserter = rotate_entity(furnace1_inserter, Direction.RIGHT)\n\n# Add fuel to inserter and furnace\nfurnace1_inserter = insert_item(Prototype.Coal, furnace1_inserter, quantity=20)\nfurnace1 = insert_item(Prototype.Coal, furnace1, quantity=20)\n\n# Connect drill output to furnace inserter with belts\n# IMPORTANT: Always connect belts to inserter pickup position, never directly to furnace\nconnect_entities(\n    drill1.drop_position,\n    furnace1_inserter.pickup_position,\n    Prototype.TransportBelt\n)\n\n# Log positions and status\nprint(f"First furnace at: {furnace1.position}")\nprint(f"First furnace inserter at: {furnace1_inserter.position}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        test_string_1 = '# Get updated drill1 position\ndrill1 = get_entity(Prototype.ElectricMiningDrill, Position(x=19.5, y=19.5))\n\n# Place second drill 3 tiles to the right of first drill (accounting for 3x3 size)\ndrill2_pos = Position(x=drill1.position.x + 3, y=drill1.position.y)\nmove_to(drill2_pos)\ndrill2 = place_entity(Prototype.ElectricMiningDrill, position=drill2_pos)\nprint(f"Placed second drill at {drill2.position}")\n\n# Connect power to second drill\nconnect_entities(drill1.position, drill2.position, Prototype.SmallElectricPole)\n\n# Get first furnace position\nfurnace1 = get_entity(Prototype.StoneFurnace, Position(x=30.0, y=20.0))\n\n# Place second furnace 2 tiles to the right of first furnace (accounting for 2x2 size)\nfurnace2_pos = Position(x=furnace1.position.x + 2, y=furnace1.position.y)\nmove_to(furnace2_pos)\nfurnace2 = place_entity(Prototype.StoneFurnace, position=furnace2_pos)\nprint(f"Placed second furnace at {furnace2.position}")\n\n# Place inserter for second furnace\n# Always use 0 spacing for inserters\nfurnace2_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace2.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\nprint(f"Placed second furnace inserter at {furnace2_inserter.position}")\n\n# Rotate inserter to put items into furnace\nfurnace2_inserter = rotate_entity(furnace2_inserter, Direction.RIGHT)\n\n# Add fuel to new entities\nfurnace2_inserter = insert_item(Prototype.Coal, furnace2_inserter, quantity=20)\nfurnace2 = insert_item(Prototype.Coal, furnace2, quantity=20)\n\n# Connect second drill to second furnace inserter\nconnect_entities(\n    drill2.drop_position,\n    furnace2_inserter.pickup_position,\n    Prototype.TransportBelt\n)\n\n# Log positions and status\nprint(f"Second drill at: {drill2.position}")\nprint(f"Second furnace at: {furnace2.position}")\nprint(f"Second furnace inserter at: {furnace2_inserter.position}")'

        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        test_string_1 = '# First pickup the misplaced furnace\npickup_entity(Prototype.StoneFurnace, Position(x=32.0, y=20.0))\n\n# Place second furnace with more spacing (3 tiles) from first furnace\nfurnace1 = get_entity(Prototype.StoneFurnace, Position(x=30.0, y=20.0))\nfurnace2_pos = Position(x=furnace1.position.x + 3, y=furnace1.position.y)\nmove_to(furnace2_pos)\nfurnace2 = place_entity(Prototype.StoneFurnace, position=furnace2_pos)\nprint(f"Placed second furnace at {furnace2.position}")\n\n# Place inserter for second furnace\n# Always use 0 spacing for inserters\nfurnace2_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace2.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\nprint(f"Placed second furnace inserter at {furnace2_inserter.position}")\n\n# Rotate inserter to put items into furnace\nfurnace2_inserter = rotate_entity(furnace2_inserter, Direction.RIGHT)\n\n# Add fuel to new entities\nfurnace2_inserter = insert_item(Prototype.Coal, furnace2_inserter, quantity=20)\nfurnace2 = insert_item(Prototype.Coal, furnace2, quantity=20)\n\n# Get second drill\ndrill2 = get_entity(Prototype.ElectricMiningDrill, Position(x=22.5, y=19.5))\n\n# Connect second drill to second furnace inserter\nconnect_entities(\n    drill2.drop_position,\n    furnace2_inserter.pickup_position,\n    Prototype.TransportBelt\n)\n\n# Log positions and status\nprint(f"Second furnace at: {furnace2.position}")\nprint(f"Second furnace inserter at: {furnace2_inserter.position}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        
        print("asda")

def test_achievements_6():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY)

        #test_string_1 = '# Find copper ore patch\ncopper_pos = nearest(Resource.CopperOre)\nprint(f"Found copper ore at {copper_pos}")\n\n# Move there and place first drill\nmove_to(copper_pos)\ndrill1 = place_entity(Prototype.BurnerMiningDrill, position=copper_pos)\ndrill1 = insert_item(Prototype.Coal, drill1, quantity=5)\nprint(f"Placed first drill at {drill1.position}")\n\n# Place second drill\ndrill2_pos = Position(x=drill1.position.x + 3, y=drill1.position.y)\nmove_to(drill2_pos)\ndrill2 = place_entity(Prototype.BurnerMiningDrill, position=drill2_pos)\ndrill2 = insert_item(Prototype.Coal, drill2, quantity=5)\nprint(f"Placed second drill at {drill2.position}")\n\n# Place third drill\ndrill3_pos = Position(x=drill2.position.x + 3, y=drill2.position.y)\nmove_to(drill3_pos)\ndrill3 = place_entity(Prototype.BurnerMiningDrill, position=drill3_pos)\ndrill3 = insert_item(Prototype.Coal, drill3, quantity=5)\nprint(f"Placed third drill at {drill3.position}")\n\n# Log the positions for next step\nprint(f"Drill positions: {drill1.position}, {drill2.position}, {drill3.position}")\n# Place first furnace north of middle drill\nfurnace1_pos = Position(x=22.0, y=10.0)\nmove_to(furnace1_pos)\nfurnace1 = place_entity(Prototype.StoneFurnace, position=furnace1_pos)\nfurnace1 = insert_item(Prototype.Coal, furnace1, quantity=5)\nprint(f"Placed first furnace at {furnace1.position}")\n\n# Place second furnace next to first\nfurnace2_pos = Position(x=24.0, y=10.0)\nmove_to(furnace2_pos)\nfurnace2 = place_entity(Prototype.StoneFurnace, position=furnace2_pos)\nfurnace2 = insert_item(Prototype.Coal, furnace2, quantity=5)\nprint(f"Placed second furnace at {furnace2.position}")\n\n# Get the drill entities again to ensure fresh state\ndrill1 = get_entity(Prototype.BurnerMiningDrill, Position(x=20.0, y=20.0))\ndrill2 = get_entity(Prototype.BurnerMiningDrill, Position(x=23.0, y=20.0))\ndrill3 = get_entity(Prototype.BurnerMiningDrill, Position(x=26.0, y=20.0))\n\n# Connect drills with transport belts to create a collection line\nbelts1 = connect_entities(drill1.drop_position, drill2.drop_position, Prototype.TransportBelt)\nbelts2 = connect_entities(drill2.drop_position, drill3.drop_position, Prototype.TransportBelt)\n\n# Connect the collection line to both furnaces using inserters\n# Place inserter for first furnace\ninserter1 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace1.position,\n    direction=Direction.DOWN,\n    spacing=0\n)\ninserter1 = insert_item(Prototype.Coal, inserter1, quantity=1)\nprint(f"Placed first inserter at {inserter1.position}")\n\n# Place inserter for second furnace\ninserter2 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace2.position,\n    direction=Direction.DOWN,\n    spacing=0\n)\ninserter2 = insert_item(Prototype.Coal, inserter2, quantity=1)\nprint(f"Placed second inserter at {inserter2.position}")\n\n# Connect collection line to furnace inserters\nconnect_entities(drill2.drop_position, inserter1.pickup_position, Prototype.TransportBelt)\nconnect_entities(drill3.drop_position, inserter2.pickup_position, Prototype.TransportBelt)\n\n# Log current state\n# Get existing inserters\ninserter1 = get_entity(Prototype.BurnerInserter, Position(x=22.5, y=11.5))\ninserter2 = get_entity(Prototype.BurnerInserter, Position(x=24.5, y=11.5))\n\n# Rotate input inserters to pick up from belts and insert into furnaces\ninserter1 = rotate_entity(inserter1, Direction.UP)\ninserter2 = rotate_entity(inserter2, Direction.UP)\n\n# Add output inserters for furnaces\n# First furnace output inserter\noutput_inserter1 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=Position(x=22.0, y=16.0),  # first furnace position\n    direction=Direction.RIGHT,\n    spacing=0\n)\noutput_inserter1 = insert_item(Prototype.Coal, output_inserter1, quantity=1)\nprint(f"Placed first output inserter at {output_inserter1.position}")\n\n# Second furnace output inserter\noutput_inserter2 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=Position(x=24.0, y=16.0),  # second furnace position\n    direction=Direction.RIGHT,\n    spacing=0\n)\noutput_inserter2 = insert_item(Prototype.Coal, output_inserter2, quantity=1)\nprint(f"Placed second output inserter at {output_inserter2.position}")\n\n# Place a chest to collect copper plates\ncollection_chest = place_entity(\n    Prototype.WoodenChest,\n    position=Position(x=26.0, y=16.0)  # Right of second furnace\n)\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Connect output inserters to chest with belts\nconnect_entities(output_inserter1.drop_position, collection_chest.position, Prototype.TransportBelt)\nconnect_entities(output_inserter2.drop_position, collection_chest.position, Prototype.TransportBelt)\n\n# Log current state'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print("asda")
        test_string_1 = '# Find copper ore patch\ncopper_pos = nearest(Resource.CopperOre)\nprint(f"Found copper ore at {copper_pos}")\n\n# Place first electric mining drill\nmove_to(copper_pos)\ndrill1 = place_entity(Prototype.ElectricMiningDrill, position=copper_pos)\nprint(f"Placed first drill at {drill1.position}")\n\n# Place second drill next to it\ndrill2 = place_entity_next_to(\n    Prototype.ElectricMiningDrill,\n    reference_position=drill1.position,\n    direction=Direction.RIGHT,\n    spacing=1\n)\nprint(f"Placed second drill at {drill2.position}")\n\n# Log the drill positions for future reference\nprint(f"Drill 1 drop position: {drill1.drop_position}")\nprint(f"Drill 2 drop position: {drill2.drop_position}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        test_string_1 = '# Find water and place offshore pump\nwater_pos = nearest(Resource.Water)\nprint(f"Found water at {water_pos}")\nmove_to(water_pos)\npump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {pump.position}")\n\n# Place boiler with spacing for pipes\nboiler = place_entity_next_to(\n    Prototype.Boiler,\n    reference_position=pump.position,\n    direction=Direction.RIGHT,\n    spacing=3\n)\nprint(f"Placed boiler at {boiler.position}")\n\n# Place steam engine\nsteam_engine = place_entity_next_to(\n    Prototype.SteamEngine,\n    reference_position=boiler.position,\n    direction=Direction.RIGHT,\n    spacing=3\n)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect pump to boiler with pipes\nwater_pipes = connect_entities(pump, boiler, Prototype.Pipe)\nprint("Connected pump to boiler")\n\n# Connect boiler to steam engine with pipes\nsteam_pipes = connect_entities(boiler, steam_engine, Prototype.Pipe)\nprint("Connected boiler to steam engine")\n\n# Add fuel to boiler\nboiler = insert_item(Prototype.Coal, boiler, quantity=50)\nprint("Added fuel to boiler")\n\n# Connect power to drills using small electric poles\ndrill1 = get_entity(Prototype.ElectricMiningDrill, Position(x=19.5, y=19.5))\ndrill2 = get_entity(Prototype.ElectricMiningDrill, Position(x=23.5, y=19.5))\n\nconnect_entities(steam_engine.position, drill1.position, Prototype.SmallElectricPole)\nconnect_entities(drill1.position, drill2.position, Prototype.SmallElectricPole)\n\nprint("Connected power to drills")\nsleep(5)  # Wait for power to stabilize\n\n# Verify power status\ndrill1 = get_entity(Prototype.ElectricMiningDrill, Position(x=19.5, y=19.5))\ndrill2 = get_entity(Prototype.ElectricMiningDrill, Position(x=23.5, y=19.5))\nprint(f"Drill 1 status: {drill1.status}")\nprint(f"Drill 2 status: {drill2.status}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        test_string_1 = '# Place furnaces 10 spaces south of drill1\'s drop position\nfurnace_start_pos = Position(x=drill1.position.x, y=drill1.position.y + 10)\nmove_to(furnace_start_pos)\n\n# Place two furnaces side by side\nfurnace1 = place_entity(Prototype.StoneFurnace, position=furnace_start_pos)\nprint(f"Placed first furnace at {furnace1.position}")\n\nfurnace2 = place_entity_next_to(\n    Prototype.StoneFurnace,\n    reference_position=furnace1.position,\n    direction=Direction.RIGHT,\n    spacing=1\n)\nprint(f"Placed second furnace at {furnace2.position}")\n\n# Add input inserters for both furnaces\n# always use 0 spacing for inserters\nfurnace1_input = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace1.position,\n    direction=Direction.UP,\n    spacing=0\n)\nprint(f"Placed furnace1 input inserter at {furnace1_input.position}")\n\nfurnace2_input = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace2.position,\n    direction=Direction.UP,\n    spacing=0\n)\nprint(f"Placed furnace2 input inserter at {furnace2_input.position}")\n\n# Add fuel to inserters\nfurnace1_input = insert_item(Prototype.Coal, furnace1_input, quantity=20)\nfurnace2_input = insert_item(Prototype.Coal, furnace2_input, quantity=20)\n\n# Add fuel to furnaces\nfurnace1 = insert_item(Prototype.Coal, furnace1, quantity=20)\nfurnace2 = insert_item(Prototype.Coal, furnace2, quantity=20)\n\n# Connect drill1\'s output to furnace input inserters with belts\nbelts1 = connect_entities(\n    drill1.drop_position,\n    furnace1_input.pickup_position,\n    Prototype.TransportBelt\n)\n\n# Connect drill2\'s output to furnace input inserters with belts\nbelts2 = connect_entities(\n    drill2.drop_position,\n    furnace2_input.pickup_position,\n    Prototype.TransportBelt\n)\n\nprint("Connected drills to furnaces with belts")\n\n# Place wooden chest for output 5 spaces south of furnaces\nchest_pos = Position(x=furnace1.position.x + 1, y=furnace1.position.y + 5)\nmove_to(chest_pos)\noutput_chest = place_entity(Prototype.WoodenChest, position=chest_pos)\nprint(f"Placed output chest at {output_chest.position}")\n\n# Add output inserters for both furnaces\n# always use 0 spacing for inserters\nfurnace1_output = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace1.position,\n    direction=Direction.DOWN,\n    spacing=0\n)\nfurnace1_output = rotate_entity(furnace1_output, Direction.DOWN)\nfurnace1_output = insert_item(Prototype.Coal, furnace1_output, quantity=20)\n\nfurnace2_output = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace2.position,\n    direction=Direction.DOWN,\n    spacing=0\n)\nfurnace2_output = rotate_entity(furnace2_output, Direction.DOWN)\nfurnace2_output = insert_item(Prototype.Coal, furnace2_output, quantity=20)\n\n# Connect output inserters to chest with belts\nconnect_entities(furnace1_output.drop_position, output_chest.position, Prototype.TransportBelt)\nconnect_entities(furnace2_output.drop_position, output_chest.position, Prototype.TransportBelt)\n\nprint("Connected furnaces to output chest")'

        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        test_string_1 = '# Get current entities\ndrill1 = get_entity(Prototype.ElectricMiningDrill, Position(x=19.5, y=19.5))\ndrill2 = get_entity(Prototype.ElectricMiningDrill, Position(x=23.5, y=19.5))\nfurnace1 = get_entity(Prototype.StoneFurnace, Position(x=20.0, y=30.0))\nfurnace2 = get_entity(Prototype.StoneFurnace, Position(x=23.0, y=30.0))\nfurnace1_input = get_entity(Prototype.BurnerInserter, Position(x=20.5, y=28.5))\nfurnace2_input = get_entity(Prototype.BurnerInserter, Position(x=23.5, y=28.5))\n\n# Fix input inserter rotations - they need to face DOWN to put items into furnaces\nfurnace1_input = rotate_entity(furnace1_input, Direction.DOWN)\nfurnace2_input = rotate_entity(furnace2_input, Direction.DOWN)\n\n# Reconnect belts from drills to furnace input inserters\n# First remove any existing belts by picking them up\nprint("Reconnecting belts from drills to furnaces")\n\n# Connect drill1 to furnace1 input inserter\nbelts1 = connect_entities(\n    drill1.drop_position,\n    furnace1_input.pickup_position,\n    Prototype.TransportBelt\n)\n\n# Connect drill2 to furnace2 input inserter\nbelts2 = connect_entities(\n    drill2.drop_position,\n    furnace2_input.pickup_position,\n    Prototype.TransportBelt\n)\n\nprint("Fixed belt connections and inserter rotations")\n\n# Wait to see if ore starts flowing\nsleep(10)\n\n# Check status of components\ndrill1 = get_entity(Prototype.ElectricMiningDrill, Position(x=19.5, y=19.5))\ndrill2 = get_entity(Prototype.ElectricMiningDrill, Position(x=23.5, y=19.5))\nfurnace1 = get_entity(Prototype.StoneFurnace, Position(x=20.0, y=30.0))\nfurnace2 = get_entity(Prototype.StoneFurnace, Position(x=23.0, y=30.0))\n\nprint(f"Drill 1 status: {drill1.status}")\nprint(f"Drill 2 status: {drill2.status}")\nprint(f"Furnace 1 status: {furnace1.status}")\nprint(f"Furnace 2 status: {furnace2.status}")\nprint(f"Furnace 1 contents: {inspect_inventory(furnace1)}")\nprint(f"Furnace 2 contents: {inspect_inventory(furnace2)}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        
        print("asda")


def test_achievements_7():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY)


        #test_string_1 = 'move_to(Position(x = 28, y = 2))\nbuilding_box = BuildingBox(width = 4, height = 4)\nbbox = nearest_buildable(Prototype.WoodenChest, building_box, Position(x = -10, y = 0))\nprint(bbox)\nmove_to(bbox)'
        test_string_1 = '# Find iron ore patch\niron_ore_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore at {iron_ore_pos}")\n\n# Create building box for 3 drills\nbuilding_box = BuildingBox(width=9, height=2)\nbuildable_coordinates = nearest_buildable(Prototype.ElectricMiningDrill, building_box, iron_ore_pos)\n\n# Get leftmost position to start placing drills\ncenter = buildable_coordinates["centre"]\nwidth_margin = buildable_coordinates["width_margin"]\nleftmost_point = Position(x=center.x - width_margin, y=center.y)\n\n# Move to center first\nmove_to(center)\n\n# Place 3 drills in a line\ndrills = []\nfor i in range(3):\n    drill_pos = Position(x=leftmost_point.x + 2*i, y=leftmost_point.y)\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_pos)\n    drills.append(drill)\n    print(f"Placed drill {i+1} at {drill_pos}")\n\n# Place chest 10 spaces away from last drill\nchest_pos = Position(x=drills[-1].position.x + 10, y=drills[-1].position.y)\nmove_to(chest_pos)\n\n# Use building box for chest\nchest_box = BuildingBox(width=1, height=1)\nchest_coordinates = nearest_buildable(Prototype.WoodenChest, chest_box, chest_pos)\nchest = place_entity(Prototype.WoodenChest, position=chest_coordinates["centre"])\nprint(f"Placed collection chest at {chest.position}")\n\n# Place inserter next to chest\ninserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=chest.position, \n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\ninserter = rotate_entity(inserter, Direction.RIGHT)\nprint(f"Placed and rotated inserter at {inserter.position}")\n\n# Connect drills to inserter with transport belts\nfor drill in drills:\n    connect_entities(drill.drop_position, inserter.pickup_position, Prototype.TransportBelt)\n\n# Log positions for next step\nprint(f"Drills positioned at: {[d.position for d in drills]}")\nprint(f"Chest positioned at: {chest.position}")'
        
        #test_string_1 = '# Find iron ore patch\niron_ore_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore at {iron_ore_pos}")\nmove_to(Position(x=-19, y=29))\ndrill = place_entity(Prototype.ElectricMiningDrill, position=Position(x=-19.5, y=28.5))\ndrill = place_entity(Prototype.ElectricMiningDrill, position=Position(x=-17.5, y=28.5))\ndrill = place_entity(Prototype.ElectricMiningDrill, position=Position(x=-15.5, y=28.5))'

        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(f"asda")
        

def test_achievements_7():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = '# Find water and place offshore pump\nwater_pos = nearest(Resource.Water)\nprint(f"Found water at {water_pos}")\nmove_to(water_pos)\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {offshore_pump.position}")\n\n# Place boiler with spacing for pipes\nboiler = place_entity_next_to(\n    Prototype.Boiler,\n    reference_position=offshore_pump.position,\n    direction=Direction.RIGHT,\n    spacing=3\n)\nprint(f"Placed boiler at {boiler.position}")\n\n# Add steam engine with spacing\nsteam_engine = place_entity_next_to(\n    Prototype.SteamEngine,\n    reference_position=boiler.position,\n    direction=Direction.RIGHT,\n    spacing=3\n)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect with pipes\npipes = connect_entities(offshore_pump, boiler, Prototype.Pipe)\nsteam_pipes = connect_entities(boiler, steam_engine, Prototype.Pipe)\n\n# Fuel the boiler\nboiler = insert_item(Prototype.Coal, boiler, quantity=50)\n\n# Log positions for future reference\nprint(f"Power system positions - Pump: {offshore_pump.position}, Boiler: {boiler.position}, Engine: {steam_engine.position}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        
        #test_string_1 = '# Find iron ore patch\niron_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore at {iron_pos}")\n\n# Get steam engine position for power connection\nsteam_engine = get_entity(Prototype.SteamEngine, Position(x=-2.5, y=-1.5))\n\n# Define building box for 3 drills (each electric drill is 3 wide)\nbuilding_box = BuildingBox(width=9, height=3)  # 3 drills * 3 width each\nbuildable_coordinates = nearest_buildable(Prototype.ElectricMiningDrill, building_box, iron_pos)\nprint(f"Found buildable area at {buildable_coordinates}")\n\n# Place drills in a line\ndrills = []\ncentre = buildable_coordinates["centre"]\nwidth_margin = buildable_coordinates["width_margin"]\nleftmost_point = Position(x=centre.x - width_margin, y=centre.y)\nmove_to(centre)\n\nfor i in range(3):\n    drill_pos = Position(x=leftmost_point.x + i*3, y=leftmost_point.y)\n    move_to(drill_pos)\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_pos)\n    drills.append(drill)\n    print(f"Placed drill {i+1} at {drill.position}")\n\n# Connect power from steam engine to drills\n# First place pole near steam engine\nmove_to(steam_engine.position)\nfirst_pole = place_entity(Prototype.SmallElectricPole, \n    position=Position(x=steam_engine.position.x, y=steam_engine.position.y-3))\nprint(f"Placed first power pole at {first_pole.position}")\n\n# Connect power to all drills\nlast_pole = connect_entities(first_pole.position, drills[0].position, Prototype.SmallElectricPole)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        
        test_string_1 = '# Find iron ore patch\niron_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore at {iron_pos}")\n\n# Get steam engine position for power connection\nsteam_engine = get_entity(Prototype.SteamEngine, Position(x=-2.5, y=-1.5))\n\n# Place drills individually with smaller building boxes\ndrills = []\nmove_to(Position(x=-13.5 ,y=25.5))\ndrill = place_entity(Prototype.ElectricMiningDrill, position=Position(x=-13.5 ,y=25.5))\ndrills.append(drill)\nmove_to(Position(x=-14.5 ,y=21.5))\ndrill = place_entity(Prototype.ElectricMiningDrill, position=Position(x=-14.5 ,y=21.5))\ndrills.append(drill)\ndrill = place_entity(Prototype.ElectricMiningDrill, position=Position(x=-17.5 ,y=26.5))\ndrills.append(drill)\n# Connect power from steam engine to drills\n# First place pole near steam engine\nmove_to(steam_engine.position)\nfirst_pole = place_entity(Prototype.SmallElectricPole, \n    position=Position(x=steam_engine.position.x, y=steam_engine.position.y-3))\nprint(f"Placed first power pole at {first_pole.position}")\n\n# Connect power to all drills using small electric poles\nfor drill in drills:\n    connect_entities(first_pole.position, drill.position, Prototype.SmallElectricPole)\n    print(f"Connected power to drill at {drill.position}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        test_string_1 = '# Get the drill positions\ndrill1 = get_entity(Prototype.ElectricMiningDrill, Position(x=-13.5, y=25.5))\ndrill2 = get_entity(Prototype.ElectricMiningDrill, Position(x=-14.5, y=21.5))\ndrill3 = get_entity(Prototype.ElectricMiningDrill, Position(x=-17.5, y=26.5))\n\n# Place chest about 10 spaces away from the middle drill\nmove_to(Position(x=-3.5, y=22.5))\ncollection_chest = place_entity(Prototype.WoodenChest, position=Position(x=-3.5, y=22.5))\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Place inserter next to chest\nchest_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter = rotate_entity(chest_inserter, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter.position}")\n\n# Add fuel to inserter\nchest_inserter = insert_item(Prototype.Coal, chest_inserter, quantity=50)\n\n# Connect all drills to the inserter\'s pickup position using transport belts\nfor drill in [drill1, drill2, drill3]:\n    belts = connect_entities(\n        drill.drop_position,\n        chest_inserter.pickup_position,\n        Prototype.TransportBelt\n    )\n    print(f"Connected drill at {drill.position} to collection system")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)


def test_achievements_8():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = '# Find iron ore patch\niron_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore at {iron_pos}")\n\n# Place drills individually with smaller building boxes\ndrills = []\nmove_to(Position(x=-13.5 ,y=25.5))\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13.5 ,y=25.5))\ndrills.append(drill)\nmove_to(Position(x=-14.5 ,y=21.5))\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-14.5 ,y=21.5))\ndrills.append(drill)\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-17.5 ,y=26.5))\ndrills.append(drill)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        #test_string_1 = '# Get the drill positions\ndrill1 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13.5, y=25.5))\ndrill2 = get_entity(Prototype.BurnerMiningDrill, Position(x=-14.5, y=21.5))\ndrill3 = get_entity(Prototype.BurnerMiningDrill, Position(x=-17.5, y=26.5))\n\n# Place chest about 10 spaces away from the middle drill\nmove_to(Position(x=-3.5, y=22.5))\ncollection_chest = place_entity(Prototype.WoodenChest, position=Position(x=-3.5, y=22.5))\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Place inserter next to chest\nchest_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter = rotate_entity(chest_inserter, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter.position}")\n\n# Add fuel to inserter\nchest_inserter = insert_item(Prototype.Coal, chest_inserter, quantity=50)\n\n# Connect all drills to the inserter\'s pickup position using transport belts\nfor drill in [drill1, drill2, drill3]:\n    belts = connect_entities(\n        drill.drop_position,\n        chest_inserter.pickup_position,\n        Prototype.TransportBelt\n    )\n    print(f"Connected drill at {drill.position} to collection system")'
        test_string_1 = '# Get the drill positions\ndrill1 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13.5, y=25.5))\ndrill2 = get_entity(Prototype.BurnerMiningDrill, Position(x=-14.5, y=21.5))\ndrill3 = get_entity(Prototype.BurnerMiningDrill, Position(x=-17.5, y=26.5))\n\n# Place chest about 10 spaces away from the middle drill\nmove_to(Position(x=-3.5, y=22.5))\ncollection_chest = place_entity(Prototype.WoodenChest, position=Position(x=-3.5, y=22.5))\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Place inserter next to chest\nchest_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter = rotate_entity(chest_inserter, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter.position}")\n\n# Add fuel to inserter\nchest_inserter = insert_item(Prototype.Coal, chest_inserter, quantity=50)\n# connect the first drill to the connection system\nmain_connection= connect_entities(drill3.drop_position,chest_inserter.pickup_position, Prototype.TransportBelt)\n\n# connect the first drill to the connection system\nbelts = connect_entities(drill2.drop_position,main_connection[0], Prototype.TransportBelt)\n\n# connect the first drill to the connection system\nbelts = connect_entities(drill1.drop_position,main_connection[0], Prototype.TransportBelt)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)



def test_achievements_9():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = '# Find iron ore patch\niron_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore at {iron_pos}")\n\n# Place drills individually with smaller building boxes\ndrills = []\nmove_to(Position(x=-13 ,y=25))\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13 ,y=25), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)\nmove_to(Position(x=-13 ,y=23))\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13 ,y=23), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13 ,y=21), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        #test_string_1 = '# Get the drill positions\ndrill1 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13.5, y=25.5))\ndrill2 = get_entity(Prototype.BurnerMiningDrill, Position(x=-14.5, y=21.5))\ndrill3 = get_entity(Prototype.BurnerMiningDrill, Position(x=-17.5, y=26.5))\n\n# Place chest about 10 spaces away from the middle drill\nmove_to(Position(x=-3.5, y=22.5))\ncollection_chest = place_entity(Prototype.WoodenChest, position=Position(x=-3.5, y=22.5))\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Place inserter next to chest\nchest_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter = rotate_entity(chest_inserter, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter.position}")\n\n# Add fuel to inserter\nchest_inserter = insert_item(Prototype.Coal, chest_inserter, quantity=50)\n\n# Connect all drills to the inserter\'s pickup position using transport belts\nfor drill in [drill1, drill2, drill3]:\n    belts = connect_entities(\n        drill.drop_position,\n        chest_inserter.pickup_position,\n        Prototype.TransportBelt\n    )\n    print(f"Connected drill at {drill.position} to collection system")'
        test_string_1 = '# Get the drill positions\ndrill1 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13, y=25))\ndrill2 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13 ,y=23))\ndrill3 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13 ,y=21))\n\n# Place chest about 10 spaces away from the middle drill\nmove_to(Position(x=-3.5, y=22.5))\ncollection_chest = place_entity(Prototype.WoodenChest, position=Position(x=-3.5, y=22.5))\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Place inserter next to chest\nchest_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter = rotate_entity(chest_inserter, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter.position}")\n\n# Add fuel to inserter\nchest_inserter = insert_item(Prototype.Coal, chest_inserter, quantity=50)\n# connect the first drill to the connection system\nmain_connection= connect_entities(drill2.drop_position,chest_inserter.pickup_position, Prototype.TransportBelt)\n\n# connect the first drill to the connection system\nbelts = connect_entities(drill1.drop_position,main_connection[0], Prototype.TransportBelt)\n\n# connect the first drill to the connection system\nbelts = connect_entities(drill3.drop_position,main_connection[0], Prototype.TransportBelt)'
        #test_string_1 = '# Get the drill positions\ndrill1 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13, y=25))\ndrill2 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13 ,y=23))\ndrill3 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13 ,y=21))\n\n# Place chest about 10 spaces away from the middle drill\nmove_to(Position(x=-3.5, y=22.5))\ncollection_chest = place_entity(Prototype.WoodenChest, position=Position(x=-3.5, y=22.5))\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Place inserter next to chest\nchest_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter = rotate_entity(chest_inserter, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter.position}")\n\n# Add fuel to inserter\nchest_inserter = insert_item(Prototype.Coal, chest_inserter, quantity=50)\n# connect the first drill to the connection system\nmain_connection= connect_entities(drill1.drop_position,chest_inserter.pickup_position, Prototype.TransportBelt)'
        
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)


def test_achievements_10():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = '# Find iron ore patch\niron_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore at {iron_pos}")\n\n# Place drills individually with smaller building boxes\ndrills = []\nmove_to(Position(x=-13 ,y=25))\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13 ,y=25), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)\nmove_to(Position(x=-13 ,y=23))\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13 ,y=23), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13 ,y=21), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)'
        test_string_1 = '# Find iron ore patch\niron_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore at {iron_pos}")\n\n# Place drills individually with smaller building boxes\ndrills = []\nmove_to(Position(x=-13 ,y=25))\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13.5, y=25.5), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)\nmove_to(Position(x=-13 ,y=23))\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-17.5, y=26.5), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-14.5, y=21.5), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)'
        
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        #test_string_1 = '# Get the drill positions\ndrill1 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13.0 ,y=26.0))\ndrill2 = get_entity(Prototype.BurnerMiningDrill, Position(x=-17.0 ,y=27.0))\ndrill3 = get_entity(Prototype.BurnerMiningDrill, Position(x=-14.0 ,y=22.0))\n\n# Place chest about 10 spaces away from the middle drill\nmove_to(Position(x=-23.5, y=22.5))\ncollection_chest = place_entity(Prototype.WoodenChest, position=Position(x=-23.5, y=22.5))\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Place inserter next to chest\nchest_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter = rotate_entity(chest_inserter, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter.position}")\n\n# Add fuel to inserter\nchest_inserter = insert_item(Prototype.Coal, chest_inserter, quantity=50)\n\n# Connect all drills to the inserter\'s pickup position using transport belts\nbelts = connect_entities(drill2.drop_position,chest_inserter.pickup_position,Prototype.TransportBelt)\nprint(f"Connected drill at {drill.position} to collection")\nbelts = connect_entities(drill1.drop_position,belts[0],Prototype.TransportBelt)\nprint(f"Connected drill at {drill.position} to collection system")\nbelts = connect_entities(drill3.drop_position,belts[0],Prototype.TransportBelt)'
        test_string_1 = '# Find iron ore patch\niron_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore at {iron_pos}")\n\n# Place drills individually with smaller building boxes\ndrills = []\nmove_to(Position(x=-13 ,y=25))\ndrill1 = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13.5, y=25.5), direction = Direction.LEFT)\nprint(f"placed drill at {drill1.position}")\nmove_to(Position(x=-13 ,y=23))\ndrill2 = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-17.5, y=26.5), direction = Direction.LEFT)\nprint(f"placed drill at {drill2.position}")\ndrill3 = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-14.5, y=21.5), direction = Direction.LEFT)\nprint(f"placed drill at {drill3.position}")\nmove_to(Position(x=-23.5, y=22.5))\ncollection_chest = place_entity(Prototype.WoodenChest, position=Position(x=-23.5, y=22.5))\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Place inserter next to chest\nchest_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter = rotate_entity(chest_inserter, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter.position}")\n\n# Add fuel to inserter\nchest_inserter = insert_item(Prototype.Coal, chest_inserter, quantity=50)\n\n# Connect all drills to the inserter\'s pickup position using transport belts\nbelts = connect_entities(drill2.drop_position,chest_inserter.pickup_position,Prototype.TransportBelt)\nprint(f"Connected drill at {drill2.position} to collection")\nbelts = connect_entities(drill1.drop_position,belts[0],Prototype.TransportBelt)\nprint(f"Connected drill at {drill1.position} to collection system")\nbelts = connect_entities(drill3.drop_position,belts[0],Prototype.TransportBelt)'
        
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(f"asda")

def test_achievements_11():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = '# Find iron ore patch\niron_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore at {iron_pos}")\n\n# Place drills individually with smaller building boxes\ndrills = []\nmove_to(Position(x=-13 ,y=25))\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13 ,y=25), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)\nmove_to(Position(x=-13 ,y=23))\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13 ,y=23), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13 ,y=21), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        #test_string_1 = '# Get the drill positions\ndrill1 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13.5, y=25.5))\ndrill2 = get_entity(Prototype.BurnerMiningDrill, Position(x=-14.5, y=21.5))\ndrill3 = get_entity(Prototype.BurnerMiningDrill, Position(x=-17.5, y=26.5))\n\n# Place chest about 10 spaces away from the middle drill\nmove_to(Position(x=-3.5, y=22.5))\ncollection_chest = place_entity(Prototype.WoodenChest, position=Position(x=-3.5, y=22.5))\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Place inserter next to chest\nchest_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter = rotate_entity(chest_inserter, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter.position}")\n\n# Add fuel to inserter\nchest_inserter = insert_item(Prototype.Coal, chest_inserter, quantity=50)\n\n# Connect all drills to the inserter\'s pickup position using transport belts\nfor drill in [drill1, drill2, drill3]:\n    belts = connect_entities(\n        drill.drop_position,\n        chest_inserter.pickup_position,\n        Prototype.TransportBelt\n    )\n    print(f"Connected drill at {drill.position} to collection system")'
        #test_string_1 = '# Get the drill positions\ndrill1 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13, y=25))\ndrill2 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13 ,y=23))\ndrill3 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13 ,y=21))\n\n# Place chest about 10 spaces away from the middle drill\nmove_to(Position(x=-3.5, y=22.5))\ncollection_chest = place_entity(Prototype.WoodenChest, position=Position(x=-3, y=22.5))\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Place inserter next to chest\nchest_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter = rotate_entity(chest_inserter, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter.position}")\n\ncollection_chest2 = place_entity(Prototype.WoodenChest, position=Position(x=-3, y=18))\nprint(f"Placed collection chest at {collection_chest2.position}")\n\n# Place inserter next to chest\nchest_inserter2 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest2.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter2 = rotate_entity(chest_inserter2, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter2.position}")\n\ncollection_chest3 = place_entity(Prototype.WoodenChest, position=Position(x=-3, y=28))\nprint(f"Placed collection chest at {collection_chest3.position}")\n\n# Place inserter next to chest\nchest_inserter3 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest3.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter3 = rotate_entity(chest_inserter3, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter3.position}")\n\n# Add fuel to inserter\nchest_inserter = insert_item(Prototype.Coal, chest_inserter, quantity=50)\n# connect the first drill to the connection system\nmain_connection= connect_entities(drill2.drop_position,chest_inserter2.pickup_position, Prototype.TransportBelt)\n# extend connection\nmain_connection = connect_entities(main_connection[0],chest_inserter.pickup_position ,Prototype.TransportBelt)\nprint(main_connection)'
        test_string_1 = '# Get the drill positions\ndrill1 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13, y=25))\ndrill2 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13 ,y=23))\ndrill3 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13 ,y=21))\n\n# Place chest about 10 spaces away from the middle drill\nmove_to(Position(x=-3.5, y=22.5))\ncollection_chest = place_entity(Prototype.WoodenChest, position=Position(x=-3, y=22.5))\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Place inserter next to chest\nchest_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter = rotate_entity(chest_inserter, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter.position}")\n\ncollection_chest2 = place_entity(Prototype.WoodenChest, position=Position(x=-3, y=18))\nprint(f"Placed collection chest at {collection_chest2.position}")\n\n# Place inserter next to chest\nchest_inserter2 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest2.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter2 = rotate_entity(chest_inserter2, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter2.position}")\n\ncollection_chest3 = place_entity(Prototype.WoodenChest, position=Position(x=-3, y=28))\nprint(f"Placed collection chest at {collection_chest3.position}")\n\n# Place inserter next to chest\nchest_inserter3 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest3.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter3 = rotate_entity(chest_inserter3, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter3.position}")\n\n# Add fuel to inserter\nchest_inserter = insert_item(Prototype.Coal, chest_inserter, quantity=50)\n# connect the first drill to the connection system\nmain_connection= connect_entities(drill2.drop_position,chest_inserter2.pickup_position, Prototype.TransportBelt)\nprint(main_connection)\n# extend connection\nmain_connection = connect_entities(main_connection[0],chest_inserter.pickup_position ,Prototype.TransportBelt)\nprint(main_connection)'
        
        #test_string_1 = '# Get the drill positions\ndrill1 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13, y=25))\ndrill2 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13 ,y=23))\ndrill3 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13 ,y=21))\n\n# Place chest about 10 spaces away from the middle drill\nmove_to(Position(x=-3.5, y=22.5))\ncollection_chest = place_entity(Prototype.WoodenChest, position=Position(x=-3.5, y=22.5))\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Place inserter next to chest\nchest_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter = rotate_entity(chest_inserter, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter.position}")\n\n# Add fuel to inserter\nchest_inserter = insert_item(Prototype.Coal, chest_inserter, quantity=50)\n# connect the first drill to the connection system\nmain_connection= connect_entities(drill1.drop_position,chest_inserter.pickup_position, Prototype.TransportBelt)'
        
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)



def test_achievements_12():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = '# Find iron ore patch\niron_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore at {iron_pos}")\n\n# Place drills individually with smaller building boxes\ndrills = []\nmove_to(Position(x=-13 ,y=25))\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13 ,y=25), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)\nmove_to(Position(x=-13 ,y=23))\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13 ,y=23), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13 ,y=21), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print("asda")
        #test_string_1 = '# Get the drill positions\ndrill1 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13, y=25))\ndrill2 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13 ,y=23))\ndrill3 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13 ,y=21))\n\n# Place chest about 10 spaces away from the middle drill\nmove_to(Position(x=-3.5, y=22.5))\ncollection_chest = place_entity(Prototype.WoodenChest, position=Position(x=-3.5, y=22.5))\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Place inserter next to chest\nchest_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter = rotate_entity(chest_inserter, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter.position}")\n\n# Add fuel to inserter\nchest_inserter = insert_item(Prototype.Coal, chest_inserter, quantity=50)\n# connect the first drill to the connection system\nmain_connection= connect_entities(drill2.drop_position,chest_inserter.pickup_position, Prototype.TransportBelt)'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)


def test_achievements_13():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        #test_string_1 = '# Find iron ore patch\niron_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore at {iron_pos}")\n\n# Place drills individually with smaller building boxes\ndrills = []\nmove_to(Position(x=-13 ,y=25))\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13 ,y=25), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)\nmove_to(Position(x=-13 ,y=23))\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13 ,y=23), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)\ndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13 ,y=21), direction = Direction.LEFT)\nprint(f"placed drill at {drill.position}")\ndrills.append(drill)'
        #test_string_1 = '# Find iron ore patch\niron_pos = nearest(Resource.IronOre)\n# Place drills individually with smaller building boxes\nmove_to(Position(x=-13 ,y=23))\nndrill = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13 ,y=23), direction = Direction.LEFT)'
        #
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        #test_string_1 = '# Get the drill positions\ndrill1 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13, y=25))\ndrill2 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13 ,y=23))\ndrill3 = get_entity(Prototype.BurnerMiningDrill, Position(x=-13 ,y=21))\n\n# Place chest about 10 spaces away from the middle drill\nmove_to(Position(x=-3.5, y=22.5))\ncollection_chest = place_entity(Prototype.WoodenChest, position=Position(x=-3, y=22.5))\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Place inserter next to chest\nchest_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter = rotate_entity(chest_inserter, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter.position}")\n\ncollection_chest2 = place_entity(Prototype.WoodenChest, position=Position(x=-3, y=18))\nprint(f"Placed collection chest at {collection_chest2.position}")\n\n# Place inserter next to chest\nchest_inserter2 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest2.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter2 = rotate_entity(chest_inserter2, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter2.position}")\n\ncollection_chest3 = place_entity(Prototype.WoodenChest, position=Position(x=-3, y=28))\nprint(f"Placed collection chest at {collection_chest3.position}")\n\n# Place inserter next to chest\nchest_inserter3 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest3.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter3 = rotate_entity(chest_inserter3, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter3.position}")\n\n# Add fuel to inserter\nchest_inserter = insert_item(Prototype.Coal, chest_inserter, quantity=50)\n# connect the first drill to the connection system\nmain_connection= connect_entities(drill2.drop_position,chest_inserter2.pickup_position, Prototype.TransportBelt)\n# extend connection\nmain_connection = connect_entities(main_connection[0],chest_inserter.pickup_position ,Prototype.TransportBelt)'
        test_string_1 = '# Find iron ore patch\niron_pos = nearest(Resource.IronOre)\nmove_to(Position(x=-13 ,y=23))\n# Place drills individually with smaller building boxes\ndrill2 = place_entity(Prototype.BurnerMiningDrill, position=Position(x=-13 ,y=23), direction = Direction.LEFT)\n# Place chest about 10 spaces away from the middle drill\nmove_to(Position(x=-3.5, y=22.5))\ncollection_chest = place_entity(Prototype.WoodenChest, position=Position(x=-3, y=22.5))\nprint(f"Placed collection chest at {collection_chest.position}")\n\n# Place inserter next to chest\nchest_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter = rotate_entity(chest_inserter, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter.position}")\n\ncollection_chest2 = place_entity(Prototype.WoodenChest, position=Position(x=-3, y=18))\nprint(f"Placed collection chest at {collection_chest2.position}")\n\n# Place inserter next to chest\nchest_inserter2 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=collection_chest2.position,\n    direction=Direction.LEFT,\n    spacing=0\n)\n# Rotate inserter to put items into chest\nchest_inserter2 = rotate_entity(chest_inserter2, Direction.RIGHT)\nprint(f"Placed chest inserter at {chest_inserter2.position}")\n# connect the first drill to the connection system\nmain_connection= connect_entities(drill2.drop_position,chest_inserter2.pickup_position, Prototype.TransportBelt)\n# extend connection\nmain_connection = connect_entities(main_connection[0],chest_inserter.pickup_position ,Prototype.TransportBelt)'

        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)




def test_achievements_14():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = 'iron_ore_position = nearest(Resource.IronOre)\nmove_to(iron_ore_position)\nbuilding_box = BuildingBox(width = 1, height = 4)\n# get the nearest buildable area around the iron_ore_position\nbuildable_coordinates = nearest_buildable(Prototype.BurnerMiningDrill, building_box, iron_ore_position)\nprint(buildable_coordinates)\nmove_to(buildable_coordinates["right_bottom"])'

        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)


def test_achievements_15():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        #test_string_1 = 'belt_end_position = Position(x=-11.5, y=26.5)\nchest_central_pos = Position(x = belt_end_position.x+10, y = belt_end_position.y)\nbuilding_box = BuildingBox(width = 3, height = 1)\nbuildable_coordinates = nearest_buildable(Prototype.WoodenChest, building_box, chest_central_pos)\nmove_to(buildable_coordinates["right_bottom"])'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print("asda")
        #test_string_1 = 'bottom_drill = place_entity(Prototype.BurnerMiningDrill,position=Position(0, 0), direction = Direction.UP)\nbottom_drill = place_entity(Prototype.ElectricMiningDrill,position=Position(3, 0), direction = Direction.UP)\nmove_to(Position(0, 5))'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #
#
        #test_string_1 = 'iron_ore_pos = nearest(Resource.IronOre)\nnum_drills = 3\ndrills = []\nbuilding_box = BuildingBox(width = 3*num_drills, height = 7)\nbuildable_coordinates = nearest_buildable(Prototype.ElectricMiningDrill, building_box, iron_ore_pos)\nleft_top = buildable_coordinates["left_top"]\nleft_bottom = buildable_coordinates["left_bottom"]\nupper_drills = []\nfor i in range(num_drills):\n        upper_drill_position = Position(x=left_top.x + 1 + i * 3,y=left_top.y)\n        move_to(upper_drill_position)\n        # Place and configure each drill\n        upper_drill = place_entity(Prototype.ElectricMiningDrill,position=upper_drill_position)\n        upper_drill = rotate_entity(upper_drill, direction = Direction.DOWN)\n        print(f"Placed upper drill {i} at {upper_drill.position}")\n        upper_drills.append(upper_drill)\n        bottom_drill_position = Position(x=left_bottom.x + i * 3 + 1,y=left_bottom.y-1)\n        bottom_drill = place_entity(Prototype.ElectricMiningDrill,position=bottom_drill_position, direction = Direction.UP)\nbelt_start = upper_drills[0].drop_position\nbelt_end = upper_drills[-1].drop_position\nmain_belt = connect_entities(belt_start,belt_end,Prototype.TransportBelt)\nprint(f"Created the main belt: {main_belt}")'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
         

        test_string_1 = 'iron_ore_pos = nearest(Resource.IronOre)\nnum_drills = 5\ndrills = []\nbuilding_box = BuildingBox(width = 2*num_drills, height = 5)\nbuildable_coordinates = nearest_buildable(Prototype.BurnerMiningDrill, building_box, iron_ore_pos)\nleft_top = buildable_coordinates["left_top"]\ndrills = []\nfor i in range(num_drills):\n        upper_drill_position = Position(x=left_top.x + i * 2,y=left_top.y)\n        move_to(upper_drill_position)\n        # Place and configure each drill\n        upper_drill = place_entity(Prototype.BurnerMiningDrill,position=upper_drill_position, direction = Direction.DOWN)\n        print(f"Placed upper drill {i} at {upper_drill.position}")\n        drills.append(upper_drill)\n        bottom_drill = place_entity_next_to(Prototype.BurnerMiningDrill,reference_position=upper_drill.position, direction = Direction.DOWN, spacing = 1)\n        bottom_drill = rotate_entity(bottom_drill, direction = Direction.UP)\n        drills.append(bottom_drill)\nx_coordinates = [drill.drop_position.x for drill in drills]\nstart_x = min(x_coordinates)\nend_x = max(x_coordinates)\nshared_y_coordinate = drills[0].drop_position.y\nbelt_start = Position(x = start_x, y = shared_y_coordinate)\nbelt_end = Position(x = end_x, y = shared_y_coordinate)\nmain_belt = connect_entities(belt_start,belt_end,Prototype.TransportBelt)\nprint(f"Created the main belt: {main_belt}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        
        test_string_1 = 'belt_end_position = Position(x=-11.5, y=26.5)\nchest_central_pos = Position(x = belt_end_position.x+10, y = belt_end_position.y)\nbuilding_box = BuildingBox(width = 3, height = 1)\nbuildable_coordinates = nearest_buildable(Prototype.WoodenChest, building_box, chest_central_pos)\nleft_top = buildable_coordinates["left_top"]\nchest = place_entity(Prototype.WoodenChest, position = left_top)\nprint(f"placed collection chest at {chest.position}")\nchest_inserter = place_entity_next_to(Prototype.BurnerInserter,chest.position,direction=Direction.RIGHT, spacing = 0)\nchest_inserter = rotate_entity(chest_inserter, Direction.LEFT)\nmain_belt_extended = connect_entities(belt_end_position,chest_inserter.pickup_position,Prototype.TransportBelt)\nprint(f"Extended the resource belt: {main_belt_extended}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print("asda")
        

def test_achievements_16():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 


        test_string_1 = 'water_position = nearest(Resource.Water)\nmove_to(water_position)\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_position)\nprint(offshore_pump)\nboiler = place_entity_next_to(Prototype.Boiler,reference_position=offshore_pump.position,spacing=3)\nboiler = insert_item(Prototype.Coal, boiler, 10)\nsteam_engine = place_entity_next_to(Prototype.SteamEngine,reference_position=boiler.position, spacing=3)\nprint(f"Placed steam_engine at {steam_engine.position}") # Position(x=4, y = -21)\nwater_pipes = connect_entities(offshore_pump, boiler, Prototype.Pipe)\nsteam_pipes = connect_entities(boiler, steam_engine, Prototype.Pipe)\nsleep(5)\nprint(steam_engine)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print("asda")

def test_achievements_17():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 


        test_string_1 = 'move_to(Position(x=-11.5, y=21.5))\nplace_entity(Prototype.BurnerInserter, position = Position(x=-11.5, y=21.5))\npickup_entity(Prototype.BurnerInserter, Position(x=-11.5, y=21.5))'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print("asda")


def test_achievements_18():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 


        test_string_1 = 'for i in range(10):\n    if i < 5:\n        j = 0\n        while j < 3:\n            j +=1\n            if j == 2:\n                try:\n                    int("asd")\n                except:\n                    print("fucked")\n                    continue\n            print(j)\n        print(f"first lower loop for {i}")\n    else:        print(f"second lower loop for {i}")\n    print(f"Placed inserter {i}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)



def test_achievements_19():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 


        test_string_1 = 'belts = connect_entities(Position(x = 10, y = -9), Position(x = 0, y = 0), Prototype.TransportBelt)\nprint(belts)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

def test_achievements_20():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 


        test_string_1 = 'belts = connect_entities(Position(x = 10, y = -9), Position(x = 0, y = 0), Prototype.TransportBelt)\nprint(belts)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)


def test_achievements_20():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 


        test_string_1 = 'water_position = nearest(Resource.Water)\nmove_to(water_position)\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_position)\nprint(offshore_pump)\nboiler = place_entity_next_to(Prototype.Boiler,reference_position=offshore_pump.position,spacing=3)\nboiler = insert_item(Prototype.Coal, boiler, 10)\nsteam_engine = place_entity_next_to(Prototype.SteamEngine,reference_position=boiler.position, spacing=3)\nprint(f"Placed steam_engine at {steam_engine.position}") # Position(x=4, y = -21)\nwater_pipes = connect_entities(offshore_pump, boiler, Prototype.Pipe)\nsteam_pipes = connect_entities(boiler, steam_engine, Prototype.Pipe)\nsleep(5)\nprint(steam_engine)\noutp = connect_entities(steam_engine.position, Position(x = 4, y = -20), Prototype.SmallElectricPole)\nprint(get_entities())'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print("asda")


def test_achievements_21():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = 'move_to(Position(x = 0, y = 0))\nprint(can_place_entity(Prototype.Boiler, position=Position(x = 0, y = 0)))'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        test_string_1 = '# Power system pattern\nwater_position = nearest(Resource.Water)\nmove_to(water_position)\n# first place offshore pump on the water system\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_position)\nprint(f"Placed offshore pump at {offshore_pump.position}")\n# Then place the boiler close to the offshore pump\n# IMPORTANT: We need to be careful as there is water nearby which is unplaceable,\n# We do not know where the water is so we will use can_place_entity for safety\n# We will also need to be atleast 6 tiles away as the entities are large and otherwise wont have room for connections\n# construct 6 potential positions for the boiler, each 6 tiles away from offshore pump\npotential_positions = [Position(x = offshore_pump.position.x+6, y = offshore_pump.position.y),Position(x = offshore_pump.position.x-6, y = offshore_pump.position.y),Position(x = offshore_pump.position.x, y = offshore_pump.position.y+6),Position(x = offshore_pump.position.x, y = offshore_pump.position.y-6)]\nboiler_placed = False # variable to check if boiler was placed\nfor boiler_position in potential_positions:\n    if can_place_entity(Prototype.Boiler, position=boiler_position):\n        # place the boiler\n        boiler = place_entity(Prototype.Boiler, position=boiler_position)\n        boiler_placed = True\n        print(f"Placed boiler at {boiler_position}")\n        break\nassert boiler_placed, f"Could not find a safe tile to place boiler close to offshore pump 6 spaces away. Consider enlargening the grid"\n# add coal to boiler to start the power generation\nboiler = insert_item(Prototype.Coal, boiler, 10)\n# Finally we need to place the steam engine close to the boiler\n# IMPORTANT: We again need to be safe and use can_place_entity with a tile size of 6\npotential_positions = [Position(x = boiler.position.x+6, y = boiler.position.y),Position(x = boiler.position.x-6, y = boiler.position.y),Position(x = boiler.position.x, y = boiler.position.y+6), Position(x = boiler.position.x, y = boiler.position.y-6)]\nsteam_engine_placed = False # variable to check if boiler was placed\nfor steam_engine_position in potential_positions:\n    move_to(steam_engine_position)\n    if can_place_entity(Prototype.SteamEngine, position=steam_engine_position):\n        # place the steam engine\n        steam_engine = place_entity(Prototype.SteamEngine,position=steam_engine_position)\n        # update the variable\n        steam_engine_placed = True\n        print(f"Placed steam_engine at {steam_engine.position}")\n        break\nassert steam_engine_placed, f"Could not find a safe tile to place steam_engine 6 spaces away from boiler. Consider enlargening the grid"'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print("asda")



def test_achievements_22():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = '# Locate the nearest copper ore patch\ncopper_ore_position = nearest(Resource.CopperOre)\nprint(f"Located copper ore patch at {copper_ore_position}")\n\n# Define the BuildingBox for the drills. ElectricMiningDrill has 3x3 dimensions.\nbuilding_box = BuildingBox(width=3, height=3)\n\n# Get the nearest buildable area around the copper_ore_position\nbuildable_coordinates = nearest_buildable(Prototype.ElectricMiningDrill, building_box, copper_ore_position)\n\n# Place two electric mining drills on the copper ore patch\n# Start from the leftmost position of the buildable area\nleft_top = buildable_coordinates["left_top"]\n\n# Move to the position to place the first drill\nmove_to(left_top)\ndrill_1 = place_entity(Prototype.ElectricMiningDrill, position=left_top)\nprint(f"Placed first ElectricMiningDrill at {drill_1.position} to mine copper ore")\n\n# Place the second drill next to the first one\ndrill_2_position = left_top + Position(x=3, y=0)  # Move 3 tiles to the right\nmove_to(drill_2_position)\ndrill_2 = place_entity(Prototype.ElectricMiningDrill, position=drill_2_position)\nprint(f"Placed second ElectricMiningDrill at {drill_2.position} to mine copper ore")\n\n# Set up a power source for the drills\n# Locate the nearest water source for the offshore pump\nwater_position = nearest(Resource.Water)\nprint(f"Located water source at {water_position}")\n\n# Move to the water position and place the offshore pump\nmove_to(water_position)\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_position)\nprint(f"Placed OffshorePump at {offshore_pump.position} to get water")\n\n# Place a boiler close to the offshore pump\n# Ensure there is enough space for connections\nboiler_position = Position(x=offshore_pump.position.x + 4, y=offshore_pump.position.y)\nmove_to(boiler_position)\nboiler = place_entity(Prototype.Boiler, position=boiler_position)\nprint(f"Placed Boiler at {boiler.position} to generate steam")\n\n# Insert coal into the boiler to start generating steam\nboiler = insert_item(Prototype.Coal, boiler, quantity=20)\n\n# Place a steam engine close to the boiler\nsteam_engine_position = Position(x=boiler.position.x + 4, y=boiler.position.y)\nmove_to(steam_engine_position)\nsteam_engine = place_entity(Prototype.SteamEngine, position=steam_engine_position)\nprint(f"Placed SteamEngine at {steam_engine.position} to generate electricity")\n\n# Connect the offshore pump to the boiler with pipes\nwater_pipes = connect_entities(offshore_pump, boiler, Prototype.Pipe)\nprint(f"Connected OffshorePump at {offshore_pump.position} to Boiler at {boiler.position} with pipes {water_pipes}")\n\n# Connect the boiler to the steam engine with pipes\nsteam_pipes = connect_entities(boiler, steam_engine, Prototype.Pipe)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)


def test_achievements_24():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        PLACEMENT_STARTING_INVENTORY = {"iron-plate": 19}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = 'craft_item(Prototype.BurnerMiningDrill, quantity=1)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)


def test_achievements_24():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = '# Place storage chest at end of main belt\nstorage_pos = Position(x=-8.5, y=30.5)\nmove_to(storage_pos)\nstorage_chest = place_entity(Prototype.WoodenChest, position=storage_pos)\nprint(f"Placed storage chest at {storage_pos}")\n\n# Connect main belt to storage chest\nbelt_end = Position(x=-10.5, y=30.5)\nconnect_entities(belt_end, storage_pos, Prototype.TransportBelt)\nprint(f"Connected main belt at {belt_end} to storage chest at {storage_pos}")\n\n# Verify ore flow to storage chest\nsleep(10)\nstorage_chest = get_entity(Prototype.WoodenChest, storage_pos)\nstorage_inv = inspect_inventory(storage_chest)'
        #test_string_1 = '# Place storage chest at end of main belt\nstorage_pos = Position(x=-8.5, y=30.5)\nmove_to(storage_pos)\nstorage_chest = place_entity(Prototype.WoodenChest, position=storage_pos)\nprint(f"Placed storage chest at {storage_pos}")\nstorage_chest = get_entity(Prototype.WoodenChest, storage_pos)\nstorage_inv = inspect_inventory(storage_chest)\nassert storage_inv[Prototype.IronOre] > 0, "Ore not reaching storage chest"\nprint(f"Storage chest now has {storage_inv[Prototype.IronOre]} iron ore")\n\n# Final system verification\nprint(f"Current throughput: {production_stats()}")\nprint(f"Current inventory: {inspect_inventory()}")\nprint(f"Updated entities on the map: {get_entities()}")'
        
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print("asda")

def test_achievements_25():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = 'nearest(Resource.Water)'
        #test_string_1 = '# Place storage chest at end of main belt\nstorage_pos = Position(x=-8.5, y=30.5)\nmove_to(storage_pos)\nstorage_chest = place_entity(Prototype.WoodenChest, position=storage_pos)\nprint(f"Placed storage chest at {storage_pos}")\nstorage_chest = get_entity(Prototype.WoodenChest, storage_pos)\nstorage_inv = inspect_inventory(storage_chest)\nassert storage_inv[Prototype.IronOre] > 0, "Ore not reaching storage chest"\nprint(f"Storage chest now has {storage_inv[Prototype.IronOre]} iron ore")\n\n# Final system verification\nprint(f"Current throughput: {production_stats()}")\nprint(f"Current inventory: {inspect_inventory()}")\nprint(f"Updated entities on the map: {get_entities()}")'
        
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print("asda")



def test_achievements_26():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = '# Move to the nearest copper ore position\ncopper_ore_position = nearest(Resource.CopperOre)\nmove_to(copper_ore_position)\nprint(f"Moved to copper ore position at {copper_ore_position}")\n\n# Define the building box for the drill line\nbuilding_box = BuildingBox(width=2*5, height=4) # 5 drills, 2 width per drill, 4 height to account for inserter and belt\n# Get the nearest buildable area around the copper ore position\nbuildable_coordinates = nearest_buildable(Prototype.ElectricMiningDrill, building_box, copper_ore_position)\n\n# Place the drill line\nleft_top = buildable_coordinates["left_top"]\nmove_to(left_top)\nfor i in range(5):\n    drill_position = Position(x=left_top.x + 2*i, y=left_top.y)\n    move_to(drill_position)\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_position, direction=Direction.DOWN)\n    print(f"Placed ElectricMiningDrill {i} at {drill.position} to mine copper ore")\n\n# Place the furnace line\nfurnace_positions = []\nfor i in range(5):\n    furnace_position = Position(x=left_top.x + 2*i, y=left_top.y + 2)\n    move_to(furnace_position)\n    furnace = place_entity(Prototype.StoneFurnace, position=furnace_position)\n    furnace_positions.append(furnace_position)\n    print(f"Placed StoneFurnace {i} at {furnace_position} to smelt copper plates")\n\n# Connect the drill line to the furnace line with inserters and belts\nfor i in range(5):\n    drill = get_entity(Prototype.ElectricMiningDrill, position=Position(x=left_top.x + 2*i, y=left_top.y))\n    furnace = get_entity(Prototype.StoneFurnace, position=furnace_positions[i])\n    inserter = place_entity_next_to(Prototype.BurnerInserter, reference_position=drill.position, direction=Direction.DOWN, spacing=0)\n    print(f"Placed BurnerInserter {i} at {inserter.position} to input copper ore to furnace")\n    inserter = rotate_entity(inserter, Direction.DOWN) # Face inserter towards furnace\n    belts = connect_entities(drill.drop_position, inserter.pickup_position, Prototype.TransportBelt)\n    print(f"Connected ElectricMiningDrill {i} to BurnerInserter {i} with {belts}")\n\n# Connect the furnace line to a chest with inserters and belts\nchest_position = Position(x=left_top.x + 5, y=left_top.y + 1)\nmove_to(chest_position)\nchest = place_entity(Prototype.WoodenChest, position=chest_position)\nprint(f"Placed WoodenChest at {chest_position} to collect copper plates")\nfor i in range(5):\n    furnace = get_entity(Prototype.StoneFurnace, position=furnace_positions[i])\n    inserter = place_entity_next_to(Prototype.BurnerInserter, reference_position=furnace.position, direction=Direction.RIGHT, spacing=0)\n    print(f"Placed BurnerInserter {i} at {inserter.position} to output copper plates to chest")\n    inserter = rotate_entity(inserter, Direction.LEFT) # Face inserter towards chest\n    belts = connect_entities(furnace.position, inserter.pickup_position, Prototype.TransportBelt)\n    print(f"Connected StoneFurnace {i} to BurnerInserter {i} with {belts}")\n    belts = connect_entities(inserter.drop_position, chest.position, Prototype.TransportBelt)\n    print(f"Connected BurnerInserter {i} to WoodenChest with {belts}")'
        test_string_1 = '# Move to the nearest copper ore position\ncopper_ore_position = nearest(Resource.CopperOre)\nmove_to(copper_ore_position)\nprint(f"Moved to copper ore position at {copper_ore_position}")\n\n# Define the building box for the drill line\nbuilding_box = BuildingBox(width=2*5, height=4) # 5 drills, 2 width per drill, 4 height to account for inserter and belt\n# Get the nearest buildable area around the copper ore position\nbuildable_coordinates = nearest_buildable(Prototype.ElectricMiningDrill, building_box, copper_ore_position)\n\n# Place the drill line\nleft_top = buildable_coordinates["left_top"]\nmove_to(left_top)\nfor i in range(5):\n    drill_position = Position(x=left_top.x + 2*i, y=left_top.y)\n    move_to(drill_position)\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_position, direction=Direction.DOWN)\n    print(f"Placed ElectricMiningDrill {i} at {drill.position} to mine copper ore")\n\n# Place the furnace line\nfurnace_positions = []\nfor i in range(5):\n    furnace_position = Position(x=left_top.x + 2*i, y=left_top.y + 2)\n    move_to(furnace_position)\n    furnace = place_entity(Prototype.StoneFurnace, position=furnace_position)\n    furnace_positions.append(furnace_position)\n    print(f"Placed StoneFurnace {i} at {furnace_position} to smelt copper plates")\n\n# Connect the drill line to the furnace line with inserters and belts\nfor i in range(5):\n    drill = get_entity(Prototype.ElectricMiningDrill, position=Position(x=left_top.x + 2*i, y=left_top.y))'
        test_string_1 = '# Move to the nearest copper ore position\ncopper_ore_position = nearest(Resource.CopperOre)\nmove_to(copper_ore_position)\nprint(f"Moved to copper ore position at {copper_ore_position}")\n\n# Define the building box for the drill line\nbuilding_box = BuildingBox(width=2*5, height=4) # 5 drills, 2 width per drill, 4 height to account for inserter and belt\n# Get the nearest buildable area around the copper ore position\nbuildable_coordinates = nearest_buildable(Prototype.ElectricMiningDrill, building_box, copper_ore_position)\n\n# Place the drill line\nleft_top = buildable_coordinates["left_top"]\nmove_to(left_top)\nfor i in range(5):\n    drill_position = Position(x=left_top.x + 2*i, y=left_top.y)\n    move_to(drill_position)\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_position, direction=Direction.DOWN)\n    print(f"Placed ElectricMiningDrill {i} at {drill.position} to mine copper ore")'
        
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print("asda")


def test_achievements_27():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = '# Locate the nearest copper ore patch\ncopper_ore_position = nearest(Resource.CopperOre)\nprint(f"Found copper ore at {copper_ore_position}")\n\n# Define the BuildingBox for the drill line\n# ElectricMiningDrill has dimensions 3x3\n# We need 2 drills so width is 3*2, height is 4 (3 for drill, 1 for furnace)\nbuilding_box = BuildingBox(width=3*2, height=4)\n\n# Get the nearest buildable area around the copper_ore_position\nbuildable_coordinates = nearest_buildable(Prototype.ElectricMiningDrill, building_box, copper_ore_position)\n\n# Place the first electric mining drill\ndrill_1_position = buildable_coordinates["left_top"]\nmove_to(drill_1_position)\ndrill_1 = place_entity(Prototype.ElectricMiningDrill, position=drill_1_position, direction=Direction.DOWN)\nprint(f"Placed ElectricMiningDrill at {drill_1.position} to mine copper ore")\n\n# Place the second electric mining drill next to the first one\ndrill_2_position = drill_1_position.right()\nmove_to(drill_2_position)\ndrill_2 = place_entity(Prototype.ElectricMiningDrill, position=drill_2_position, direction=Direction.DOWN)'
         
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print("asda")


def test_achievements_28():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = 'water_position = nearest(Resource.Water)\nmove_to(water_position)\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_position)\nprint(offshore_pump)\nbbox = BuildingBox(height = 6, width = 6)\ncoords = nearest_buildable(Prototype.Boiler,bbox,offshore_pump.position)\ntop_left_coord = coords["left_top"]\ncenter = Position(top_left_coord.x +3, top_left_coord.y +3)\nboiler = place_entity(Prototype.Boiler, position = center)\nbbox = BuildingBox(height = 7, width = 7)\ncoords = nearest_buildable(Prototype.SteamEngine,bbox,boiler.position)\ntop_left_coord = coords["left_top"]\ncenter = Position(top_left_coord.x +3, top_left_coord.y +3)\nmove_to(center)\nsteam_engine = place_entity(Prototype.SteamEngine, position = center)\nwater_pipes = connect_entities(offshore_pump, boiler, Prototype.Pipe)\nsteam_pipes = connect_entities(boiler, steam_engine, Prototype.Pipe)'
        
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print("asda")

def test_achievements_29():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = 'belts = connect_entities(Position(x = 10, y = -9), Position(x = -19, y = 22), Prototype.TransportBelt)\nprint(belts)\nprint(belts[0].belts)\npickup_entity(Prototype.TransportBelt, Position(x=-14.5, y=17.5))'

        test_string_1 = 'belts = connect_entities(Position(x = 1, y = -1), Position(x = -2, y = 0), Prototype.TransportBelt)\nprint(belts)\nprint(belts[0].belts)\npickup_entity(Prototype.TransportBelt, Position(x=1.5, y=0.5))'

        test_string_1 = 'belts = connect_entities(Position(x = 1, y = -1), Position(x = -2, y = 0), Prototype.TransportBelt)\nprint(belts)\nprint(belts[0].belts)\nfor belt in belts[0].belts:\n    pickup_entity(Prototype.TransportBelt, belt.position)\n    print(f"Pickup belt at {belt.position}")'
        test_string_1 = 'belts = connect_entities(Position(x = 1, y = -1), Position(x = -2, y = 0), Prototype.TransportBelt)\nprint(len(belts[0].belts))\nprint(belts[0].belts)\nfor belt in belts[0].belts:\n    pickup_entity(Prototype.TransportBelt, belt.position)\n    print(f"Pickup belt at {belt.position}")'

        test_string_1 = 'belts = connect_entities(Position(x = 1, y = -1), Position(x = -2, y = 0), Prototype.TransportBelt)\nbelts_in_beltgroup = [x.position for x in belts[0].belts]\nprint(len(belts_in_beltgroup))\nprint(belts_in_beltgroup)\nfor i, specific_belt in enumerate(belts_in_beltgroup):\n    pickup_entity(Prototype.TransportBelt, specific_belt)\n    print(i)\nprint(f"done")'

        test_string_1 = 'belts = connect_entities(Position(x = 1, y = -1), Position(x = -2, y = 0), Prototype.TransportBelt)\nbelts_in_beltgroup = [x.position for x in belts[0].belts]\nprint(len(belts_in_beltgroup))\nprint(belts_in_beltgroup)\nfor i, specific_belt in enumerate(belts_in_beltgroup):\n    pickup_entity(Prototype.TransportBelt, specific_belt)\n    print(i)\nprint(f"done")'
        
        test_string_1 = 'belts = connect_entities(Position(x = 1, y = -1), Position(x = -2, y = 0), Prototype.TransportBelt)\nbelts_in_beltgroup = [x.position for x in belts[0].belts]\nprint(len(belts_in_beltgroup))\nprint(belts_in_beltgroup)\npickup_entity(Prototype.BeltGroup, belts[0].position)'
        
        #test_string_1 = 'belts = connect_entities(Position(x = 1, y = -1), Position(x = -2, y = 0), Prototype.Pipe)\nprint(belts)\nprint(belts[0].pipes)\nfor belt in belts[0].pipes:\n    pickup_entity(Prototype.Pipe, belt.position)\n    print(f"Pickup belt at {belt.position}")'

        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print("asda")


def test_achievements_30():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = 'steam_engine_pos = Position(x=-8.5, y=10.5)\nboiler_pos = Position(x=-8.5, y=5.5)\nwater_pos = nearest(Resource.Water)\nmove_to(water_pos)\noffshore_pump = place_entity(Prototype.OffshorePump,position = water_pos)\nprint(offshore_pump)\nmove_to(boiler_pos)\nboiler =  place_entity(Prototype.Boiler, position = boiler_pos)\ninsert_item(Prototype.Coal, boiler, 20)\nwater_pipes = connect_entities(offshore_pump, boiler, Prototype.Pipe)\nassert len(water_pipes) == 1\nmove_to(steam_engine_pos)\nengine = place_entity(Prototype.SteamEngine, position = steam_engine_pos)\nsteam_pipes = connect_entities(boiler, engine, Prototype.Pipe)\nassert len(steam_pipes) ==1\nengine=get_entity(Prototype.SteamEngine, engine.position)\nassert engine.energy > 0'
        #test_string_1 = 'belts = connect_entities(Position(x = 1, y = -1), Position(x = -2, y = 0), Prototype.Pipe)\nprint(belts)\nprint(belts[0].pipes)\nfor belt in belts[0].pipes:\n    pickup_entity(Prototype.Pipe, belt.position)\n    print(f"Pickup belt at {belt.position}")'

        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print("asda")


def test_achievements_31():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = '# Step 1: Locate the nearest iron ore patch\niron_ore_position = nearest(Resource.IronOre)\nprint(f"Nearest iron ore patch located at {iron_ore_position}")\n\n# Step 2: Set up 3 electric mining drills on the iron ore patch\n# Define the BuildingBox for the drills. ElectricMiningDrill has 3x3 dimensions.\nbuilding_box = BuildingBox(width=3*3, height=3)\ndrill_positions = nearest_buildable(Prototype.ElectricMiningDrill, building_box, iron_ore_position)\n\n# Place the electric mining drills\ndrills = []\nfor i in range(3):\n    drill_pos = Position(x=drill_positions.left_top.x + i * 3, y=drill_positions.left_top.y)\n    move_to(drill_pos)\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_pos)\n    drills.append(drill)\n    print(f"Placed ElectricMiningDrill {i} at {drill.position} to mine iron ore")\n\n# Step 3: Place 4 stone furnaces to smelt the iron ore into copper plates\n# Define the BuildingBox for the furnaces. StoneFurnace has 2x2 dimensions.\nfurnace_box = BuildingBox(width=4*2, height=2)\nfurnace_positions = nearest_buildable(Prototype.StoneFurnace, furnace_box, Position(x=drill_positions.left_top.x, y=drill_positions.left_top.y + 5))\n\nfurnaces = []\nfor i in range(4):\n    furnace_pos = Position(x=furnace_positions.left_top.x + i * 2, y=furnace_positions.left_top.y)\n    move_to(furnace_pos)\n    furnace = place_entity(Prototype.StoneFurnace, position=furnace_pos)\n    furnaces.append(furnace)\n    print(f"Placed StoneFurnace {i} at {furnace.position} to smelt iron ore into copper plates")\n\n# Step 4: Connect the mining drills to the furnaces using transport belts\nfor drill, furnace in zip(drills, furnaces):\n    belts = connect_entities(drill.drop_position, furnace.position, Prototype.TransportBelt)\n    print(f"Connected {drill} to {furnace} with belts: {belts}")\n\n# Step 5: Fuel the furnaces with coal\nfor furnace in furnaces:\n    furnace = insert_item(Prototype.Coal, furnace, quantity=20)\n    print(f"Fueled {furnace} with coal")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        test_string_1 = '# Step 1: Set up a power generation system\n# Move to the nearest water source to place an offshore pump\nwater_position = nearest(Resource.Water)\nmove_to(water_position)\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_position)\nprint(f"Placed OffshorePump at {offshore_pump.position}")\n\n# Place a boiler near the offshore pump\nboiler_position = Position(x=water_position.x + 4, y=water_position.y)\nmove_to(boiler_position)\nboiler = place_entity(Prototype.Boiler, position=boiler_position)\nprint(f"Placed Boiler at {boiler.position}")\n\n# Place a steam engine near the boiler\nsteam_engine_position = Position(x=boiler_position.x + 5, y=boiler_position.y)\nmove_to(steam_engine_position)\nsteam_engine = place_entity(Prototype.SteamEngine, position=steam_engine_position)\nprint(f"Placed SteamEngine at {steam_engine.position}")\n\n# Connect the offshore pump to the boiler and the boiler to the steam engine with pipes\nconnect_entities(offshore_pump, boiler, Prototype.Pipe)\nconnect_entities(boiler, steam_engine, Prototype.Pipe)\n\n# Fuel the boiler with coal\nboiler = insert_item(Prototype.Coal, boiler, quantity=20)\nprint(f"Fueled Boiler at {boiler.position} with coal")\n\n# Step 2: Connect the electric mining drills to the power network\nfor drill in drills:\n    connect_entities(drill, steam_engine, Prototype.SmallElectricPole)\n    print(f"Connected ElectricMiningDrill at {drill.position} to the power network")\n\n# Step 3: Fuel the stone furnaces with coal\nfor furnace in furnaces:\n    furnace = insert_item(Prototype.Coal, furnace, quantity=20)\n    print(f"Fueled StoneFurnace at {furnace.position} with coal")\n\n# Step 4: Retry connecting the mining drills to the furnaces using transport belts\nfor drill, furnace in zip(drills, furnaces):\n    belts = connect_entities(drill.drop_position, furnace.position, Prototype.TransportBelt)\n    print(f"Connected {drill} to {furnace} with belts: {belts}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        
        test_string_1 = '# Step 1: Place chests at the drop positions of the mining drills\nfor drill in drills:\n    drop_position = drill.drop_position\n    move_to(drop_position)\n    chest = place_entity(Prototype.WoodenChest, position=drop_position)\n    print(f"Placed WoodenChest at {chest.position} to collect iron ore from {drill}")\n\n# Step 2: Connect the chests to the furnaces using transport belts\nfor drill, furnace in zip(drills, furnaces):\n    chest = get_entity(Prototype.WoodenChest, position=drill.drop_position)\n    belts = connect_entities(chest.position, furnace.position, Prototype.TransportBelt)\n    print(f"Connected {chest} to {furnace} with belts: {belts}")\n\n# Step 3: Verify connections and ensure that iron ore reaches the furnaces\n# Wait a few seconds to ensure the system is working\nsleep(10)\n# Check the status of furnaces\nfor furnace in furnaces:\n    furnace = get_entity(Prototype.StoneFurnace, position=furnace.position)\n    assert furnace.status != EntityStatus.NO_INGREDIENTS, f"Furnace at {furnace.position} is not receiving iron ore"\n    print(f"Furnace at {furnace.position} is operational and receiving iron ore")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        
        test_string_1 = '# Step 1: Reconnect the electric mining drills to the power network\n# Identify the nearest electric pole to the mining drills\nnearest_pole_position = nearest(Prototype.SmallElectricPole)\nfor drill in drills:\n    connect_entities(drill, nearest_pole_position, Prototype.SmallElectricPole)\n    print(f"Reconnected ElectricMiningDrill at {drill.position} to the power network")\n\n# Step 2: Verify and adjust the transport belt connections from chests to furnaces\nfor drill, furnace in zip(drills, furnaces):\n    chest = get_entity(Prototype.WoodenChest, position=drill.drop_position)\n    # Ensure belts are correctly connecting the chest to the furnace\n    belts = connect_entities(chest.position, furnace.position, Prototype.TransportBelt)\n    print(f"Connected {chest} to {furnace} with belts: {belts}")\n\n# Step 3: Verify furnaces are receiving iron ore and are operational\n# Wait a few seconds to ensure the system is working\nsleep(10)\n# Check the status of furnaces\nfor furnace in furnaces:\n    furnace = get_entity(Prototype.StoneFurnace, position=furnace.position)\n    assert furnace.status != EntityStatus.NO_INGREDIENTS, f"Furnace at {furnace.position} is not receiving iron ore"\n    print(f"Furnace at {furnace.position} is operational and receiving iron ore")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        test_string_1 = '# Step 1: Verify and ensure the fluid connections from the offshore pump to the boiler and from the boiler to the steam engine\n# Reconnect the offshore pump to the boiler\nconnect_entities(offshore_pump, boiler, Prototype.Pipe)\nprint(f"Reconnected OffshorePump at {offshore_pump.position} to Boiler at {boiler.position}")\n\n# Reconnect the boiler to the steam engine\nconnect_entities(boiler, steam_engine, Prototype.Pipe)\nprint(f"Reconnected Boiler at {boiler.position} to SteamEngine at {steam_engine.position}")\n\n# Step 2: Ensure the boiler is fueled with coal\nboiler = insert_item(Prototype.Coal, boiler, quantity=20)\nprint(f"Fueled Boiler at {boiler.position} with coal")\n\n# Step 3: Verify the power network is active and electric mining drills are operational\n# Wait a few seconds to ensure the power network is active\nsleep(10)\n# Check the status of electric mining drills\nfor drill in drills:\n    drill = get_entity(Prototype.ElectricMiningDrill, position=drill.position)\n    assert drill.status != EntityStatus.NO_POWER, f"ElectricMiningDrill at {drill.position} is not receiving power"\n    print(f"ElectricMiningDrill at {drill.position} is operational and receiving power")\n\n# Step 4: Verify transport belt connections from chests to furnaces\nfor drill, furnace in zip(drills, furnaces):\n    chest = get_entity(Prototype.WoodenChest, position=drill.drop_position)\n    belts = connect_entities(chest.position, furnace.position, Prototype.TransportBelt)\n    print(f"Connected {chest} to {furnace} with belts: {belts}")\n\n# Wait a few seconds to ensure the system is working\nsleep(10)\n# Check the status of furnaces\nfor furnace in furnaces:\n    furnace = get_entity(Prototype.StoneFurnace, position=furnace.position)\n    assert furnace.status != EntityStatus.NO_INGREDIENTS, f"Furnace at {furnace.position} is not receiving iron ore"\n    print(f"Furnace at {furnace.position} is operational and receiving iron ore")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        test_string_1 = '# Step 1: Remove the existing boiler\nmove_to(boiler.position)\npickup_entity(Prototype.Boiler, position=boiler.position)\nprint(f"Removed Boiler from {boiler.position}")\n\n# Step 2: Find a suitable position for the boiler\n# Define a new position for the boiler with clear connection points\nnew_boiler_position = Position(x=offshore_pump.position.x + 3, y=offshore_pump.position.y)\nmove_to(new_boiler_position)\nboiler = place_entity(Prototype.Boiler, position=new_boiler_position)\nprint(f"Placed Boiler at {boiler.position} with clear connection points")\n\n# Step 3: Reconnect the offshore pump to the newly positioned boiler\nconnect_entities(offshore_pump, boiler, Prototype.Pipe)\nprint(f"Connected OffshorePump at {offshore_pump.position} to Boiler at {boiler.position}")\n\n# Step 4: Reconnect the boiler to the steam engine\nconnect_entities(boiler, steam_engine, Prototype.Pipe)\nprint(f"Connected Boiler at {boiler.position} to SteamEngine at {steam_engine.position}")\n\n# Step 5: Ensure the boiler is fueled with coal\nboiler = insert_item(Prototype.Coal, boiler, quantity=20)\nprint(f"Fueled Boiler at {boiler.position} with coal")\n\n# Step 6: Verify the power network is active and electric mining drills are operational\n# Wait a few seconds to ensure the power network is active\nsleep(10)\n# Check the status of electric mining drills\nfor drill in drills:\n    drill = get_entity(Prototype.ElectricMiningDrill, position=drill.position)\n    assert drill.status != EntityStatus.NO_POWER, f"ElectricMiningDrill at {drill.position} is not receiving power"\n    print(f"ElectricMiningDrill at {drill.position} is operational and receiving power")\n\n# Step 7: Verify transport belt connections from chests to furnaces\nfor drill, furnace in zip(drills, furnaces):\n    chest = get_entity(Prototype.WoodenChest, position=drill.drop_position)\n    belts = connect_entities(chest.position, furnace.position, Prototype.TransportBelt)\n    print(f"Connected {chest} to {furnace} with belts: {belts}")\n\n# Wait a few seconds to ensure the system is working\nsleep(10)\n# Check the status of furnaces\nfor furnace in furnaces:\n    furnace = get_entity(Prototype.StoneFurnace, position=furnace.position)\n    assert furnace.status != EntityStatus.NO_INGREDIENTS, f"Furnace at {furnace.position} is not receiving iron ore"\n    print(f"Furnace at {furnace.position} is operational and receiving iron ore")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        
        print("asda")


def test_achievements_32():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = '# Find water source for power system\nwater_pos = Position(x=-1.0 ,y=28.0)\nprint(f"Found water source at {water_pos}")\n\n# Place offshore pump\nmove_to(water_pos)\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {offshore_pump.position}")\n\n# Place boiler next to pump\nbuilding_box = BuildingBox(width=3, height=3)\nbuildable_coords = nearest_buildable(Prototype.Boiler, building_box, offshore_pump.position)\nboiler_pos = Position(x=buildable_coords.left_top.x + 1.5, y=buildable_coords.left_top.y + 1.5)\nmove_to(boiler_pos)\nboiler = place_entity(Prototype.Boiler, position=boiler_pos)\nprint(f"Placed boiler at {boiler.position}")\n\n# Place steam engine next to boiler\nbuilding_box = BuildingBox(width=3, height=3)\nbuildable_coords = nearest_buildable(Prototype.SteamEngine, building_box, boiler.position)\nengine_pos = Position(x=buildable_coords.left_top.x + 1.5, y=buildable_coords.left_top.y + 1.5)\nmove_to(engine_pos)\nsteam_engine = place_entity(Prototype.SteamEngine, position=engine_pos)\nprint(f"Placed steam engine at {steam_engine.position}")\n# Connect offshore pump to boiler with pipes\npump_to_boiler = connect_entities(offshore_pump.position, boiler.position, Prototype.Pipe)\nprint(f"Connected offshore pump to boiler with pipes: {pump_to_boiler}")\n\n# Connect boiler to steam engine with pipes\nboiler_to_engine = connect_entities(boiler.position, steam_engine.position, Prototype.Pipe)\nprint(f"Connected boiler to steam engine with pipes: {boiler_to_engine}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        print("asda")


def test_achievements_33():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        #test_string_1 = '# Find iron ore patch\niron_ore_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore patch at {iron_ore_pos}")\n\n# Place 3 electric mining drills with smaller building boxes\ndrill_positions = []\nfor i in range(3):\n    # Use 3x3 building box for each drill\n    building_box = BuildingBox(width=3, height=3)\n    buildable_coords = nearest_buildable(Prototype.ElectricMiningDrill, building_box, iron_ore_pos)\n    \n    # Place drill at center of buildable area\n    drill_pos = Position(x=buildable_coords.left_top.x + 1.5, y=buildable_coords.left_top.y + 1.5)\n    move_to(drill_pos)\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_pos, direction=Direction.DOWN)\n    print(f"Placed electric mining drill {i+1} at {drill.position}")\n    drill_positions.append(drill.position)\n    # Update iron_ore_pos to be near last placed drill for next iteration\n    iron_ore_pos = drill.position\n\n# Place 4 stone furnaces with their own building boxes\nfurnace_positions = []\nfor i in range(4):\n    # Use 2x2 building box for each furnace\n    building_box = BuildingBox(width=2, height=2)\n    # Place furnaces 4 tiles below the drills\n    furnace_center = Position(x=drill_positions[0].x + i*2, y=drill_positions[0].y + 4)\n    buildable_coords = nearest_buildable(Prototype.StoneFurnace, building_box, furnace_center)\n    \n    # Place furnace at center of buildable area\n    furnace_pos = Position(x=buildable_coords.left_top.x + 1, y=buildable_coords.left_top.y + 1)\n    move_to(furnace_pos)\n    furnace = place_entity(Prototype.StoneFurnace, position=furnace_pos)\n    print(f"Placed stone furnace {i+1} at {furnace.position}")\n    furnace_positions.append(furnace.position)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Updated entities on the map: {get_entities()}")\n'
        #test_string_1 = '# Find iron ore patch\niron_ore_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore patch at {iron_ore_pos}")\n\n# Place 3 electric mining drills with smaller building boxes\ndrill_positions = []\nfor i in range(3):\n    # Use 3x3 building box for each drill\n    building_box = BuildingBox(width=3, height=3)\n    buildable_coords = nearest_buildable(Prototype.ElectricMiningDrill, building_box, iron_ore_pos)\n    \n    # Place drill at center of buildable area\n    drill_pos = Position(x=buildable_coords.left_top.x + 1.5, y=buildable_coords.left_top.y + 1.5)\n    move_to(drill_pos)\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_pos, direction=Direction.DOWN)\n    print(f"Placed electric mining drill {i+1} at {drill.position}")\n    drill_positions.append(drill.position)\n    # Update iron_ore_pos to be near last placed drill for next iteration\n    iron_ore_pos = drill.position\n\n# Place 4 stone furnaces with their own building boxes\nfurnace_positions = []\nfor i in range(4):\n    # Use 2x2 building box for each furnace\n    building_box = BuildingBox(width=2, height=2)\n    # Place furnaces 4 tiles below the drills\n    furnace_center = Position(x=drill_positions[0].x + i*2, y=drill_positions[0].y + 4)\n    buildable_coords = nearest_buildable(Prototype.StoneFurnace, building_box, furnace_center)\n    \n    # Place furnace at center of buildable area\n    furnace_pos = Position(x=buildable_coords.left_top.x + 1, y=buildable_coords.left_top.y + 1)\n    move_to(furnace_pos)\n    furnace = place_entity(Prototype.StoneFurnace, position=furnace_pos)\n    print(f"Placed stone furnace {i+1} at {furnace.position}")\n    furnace_positions.append(furnace.position)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Updated entities on the map: {get_entities()}")\n'
        test_string_1 = '# Find iron ore patch\niron_ore_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore patch at {iron_ore_pos}")\n\n# Place 3 electric mining drills with smaller building boxes\ndrill_positions = []\nfor i in range(3):\n    # Use 3x3 building box for each drill\n    building_box = BuildingBox(width=3, height=3)\n    buildable_coords = nearest_buildable(Prototype.ElectricMiningDrill, building_box, iron_ore_pos)\n    \n    # Place drill at center of buildable area\n    drill_pos = Position(x=buildable_coords.left_top.x + 1.5, y=buildable_coords.left_top.y + 1.5)\n    move_to(drill_pos)\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_pos, direction=Direction.DOWN)\n    print(f"Placed electric mining drill {i+1} at {drill.position}")\n    drill_positions.append(drill.position)\n    # Update iron_ore_pos to be near last placed drill for next iteration\n    iron_ore_pos = drill.position'
        
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        test_string_1 = '# Place remaining 2 electric mining drills\nfor i in range(1, 3):\n    # Use 3x3 building box for each drill\n    building_box = BuildingBox(width=3, height=3)\n    buildable_coords = nearest_buildable(Prototype.ElectricMiningDrill, building_box, Position(x=-12.5 + i*3, y=24.5))\n    \n    # Place drill at center of buildable area\n    drill_pos = Position(x=buildable_coords.left_top.x + 1.5, y=buildable_coords.left_top.y + 1.5)\n    move_to(drill_pos)\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_pos, direction=Direction.DOWN)\n    print(f"Placed electric mining drill {i+1} at {drill.position}")\n\n# Place remaining 3 stone furnaces\nfor i in range(1, 4):\n    # Use 2x2 building box for each furnace\n    building_box = BuildingBox(width=2, height=2)\n    # Place furnaces 4 tiles below the first drill\n    furnace_center = Position(x=-11.0 + i*2, y=30.0)\n    buildable_coords = nearest_buildable(Prototype.StoneFurnace, building_box, furnace_center)\n    \n    # Place furnace at center of buildable area\n    furnace_pos = Position(x=buildable_coords.left_top.x + 1, y=buildable_coords.left_top.y + 1)\n    move_to(furnace_pos)\n    furnace = place_entity(Prototype.StoneFurnace, position=furnace_pos)\n    print(f"Placed stone furnace {i+1} at {furnace.position}")\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Updated entities on the map: {get_entities()}")\n'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        
        print("asda")

def test_achievements_34():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        #test_string_1 = '# Find iron ore patch\niron_ore_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore patch at {iron_ore_pos}")\n\n# Place 3 electric mining drills with smaller building boxes\ndrill_positions = []\nfor i in range(3):\n    # Use 3x3 building box for each drill\n    building_box = BuildingBox(width=3, height=3)\n    buildable_coords = nearest_buildable(Prototype.ElectricMiningDrill, building_box, iron_ore_pos)\n    \n    # Place drill at center of buildable area\n    drill_pos = Position(x=buildable_coords.left_top.x + 1.5, y=buildable_coords.left_top.y + 1.5)\n    move_to(drill_pos)\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_pos, direction=Direction.DOWN)\n    print(f"Placed electric mining drill {i+1} at {drill.position}")\n    drill_positions.append(drill.position)\n    # Update iron_ore_pos to be near last placed drill for next iteration\n    iron_ore_pos = drill.position\n\n# Place 4 stone furnaces with their own building boxes\nfurnace_positions = []\nfor i in range(4):\n    # Use 2x2 building box for each furnace\n    building_box = BuildingBox(width=2, height=2)\n    # Place furnaces 4 tiles below the drills\n    furnace_center = Position(x=drill_positions[0].x + i*2, y=drill_positions[0].y + 4)\n    buildable_coords = nearest_buildable(Prototype.StoneFurnace, building_box, furnace_center)\n    \n    # Place furnace at center of buildable area\n    furnace_pos = Position(x=buildable_coords.left_top.x + 1, y=buildable_coords.left_top.y + 1)\n    move_to(furnace_pos)\n    furnace = place_entity(Prototype.StoneFurnace, position=furnace_pos)\n    print(f"Placed stone furnace {i+1} at {furnace.position}")\n    furnace_positions.append(furnace.position)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Updated entities on the map: {get_entities()}")\n'
        #test_string_1 = '# Find iron ore patch\niron_ore_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore patch at {iron_ore_pos}")\n\n# Place 3 electric mining drills with smaller building boxes\ndrill_positions = []\nfor i in range(3):\n    # Use 3x3 building box for each drill\n    building_box = BuildingBox(width=3, height=3)\n    buildable_coords = nearest_buildable(Prototype.ElectricMiningDrill, building_box, iron_ore_pos)\n    \n    # Place drill at center of buildable area\n    drill_pos = Position(x=buildable_coords.left_top.x + 1.5, y=buildable_coords.left_top.y + 1.5)\n    move_to(drill_pos)\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_pos, direction=Direction.DOWN)\n    print(f"Placed electric mining drill {i+1} at {drill.position}")\n    drill_positions.append(drill.position)\n    # Update iron_ore_pos to be near last placed drill for next iteration\n    iron_ore_pos = drill.position\n\n# Place 4 stone furnaces with their own building boxes\nfurnace_positions = []\nfor i in range(4):\n    # Use 2x2 building box for each furnace\n    building_box = BuildingBox(width=2, height=2)\n    # Place furnaces 4 tiles below the drills\n    furnace_center = Position(x=drill_positions[0].x + i*2, y=drill_positions[0].y + 4)\n    buildable_coords = nearest_buildable(Prototype.StoneFurnace, building_box, furnace_center)\n    \n    # Place furnace at center of buildable area\n    furnace_pos = Position(x=buildable_coords.left_top.x + 1, y=buildable_coords.left_top.y + 1)\n    move_to(furnace_pos)\n    furnace = place_entity(Prototype.StoneFurnace, position=furnace_pos)\n    print(f"Placed stone furnace {i+1} at {furnace.position}")\n    furnace_positions.append(furnace.position)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Updated entities on the map: {get_entities()}")\n'
        test_string_1 = 'for i in range(3):\n    print(i)'
        score, goal, result = instance.eval_with_error(test_string_1, 300)
        
        print("asda")



def test_achievements_35():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = 'move_to(Position(x = 4, y = -12))\nengine = place_entity(Prototype.ElectricMiningDrill, position = Position(x = 4, y = -12))\npickup_entity(Prototype.ElectricMiningDrill, engine.position)'
        score, goal, result = instance.eval_with_error(test_string_1, 300)
        
        print("asda")



def test_achievements_35():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = 'water_pos = Position(x=-13.5, y=-1.5)\nprint(f"Found water source at {water_pos}")\n\n# Place offshore pump\nmove_to(water_pos)\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {offshore_pump.position}")\nboiler_pos = Position(x=-28.5, y=1.0)\nmove_to(boiler_pos)\nboiler = place_entity(Prototype.Boiler, position=boiler_pos)\nprint(f"Placed boiler at {boiler.position}")\nengine_pos = Position(x=-4.5, y=0.5)\nmove_to(engine_pos)\nsteam_engine = place_entity(Prototype.SteamEngine, position=engine_pos)\nprint(f"Placed steam engine at {steam_engine.position}")\n# Connect offshore pump to boiler with pipes\npump_to_boiler = connect_entities(offshore_pump.position, boiler.position, Prototype.Pipe)\nprint(f"Connected offshore pump to boiler with pipes: {pump_to_boiler}")\n\n# Connect boiler to steam engine with pipes\nboiler_to_engine = connect_entities(boiler.position, steam_engine.position, Prototype.Pipe)\nprint(f"Connected boiler to steam engine with pipes: {boiler_to_engine}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        print("asda")

def test_achievements_36():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = '# Locate the nearest copper ore patch\ncopper_ore_position = nearest(Resource.CopperOre)\n\n# Define the number of drills needed and place them\nnum_drills = 3\ndrills = []\n\n# Place electric mining drills on the copper ore patch\nfor i in range(num_drills):\n    # Calculate positions with proper spacing\n    drill_position = Position(\n        x=copper_ore_position.x + i * 3,  # Assuming each drill occupies 3 tiles\n        y=copper_ore_position.y\n    )\n    move_to(drill_position)\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_position)\n    drills.append(drill)\n    print(f"Placed ElectricMiningDrill {i+1} at {drill.position} to mine copper ore")\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Updated entities on the map: {get_entities()}")\n'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        
        test_string_1 = '# Locate the nearest water source for the offshore pump\nwater_position = nearest(Resource.Water)\n\n# Move to the water position and place the offshore pump\nmove_to(water_position)\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_position)\nprint(f"Placed offshore pump at {offshore_pump.position}")\n\n# Place the boiler close to the offshore pump\nboiler_position = Position(x=offshore_pump.position.x + 2, y=offshore_pump.position.y)\nmove_to(boiler_position)\nboiler = place_entity(Prototype.Boiler, position=boiler_position)\nprint(f"Placed boiler at {boiler.position}")\n\n# Place the steam engine close to the boiler\nsteam_engine_position = Position(x=boiler.position.x + 2, y=boiler.position.y)\nmove_to(steam_engine_position)\nsteam_engine = place_entity(Prototype.SteamEngine, position=steam_engine_position)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect the offshore pump to the boiler\nwater_pipes = connect_entities(offshore_pump, boiler, Prototype.Pipe)\nprint(f"Connected offshore pump to boiler with pipes: {water_pipes}")\n\n# Connect the boiler to the steam engine\nsteam_pipes = connect_entities(boiler, steam_engine, Prototype.Pipe)\nprint(f"Connected boiler to steam engine with pipes: {steam_pipes}")\n\n# Add fuel to the boiler\nboiler = insert_item(Prototype.Coal, boiler, quantity=20)\nprint(f"Added fuel to boiler at {boiler.position}")\n\n# Connect the electric mining drills to the power network using small electric poles\nfor drill in drills:\n    connect_entities(drill, steam_engine, Prototype.SmallElectricPole)\n    print(f"Connected electric mining drill at {drill.position} to power network")\n\nprint(f"Updated entities on the map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        test_string_1 = 'steam_engine_position = nearest(Prototype.SteamEngine)\nprint(f"Found steam engine at {steam_engine_position}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)


        print("asda")

## BUG 1
def test_achievements_36():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = 'furnace = place_entity(Prototype.StoneFurnace, position = Position(x = 2, y = 0))\nblets = connect_entities(Position(x = 0, y = 0), furnace.position, Prototype.TransportBelt)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        print("asda")


## BUG 2
def test_achievements_37():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = 'boiler_position = Position(x=3.5, y=28.0)\nmove_to(boiler_position)\nboiler = place_entity(Prototype.Boiler, position=boiler_position)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        print("asda")



## BUG 2
def test_achievements_38():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = '# Step 1: Locate the nearest iron ore patch\niron_ore_position = nearest(Resource.IronOre)\nprint(f"Nearest iron ore patch located at {iron_ore_position}")\n\n# Step 2: Set up 3 electric mining drills on the iron ore patch\n# Define the BuildingBox for the drills. ElectricMiningDrill has 3x3 dimensions.\nbuilding_box = BuildingBox(width=3*3, height=3)\ndrill_positions = nearest_buildable(Prototype.ElectricMiningDrill, building_box, iron_ore_position)\n\n# Place the electric mining drills\ndrills = []\nfor i in range(3):\n    drill_pos = Position(x=drill_positions.left_top.x + i * 3, y=drill_positions.left_top.y)\n    move_to(drill_pos)\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_pos)\n    drills.append(drill)\n    print(f"Placed ElectricMiningDrill {i} at {drill.position} to mine iron ore")\n\n# Step 3: Place 4 stone furnaces to smelt the iron ore into copper plates\n# Define the BuildingBox for the furnaces. StoneFurnace has 2x2 dimensions.\nfurnace_box = BuildingBox(width=4*2, height=2)\nfurnace_positions = nearest_buildable(Prototype.StoneFurnace, furnace_box, Position(x=drill_positions.left_top.x, y=drill_positions.left_top.y + 5))\n\nfurnaces = []\nfor i in range(4):\n    furnace_pos = Position(x=furnace_positions.left_top.x + i * 2, y=furnace_positions.left_top.y)\n    move_to(furnace_pos)\n    furnace = place_entity(Prototype.StoneFurnace, position=furnace_pos)\n    furnaces.append(furnace)\n    print(f"Placed StoneFurnace {i} at {furnace.position} to smelt iron ore into copper plates")\n\n# Step 4: Connect the mining drills to the furnaces using transport belts\nfor drill, furnace in zip(drills, furnaces):\n    belts = connect_entities(drill.drop_position, furnace.position, Prototype.TransportBelt)\n    print(f"Connected {drill} to {furnace} with belts: {belts}")\n\n# Step 5: Fuel the furnaces with coal\nfor furnace in furnaces:\n    furnace = insert_item(Prototype.Coal, furnace, quantity=20)\n    print(f"Fueled {furnace} with coal")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        test_string_1 = '# Step 1: Place chests at the drop positions of the mining drills\nfor drill in drills:\n    drop_position = drill.drop_position\n    move_to(drop_position)\n    chest = place_entity(Prototype.WoodenChest, position=drop_position)\n    print(f"Placed WoodenChest at {chest.position} to collect iron ore from {drill}")\n\n# Step 2: Connect the chests to the furnaces using transport belts\nfor drill, furnace in zip(drills, furnaces):\n    chest = get_entity(Prototype.WoodenChest, position=drill.drop_position)\n    belts = connect_entities(chest.position, furnace.position, Prototype.TransportBelt)\n    print(f"Connected {chest} to {furnace} with belts: {belts}")\n\n# Step 3: Verify connections and ensure that iron ore reaches the furnaces\n# Wait a few seconds to ensure the system is working\nsleep(10)\n# Check the status of furnaces\nfor furnace in furnaces:\n    furnace = get_entity(Prototype.StoneFurnace, position=furnace.position)\n    assert furnace.status != EntityStatus.NO_INGREDIENTS, f"Furnace at {furnace.position} is not receiving iron ore"\n    print(f"Furnace at {furnace.position} is operational and receiving iron ore")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)


        print("asda")



## BUG 2
def test_achievements_39():
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = '# Step 1: Locate the nearest iron ore patch\niron_ore_position = nearest(Resource.IronOre)\nprint(f"Nearest iron ore patch located at {iron_ore_position}")\n\n# Step 2: Set up 3 electric mining drills on the iron ore patch\n# Define the BuildingBox for the drills. ElectricMiningDrill has 3x3 dimensions.\nbuilding_box = BuildingBox(width=3*3, height=3)\ndrill_positions = nearest_buildable(Prototype.ElectricMiningDrill, building_box, iron_ore_position)\n\n# Place the electric mining drills\ndrills = []\nfor i in range(3):\n    drill_pos = Position(x=drill_positions.left_top.x + i * 3, y=drill_positions.left_top.y)\n    move_to(drill_pos)\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_pos)\n    drills.append(drill)\n    print(f"Placed ElectricMiningDrill {i} at {drill.position} to mine iron ore")\n    chest = place_entity(Prototype.WoodenChest, position=drill.drop_position)\n\n# Step 3: Place 4 stone furnaces to smelt the iron ore into copper plates\n# Define the BuildingBox for the furnaces. StoneFurnace has 2x2 dimensions.\nfurnace_box = BuildingBox(width=4*2, height=2)\nfurnace_positions = nearest_buildable(Prototype.StoneFurnace, furnace_box, Position(x=drill_positions.left_top.x, y=drill_positions.left_top.y + 5))\n\ninserters = []\nfor i in range(4):\n    furnace_pos = Position(x=furnace_positions.left_top.x + i * 2, y=furnace_positions.left_top.y+2)\n    move_to(furnace_pos)\n    furnace = place_entity(Prototype.StoneFurnace, position=furnace_pos)\n    inserter = place_entity_next_to(Prototype.BurnerInserter, reference_position=furnace_pos, direction = Direction.UP, spacing = 0)\n    inserter = rotate_entity(inserter, Direction.DOWN)\n    inserters.append(inserter)\n# Step 2: Connect the chests to the furnaces using transport belts\nfor drill, inserter in zip(drills, inserters):\n    chest = get_entity(Prototype.WoodenChest, position=drill.drop_position)\n    belts = connect_entities(chest.position, inserter.pickup_position, Prototype.TransportBelt)\n    print(f"Connected chest to furnace with belts: {len(belts)}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        print("asda")


def test_achievements_40(): # For appendix
        PLACEMENT_STARTING_INVENTORY = {"coal": 200, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = 'water_pos = nearest(Resource.Water)\nprint(f"Found water source at {water_pos}")\n\n# Place offshore pump\nmove_to(water_pos)\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {offshore_pump.position}")\n\nboiler = place_entity_next_to(Prototype.Boiler, reference_position=offshore_pump.position, spacing = 4, direction = Direction.RIGHT)\nprint(f"Placed boiler at {boiler.position}")\nsteam_engine = place_entity_next_to(Prototype.SteamEngine, reference_position=boiler.position, spacing = 5, direction = Direction.RIGHT)\nprint(f"Placed steam engine at {steam_engine.position}")\n# Connect offshore pump to boiler with pipes\npump_to_boiler = connect_entities(offshore_pump.position, boiler.position, Prototype.Pipe)\nprint(f"Connected offshore pump to boiler with pipes: {pump_to_boiler}")\n\n# Connect boiler to steam engine with pipes\nboiler_to_engine = connect_entities(boiler.position, steam_engine.position, Prototype.Pipe)\nprint(f"Connected boiler to steam engine with pipes: {boiler_to_engine}")\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Updated entities on the map: {get_entities()}")\n'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        test_string_1 = 'iron_pos = nearest(Resource.IronOre)\nmove_to(iron_pos)\ndrill = place_entity(Prototype.ElectricMiningDrill, position = iron_pos)\nprint(f"Put a drill to mine iron at {drill.position}")\nsteam_engine = get_entity(Prototype.SteamEngine, position = Position(x = 3.5, y=-0.5))\npoles = connect_entities(steam_engine,drill,Prototype.SmallElectricPole)\nprint(f"Used poles {poles} to power drill at {drill.position}")\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Updated entities on the map: {get_entities()}")\n'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(f"asd")


def test_achievements_41(): # DEMO
        PLACEMENT_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = '# Find iron ore patch and get position\niron_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore at {iron_pos}")\n\n# Define building box for drill (2x2) plus furnace (2x2)\nbuilding_box = BuildingBox(width=2, height=4)\n\n# Get buildable area\nbuildable_coords = nearest_buildable(Prototype.BurnerMiningDrill, building_box, iron_pos)\ndrill_pos = buildable_coords.left_top\n\n# Place drill\nmove_to(drill_pos)\ndrill = place_entity(Prototype.BurnerMiningDrill, position=drill_pos, direction=Direction.DOWN)\nprint(f"Placed drill at {drill.position}")\n\n# Place furnace at drop position\nfurnace = place_entity(Prototype.StoneFurnace, position=drill.drop_position)\nprint(f"Placed furnace at {furnace.position}")\n\n# Add coal to drill\ndrill = insert_item(Prototype.Coal, drill, quantity=50)\nprint(f"Added coal to drill")\nprint(f"Current inventory: {inspect_inventory()}")\nprint(f"Updated entities on the map: {get_entities()}")\n'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        test_string_1 = '# Get current entities\ndrill = get_entity(Prototype.BurnerMiningDrill, Position(x=-13.0, y=22.0))\nfurnace = get_entity(Prototype.StoneFurnace, Position(x=-12.0, y=24.0))\n\n# Add coal to furnace\nfurnace = insert_item(Prototype.Coal, furnace, quantity=50)\nprint(f"Added coal to furnace")\n\n# Place inserter between drill and furnace\ninserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace.position,\n    direction=Direction.DOWN,\n    spacing=0\n)\nprint(f"Placed inserter at {inserter.position}")\n\n# Add coal to inserter\ninserter = insert_item(Prototype.Coal, inserter, quantity=50)\nprint(f"Added coal to inserter")\n\n# Log current state\nprint(f"Current inventory: {inspect_inventory()}")\nprint(f"Updated entities: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(f"asd")

        test_string_1 = '# Find water and setup power\nwater_pos = nearest(Resource.Water)\nprint(f"Found water at {water_pos}")\n\n# Place offshore pump\nmove_to(water_pos)\npump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed pump at {pump.position}")\n\n# Place boiler with spacing of 3 to ensure room for pipes\nboiler = place_entity_next_to(\n    Prototype.Boiler,\n    reference_position=pump.position,\n    direction=Direction.LEFT,\n    spacing=3\n)\nprint(f"Placed boiler at {boiler.position}")\n\n# Add coal to boiler\nboiler = insert_item(Prototype.Coal, boiler, quantity=50)\n\n# Place steam engine with spacing of 3\nengine = place_entity_next_to(\n    Prototype.SteamEngine,\n    reference_position=boiler.position,\n    direction=Direction.DOWN,\n    spacing=3\n)\nprint(f"Placed steam engine at {engine.position}")\n\n# Connect pump to boiler to steam engine with pipes\nconnect_entities(pump, boiler, Prototype.Pipe)\nconnect_entities(boiler, engine, Prototype.Pipe)\n\n# Place assembling machine 10 spaces away from furnace\nfurnace = get_entity(Prototype.StoneFurnace, Position(x=-12.0, y=24.0))\ntarget_pos = Position(x=furnace.position.x + 10, y=furnace.position.y)\n\n# Define building box for assembling machine (3x3) plus inserter (1x1)\nbuilding_box = BuildingBox(width=4, height=3)\nbuildable_coords = nearest_buildable(Prototype.AssemblingMachine1, building_box, target_pos)\n\n# Place assembling machine\nmove_to(buildable_coords.left_top)\nassembler = place_entity(Prototype.AssemblingMachine1, position=buildable_coords.left_top)\nprint(f"Placed assembling machine at {assembler.position}")\n\n# Connect power with electric poles\nconnect_entities(engine.position, assembler.position, Prototype.SmallElectricPole)\n\n# Set recipe for iron gear wheels\nset_entity_recipe(assembler, Prototype.IronGearWheel)\n\nprint(f"Current entities: {get_entities()}")\nprint(f"Current inventory: {inspect_inventory()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        test_string_1 = '# Get current entities\nfurnace = get_entity(Prototype.StoneFurnace, Position(x=-12.0, y=24.0))\nassembler = get_entity(Prototype.AssemblingMachine1, Position(x=3.5, y=29.5))\n\n# Place inserter next to furnace to take out plates\nfurnace_output_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=furnace.position,\n    direction=Direction.RIGHT,\n    spacing=0\n)\nprint(f"Placed furnace output inserter at {furnace_output_inserter.position}")\n\n# Add coal to inserter\nfurnace_output_inserter = insert_item(Prototype.Coal, furnace_output_inserter, quantity=50)\n\n# Place inserter next to assembling machine to input plates\nassembler_input_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=assembler.position,\n    direction=Direction.DOWN,\n    spacing=0\n)\nprint(f"Placed assembler input inserter at {assembler_input_inserter.position}")\n\n# Rotate assembler input inserter to face assembler\nassembler_input_inserter = rotate_entity(assembler_input_inserter, Direction.UP)\n\n# Add coal to inserter\nassembler_input_inserter = insert_item(Prototype.Coal, assembler_input_inserter, quantity=50)\n\n# Connect the two inserters with transport belt\nbelts = connect_entities(\n    furnace_output_inserter.drop_position,\n    assembler_input_inserter.pickup_position,\n    Prototype.TransportBelt\n)\nprint(f"Connected inserters with transport belts")\n\n# Add output inserter for iron gear wheels\noutput_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    reference_position=assembler.position,\n    direction=Direction.DOWN,\n    spacing=0\n)\nprint(f"Placed output inserter at {output_inserter.position}")\n\n# Add coal to output inserter\noutput_inserter = insert_item(Prototype.Coal, output_inserter, quantity=50)\n\n# Place chest to collect gear wheels\nchest = place_entity_next_to(\n    Prototype.WoodenChest,\n    reference_position=output_inserter.position,\n    direction=Direction.DOWN,\n    spacing=0\n)\nprint(f"Placed collection chest at {chest.position}")\n\nprint(f"Current entities: {get_entities()}")\nprint(f"Current inventory: {inspect_inventory()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(f"asd")


def test_achievements_42(): # DEMO
        PLACEMENT_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\nfurnace_pos = Position(x = drill.position.x - 9, y =  drill.position.y)\nbelts = connect_entities(drill.drop_position, furnace_pos, Prototype.TransportBelt)\nprint(f"Connected drill at {drill.position} to {furnace_pos} with belts {belts}")\n# wait for 10 seconds and check if furnace is smelting plates\nsleep(30)\nprint(get_entities())'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        game_state = GameState.from_instance(instance)
        instance.reset(game_state)
        test_string_1 = 'print(get_entities())'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        
        print(f"asd")


def test_achievements_43(): # DEMO
        PLACEMENT_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        #test_string_1 = '\n# log your general idea what you will do next\nprint(f"I will create a power generation setup with a steam engine")\n# get the water position\nwater_position = nearest(Resource.Water)\n# moveto water positon\nmove_to(water_position)\n# first place offshore pump on the water system\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_position)\nprint(f"Placed offshore pump to get water at {offshore_pump.position}")\n# place the boiler next to offshore pump\nboiler = place_entity_next_to(Prototype.Boiler, reference_position = offshore_pump.position, spacing = 1, direction = Direction.DOWN)'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        #test_string_1 = '# Use nearest_buildable to find a valid position for the boiler\n# The boiler has a dimension of 2x3, so we need to ensure there is enough space\nboiler_building_box = BuildingBox(width=3, height=2)\noffshore_pump_position = Position(x=-10.5, y=1.5)\noffshore_pump = get_entity(Prototype.OffshorePump, position = offshore_pump_position)\n\n# Find the nearest buildable position for the boiler\nboiler_bounding_box = nearest_buildable(\n    Prototype.Boiler,\n    building_box=boiler_building_box,\n    center_position=offshore_pump_position\n)\n\n# Log the found position for the boiler\nprint(f"Found buildable position for boiler: {boiler_bounding_box.center()}")\n\n# Move to the center of the bounding box and place the boiler\nmove_to(boiler_bounding_box.center())\nboiler = place_entity(Prototype.Boiler, position=boiler_bounding_box.center())\nprint(f"Placed boiler at {boiler.position}")\n\n# Connect the offshore pump to the boiler with pipes\npipes_to_boiler = connect_entities(offshore_pump.position, boiler.position, Prototype.Pipe)\nprint(f"Connected offshore pump to boiler with pipes: {pipes_to_boiler}")\nsleep(2)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Updated entities on the map: {get_entities()}")\n'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        #test_string_1 = 'water_position = nearest(Resource.Water)\n# moveto water positon\nmove_to(water_position)\n# first place offshore pump on the water system\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_position)\nprint(f"Placed offshore pump to get water at {offshore_pump.position}")\n# Use nearest_buildable to find a valid position for the boiler\n# The boiler has a dimension of 2x3, so we need to ensure there is enough space\nboiler_building_box = BuildingBox(width=3, height=2)\nboiler_bounding_box = nearest_buildable(\n    Prototype.Boiler,\n    building_box=boiler_building_box,\n    center_position=offshore_pump.position\n)\n\n# Log the found position for the boiler\nprint(f"Found buildable position for boiler: {boiler_bounding_box.center()}")\n\n# Move to the center of the bounding box and place the boiler\nmove_to(boiler_bounding_box.center())\nboiler = place_entity(Prototype.Boiler, position=boiler_bounding_box.center())\nprint(f"Placed boiler at {boiler.position}")\n\n# Connect the offshore pump to the boiler with pipes\npipes_to_boiler = connect_entities(offshore_pump.position, boiler.position, Prototype.Pipe)\nprint(f"Connected offshore pump to boiler with pipes: {pipes_to_boiler}")\nsleep(2)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Updated entities on the map: {get_entities()}")\n'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        test_string_1 = 'water_position = nearest(Resource.Water)\n# moveto water positon\nmove_to(water_position)\n# first place offshore pump on the water system\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_position)\nprint(f"Placed offshore pump to get water at {offshore_pump.position}")\n# Use nearest_buildable to find a valid position for the boiler\n# The boiler has a dimension of 2x3, so we need to ensure there is enough space\nboiler_building_box = BuildingBox(width=7, height=7)\nboiler_bounding_box = nearest_buildable(\n    Prototype.Boiler,\n    building_box=boiler_building_box,\n    center_position=offshore_pump.position\n)\n\n# Log the found position for the boiler\nprint(f"Found buildable position for boiler: {boiler_bounding_box.center}")\n\n# Move to the center of the bounding box and place the boiler\nmove_to(boiler_bounding_box.center)\nboiler = place_entity(Prototype.Boiler, position=boiler_bounding_box.center)\nprint(f"Placed boiler at {boiler.position}")\n\n# Connect the offshore pump to the boiler with pipes\npipes_to_boiler = connect_entities(offshore_pump, boiler, Prototype.Pipe)\nprint(f"Connected offshore pump to boiler with pipes: {pipes_to_boiler}")\nsleep(2)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Updated entities on the map: {get_entities()}")\n'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        
        print(f"asd")


def test_achievements_44(): # DEMO
        PLACEMENT_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        #test_string_1 = '\n# log your general idea what you will do next\nprint(f"I will create a power generation setup with a steam engine")\n# get the water position\nwater_position = nearest(Resource.Water)\n# moveto water positon\nmove_to(water_position)\n# first place offshore pump on the water system\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_position)\nprint(f"Placed offshore pump to get water at {offshore_pump.position}")\n# place the boiler next to offshore pump\nboiler = place_entity_next_to(Prototype.Boiler, reference_position = offshore_pump.position, spacing = 1, direction = Direction.DOWN)'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        #test_string_1 = '# Use nearest_buildable to find a valid position for the boiler\n# The boiler has a dimension of 2x3, so we need to ensure there is enough space\nboiler_building_box = BuildingBox(width=3, height=2)\noffshore_pump_position = Position(x=-10.5, y=1.5)\noffshore_pump = get_entity(Prototype.OffshorePump, position = offshore_pump_position)\n\n# Find the nearest buildable position for the boiler\nboiler_bounding_box = nearest_buildable(\n    Prototype.Boiler,\n    building_box=boiler_building_box,\n    center_position=offshore_pump_position\n)\n\n# Log the found position for the boiler\nprint(f"Found buildable position for boiler: {boiler_bounding_box.center()}")\n\n# Move to the center of the bounding box and place the boiler\nmove_to(boiler_bounding_box.center())\nboiler = place_entity(Prototype.Boiler, position=boiler_bounding_box.center())\nprint(f"Placed boiler at {boiler.position}")\n\n# Connect the offshore pump to the boiler with pipes\npipes_to_boiler = connect_entities(offshore_pump.position, boiler.position, Prototype.Pipe)\nprint(f"Connected offshore pump to boiler with pipes: {pipes_to_boiler}")\nsleep(2)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Updated entities on the map: {get_entities()}")\n'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        test_string_1 = '# Step 1: Locate the nearest water source for power generation\nwater_pos = nearest(Resource.Water)\nprint(f"Found water source at {water_pos}")\n\n# Define a safe area for boiler and steam engine placement\nboiler_steam_box = BuildingBox(width=5, height=5)\nboiler_area = nearest_buildable(Prototype.Boiler, boiler_steam_box, water_pos)\n\n# Place boiler\nboiler_pos = boiler_area.left_top\nmove_to(boiler_pos)\nboiler = place_entity(Prototype.Boiler, position=boiler_pos)\nprint(f"Placed Boiler at {boiler.position}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        print(f"asd")


def test_achievements_45(): # DEMO
        from eval.open.model.game_state import GameState
        PLACEMENT_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 200,
                                "stone-furnace": 5, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 200, "pipe": 100,
                                "assembling-machine-1": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=PLACEMENT_STARTING_INVENTORY) 

        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\nsleep(5)\ninserter_to_furnace1 = place_entity_next_to(Prototype.StoneFurnace,reference_position=drill.drop_position, spacing=0)'
        #test_string_1 = 'print(Prototype.BurnerMiningDrill.WIDTH)\nprint(Prototype.AssemblingMachine2.HEIGHT)\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\nbbox = BuildingBox(height = 2,width = 3)\ncoords = nearest_buildable(entity = Prototype.Boiler, building_box = bbox, center_position = drill.drop_position)\nfurn = place_entity(Prototype.Boiler, position = coords.left_top, direction = Direction.RIGHT)'
        test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\nbbox = BuildingBox(width = Prototype.WoodenChest.WIDTH+1, height = Prototype.WoodenChest.HEIGHT+1)\nbuildable_coordinates = nearest_buildable(Prototype.WoodenChest, bbox, drill.drop_position)\nfurn = place_entity(Prototype.WoodenChest, position = buildable_coordinates.center)\nprint(buildable_coordinates.width())\nprint(buildable_coordinates.height())'
        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        print(f"asd")


def test_achievements_46(): # DEMO
        from eval.open.model.game_state import GameState
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-1": 5, "electric-furnace": 10}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\nsleep(5)\ninserter_to_furnace1 = place_entity_next_to(Prototype.StoneFurnace,reference_position=drill.drop_position, spacing=0)'
        #test_string_1 = 'print(Prototype.BurnerMiningDrill.WIDTH)\nprint(Prototype.AssemblingMachine2.HEIGHT)\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\nbbox = BuildingBox(height = 2,width = 3)\ncoords = nearest_buildable(entity = Prototype.Boiler, building_box = bbox, center_position = drill.drop_position)\nfurn = place_entity(Prototype.Boiler, position = coords.left_top, direction = Direction.RIGHT)'
        test_string_1 = '# Find water for power generation\nprint("Starting to build power infrastructure")\nwater_pos = nearest(Resource.Water)\nmove_to(water_pos)\n\n# Place offshore pump\npump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {pump.position}")\n\n# Place boiler with spacing for pipes\nboiler = place_entity_next_to(\n    Prototype.Boiler,\n    reference_position=pump.position,\n    direction=Direction.RIGHT,\n    spacing=2\n)\nprint(f"Placed boiler at {boiler.position}")\n\n# Add coal to boiler\nboiler = insert_item(Prototype.Coal, boiler, 50)\nprint(f"Added coal to boiler")\n\n# Place steam engine with spacing for pipes\nsteam_engine = place_entity_next_to(\n    Prototype.SteamEngine,\n    reference_position=boiler.position,\n    direction=Direction.RIGHT,\n    spacing=2\n)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect pump to boiler with pipes\nwater_connection = connect_entities(pump, boiler, Prototype.Pipe)\nprint(f"Connected water from pump to boiler")\n\n# Connect boiler to steam engine with pipes\nsteam_connection = connect_entities(boiler, steam_engine, Prototype.Pipe)\nprint(f"Connected steam from boiler to engine")\n\n# Sleep to let system start up\nsleep(5)\n\n# Verify power generation\nsteam_engine = get_entity(Prototype.SteamEngine, steam_engine.position)\nassert steam_engine.energy > 0, "Steam engine is not generating power"\nprint("Power infrastructure successfully built and generating electricity")\npole_group = connect_entities(steam_engine, Position(x = 0, y = 0), Prototype.SmallElectricPole)\npole_group = connect_entities(pole_group, Position(x = 10, y = -10), Prototype.SmallElectricPole)'
        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)


        print(f"asd")

def rotation_error(): # DEMO
        from eval.open.model.game_state import GameState
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-1": 5, "electric-furnace": 10, "assembling-machine-2": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        test_string_1 = '\nassembly_pos = Position(x=-34.5, y=-14.5)\nmove_to(assembly_pos)\ntarget_machine = place_entity(Prototype.AssemblingMachine2, position=assembly_pos, direction = Direction.DOWN)\nset_entity_recipe(entity = target_machine, prototype = Prototype.Concrete)\nprint(f"Placed AssemblingMachine1 at {target_machine.position} to automatically create copper cables")\n# put a inserter next to the assembly machine\n# always use 0 spacing for inserters\n# direction is RIGHT as we added to the width of the buildable coordinates\nmachine_input_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=target_machine.position,\n    direction=Direction.RIGHT,\n    spacing = 0)\n# rotate the inserter as we need to put items into the chest\nmachine_input_inserter = rotate_entity(machine_input_inserter, direction = Direction.LEFT)\nprint(f"Placed a inserter at {machine_input_inserter.position} to put copper plates into assembling machine at {target_machine.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nmachine_output_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=target_machine.position,\n    direction=Direction.LEFT,\n    spacing = 0)\nprint(f"Placed a inserter at {machine_output_inserter.position} to put copper plates into assembling machine at {target_machine.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nchest = place_entity(Prototype.WoodenChest, position = machine_output_inserter.drop_position)\ntarget_machine = rotate_entity(target_machine, direction = Direction.LEFT)'

        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        print(f"asd")


def create_concrete(): # DEMO
        from eval.open.model.game_state import GameState
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-1": 5, "electric-furnace": 10, "assembling-machine-2": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\nsleep(5)\ninserter_to_furnace1 = place_entity_next_to(Prototype.StoneFurnace,reference_position=drill.drop_position, spacing=0)'
        #test_string_1 = 'print(Prototype.BurnerMiningDrill.WIDTH)\nprint(Prototype.AssemblingMachine2.HEIGHT)\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\nbbox = BuildingBox(height = 2,width = 3)\ncoords = nearest_buildable(entity = Prototype.Boiler, building_box = bbox, center_position = drill.drop_position)\nfurn = place_entity(Prototype.Boiler, position = coords.left_top, direction = Direction.RIGHT)'
        test_string_1 = '# Find water for power generation\nprint("Starting to build power infrastructure")\nwater_pos = nearest(Resource.Water)\nmove_to(water_pos)\n\n# Place offshore pump\npump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {pump.position}")\n\n# Place boiler with spacing for pipes\nboiler = place_entity_next_to(\n    Prototype.Boiler,\n    reference_position=pump.position,\n    direction=Direction.RIGHT,\n    spacing=2\n)\nprint(f"Placed boiler at {boiler.position}")\n\n# Add coal to boiler\nboiler = insert_item(Prototype.Coal, boiler, 50)\nprint(f"Added coal to boiler")\n\n# Place steam engine with spacing for pipes\nsteam_engine = place_entity_next_to(\n    Prototype.SteamEngine,\n    reference_position=boiler.position,\n    direction=Direction.RIGHT,\n    spacing=2\n)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect pump to boiler with pipes\nwater_connection = connect_entities(pump, boiler, Prototype.Pipe)\nprint(f"Connected water from pump to boiler")\n\n# Connect boiler to steam engine with pipes\nsteam_connection = connect_entities(boiler, steam_engine, Prototype.Pipe)\nprint(f"Connected steam from boiler to engine")\n\n# Sleep to let system start up\nsleep(5)\n\n# Verify power generation\nsteam_engine = get_entity(Prototype.SteamEngine, steam_engine.position)\nassert steam_engine.energy > 0, "Steam engine is not generating power"\nprint("Power infrastructure successfully built and generating electricity")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)
        test_string_1 = '\nstone_loc = nearest(Resource.Stone)\nmove_to(stone_loc)\n# define the BuildingBox for the drill. \n# We need 3 drills so width is 4*drill.WIDTH, height is drill.HEIGHT + furnace.HEIGHT, 3 for drill, one for furnace\nbuilding_box = BuildingBox(width = 3 * Prototype.ElectricMiningDrill.WIDTH, height = Prototype.ElectricMiningDrill.HEIGHT + Prototype.StoneFurnace.HEIGHT)\n# get the nearest buildable area around the source_position\nbuildable_coordinates = nearest_buildable(Prototype.BurnerMiningDrill, building_box, stone_loc)\n# Place miners in a line\n# we first get the leftmost coordinate of the buildingbox to start building from\nleft_top = buildable_coordinates.left_top\n# first lets move to the left_top to ensure building\nmove_to(left_top)\nfor i in range(3):\n    # we now iterate from the leftmost point towards the right\n    # take steps of 2 as drills have width of 2\n    drill_pos = Position(x=left_top.x + Prototype.ElectricMiningDrill.WIDTH*i, y=left_top.y)\n    # Place the drill facing down as we start from top coordinate\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_pos, direction = Direction.DOWN)\n    print(f"Placed ElectricMiningDrill {i} at {drill.position} to mine copper ore")\n    # place a furnace to catch the ore\n    # As a furnace has 2x2 dimensions, we need to use place_entity_next_to to ensure no overlap with drill\n    # We use the drill.direction as the direction, which will place it next to the drill covering the drop position \n    furnace = place_entity_next_to(Prototype.StoneFurnace, reference_position=drill.position, direction = drill.direction)\n    print(f"Placed furnace at {furnace.position} to smelt the copper ore for drill {i} at {drill.position}")\n    insert_item(Prototype.Coal, furnace, 50)'
        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = 'furnace_1 = get_entity(Prototype.StoneFurnace, Position(x=-14.0, y=-14.0))\nfurnace_2 = get_entity(Prototype.StoneFurnace, Position(x=-17.0, y=-14.0))\nfurnace_3 = get_entity(Prototype.StoneFurnace, Position(x=-20.0, y=-14.0))\nfor furnace in [furnace_1, furnace_2, furnace_3]:\n    inserter = place_entity_next_to(Prototype.BurnerInserter, reference_position = furnace.position, direction=Direction.DOWN, spacing = 0)\n    insert_item(Prototype.Coal, inserter, 50)'
        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)

        test_string_1 = 'drill_1 = get_entity(Prototype.ElectricMiningDrill, Position(x=-20.4, y=-16.5))\ndrill_2 = get_entity(Prototype.ElectricMiningDrill, Position(x=-17.5, y=-16.5))\ndrill_3 = get_entity(Prototype.ElectricMiningDrill, Position(x=-14.5, y=-16.5))\nsteam_engine = get_entity(Prototype.SteamEngine, Position(x=-1.5, y=1.5))\nfor drill in [drill_1, drill_2, drill_3]:\n    group = connect_entities(drill,steam_engine, Prototype.SmallElectricPole)    \nprint(f"Connected drill {drill.position} with {group}")'
        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


        test_string_1 = '\ntarget_position = Position(x = -37, y = -16.5)\n# move to the position to place the entity\nmove_to(target_position)\n# define the buildable area for the assembling machine\nprint(f"AssemblingMachine2 width: {Prototype.AssemblingMachine2.WIDTH}, height: {Prototype.AssemblingMachine2.HEIGHT}") # width 3, height 3\n# use the prototype width and height attributes \n# Need to add the 2 inserters to the width as we need to account for the inserter picking up items and putting to assembling machine\nbuilding_box = BuildingBox(width = Prototype.AssemblingMachine2.WIDTH + 2*Prototype.BurnerInserter.HEIGHT, height = Prototype.AssemblingMachine2.HEIGHT)\n# get the nearest buildable area around the target_position\nbuildable_coordinates = nearest_buildable(Prototype.AssemblingMachine2, building_box, target_position)\n# use the center coordinate to put the target_machine as one inserter will be above and another below\nassembly_pos = buildable_coordinates.center\nmove_to(assembly_pos)\ntarget_machine = place_entity(Prototype.AssemblingMachine2, position=assembly_pos, direction = Direction.DOWN)\nprint(f"Placed AssemblingMachine1 at {target_machine.position} to automatically create copper cables")\nset_entity_recipe(entity = target_machine, prototype = Prototype.Concrete)\n# put a inserter next to the assembly machine\n# always use 0 spacing for inserters\n# direction is RIGHT as we added to the width of the buildable coordinates\nmachine_input_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=target_machine.position,\n    direction=Direction.RIGHT,\n    spacing = 0)\n# rotate the inserter as we need to put items into the chest\nmachine_input_inserter = rotate_entity(machine_input_inserter, direction = Direction.LEFT)\nprint(f"Placed a inserter at {machine_input_inserter.position} to put copper plates into assembling machine at {target_machine.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nmachine_output_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=target_machine.position,\n    direction=Direction.LEFT,\n    spacing = 0)\nprint(f"Placed a inserter at {machine_output_inserter.position} to put copper plates into assembling machine at {target_machine.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nchest = place_entity(Prototype.WoodenChest, position = machine_output_inserter.drop_position)'

        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


        test_string_1 = 'ass_machine = get_entity(Prototype.AssemblingMachine2, Position( x=-34.5, y=-14.5))\nass_machine = rotate_entity(ass_machine, direction = Direction.DOWN)\nsteam_engine = get_entity(Prototype.SteamEngine, Position(x=-1.5, y=1.5))\ngroup = connect_entities(ass_machine,steam_engine, Prototype.SmallElectricPole)\nprint(f"Connected ass_machine {ass_machine.position} with {group}")\n# Find water for power generation\nprint("Starting to build power infrastructure")\nwater_pos = nearest(Resource.Water)\nmove_to(water_pos)\n\n# Place offshore pump\npump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {pump.position}")\ngroup = connect_entities(pump, ass_machine, Prototype.Pipe)\nprint(f"Connected ass_machine to water {ass_machine.position} with {group}")'
        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        print(f"asd")

def create_wall(): # DEMO
        from eval.open.model.game_state import GameState
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-1": 5, "electric-furnace": 10, "assembling-machine-2": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\nsleep(5)\ninserter_to_furnace1 = place_entity_next_to(Prototype.StoneFurnace,reference_position=drill.drop_position, spacing=0)'
        #test_string_1 = 'print(Prototype.BurnerMiningDrill.WIDTH)\nprint(Prototype.AssemblingMachine2.HEIGHT)\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\nbbox = BuildingBox(height = 2,width = 3)\ncoords = nearest_buildable(entity = Prototype.Boiler, building_box = bbox, center_position = drill.drop_position)\nfurn = place_entity(Prototype.Boiler, position = coords.left_top, direction = Direction.RIGHT)'
        test_string_1 = '# Find water for power generation\nprint("Starting to build power infrastructure")\nwater_pos = nearest(Resource.Water)\nmove_to(water_pos)\n\n# Place offshore pump\npump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {pump.position}")\n\n# Place boiler with spacing for pipes\nboiler = place_entity_next_to(\n    Prototype.Boiler,\n    reference_position=pump.position,\n    direction=Direction.RIGHT,\n    spacing=2\n)\nprint(f"Placed boiler at {boiler.position}")\n\n# Add coal to boiler\nboiler = insert_item(Prototype.Coal, boiler, 50)\nprint(f"Added coal to boiler")\n\n# Place steam engine with spacing for pipes\nsteam_engine = place_entity_next_to(\n    Prototype.SteamEngine,\n    reference_position=boiler.position,\n    direction=Direction.RIGHT,\n    spacing=2\n)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect pump to boiler with pipes\nwater_connection = connect_entities(pump, boiler, Prototype.Pipe)\nprint(f"Connected water from pump to boiler")\n\n# Connect boiler to steam engine with pipes\nsteam_connection = connect_entities(boiler, steam_engine, Prototype.Pipe)\nprint(f"Connected steam from boiler to engine")\n\n# Sleep to let system start up\nsleep(5)\n\n# Verify power generation\nsteam_engine = get_entity(Prototype.SteamEngine, steam_engine.position)\nassert steam_engine.energy > 0, "Steam engine is not generating power"\nprint("Power infrastructure successfully built and generating electricity")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)
        test_string_1 = '\nstone_loc = nearest(Resource.Stone)\nmove_to(stone_loc)\n# define the BuildingBox for the drill. \n# We need 3 drills so width is 4*drill.WIDTH, height is drill.HEIGHT + furnace.HEIGHT, 3 for drill, one for furnace\nbuilding_box = BuildingBox(width = 3 * Prototype.ElectricMiningDrill.WIDTH, height = Prototype.ElectricMiningDrill.HEIGHT + Prototype.StoneFurnace.HEIGHT)\n# get the nearest buildable area around the source_position\nbuildable_coordinates = nearest_buildable(Prototype.BurnerMiningDrill, building_box, stone_loc)\n# Place miners in a line\n# we first get the leftmost coordinate of the buildingbox to start building from\nleft_top = buildable_coordinates.left_top\n# first lets move to the left_top to ensure building\nmove_to(left_top)\nfor i in range(3):\n    # we now iterate from the leftmost point towards the right\n    # take steps of 2 as drills have width of 2\n    drill_pos = Position(x=left_top.x + Prototype.ElectricMiningDrill.WIDTH*i, y=left_top.y)\n    # Place the drill facing down as we start from top coordinate\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_pos, direction = Direction.DOWN)\n    print(f"Placed ElectricMiningDrill {i} at {drill.position} to mine copper ore")\n    # place a furnace to catch the ore\n    # As a furnace has 2x2 dimensions, we need to use place_entity_next_to to ensure no overlap with drill\n    # We use the drill.direction as the direction, which will place it next to the drill covering the drop position \n    furnace = place_entity_next_to(Prototype.StoneFurnace, reference_position=drill.position, direction = drill.direction)\n    print(f"Placed furnace at {furnace.position} to smelt the copper ore for drill {i} at {drill.position}")\n    insert_item(Prototype.Coal, furnace, 50)'
        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = 'furnace_1 = get_entity(Prototype.StoneFurnace, Position(x=-14.0, y=-14.0))\nfurnace_2 = get_entity(Prototype.StoneFurnace, Position(x=-17.0, y=-14.0))\nfurnace_3 = get_entity(Prototype.StoneFurnace, Position(x=-20.0, y=-14.0))\nfor furnace in [furnace_1, furnace_2, furnace_3]:\n    inserter = place_entity_next_to(Prototype.BurnerInserter, reference_position = furnace.position, direction=Direction.DOWN, spacing = 0)\n    print(f"placed inserter at {inserter.position}")\n    insert_item(Prototype.Coal, inserter, 50)'
        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = 'drill_1 = get_entity(Prototype.ElectricMiningDrill, Position(x=-20.4, y=-16.5))\ndrill_2 = get_entity(Prototype.ElectricMiningDrill, Position(x=-17.5, y=-16.5))\ndrill_3 = get_entity(Prototype.ElectricMiningDrill, Position(x=-14.5, y=-16.5))\nsteam_engine = get_entity(Prototype.SteamEngine, Position(x=-1.5, y=1.5))\nfor drill in [drill_1, drill_2, drill_3]:\n    group = connect_entities(drill,steam_engine, Prototype.SmallElectricPole)    \nprint(f"Connected drill {drill.position} with {group}")'
        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


        test_string_1 = '\ntarget_position = Position(x = -37, y = -16.5)\n# move to the position to place the entity\nmove_to(target_position)\n# define the buildable area for the assembling machine\nprint(f"AssemblingMachine2 width: {Prototype.AssemblingMachine2.WIDTH}, height: {Prototype.AssemblingMachine2.HEIGHT}") # width 3, height 3\n# use the prototype width and height attributes \n# Need to add the 2 inserters to the width as we need to account for the inserter picking up items and putting to assembling machine\nbuilding_box = BuildingBox(width = Prototype.AssemblingMachine2.WIDTH + 2*Prototype.BurnerInserter.HEIGHT, height = Prototype.AssemblingMachine2.HEIGHT)\n# get the nearest buildable area around the target_position\nbuildable_coordinates = nearest_buildable(Prototype.AssemblingMachine2, building_box, target_position)\n# use the center coordinate to put the target_machine as one inserter will be above and another below\nassembly_pos = buildable_coordinates.center\nmove_to(assembly_pos)\ntarget_machine = place_entity(Prototype.AssemblingMachine2, position=assembly_pos, direction = Direction.DOWN)\nprint(f"Placed AssemblingMachine1 at {target_machine.position} to automatically create copper cables")\nset_entity_recipe(entity = target_machine, prototype = Prototype.StoneWall)\n# put a inserter next to the assembly machine\n# always use 0 spacing for inserters\n# direction is RIGHT as we added to the width of the buildable coordinates\nmachine_input_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=target_machine.position,\n    direction=Direction.RIGHT,\n    spacing = 0)\n# rotate the inserter as we need to put items into the chest\nmachine_input_inserter = rotate_entity(machine_input_inserter, direction = Direction.LEFT)\nprint(f"Placed input inserter at {machine_input_inserter.position} to put copper plates into assembling machine at {target_machine.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nmachine_output_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=target_machine.position,\n    direction=Direction.LEFT,\n    spacing = 0)\nprint(f"Placed a inserter at {machine_output_inserter.position} to put copper plates into assembling machine at {target_machine.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nchest = place_entity(Prototype.WoodenChest, position = machine_output_inserter.drop_position)'

        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


        test_string_1 = 'ass_machine = get_entity(Prototype.AssemblingMachine2, Position( x=-34.5, y=-14.5))\nass_machine = rotate_entity(ass_machine, direction = Direction.DOWN)\nsteam_engine = get_entity(Prototype.SteamEngine, Position(x=-1.5, y=1.5))\ngroup = connect_entities(ass_machine,steam_engine, Prototype.SmallElectricPole)\nprint(f"Connected ass_machine {ass_machine.position} with {group}")'
        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = 'inserter_1 = get_entity(Prototype.BurnerInserter, Position( x=-13.5,y=-12.5))\ninserter_2 = get_entity(Prototype.BurnerInserter, Position( x=-16.5,y=-12.5))\ninserter_3 = get_entity(Prototype.BurnerInserter, Position( x=-19.5,y=-12.5))\ninput_ins = get_entity(Prototype.BurnerInserter, Position( x=-32.5,y=-14.5))\ngroup = connect_entities(inserter_1.drop_position,inserter_2.drop_position, Prototype.TransportBelt)\ngroup = connect_entities(group,inserter_3.drop_position, Prototype.TransportBelt)\ngroup = connect_entities(group,input_ins.pickup_position, Prototype.TransportBelt)'
        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        print(f"asd")


def create_gear_wheels(): # DEMO
        from eval.open.model.game_state import GameState
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-1": 5, "electric-furnace": 10, "assembling-machine-2": 5}
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\nsleep(5)\ninserter_to_furnace1 = place_entity_next_to(Prototype.StoneFurnace,reference_position=drill.drop_position, spacing=0)'
        #test_string_1 = 'print(Prototype.BurnerMiningDrill.WIDTH)\nprint(Prototype.AssemblingMachine2.HEIGHT)\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\nbbox = BuildingBox(height = 2,width = 3)\ncoords = nearest_buildable(entity = Prototype.Boiler, building_box = bbox, center_position = drill.drop_position)\nfurn = place_entity(Prototype.Boiler, position = coords.left_top, direction = Direction.RIGHT)'
        test_string_1 = '# Find water for power generation\nprint("Starting to build power infrastructure")\nwater_pos = nearest(Resource.Water)\nmove_to(water_pos)\n\n# Place offshore pump\npump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {pump.position}")\n\n# Place boiler with spacing for pipes\nboiler = place_entity_next_to(\n    Prototype.Boiler,\n    reference_position=pump.position,\n    direction=Direction.RIGHT,\n    spacing=2\n)\nprint(f"Placed boiler at {boiler.position}")\n\n# Add coal to boiler\nboiler = insert_item(Prototype.Coal, boiler, 50)\nprint(f"Added coal to boiler")\n\n# Place steam engine with spacing for pipes\nsteam_engine = place_entity_next_to(\n    Prototype.SteamEngine,\n    reference_position=boiler.position,\n    direction=Direction.RIGHT,\n    spacing=2\n)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect pump to boiler with pipes\nwater_connection = connect_entities(pump, boiler, Prototype.Pipe)\nprint(f"Connected water from pump to boiler")\n\n# Connect boiler to steam engine with pipes\nsteam_connection = connect_entities(boiler, steam_engine, Prototype.Pipe)\nprint(f"Connected steam from boiler to engine")\n\n# Sleep to let system start up\nsleep(5)\n\n# Verify power generation\nsteam_engine = get_entity(Prototype.SteamEngine, steam_engine.position)\nassert steam_engine.energy > 0, "Steam engine is not generating power"\nprint("Power infrastructure successfully built and generating electricity")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)
        test_string_1 = '\nstone_loc = nearest(Resource.IronOre)\nmove_to(stone_loc)\n# define the BuildingBox for the drill. \n# We need 3 drills so width is 4*drill.WIDTH, height is drill.HEIGHT + furnace.HEIGHT, 3 for drill, one for furnace\nbuilding_box = BuildingBox(width = 3 * Prototype.ElectricMiningDrill.WIDTH, height = Prototype.ElectricMiningDrill.HEIGHT + Prototype.StoneFurnace.HEIGHT)\n# get the nearest buildable area around the source_position\nbuildable_coordinates = nearest_buildable(Prototype.BurnerMiningDrill, building_box, stone_loc)\n# Place miners in a line\n# we first get the leftmost coordinate of the buildingbox to start building from\nleft_top = buildable_coordinates.left_top\n# first lets move to the left_top to ensure building\nmove_to(left_top)\nfor i in range(3):\n    # we now iterate from the leftmost point towards the right\n    # take steps of 2 as drills have width of 2\n    drill_pos = Position(x=left_top.x + Prototype.ElectricMiningDrill.WIDTH*i, y=left_top.y)\n    # Place the drill facing down as we start from top coordinate\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_pos, direction = Direction.DOWN)\n    print(f"Placed ElectricMiningDrill {i} at {drill.position} to mine copper ore")\n    # place a furnace to catch the ore\n    # As a furnace has 2x2 dimensions, we need to use place_entity_next_to to ensure no overlap with drill\n    # We use the drill.direction as the direction, which will place it next to the drill covering the drop position \n    furnace = place_entity_next_to(Prototype.StoneFurnace, reference_position=drill.position, direction = drill.direction)\n    print(f"Placed furnace at {furnace.position} to smelt the copper ore for drill {i} at {drill.position}")\n    insert_item(Prototype.Coal, furnace, 50)'
        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = 'furnace_1 = get_entity(Prototype.StoneFurnace, Position(x=-14.0, y=26))\nfurnace_2 = get_entity(Prototype.StoneFurnace, Position(x=-17.0, y=26))\nfurnace_3 = get_entity(Prototype.StoneFurnace, Position(x=-20.0, y=26))\nfor furnace in [furnace_1, furnace_2, furnace_3]:\n    inserter = place_entity_next_to(Prototype.BurnerInserter, reference_position = furnace.position, direction=Direction.DOWN, spacing = 0)\n    print(f"placed inserter at {inserter.position}")\n    insert_item(Prototype.Coal, inserter, 50)'
        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = 'drill_1 = get_entity(Prototype.ElectricMiningDrill, Position(x=-20.5, y=23.5))\ndrill_2 = get_entity(Prototype.ElectricMiningDrill, Position(x=-17.5, y=23.5))\ndrill_3 = get_entity(Prototype.ElectricMiningDrill, Position(x=-14.5, y=23.5))\nsteam_engine = get_entity(Prototype.SteamEngine, Position(x=-1.5, y=1.5))\nfor drill in [drill_1, drill_2, drill_3]:\n    group = connect_entities(drill,steam_engine, Prototype.SmallElectricPole)    \nprint(f"Connected drill {drill.position} with {group}")'
        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


        test_string_1 = '\ntarget_position = Position(x = -37, y = -16.5)\n# move to the position to place the entity\nmove_to(target_position)\n# define the buildable area for the assembling machine\nprint(f"AssemblingMachine2 width: {Prototype.AssemblingMachine2.WIDTH}, height: {Prototype.AssemblingMachine2.HEIGHT}") # width 3, height 3\n# use the prototype width and height attributes \n# Need to add the 2 inserters to the width as we need to account for the inserter picking up items and putting to assembling machine\nbuilding_box = BuildingBox(width = Prototype.AssemblingMachine2.WIDTH + 2*Prototype.BurnerInserter.HEIGHT, height = Prototype.AssemblingMachine2.HEIGHT)\n# get the nearest buildable area around the target_position\nbuildable_coordinates = nearest_buildable(Prototype.AssemblingMachine2, building_box, target_position)\n# use the center coordinate to put the target_machine as one inserter will be above and another below\nassembly_pos = buildable_coordinates.center\nmove_to(assembly_pos)\ntarget_machine = place_entity(Prototype.AssemblingMachine2, position=assembly_pos, direction = Direction.DOWN)\nprint(f"Placed AssemblingMachine1 at {target_machine.position} to automatically create copper cables")\nset_entity_recipe(entity = target_machine, prototype = Prototype.IronGearWheel)\n# put a inserter next to the assembly machine\n# always use 0 spacing for inserters\n# direction is RIGHT as we added to the width of the buildable coordinates\nmachine_input_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=target_machine.position,\n    direction=Direction.RIGHT,\n    spacing = 0)\n# rotate the inserter as we need to put items into the chest\nmachine_input_inserter = rotate_entity(machine_input_inserter, direction = Direction.LEFT)\nprint(f"Placed input inserter at {machine_input_inserter.position} to put copper plates into assembling machine at {target_machine.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nmachine_output_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=target_machine.position,\n    direction=Direction.LEFT,\n    spacing = 0)\nprint(f"Placed a inserter at {machine_output_inserter.position} to put copper plates into assembling machine at {target_machine.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nchest = place_entity(Prototype.WoodenChest, position = machine_output_inserter.drop_position)'

        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


        test_string_1 = 'ass_machine = get_entity(Prototype.AssemblingMachine2, Position( x=-34.5, y=-14.5))\nass_machine = rotate_entity(ass_machine, direction = Direction.DOWN)\nsteam_engine = get_entity(Prototype.SteamEngine, Position(x=-1.5, y=1.5))\ngroup = connect_entities(ass_machine,steam_engine, Prototype.SmallElectricPole)\nprint(f"Connected ass_machine {ass_machine.position} with {group}")'
        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = 'inserter_1 = get_entity(Prototype.BurnerInserter, Position( x=-13.5,y=27.5))\ninserter_2 = get_entity(Prototype.BurnerInserter, Position( x=-16.5,y=27.5))\ninserter_3 = get_entity(Prototype.BurnerInserter, Position( x=-19.5,y=27.5))\ninput_ins = get_entity(Prototype.BurnerInserter, Position( x=-32.5,y=-14.5))\ngroup = connect_entities(inserter_1.drop_position,inserter_2.drop_position, Prototype.TransportBelt)\ngroup = connect_entities(group,inserter_3.drop_position, Prototype.TransportBelt)\ngroup = connect_entities(group,input_ins.pickup_position, Prototype.TransportBelt)'
        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\ninserter_to_furnace1 = place_entity_next_to(Prototype.WoodenChest,reference_position=drill.position, direction = drill.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        print(f"asd")



def create_nonliquid_items(): # DEMO
        from eval.open.model.game_state import GameState
        from env.src.game_types import Prototype, Resource, Direction, Position, BuildingBox   
        tests = [
                #{"inputs": [("stone-wall", "Prototype.StoneWall"), 
                #            ("grenade", "Prototype.Grenade"),
                #              ("piercing-rounds-magazine", "Prototype.PiercingRoundsMagazine"),],
                # "output": ("military-science-pack", "Prototype.MilitarySciencePack")},
                # {"inputs": [("inserter", "Prototype.Inserter"), 
                #            ("transport-belt", "Prototype.TransportBelt")],
                # "output": ("logistic-science-pack", "Prototype.LogisticsSciencePack")},
                # {"inputs": [("iron-gear-wheel", "Prototype.IronGearWheel"), 
                #            ("electronic-circuit", "Prototype.ElectronicCircuit"),
                #              ("iron-plate", "Prototype.IronPlate"),],
                # "output": ("inserter", "Prototype.Inserter")},
                # {"inputs": [("iron-gear-wheel", "Prototype.IronGearWheel"), 
                #              ("iron-plate", "Prototype.IronPlate"),],
                # "output": ("transport-belt", "Prototype.TransportBelt")},
                # {"inputs": [("iron-gear-wheel", "Prototype.IronGearWheel"), 
                #              ("copper-plate", "Prototype.CopperPlate"),],
                # "output": ("automation-science-pack", "Prototype.AutomationSciencePack")},
                # {"inputs": [("copper-cable", "Prototype.CopperCable"), 
                #              ("iron-plate", "Prototype.IronPlate"),],
                # "output": ("electronic-circuit", "Prototype.ElectronicCircuit")},

                # {"inputs": [("copper-cable", "Prototype.CopperCable"), 
                #             ("electronic-circuit", "Prototype.ElectronicCircuit"),
                #            ("plastic-bar", "Prototype.PlasticBar")],
                # "output": ("advanced-circuit", "Prototype.AdvancedCircuit")},
                # {"inputs": [("advanced-circuit", "Prototype.AdvancedCircuit"), 
                #            ("engine-unit", "Prototype.EngineUnit"),
                #              ("sulfur", "Prototype.Sulfur"),],
                # "output": ("chemical-science-pack", "Prototype.ChemicalSciencePack")},
                # {"inputs": [("steel-plate", "Prototype.SteelPlate"), 
                #            ("pipe", "Prototype.Pipe"),
                #              ("iron-gear-wheel", "Prototype.IronGearWheel"),],
                # "output": ("engine-unit", "Prototype.EngineUnit"),},
                # {"inputs": [("advanced-circuit", "Prototype.AdvancedCircuit"), 
                #              ("steel-plate", "Prototype.SteelPlate"), 
                #              ("stone-brick", "Prototype.StoneBrick")],
                # "output": ("electric-furnace", "Prototype.ElectricFurnace")},
                # {"inputs": [("plastic-bar", "Prototype.PlasticBar"), 
                #              ("steel-plate", "Prototype.SteelPlate"), 
                #              ("copper-plate", "Prototype.CopperPlate")],
                # "output": ("low-density-structure", "Prototype.LowDensityStructure")},
                #{"inputs": [("iron-plate", "Prototype.IronPlate")],
                #"output": ("iron-stick", "Prototype.IronStick")},
                #{"inputs": [("iron-plate", "Prototype.IronPlate")],
                #"output": ("iron-gear-wheel", "Prototype.IronGearWheel")},
                #{"inputs": [("copper-plate", "Prototype.CopperPlate"),],
                #"output": ("copper-cable", "Prototype.CopperCable"),},
                #{"inputs": [("stone-brick", "Prototype.StoneBrick"),],
                #"output": ("stone-wall", "Prototype.StoneWall"),},

                # {"inputs": [("advanced-circuit", "Prototype.AdvancedCircuit"), 
                #             ("electronic-circuit", "Prototype.ElectronicCircuit"),],
                # "output": ("productivity-module", "Prototype.ProductivityModule")},
                # {"inputs": [("advanced-circuit", "Prototype.AdvancedCircuit"), 
                #             ("processing-unit", "Prototype.ProcessingUnit"),
                #             ("productivity-module", "Prototype.ProductivityModule")],
                # "output": ("productivity-module-2", "Prototype.ProductivityModule2")},
                # {"inputs": [("advanced-circuit", "Prototype.AdvancedCircuit"), 
                #             ("processing-unit", "Prototype.ProcessingUnit"),
                #             ("productivity-module-2", "Prototype.ProductivityModule2")],
                # "output": ("productivity-module-3", "Prototype.ProductivityModule3")},
                # {"inputs": [("iron-stick", "Prototype.IronStick"),
                #             ("steel-plate", "Prototype.SteelPlate"),
                #             ("stone", "Prototype.Stone")],
                # "output": ("rail", "Prototype.Rail")},
                #{"inputs": [("rail", "Prototype.Rail"),
                #             ("productivity-module", "Prototype.ProductivityModule"),
                #             ("electric-furnace", "Prototype.ElectricFurnace")],
                # "output": ("production-science-pack", "Prototype.ProductionSciencePack")},
                
                {"inputs": [("battery", "Prototype.Battery"),
                             ("electric-engine-unit", "Prototype.ElectricEngineUnit"),
                             ("electronic-circuit", "Prototype.ElectronicCircuit"),
                             ("steel-plate", "Prototype.SteelPlate")],
                 "output": ("flying-robot-frame", "Prototype.FlyingRobotFrame")},
                
                {"inputs": [("flying-robot-frame", "Prototype.FlyingRobotFrame"),
                             ("low-density-structure", "Prototype.LowDensityStructure"),
                             ("processing-unit", "Prototype.ProcessingUnit")],
                 "output": ("utility-science-pack", "Prototype.UtilitySciencePack")},
        ]
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-1": 5, "electric-furnace": 10, "assembling-machine-2": 5}
        for test in tests:
                for input in test["inputs"]:
                        if input[0] not in LAB_PLAY_POPULATED_STARTING_INVENTORY:
                                LAB_PLAY_POPULATED_STARTING_INVENTORY[input[0]] = 100
                        else:
                                LAB_PLAY_POPULATED_STARTING_INVENTORY[input[0]] += 100
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        test_string_1 = '# Find water for power generation\nprint("Starting to build power infrastructure")\nwater_pos = nearest(Resource.Water)\nmove_to(water_pos)\n\n# Place offshore pump\npump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {pump.position}")\n\n# Place boiler with spacing for pipes\nboiler = place_entity_next_to(\n    Prototype.Boiler,\n    reference_position=pump.position,\n    direction=Direction.RIGHT,\n    spacing=2\n)\nprint(f"Placed boiler at {boiler.position}")\n\n# Add coal to boiler\nboiler = insert_item(Prototype.Coal, boiler, 50)\nprint(f"Added coal to boiler")\n\n# Place steam engine with spacing for pipes\nsteam_engine = place_entity_next_to(\n    Prototype.SteamEngine,\n    reference_position=boiler.position,\n    direction=Direction.RIGHT,\n    spacing=2\n)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect pump to boiler with pipes\nwater_connection = connect_entities(pump, boiler, Prototype.Pipe)\nprint(f"Connected water from pump to boiler")\n\n# Connect boiler to steam engine with pipes\nsteam_connection = connect_entities(boiler, steam_engine, Prototype.Pipe)\nprint(f"Connected steam from boiler to engine")\n\n# Sleep to let system start up\nsleep(5)\n\n# Verify power generation\nsteam_engine = get_entity(Prototype.SteamEngine, steam_engine.position)\nassert steam_engine.energy > 0, "Steam engine is not generating power"\nprint("Power infrastructure successfully built and generating electricity")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = 'assembly_pos = Position(x = -37, y = -16.5)\nmove_to(assembly_pos)\ntarget_machine = place_entity(Prototype.AssemblingMachine2, position=assembly_pos, direction = Direction.DOWN)\nprint(f"Placed AssemblingMachine1 at {target_machine.position} to automatically create copper cables")\n# put a inserter next to the assembly machine\n# always use 0 spacing for inserters\n# direction is RIGHT as we added to the width of the buildable coordinates\nmachine_input_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=target_machine.position,\n    direction=Direction.RIGHT,\n    spacing = 0)\n# rotate the inserter as we need to put items into the chest\nmachine_input_inserter = rotate_entity(machine_input_inserter, direction = Direction.LEFT)\ninput_chest = place_entity(Prototype.WoodenChest,position=machine_input_inserter.pickup_position)\nprint(f"Placed input inserter at {machine_input_inserter.position} and chest at {input_chest.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nmachine_input_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=target_machine.position,\n    direction=Direction.LEFT,\n    spacing = 0)\n# rotate the inserter as we need to put items into the chest\nmachine_input_inserter = rotate_entity(machine_input_inserter, direction = Direction.RIGHT)\ninput_chest = place_entity(Prototype.WoodenChest,position=machine_input_inserter.pickup_position)\nprint(f"Placed input inserter at {machine_input_inserter.position} and chest at {input_chest.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nmachine_input_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=machine_input_inserter.position,\n    direction=Direction.UP,\n    spacing = 0)\n# rotate the inserter as we need to put items into the chest\nmachine_input_inserter = rotate_entity(machine_input_inserter, direction = Direction.RIGHT)\ninput_chest = place_entity(Prototype.WoodenChest,position=machine_input_inserter.pickup_position)\nprint(f"Placed input inserter at {machine_input_inserter.position} and chest at {input_chest.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nmachine_input_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=machine_input_inserter.position,\n    direction=Direction.DOWN,\n    spacing = 1)\n# rotate the inserter as we need to put items into the chest\nmachine_input_inserter = rotate_entity(machine_input_inserter, direction = Direction.RIGHT)\ninput_chest = place_entity(Prototype.WoodenChest,position=machine_input_inserter.pickup_position)\nprint(f"Placed input inserter at {machine_input_inserter.position} and chest at {input_chest.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nmachine_output_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=target_machine.position,\n    direction=Direction.UP,\n    spacing = 0)\nprint(f"Placed a inserter at {machine_output_inserter.position} to put copper plates into assembling machine at {target_machine.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nchest = place_entity(Prototype.WoodenChest, position = machine_output_inserter.drop_position)\nprint(f"Placed output chest at {chest.position}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


        test_string_1 = 'ass_machine = get_entity(Prototype.AssemblingMachine2, Position(x = -37, y = -16.5))\nsteam_engine = get_entity(Prototype.SteamEngine, Position(x=-1.5, y=1.5))\ngroup = connect_entities(ass_machine,steam_engine, Prototype.SmallElectricPole)\nprint(f"Connected ass_machine {ass_machine.position} with {group}")\nass_machine = get_entity(Prototype.AssemblingMachine2, Position(x = -37, y = -16.5))\nassert ass_machine.energy > 0, "Assembly machine not connected to power"'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)
        assert "Error" not in result, "Could not connect ass machine to power"
        game_state = GameState.from_instance(instance)

        for test in tests:

                ingredient_list = [x[1] for x in test["inputs"]]
                ingredient_list = str(ingredient_list)
                ingredient_list = ingredient_list.replace("'", "")
                test_string_1 = f'ass_machine = get_entity(Prototype.AssemblingMachine2, Position(x = -37, y = -16.5))\nset_entity_recipe(entity = ass_machine, prototype = {test["output"][1]})\nchest_1 = get_entity(Prototype.WoodenChest, Position( x=-33.5 ,y=-16.5))\nchest_2 = get_entity(Prototype.WoodenChest, Position( x=-39.5,y=-16.5))\nchest_3 = get_entity(Prototype.WoodenChest, Position( x=-39.5,y=-17.5))\nchest_4 = get_entity(Prototype.WoodenChest, Position( x=-39.5, y=-15.5))\nfor idx, item in enumerate({ingredient_list}):\n    insert_item(item, [chest_1, chest_2, chest_3, chest_4][idx], quantity=100)\nsleep(120)\noutput_chest = get_entity(Prototype.WoodenChest, Position(x=-36.5 ,y=-19.5))\noutput_inv = inspect_inventory(output_chest)\nprint(output_inv)\nassert output_inv.get({test["output"][1]}, 0) > 0, f"Test for {test["output"][1]} failed"'
                output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
                print(result)
                assert "Error" not in result, f"Error in test {test['output'][1]}"

                instance.reset(game_state)
        print(f"asd")


def create_liquid_items(): # DEMO
        from eval.open.model.game_state import GameState
        from env.src.game_types import Prototype, Resource, Direction, Position, BuildingBox   
        tests = [
                #{"solid_inputs": [("iron-ore", "Prototype.IronOre"), 
                #            ("stone-brick", "Prototype.StoneBrick")],
                #"liquid_input": ("water", "Prototype.Water"),
                # "output": ("concrete", "Prototype.Concrete")},
                
                {"solid_inputs": [("solid-fuel", "Prototype.SolidFuel")],
                "liquid_input": ("light-oil", "Prototype.LightOil"),
                 "output": ("rocket-fuel", "Prototype.RocketFuel")},

                #{"solid_inputs": [("advanced-circuit", "Prototype.AdvancedCircuit"), 
                #            ("electronic-circuit", "Prototype.ElectronicCircuit")],
                #"liquid_input": ("sulfuric-acid", "Prototype.SulfuricAcid"),
                # "output": ("processing-unit", "Prototype.ProcessingUnit")},
                
                #{"solid_inputs": [("electronic-circuit", "Prototype.ElectronicCircuit"),
                #            ("engine-unit", "Prototype.EngineUnit")],
                #"liquid_input": ("lubricant", "Prototype.Lubricant"),
                # "output": ("electric-engine-unit", "Prototype.ElectricEngineUnit")},
#
                # {"solid_inputs": [("electronic-circuit", "Prototype.ElectronicCircuit"),
                #            ("engine-unit", "Prototype.EngineUnit")],
                #"liquid_input": ("lubricant", "Prototype.Lubricant"),
                # "output": ("electric-engine-unit", "Prototype.ElectricEngineUnit")},
                
                
                
        ]
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-1": 5, "electric-furnace": 10, "assembling-machine-2": 5, "storage-tank": 8}
        for test in tests:
                for input in test["solid_inputs"]:
                        if input[0] not in LAB_PLAY_POPULATED_STARTING_INVENTORY:
                                LAB_PLAY_POPULATED_STARTING_INVENTORY[input[0]] = 100
                        else:
                                LAB_PLAY_POPULATED_STARTING_INVENTORY[input[0]] += 100
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        test_string_1 = '# Find water for power generation\nprint("Starting to build power infrastructure")\nwater_pos = nearest(Resource.Water)\nmove_to(water_pos)\n\n# Place offshore pump\npump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {pump.position}")\n\n# Place boiler with spacing for pipes\nboiler = place_entity_next_to(\n    Prototype.Boiler,\n    reference_position=pump.position,\n    direction=Direction.RIGHT,\n    spacing=2\n)\nprint(f"Placed boiler at {boiler.position}")\n\n# Add coal to boiler\nboiler = insert_item(Prototype.Coal, boiler, 50)\nprint(f"Added coal to boiler")\n\n# Place steam engine with spacing for pipes\nsteam_engine = place_entity_next_to(\n    Prototype.SteamEngine,\n    reference_position=boiler.position,\n    direction=Direction.RIGHT,\n    spacing=2\n)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect pump to boiler with pipes\nwater_connection = connect_entities(pump, boiler, Prototype.Pipe)\nprint(f"Connected water from pump to boiler")\n\n# Connect boiler to steam engine with pipes\nsteam_connection = connect_entities(boiler, steam_engine, Prototype.Pipe)\nprint(f"Connected steam from boiler to engine")\n\n# Sleep to let system start up\nsleep(5)\n\n# Verify power generation\nsteam_engine = get_entity(Prototype.SteamEngine, steam_engine.position)\nassert steam_engine.energy > 0, "Steam engine is not generating power"\nprint("Power infrastructure successfully built and generating electricity")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = 'assembly_pos = Position(x = -37, y = -16.5)\nmove_to(assembly_pos)\ntarget_machine = place_entity(Prototype.AssemblingMachine2, position=assembly_pos, direction = Direction.DOWN)\nprint(f"Placed AssemblingMachine1 at {target_machine.position} to automatically create copper cables")\n# put a inserter next to the assembly machine\n# always use 0 spacing for inserters\n# direction is RIGHT as we added to the width of the buildable coordinates\nmachine_input_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=target_machine.position,\n    direction=Direction.RIGHT,\n    spacing = 0)\n# rotate the inserter as we need to put items into the chest\nmachine_input_inserter = rotate_entity(machine_input_inserter, direction = Direction.LEFT)\ninput_chest = place_entity(Prototype.WoodenChest,position=machine_input_inserter.pickup_position)\nprint(f"Placed input inserter at {machine_input_inserter.position} and chest at {input_chest.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nmachine_input_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=target_machine.position,\n    direction=Direction.LEFT,\n    spacing = 0)\n# rotate the inserter as we need to put items into the chest\nmachine_input_inserter = rotate_entity(machine_input_inserter, direction = Direction.RIGHT)\ninput_chest = place_entity(Prototype.WoodenChest,position=machine_input_inserter.pickup_position)\nprint(f"Placed input inserter at {machine_input_inserter.position} and chest at {input_chest.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nmachine_input_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=machine_input_inserter.position,\n    direction=Direction.UP,\n    spacing = 0)\n# rotate the inserter as we need to put items into the chest\nmachine_input_inserter = rotate_entity(machine_input_inserter, direction = Direction.RIGHT)\ninput_chest = place_entity(Prototype.WoodenChest,position=machine_input_inserter.pickup_position)\nprint(f"Placed input inserter at {machine_input_inserter.position} and chest at {input_chest.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nmachine_input_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=machine_input_inserter.position,\n    direction=Direction.DOWN,\n    spacing = 1)\n# rotate the inserter as we need to put items into the chest\nmachine_input_inserter = rotate_entity(machine_input_inserter, direction = Direction.RIGHT)\ninput_chest = place_entity(Prototype.WoodenChest,position=machine_input_inserter.pickup_position)\nprint(f"Placed input inserter at {machine_input_inserter.position} and chest at {input_chest.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nmachine_output_inserter = place_entity_next_to(Prototype.BurnerInserter,\n    reference_position=target_machine.position,\n    direction=Direction.UP,\n    spacing = 0)\nprint(f"Placed a inserter at {machine_output_inserter.position} to put copper plates into assembling machine at {target_machine.position}")\n# fuel the inserter\n# we also update the inserter variable by returning it from the function\n# This ensures it doesnt get stale and the inventory updates are represented in the variable\nmachine_input_inserter = insert_item(Prototype.Coal, machine_input_inserter, quantity=20)\nchest = place_entity(Prototype.WoodenChest, position = machine_output_inserter.drop_position)\nprint(f"Placed output chest at {chest.position}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


        test_string_1 = 'ass_machine = get_entity(Prototype.AssemblingMachine2, Position(x = -37, y = -16.5))\nsteam_engine = get_entity(Prototype.SteamEngine, Position(x=-1.5, y=1.5))\ngroup = connect_entities(ass_machine,steam_engine, Prototype.SmallElectricPole)\nprint(f"Connected ass_machine {ass_machine.position} with {group}")\nass_machine = get_entity(Prototype.AssemblingMachine2, Position(x = -37, y = -16.5))\nassert ass_machine.energy > 0, "Assembly machine not connected to power"'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = f'ass_machine = get_entity(Prototype.AssemblingMachine2, Position(x = -37, y = -16.5))\nset_entity_recipe(entity = ass_machine, prototype = Prototype.Concrete)\nass_machine = rotate_entity(ass_machine, Direction.DOWN)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = 'tank_pos = Position(x = -37, y = -6.5)\nmove_to(tank_pos)\ntank = place_entity(Prototype.StorageTank, position=tank_pos, direction = Direction.DOWN)\nprint(f"Placed storagetank at {tank.position}")\nass_machine = get_entity(Prototype.AssemblingMachine2, Position(x = -37, y = -16.5))\nconnect_entities(tank, ass_machine, Prototype.Pipe)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        assert "Error" not in result, "Could not connect ass machine to power"
        game_state = GameState.from_instance(instance)
        
        for test in tests:
                fluid = test["liquid_input"][0]
                command = f'/c game.surfaces[1].find_entity("storage-tank", {{-37,-6.5}}).fluidbox[1] = {{ name = "{fluid}", amount = 25000 }}'
                instance.rcon_client.send_command(command)

                ingredient_list = [x[1] for x in test["solid_inputs"]]
                ingredient_list = str(ingredient_list)
                ingredient_list = ingredient_list.replace("'", "")
                test_string_1 = f'ass_machine = get_entity(Prototype.AssemblingMachine2, Position(x = -37, y = -16.5))\nset_entity_recipe(entity = ass_machine, prototype = {test["output"][1]})\nchest_1 = get_entity(Prototype.WoodenChest, Position( x=-33.5 ,y=-16.5))\nchest_2 = get_entity(Prototype.WoodenChest, Position( x=-39.5,y=-16.5))\nchest_3 = get_entity(Prototype.WoodenChest, Position( x=-39.5,y=-17.5))\nchest_4 = get_entity(Prototype.WoodenChest, Position( x=-39.5, y=-15.5))\nfor idx, item in enumerate({ingredient_list}):\n    insert_item(item, [chest_1, chest_2, chest_3, chest_4][idx], quantity=100)\nsleep(180)\noutput_chest = get_entity(Prototype.WoodenChest, Position(x=-36.5 ,y=-19.5))\noutput_inv = inspect_inventory(output_chest)\nprint(output_inv)\nassert output_inv.get({test["output"][1]}, 0) > 0, f"Test for {test["output"][1]} failed"'
                output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
                print(result)
                assert "Error" not in result, f"Error in test {test['output'][1]}"

                instance.reset(game_state)
        print(f"asd")


def test_rotation(): # DEMO
        from eval.open.model.game_state import GameState
        from env.src.game_types import Prototype, Resource, Direction, Position, BuildingBox   
        
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-1": 5, "electric-furnace": 10, "assembling-machine-2": 5, "storage-tank": 8}
        
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 


        test_string_1 = 'assembly_pos = Position(x = -37, y = -16.5)\nmove_to(assembly_pos)\nass_machine = place_entity(Prototype.AssemblingMachine2, position=assembly_pos, direction = Direction.UP)\nass_machine = set_entity_recipe(entity = ass_machine, prototype = Prototype.Battery)\nprint(ass_machine.recipe)\nass_machine = rotate_entity(ass_machine, Direction.LEFT)\nprint(ass_machine.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        game_state = GameState.from_instance(instance)
        test_string_1 = 'ass_machine = get_entity(Prototype.AssemblingMachine2, Position(x = -37, y = -16.5))\nprint(ass_machine.direction)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

def test_solar_panels(): # DEMO
        from env.src.game_types import Prototype, Resource, Direction, Position, BuildingBox   
        
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-1": 5, "electric-furnace": 10, "assembling-machine-2": 5, "solar-panel": 100}
        
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 
        instance.speed
        #test_string_1 = '\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\nsleep(5)\ninserter_to_furnace1 = place_entity_next_to(Prototype.StoneFurnace,reference_position=drill.drop_position, spacing=0)'
        #test_string_1 = 'print(Prototype.BurnerMiningDrill.WIDTH)\nprint(Prototype.AssemblingMachine2.HEIGHT)\niron_ore_loc = nearest(Resource.IronOre)\nprint(f"found iron ore at {iron_ore_loc}")\nmove_to(iron_ore_loc)\nprint(f"Moved to iron ore location")\ndrill = place_entity(Prototype.BurnerMiningDrill, position = iron_ore_loc)\ndrill = insert_item(Prototype.Coal, drill, 30)\nprint(f"Placed drill at iron ore location ({drill.position}) and inserted coal")\nbbox = BuildingBox(height = 2,width = 3)\ncoords = nearest_buildable(entity = Prototype.Boiler, building_box = bbox, center_position = drill.drop_position)\nfurn = place_entity(Prototype.Boiler, position = coords.left_top, direction = Direction.RIGHT)'
        test_string_1 = 'power_position = Position(x = 0, y = 10)\nmove_to(power_position)\npanel = place_entity(Prototype.SolarPanel, Direction.UP, power_position)\nass_pos_1 = Position(x = 0, y = 0)\nass_pos_2 = Position(x = -10, y = 0)\nass_pos_3 = Position(x = 10, y = 0)\nmove_to(ass_pos_1)\nass_machine_1 = place_entity(Prototype.AssemblingMachine1, Direction.UP, ass_pos_1)\nmove_to(ass_pos_2)\nass_machine_2 = place_entity(Prototype.AssemblingMachine1, Direction.UP, ass_pos_2)\nmove_to(ass_pos_3)\nass_machine_3 = place_entity(Prototype.AssemblingMachine1, Direction.UP, ass_pos_3)\ngroup = connect_entities(ass_machine_1, panel, Prototype.SmallElectricPole)\ngroup = connect_entities(ass_machine_2, panel, Prototype.SmallElectricPole)\ngroup = connect_entities(ass_machine_3, panel, Prototype.SmallElectricPole)\nsleep(2)\nass_machine_1 = get_entity(Prototype.AssemblingMachine1, ass_pos_1)\nassert ass_machine_1.energy > 0, f"No power for ass machine 1"\nass_machine_2 = get_entity(Prototype.AssemblingMachine1, ass_pos_2)\nassert ass_machine_2.energy > 0, f"No power for ass machine 2"\nass_machine_3 = get_entity(Prototype.AssemblingMachine1, ass_pos_3)\nassert ass_machine_3.energy > 0, f"No power for ass machine 3"'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)
        instance.reset()

        test_string_1 = 'power_position = Position(x = 0, y = 10)\nmove_to(power_position)\npanel = place_entity(Prototype.SolarPanel, Direction.UP, power_position)\nass_pos_1 = Position(x = 0, y = 0)\nass_pos_2 = Position(x = -10, y = 0)\nass_pos_3 = Position(x = 10, y = 0)\nmove_to(ass_pos_1)\nass_machine_1 = place_entity(Prototype.AssemblingMachine1, Direction.UP, ass_pos_1)\nmove_to(ass_pos_2)\nass_machine_2 = place_entity(Prototype.AssemblingMachine1, Direction.UP, ass_pos_2)\nmove_to(ass_pos_3)\nass_machine_3 = place_entity(Prototype.AssemblingMachine1, Direction.UP, ass_pos_3)\ngroup = connect_entities(ass_machine_1, panel, Prototype.SmallElectricPole)\ngroup = connect_entities(ass_machine_2, group, Prototype.SmallElectricPole)\ngroup = connect_entities(ass_machine_3, group, Prototype.SmallElectricPole)\nsleep(2)\nass_machine_1 = get_entity(Prototype.AssemblingMachine1, ass_pos_1)\nassert ass_machine_1.energy > 0, f"No power for ass machine 1"\nass_machine_2 = get_entity(Prototype.AssemblingMachine1, ass_pos_2)\nassert ass_machine_2.energy > 0, f"No power for ass machine 2"\nass_machine_3 = get_entity(Prototype.AssemblingMachine1, ass_pos_3)\nassert ass_machine_3.energy > 0, f"No power for ass machine 3"\nprint(get_entities())'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)

        instance.reset()

        test_string_1 = 'power_position = Position(x = 0, y = 10)\nmove_to(power_position)\npanel = place_entity(Prototype.SolarPanel, Direction.UP, power_position)\nass_pos_1 = Position(x = 0, y = 0)\nass_pos_2 = Position(x = -10, y = 0)\nass_pos_3 = Position(x = 10, y = 0)\nmove_to(ass_pos_1)\nass_machine_1 = place_entity(Prototype.AssemblingMachine1, Direction.UP, ass_pos_1)\nmove_to(ass_pos_2)\nass_machine_2 = place_entity(Prototype.AssemblingMachine1, Direction.UP, ass_pos_2)\nmove_to(ass_pos_3)\nass_machine_3 = place_entity(Prototype.AssemblingMachine1, Direction.UP, ass_pos_3)\ngroup = connect_entities(ass_machine_1, ass_machine_2, ass_machine_3, panel, Prototype.SmallElectricPole)\nsleep(2)\nass_machine_1 = get_entity(Prototype.AssemblingMachine1, ass_pos_1)\nassert ass_machine_1.energy > 0, f"No power for ass machine 1"\nass_machine_2 = get_entity(Prototype.AssemblingMachine1, ass_pos_2)\nassert ass_machine_2.energy > 0, f"No power for ass machine 2"\nass_machine_3 = get_entity(Prototype.AssemblingMachine1, ass_pos_3)\nassert ass_machine_3.energy > 0, f"No power for ass machine 3"\nprint(get_entities())'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


def test_error_pattern_48(): # DEMO
        from eval.open.model.game_state import GameState
        from env.src.game_types import Prototype, Resource, Direction, Position, BuildingBox   
        
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-1": 5, "electric-furnace": 10, "assembling-machine-2": 5, "solar-panel": 100}
        
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        test_string_1 = '# Find water and set up power\nwater_pos = nearest(Resource.Water)\nprint(f"Found water at {water_pos}")\nmove_to(water_pos)\n\n# Place offshore pump\npump = place_entity(Prototype.OffshorePump, position=Position(x=-10.5, y=-0.5))\nprint(f"Placed offshore pump at {pump.position}")\nmove_to(Position(x=-5.5,y=3.0))\nboiler = place_entity(Prototype.Boiler, position=Position(x=-5.5,y=3.0))\nprint(f"Placed boiler at {boiler.position}")\n\n# Add coal to boiler\nboiler = insert_item(Prototype.Coal, boiler, 50)\n\n# Place steam engine\nmove_to(Position(x=0.5, y=7.5))\nsteam_engine = place_entity(Prototype.SteamEngine, position=Position(x=0.5, y=7.5))\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect everything with pipes\nwater_pipes = connect_entities(pump, boiler, Prototype.Pipe)\nsteam_pipes = connect_entities(boiler, steam_engine, Prototype.Pipe)\n\n# Wait for power generation to start\nsleep(5)\nsteam_engine = get_entity(Prototype.SteamEngine, steam_engine.position)\nassert steam_engine.energy > 0, "Steam engine not generating power"\nprint(f"Power infrastructure setup complete and generating power!")\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")\n'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = '# Add power poles to steam engine\nmove_to(steam_engine.position)\npower_pole = place_entity_next_to(Prototype.SmallElectricPole, \n                                 steam_engine.position,\n                                 direction=Direction.RIGHT,\n                                 spacing=1)\nprint(f"Added power pole at {power_pole.position}")\n\n# Find copper ore patch\ncopper_pos = nearest(Resource.CopperOre)\nprint(f"Found copper ore at {copper_pos}")\n\n# Plan space for 3 electric drills in a line\nbuilding_box = BuildingBox(\n    width=3 * Prototype.ElectricMiningDrill.WIDTH,\n    height=Prototype.ElectricMiningDrill.HEIGHT + Prototype.StoneFurnace.HEIGHT + 2\n)\n\ndrill_area = nearest_buildable(Prototype.ElectricMiningDrill, building_box, copper_pos)\nmove_to(drill_area.left_top)\n\n# Place 3 mining drills\ndrills = []\nfor i in range(3):\n    drill_pos = Position(\n        x=drill_area.left_top.x + (Prototype.ElectricMiningDrill.WIDTH * i),\n        y=drill_area.left_top.y\n    )\n    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_pos, direction=Direction.DOWN)\n    drills.append(drill)\n    print(f"Placed electric mining drill {i} at {drill.position}")\n\n# Connect drills to power\nfor drill in drills:\n    poles = connect_entities(power_pole, drill, Prototype.SmallElectricPole)\n    print(f"Connected power to drill at {drill.position}")\n\n# Verify power\nsleep(5)\nfor drill in drills:\n    drill = get_entity(Prototype.ElectricMiningDrill, drill.position)\n    assert drill.energy > 0, f"Drill at {drill.position} not receiving power"\n\nprint(f"Mining setup complete!")\nprint(f"Current inventory: {inspect_inventory()}")\nprint(f"Entities on map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)



def test_error_pattern_50(): # DEMO
        from eval.open.model.game_state import GameState
        from env.src.game_types import Prototype, Resource, Direction, Position, BuildingBox   
        
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-1": 5, "electric-furnace": 10, "assembling-machine-2": 5, "solar-panel": 100}
        
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        test_string_1 = '# Find water source\nwater_pos = nearest(Resource.Water)\nprint(f"Found water at {water_pos}")\n\n# Move to water\nmove_to(water_pos)\n\n# Place offshore pump\npump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {pump.position}")\n\n# Place boiler with spacing for pipes\nboiler = place_entity_next_to(Prototype.Boiler, pump.position, Direction.RIGHT, spacing=2)\nprint(f"Placed boiler at {boiler.position}")\n\n# Add coal to boiler\nboiler = insert_item(Prototype.Coal, boiler, 50)\nprint(f"Added coal to boiler")\n\n# Place steam engine\nengine = place_entity_next_to(Prototype.SteamEngine, boiler.position, Direction.RIGHT, spacing=2)\nprint(f"Placed steam engine at {engine.position}")\n\n# Connect with pipes\npipes = connect_entities(pump, boiler, Prototype.Pipe)\nprint(f"Connected pump to boiler with pipes")\n\nsteam_pipes = connect_entities(boiler, engine, Prototype.Pipe)\nprint(f"Connected boiler to steam engine with pipes")\n\n# Wait for power generation to start\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")\n'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = '# Add power pole to steam engine\npole = place_entity_next_to(Prototype.SmallElectricPole, engine.position, Direction.RIGHT, spacing=1)\nprint(f"Added power pole at {pole.position}")\n\n# Find iron ore patch\niron_pos = nearest(Resource.IronOre)\nprint(f"Found iron ore at {iron_pos}")\n\n# Move to iron position\nmove_to(iron_pos)\n\n# Calculate space needed for 2 drills side by side\nbuilding_box = BuildingBox(\n    width=Prototype.ElectricMiningDrill.WIDTH * 2 + 2, \n    height=Prototype.ElectricMiningDrill.HEIGHT + 2\n)\n\n# Find buildable area\nbuildable_coords = nearest_buildable(\n    Prototype.ElectricMiningDrill,\n    building_box,\n    iron_pos\n)\n\n# Place first drill\ndrill1 = place_entity(\n    Prototype.ElectricMiningDrill,\n    position=buildable_coords.left_top,\n    direction=Direction.DOWN\n)\nprint(f"Placed first mining drill at {drill1.position}")\n\n# Place second drill next to it\ndrill2 = place_entity_next_to(\n    Prototype.ElectricMiningDrill,\n    drill1.position,\n    direction=Direction.RIGHT,\n    spacing=0\n)\nprint(f"Placed second mining drill at {drill2.position}")\n\n# Connect power to drills\npower_connection = connect_entities(\n    pole,\n    drill1,\n    Prototype.SmallElectricPole\n)\nprint(f"Connected power to mining drills")\n\n# Verify power connection\nsleep(5)\ndrill1 = get_entity(Prototype.ElectricMiningDrill, drill1.position)\ndrill2 = get_entity(Prototype.ElectricMiningDrill, drill2.position)\nassert drill1.energy > 0 and drill2.energy > 0, "Drills not receiving power"\n\nprint(f"Current inventory: {inspect_inventory()}")\nprint(f"Entities on map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = '# Place first furnace at drill1\'s drop position\nmove_to(drill1.drop_position)\nfurnace1 = place_entity(Prototype.StoneFurnace, position=drill1.drop_position)\nprint(f"Placed first furnace at {furnace1.position}")\n\n# Add coal to first furnace\nfurnace1 = insert_item(Prototype.Coal, furnace1, 25)\nprint(f"Added coal to first furnace")\n\n# Place second furnace at drill2\'s drop position\nmove_to(drill2.drop_position)\nfurnace2 = place_entity(Prototype.StoneFurnace, position=drill2.drop_position)\nprint(f"Placed second furnace at {furnace2.position}")\n\n# Add coal to second furnace\nfurnace2 = insert_item(Prototype.Coal, furnace2, 25)\nprint(f"Added coal to second furnace")\n\n# Place assembling machine for gear wheels\n# Calculate position 5 spaces south of furnaces\nassembler_pos = Position(x=(furnace1.position.x + furnace2.position.x)/2, \n                        y=furnace1.position.y + 5)\n\n# Create building box for assembler and inserters\nbuilding_box = BuildingBox(\n    width=Prototype.AssemblingMachine2.WIDTH + 4,  # Extra space for inserters\n    height=Prototype.AssemblingMachine2.HEIGHT + 4\n)\n\nbuildable_coords = nearest_buildable(\n    Prototype.AssemblingMachine2,\n    building_box,\n    assembler_pos\n)\n\n# Place assembling machine\nmove_to(buildable_coords.center)\nassembler = place_entity(Prototype.AssemblingMachine2, position=buildable_coords.center)\nprint(f"Placed assembling machine at {assembler.position}")\n\n# Set recipe for iron gear wheels\nassembler = set_entity_recipe(assembler, Prototype.IronGearWheel)\nprint(f"Set assembling machine recipe to iron gear wheel")\n\n# Connect power to assembler\npower_connection = connect_entities(\n    pole,\n    assembler,\n    Prototype.SmallElectricPole\n)\nprint(f"Connected power to assembling machine")\n\n# Add input inserters for both furnaces\ninput_inserter1 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    furnace1.position,\n    Direction.RIGHT,\n    spacing=0\n)\ninput_inserter1 = rotate_entity(input_inserter1, Direction.LEFT)\nprint(f"Placed input inserter 1 at {input_inserter1.position}")\n\ninput_inserter2 = place_entity_next_to(\n    Prototype.BurnerInserter,\n    furnace2.position,\n    Direction.RIGHT,\n    spacing=0\n)\ninput_inserter2 = rotate_entity(input_inserter2, Direction.LEFT)\nprint(f"Placed input inserter 2 at {input_inserter2.position}")\n\n# Add coal to inserters\ninput_inserter1 = insert_item(Prototype.Coal, input_inserter1, 5)\ninput_inserter2 = insert_item(Prototype.Coal, input_inserter2, 5)\n\n# Connect furnaces to assembler with transport belts\nbelts = connect_entities(\n    input_inserter1,\n    assembler,\n    Prototype.TransportBelt\n)\nprint(f"Connected furnace 1 to assembler")\n\nbelts = connect_entities(\n    input_inserter2,\n    assembler,\n    Prototype.TransportBelt\n)\nprint(f"Connected furnace 2 to assembler")\n\nprint(f"Current inventory: {inspect_inventory()}")\nprint(f"Entities on map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = '# Add input inserter for assembling machine\nassembler_input = place_entity_next_to(\n    Prototype.BurnerInserter,\n    assembler.position,\n    Direction.LEFT,\n    spacing=0\n)\nassembler_input = rotate_entity(assembler_input, Direction.RIGHT)\nprint(f"Placed assembler input inserter at {assembler_input.position}")\n\n# Add coal to input inserter\nassembler_input = insert_item(Prototype.Coal, assembler_input, 5)\nprint(f"Added coal to assembler input inserter")\n\n# Now connect furnaces to assembler input inserter with belts\nbelts1 = connect_entities(\n    input_inserter1,\n    assembler_input,\n    Prototype.TransportBelt\n)\nprint(f"Connected furnace 1 to assembler input")\n\nbelts2 = connect_entities(\n    input_inserter2,\n    assembler_input,\n    Prototype.TransportBelt\n)\nprint(f"Connected furnace 2 to assembler input")\n\n# Add output inserter and chest\noutput_inserter = place_entity_next_to(\n    Prototype.BurnerInserter,\n    assembler.position,\n    Direction.RIGHT,\n    spacing=0\n)\nprint(f"Placed assembler output inserter at {output_inserter.position}")\n\n# Add coal to output inserter\noutput_inserter = insert_item(Prototype.Coal, output_inserter, 5)\nprint(f"Added coal to assembler output inserter")\n\n# Add output chest\noutput_chest = place_entity_next_to(\n    Prototype.WoodenChest,\n    output_inserter.position,\n    Direction.RIGHT,\n    spacing=0\n)\nprint(f"Placed output chest at {output_chest.position}")\n\n# Wait to check if system is working\nsleep(15)\n\nprint(f"Current inventory: {inspect_inventory()}")\nprint(f"Entities on map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)
        print(f"done")


def test_error_pattern_51(): # DEMO
        from env.src.game_types import Prototype, Resource, Direction, Position, BuildingBox   
        
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 50, "wooden-chest": 10, "burner-inserter": 50,"inserter": 50, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 2, "offshore-pump": 2, "steam-engine": 2,
                                "electric-mining-drill": 50, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-2": 10, "electric-furnace": 10, "pipe-to-ground": 100, "underground-belt": 100,
                                "pumpjack": 10, "oil-refinery": 5, "chemical-plant": 5, "storage-tank": 10,
                                #"solar-panel": 50,
                                }
        
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        test_string_1 = '# Find water source\nwater_pos = nearest(Resource.Water)\nprint(f"Found water at {water_pos}")\n\n# Move to water\nmove_to(water_pos)\n\n# Place offshore pump\npump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {pump.position}")\n\n# Place boiler with spacing for pipes\nboiler = place_entity_next_to(Prototype.Boiler, pump.position, Direction.RIGHT, spacing=2)\nprint(f"Placed boiler at {boiler.position}")\n\n# Add coal to boiler\nboiler = insert_item(Prototype.Coal, boiler, 50)\nprint(f"Added coal to boiler")\n\n# Place steam engine\nengine = place_entity_next_to(Prototype.SteamEngine, boiler.position, Direction.RIGHT, spacing=2)\nprint(f"Placed steam engine at {engine.position}")\n\n# Connect with pipes\npipes = connect_entities(pump, boiler, Prototype.Pipe)\nprint(f"Connected pump to boiler with pipes")\n\nsteam_pipes = connect_entities(boiler, engine, Prototype.Pipe)\nprint(f"Connected boiler to steam engine with pipes")\n\n# Wait for power generation to start\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")\n'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


        test_string_1 = 'oil_pos = nearest(Resource.CrudeOil)\nmove_to(oil_pos)\npump = place_entity(Prototype.PumpJack, position = oil_pos)\nstor_tank_pos = Position(x = oil_pos.x - 10, y = oil_pos.y)\nmove_to(stor_tank_pos)\ntank = place_entity(Prototype.StorageTank, position = stor_tank_pos)\npipes = connect_entities(pump, tank, Prototype.Pipe)\npoles = connect_entities(engine, pump, Prototype.SmallElectricPole)\nsleep(60)'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

def test_error_pattern_52(): # DEMO
        from env.src.game_types import Prototype, Resource, Direction, Position, BuildingBox   
        
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 50, "wooden-chest": 10, "burner-inserter": 50,"inserter": 50, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 2, "offshore-pump": 2, "steam-engine": 2,
                                "electric-mining-drill": 50, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-2": 10, "electric-furnace": 10, "pipe-to-ground": 100, "underground-belt": 100,
                                "pumpjack": 10, "oil-refinery": 5, "chemical-plant": 5, "storage-tank": 10,
                                #"solar-panel": 50,
                                }
        
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        test_string_1 = 'move_to(Position(x=25.5, y=63.5))\nchem_plant = place_entity(Prototype.ChemicalPlant, position = Position(x=25.5, y=63.5))\n# First set recipe again to ensure it\'s set\nchem_plant = set_entity_recipe(chem_plant, Prototype.Sulfur)\nfurnace = place_entity_next_to(Prototype.ElectricFurnace, reference_position = chem_plant.position, direction = Direction.RIGHT)\nprint(f"placed furance at {furnace.position}")\nprint(f"Reset chemical plant recipe")\n\n# Connect petroleum gas from storage tank\nmove_to(Position(x=30.5, y=58.5))\nstorage_tank = place_entity(Prototype.StorageTank, position = Position(x=30.5, y=58.5))\npetrol_pipes = connect_entities(storage_tank, chem_plant,\n                              {Prototype.Pipe, Prototype.UndergroundPipe})\nprint(f"Connected petroleum gas to chemical plant")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


        #test_string_1 = 'oil_pos = nearest(Resource.CrudeOil)\nmove_to(oil_pos)\npump = place_entity(Prototype.PumpJack, position = oil_pos)\nstor_tank_pos = Position(x = oil_pos.x - 10, y = oil_pos.y)\nmove_to(stor_tank_pos)\ntank = place_entity(Prototype.StorageTank, position = stor_tank_pos)\npipes = connect_entities(pump, tank, Prototype.Pipe)\npoles = connect_entities(engine, pump, Prototype.SmallElectricPole)\nsleep(60)'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)
        


def test_error_pattern_53(): # DEMO
        from env.src.game_types import Prototype, Resource, Direction, Position, BuildingBox   
        
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 50, "wooden-chest": 10, "burner-inserter": 50,"inserter": 50, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 2, "offshore-pump": 2, "steam-engine": 2,
                                "electric-mining-drill": 50, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-2": 10, "electric-furnace": 10, "pipe-to-ground": 100, "underground-belt": 100,
                                "pumpjack": 10, "oil-refinery": 5, "chemical-plant": 5, "storage-tank": 10,
                                #"solar-panel": 50,
                                }
        
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        test_string_1 = '# First find water\nwater_pos = nearest(Resource.Water)\nprint(f"Found water at {water_pos}")\n\n# Place offshore pump\nmove_to(water_pos)\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {offshore_pump.position}")\n\n# Place storage tank for water buffer\n# Need to find safe spot away from water\nbuilding_box = BuildingBox(width=Prototype.StorageTank.WIDTH + 4, height=Prototype.StorageTank.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.StorageTank, building_box, offshore_pump.position)\nmove_to(coords.center)\nwater_tank = place_entity(Prototype.StorageTank, position=coords.center)\nprint(f"Placed water storage tank at {water_tank.position}")\n\n# Connect pump to tank with pipes\npipes = connect_entities(offshore_pump, water_tank, {Prototype.Pipe, Prototype.UndergroundPipe})\nprint(f"Connected offshore pump to storage tank with pipes")\n\n# Wait to verify water flow\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")\n'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)

        test_string_1 = '# First set up power generation\nprint("Setting up power system...")\n# Place boiler near water tank\nbuilding_box = BuildingBox(width=Prototype.Boiler.WIDTH + 4, height=Prototype.Boiler.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.Boiler, building_box, water_tank.position)\nmove_to(coords.center)\nboiler = place_entity(Prototype.Boiler, position=coords.center)\nprint(f"Placed boiler at {boiler.position}")\n\n# Add steam engine\nbuilding_box = BuildingBox(width=Prototype.SteamEngine.WIDTH + 4, height=Prototype.SteamEngine.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.SteamEngine, building_box, boiler.position)\nmove_to(coords.center)\nsteam_engine = place_entity(Prototype.SteamEngine, position=coords.center)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect water and steam\nwater_pipes = connect_entities(water_tank, boiler, {Prototype.Pipe, Prototype.UndergroundPipe})\nsteam_pipes = connect_entities(boiler, steam_engine, {Prototype.Pipe, Prototype.UndergroundPipe})\nprint("Connected water and steam pipes")\n\n# Add fuel to boiler\nboiler = insert_item(Prototype.Coal, boiler, quantity=50)\nprint("Added coal to boiler")\n\n# Now find crude oil\ncrude_oil_pos = nearest(Resource.CrudeOil)\nprint(f"Found crude oil at {crude_oil_pos}")\n\n# Place pumpjack\nmove_to(crude_oil_pos)\npumpjack = place_entity(Prototype.PumpJack, position=crude_oil_pos)\nprint(f"Placed pumpjack at {pumpjack.position}")\n\n# Connect power to pumpjack\npower_poles = connect_entities(steam_engine, pumpjack, Prototype.SmallElectricPole)\nprint(f"Connected power to pumpjack")\n\n# Place oil refinery\nbuilding_box = BuildingBox(width=Prototype.OilRefinery.WIDTH + 4, height=Prototype.OilRefinery.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.OilRefinery, building_box, pumpjack.position)\nmove_to(coords.center)\nrefinery = place_entity(Prototype.OilRefinery, position=coords.center)\nprint(f"Placed oil refinery at {refinery.position}")\n\n# Set recipe to basic oil processing\nrefinery = set_entity_recipe(refinery, "basic-oil-processing")\n\n# Connect power to refinery\npower_poles = connect_entities(pumpjack, refinery, Prototype.SmallElectricPole)\n\n# Place petroleum gas storage tank\nbuilding_box = BuildingBox(width=Prototype.StorageTank.WIDTH + 4, height=Prototype.StorageTank.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.StorageTank, building_box, refinery.position)\nmove_to(coords.center)\npetrol_tank = place_entity(Prototype.StorageTank, position=coords.center)\nprint(f"Placed petroleum gas storage tank at {petrol_tank.position}")\n\n# Connect pumpjack to refinery and refinery to storage\ncrude_pipes = connect_entities(pumpjack, refinery, {Prototype.Pipe, Prototype.UndergroundPipe})\npetrol_pipes = connect_entities(refinery, petrol_tank, {Prototype.Pipe, Prototype.UndergroundPipe})\nprint("Connected all oil processing pipes")\n\n# Wait to verify oil flow\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        #test_string_1 = 'oil_pos = nearest(Resource.CrudeOil)\nmove_to(oil_pos)\npump = place_entity(Prototype.PumpJack, position = oil_pos)\nstor_tank_pos = Position(x = oil_pos.x - 10, y = oil_pos.y)\nmove_to(stor_tank_pos)\ntank = place_entity(Prototype.StorageTank, position = stor_tank_pos)\npipes = connect_entities(pump, tank, Prototype.Pipe)\npoles = connect_entities(engine, pump, Prototype.SmallElectricPole)\nsleep(60)'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)


def test_error_pattern_54(): # DEMO
        from env.src.game_types import Prototype, Resource, Direction, Position, BuildingBox   
        
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 50, "wooden-chest": 10, "burner-inserter": 50,"inserter": 50, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 2, "offshore-pump": 2, "steam-engine": 2,
                                "electric-mining-drill": 50, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-2": 10, "electric-furnace": 10, "pipe-to-ground": 100, "underground-belt": 100,
                                "pumpjack": 10, "oil-refinery": 5, "chemical-plant": 5, "storage-tank": 10,
                                #"solar-panel": 50,
                                }
        
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        test_string_1 = '# Find water and setup power\nwater_pos = nearest(Resource.Water)\nmove_to(water_pos)\n\n# Place offshore pump\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {offshore_pump.position}")\n\n# Place boiler with space for connections\nbuilding_box = BuildingBox(width=Prototype.Boiler.WIDTH + 4, height=Prototype.Boiler.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.Boiler, building_box, offshore_pump.position)\nmove_to(coords.center)\nboiler = place_entity(Prototype.Boiler, position=coords.center)\nprint(f"Placed boiler at {boiler.position}")\n\n# Place steam engine\nbuilding_box = BuildingBox(width=Prototype.SteamEngine.WIDTH + 4, height=Prototype.SteamEngine.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.SteamEngine, building_box, boiler.position)\nmove_to(coords.center)\nsteam_engine = place_entity(Prototype.SteamEngine, position=coords.center)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect water system\nwater_pipes = connect_entities(offshore_pump, boiler, Prototype.Pipe)\nsteam_pipes = connect_entities(boiler, steam_engine, Prototype.Pipe)\nprint(f"Connected water and steam pipes")\n\n# Add fuel to boiler\nboiler = insert_item(Prototype.Coal, boiler, 50)\nprint(f"Added coal to boiler")\n\n# Wait for power generation\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")\n'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = '# First connect power poles to steam engine\nmove_to(steam_engine.position)\npower_pole = place_entity_next_to(Prototype.SmallElectricPole, steam_engine.position, direction=Direction.RIGHT)\nprint(f"Added power pole at {power_pole.position}")\n\n# Now let\'s find oil and set up processing\noil_pos = nearest(Resource.CrudeOil)\nmove_to(oil_pos)\n\n# Place pumpjack\npumpjack = place_entity(Prototype.PumpJack, position=oil_pos)\nprint(f"Placed pumpjack at {pumpjack.position}")\n\n# Connect power to pumpjack\npoles = connect_entities(power_pole, pumpjack, Prototype.SmallElectricPole)\nprint(f"Connected power to pumpjack")\n\n# Place oil refinery with space for connections\n# Put it 20 tiles away from pumpjack to leave room for pipes\nrefinery_pos = Position(x=pumpjack.position.x + 20, y=pumpjack.position.y)\nbuilding_box = BuildingBox(width=Prototype.OilRefinery.WIDTH + 4, height=Prototype.OilRefinery.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.OilRefinery, building_box, refinery_pos)\nmove_to(coords.center)\nrefinery = place_entity(Prototype.OilRefinery, position=coords.center)\nprint(f"Placed oil refinery at {refinery.position}")\n\n# Connect power to refinery\npoles = connect_entities(pumpjack, refinery, Prototype.SmallElectricPole)\nprint(f"Connected power to refinery")\n\n# Connect pumpjack to refinery with pipes\npipes = connect_entities(pumpjack, refinery, {Prototype.Pipe, Prototype.UndergroundPipe})\nprint(f"Connected pumpjack to refinery with pipes")\n\n# Set refinery recipe to basic oil processing\nrefinery = set_entity_recipe(refinery, RecipeName.BasicOilProcessing)\nprint(f"Set refinery recipe to basic oil processing")\n\n# Place storage tank for petroleum gas output\nstorage_pos = Position(x=refinery.position.x + 10, y=refinery.position.y)\nmove_to(storage_pos)\nstorage_tank = place_entity(Prototype.StorageTank, position=storage_pos)\nprint(f"Placed storage tank at {storage_tank.position}")\n\n# Connect refinery to storage tank\npipes = connect_entities(refinery, storage_tank, {Prototype.Pipe, Prototype.UndergroundPipe})\nprint(f"Connected refinery to storage tank")\n\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


        #test_string_1 = 'oil_pos = nearest(Resource.CrudeOil)\nmove_to(oil_pos)\npump = place_entity(Prototype.PumpJack, position = oil_pos)\nstor_tank_pos = Position(x = oil_pos.x - 10, y = oil_pos.y)\nmove_to(stor_tank_pos)\ntank = place_entity(Prototype.StorageTank, position = stor_tank_pos)\npipes = connect_entities(pump, tank, Prototype.Pipe)\npoles = connect_entities(engine, pump, Prototype.SmallElectricPole)\nsleep(60)'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)


def test_error_pattern_55(): # DEMO
        from env.src.game_types import Prototype, Resource, Direction, Position, BuildingBox   
        
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 50, "wooden-chest": 10, "burner-inserter": 50,"inserter": 50, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 2, "offshore-pump": 2, "steam-engine": 2,
                                "electric-mining-drill": 50, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-2": 10, "electric-furnace": 10, "pipe-to-ground": 100, "underground-belt": 100,
                                "pumpjack": 10, "oil-refinery": 5, "chemical-plant": 5, "storage-tank": 10,
                                #"solar-panel": 50,
                                }
        
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        test_string_1 = '# Find water and setup power\nwater_pos = nearest(Resource.Water)\nmove_to(water_pos)\n\n# Place offshore pump\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {offshore_pump.position}")\n\n# Place boiler with space for connections\nbuilding_box = BuildingBox(width=Prototype.Boiler.WIDTH + 4, height=Prototype.Boiler.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.Boiler, building_box, offshore_pump.position)\nmove_to(coords.center)\nboiler = place_entity(Prototype.Boiler, position=coords.center)\nprint(f"Placed boiler at {boiler.position}")\n\n# Place steam engine\nbuilding_box = BuildingBox(width=Prototype.SteamEngine.WIDTH + 4, height=Prototype.SteamEngine.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.SteamEngine, building_box, boiler.position)\nmove_to(coords.center)\nsteam_engine = place_entity(Prototype.SteamEngine, position=coords.center)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect water system\nwater_pipes = connect_entities(offshore_pump, boiler, Prototype.Pipe)\nsteam_pipes = connect_entities(boiler, steam_engine, Prototype.Pipe)\nprint(f"Connected water and steam pipes")\n\n# Add fuel to boiler\nboiler = insert_item(Prototype.Coal, boiler, 50)\nprint(f"Added coal to boiler")\n\n# Wait for power generation\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")\n'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = '# Now let\'s find oil and set up processing\noil_pos = nearest(Resource.CrudeOil)\nmove_to(oil_pos)\n\n# Place pumpjack\npumpjack = place_entity(Prototype.PumpJack, position=oil_pos)\nprint(f"Placed pumpjack at {pumpjack.position}")\n\n# Connect power to pumpjack\n# Place oil refinery with space for connections\n# Put it 20 tiles away from pumpjack to leave room for pipes\nrefinery_pos = Position(x=pumpjack.position.x + 20, y=pumpjack.position.y)\nbuilding_box = BuildingBox(width=Prototype.OilRefinery.WIDTH + 4, height=Prototype.OilRefinery.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.OilRefinery, building_box, refinery_pos)\nmove_to(coords.center)\nrefinery = place_entity(Prototype.OilRefinery, position=coords.center)\nprint(f"Placed oil refinery at {refinery.position}")\n\n# Connect boiler to refinery with pipes\nrefinery = set_entity_recipe(refinery, RecipeName.CoalLiquefaction)\npipes = connect_entities(boiler, refinery, {Prototype.Pipe, Prototype.UndergroundPipe})\nprint(f"Connected pumpjack to refinery with pipes")\n'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)



def test_error_pattern_56(): # DEMO
        from env.src.game_types import Prototype, Resource, Direction, Position, BuildingBox   
        
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 50, "wooden-chest": 10, "burner-inserter": 50,"inserter": 50, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 2, "offshore-pump": 2, "steam-engine": 2,
                                "electric-mining-drill": 50, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-2": 10, "electric-furnace": 10, "pipe-to-ground": 100, "underground-belt": 100,
                                "pumpjack": 10, "oil-refinery": 5, "chemical-plant": 5, "storage-tank": 10,
                                #"solar-panel": 50,
                                }
        
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        test_string_1 = '# Find water and setup power\nwater_pos = nearest(Resource.Water)\nmove_to(water_pos)\n\n# Place offshore pump\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {offshore_pump.position}")\n\n# Place boiler with space for connections\nbuilding_box = BuildingBox(width=Prototype.Boiler.WIDTH + 4, height=Prototype.Boiler.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.Boiler, building_box, offshore_pump.position)\nmove_to(coords.center)\nboiler = place_entity(Prototype.Boiler, position=coords.center)\nprint(f"Placed boiler at {boiler.position}")\n\n# Place steam engine\nbuilding_box = BuildingBox(width=Prototype.SteamEngine.WIDTH + 4, height=Prototype.SteamEngine.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.SteamEngine, building_box, boiler.position)\nmove_to(coords.center)\nsteam_engine = place_entity(Prototype.SteamEngine, position=coords.center)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect water system\nwater_pipes = connect_entities(offshore_pump, boiler, Prototype.Pipe)\nsteam_pipes = connect_entities(boiler, steam_engine, Prototype.Pipe)\nprint(f"Connected water and steam pipes")\n\n# Add fuel to boiler\nboiler = insert_item(Prototype.Coal, boiler, 50)\nprint(f"Added coal to boiler")\n\n# Wait for power generation\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")\n'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = '# Now let\'s find oil and set up processing\noil_pos = nearest(Resource.CrudeOil)\nmove_to(oil_pos)\n\n# Place pumpjack\npumpjack = place_entity(Prototype.PumpJack, position=oil_pos)\nprint(f"Placed pumpjack at {pumpjack.position}")\n\n# Connect power to pumpjack\n# Place oil refinery with space for connections\n# Put it 20 tiles away from pumpjack to leave room for pipes\nrefinery_pos = Position(x=pumpjack.position.x + 20, y=pumpjack.position.y)\nbuilding_box = BuildingBox(width=Prototype.OilRefinery.WIDTH + 4, height=Prototype.OilRefinery.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.OilRefinery, building_box, refinery_pos)\nmove_to(coords.center)\nrefinery = place_entity(Prototype.OilRefinery, position=coords.center)\nprint(f"Placed oil refinery at {refinery.position}")\n\nbuilding_box = BuildingBox(width=Prototype.StorageTank.WIDTH + 10, height=Prototype.StorageTank.HEIGHT + 10)\ncoords = nearest_buildable(Prototype.StorageTank, building_box, refinery_pos)\nmove_to(coords.center)\ntank = place_entity(Prototype.StorageTank, position=coords.center)\nprint(f"Placed oil refinery at {refinery.position}")\n\n\n# Connect pump to tank with pipes\nrefinery = set_entity_recipe(refinery, RecipeName.BasicOilProcessing)\npoles = connect_entities(pumpjack, steam_engine, Prototype.SmallElectricPole)\npipes = connect_entities(pumpjack, tank, {Prototype.Pipe, Prototype.UndergroundPipe})\nsleep(10)\npipes = connect_entities(tank, refinery, {Prototype.Pipe, Prototype.UndergroundPipe})'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)



def test_error_pattern_57(): # DEMO
        from env.src.game_types import Prototype, Resource, Direction, Position, BuildingBox   
        
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 50, "wooden-chest": 10, "burner-inserter": 50,"inserter": 50, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 2, "offshore-pump": 2, "steam-engine": 2,
                                "electric-mining-drill": 50, "small-electric-pole": 500, "pipe": 500,
                                "assembling-machine-2": 10, "electric-furnace": 10, "pipe-to-ground": 100, "underground-belt": 100,
                                "pumpjack": 10, "oil-refinery": 5, "chemical-plant": 5, "storage-tank": 10,
                                #"solar-panel": 50,
                                }
        
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        test_string_1 = '# Find water for power generation\nwater_pos = nearest(Resource.Water)\nmove_to(water_pos)\n\n# Place offshore pump for power system\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {offshore_pump.position}")\n\n# Place boiler with spacing for connections\nbuilding_box = BuildingBox(width=Prototype.Boiler.WIDTH + 4, height=Prototype.Boiler.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.Boiler, building_box, offshore_pump.position)\nmove_to(coords.center)\nboiler = place_entity(Prototype.Boiler, position=coords.center)\nprint(f"Placed boiler at {boiler.position}")\n\n# Place steam engine\nbuilding_box = BuildingBox(width=Prototype.SteamEngine.WIDTH + 4, height=Prototype.SteamEngine.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.SteamEngine, building_box, boiler.position)\nmove_to(coords.center)\nsteam_engine = place_entity(Prototype.SteamEngine, position=coords.center)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect water system\nwater_pipes = connect_entities(offshore_pump, boiler, Prototype.Pipe)\nsteam_pipes = connect_entities(boiler, steam_engine, Prototype.Pipe)\n\n# Add fuel to boiler\nboiler = insert_item(Prototype.Coal, boiler, 50)\n\n# Wait for power generation to stabilize\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")\n'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
       # print(result)

        test_string_1 = '# First connect power poles to steam engine\nmove_to(steam_engine.position)\npower_pole = place_entity_next_to(Prototype.SmallElectricPole, \n                                 steam_engine.position,\n                                 direction=Direction.RIGHT,\n                                 spacing=1)\nprint(f"Added power pole at {power_pole.position}")\n\n# Find another water spot for sulfur production\nwater_pos = nearest(Resource.Water)\nmove_to(water_pos)\n\n# Place second offshore pump\nsulfur_pump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed second offshore pump for sulfur production at {sulfur_pump.position}")\n\n# Place storage tank for water with spacing for connections\nbuilding_box = BuildingBox(width=Prototype.StorageTank.WIDTH + 4, height=Prototype.StorageTank.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.StorageTank, building_box, sulfur_pump.position)\nmove_to(coords.center)\nwater_tank = place_entity(Prototype.StorageTank, position=coords.center)\nprint(f"Placed water storage tank at {water_tank.position}")\n\n# Connect water pump to storage tank\nwater_pipes = connect_entities(sulfur_pump, water_tank, {Prototype.Pipe, Prototype.UndergroundPipe})\nprint(f"Connected water system from pump to storage tank")\n\n# Wait for water to flow\nsleep(5)\n\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)


        test_string_1 = '# Find crude oil patch\noil_pos = nearest(Resource.CrudeOil)\nmove_to(oil_pos)\n\n# Place pumpjack\npumpjack = place_entity(Prototype.PumpJack, position=oil_pos)\nprint(f"Placed pumpjack at {pumpjack.position}")\n\n# Connect pumpjack to power\npoles = connect_entities(power_pole, pumpjack, Prototype.SmallElectricPole)\nprint(f"Connected pumpjack to power network")\n\n# Place oil refinery with space for connections\n# Put it 20 spaces south of pumpjack\nrefinery_pos = Position(x=pumpjack.position.x, y=pumpjack.position.y + 20)\nbuilding_box = BuildingBox(width=Prototype.OilRefinery.WIDTH + 4, height=Prototype.OilRefinery.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.OilRefinery, building_box, refinery_pos)\nmove_to(coords.center)\n\nrefinery = place_entity(Prototype.OilRefinery, position=coords.center)\nprint(f"Placed oil refinery at {refinery.position}")\n\n# Set recipe to basic oil processing\nrefinery = set_entity_recipe(refinery, RecipeName.BasicOilProcessing)\nprint(f"Set refinery recipe to basic oil processing")\n\n# Connect refinery to power\npoles = connect_entities(power_pole, refinery, Prototype.SmallElectricPole)\nprint(f"Connected refinery to power network")\n\n# Place petroleum gas storage tank\nbuilding_box = BuildingBox(width=Prototype.StorageTank.WIDTH + 4, height=Prototype.StorageTank.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.StorageTank, building_box, refinery.position)\nmove_to(coords.center)\n\ngas_tank = place_entity(Prototype.StorageTank, position=coords.center)\nprint(f"Placed petroleum gas storage tank at {gas_tank.position}")\n\n# Connect pumpjack to refinery\npipes = connect_entities(pumpjack, refinery, {Prototype.Pipe, Prototype.UndergroundPipe})\nprint(f"Connected pumpjack to refinery")\n\n# Connect refinery to gas storage tank\npipes = connect_entities(refinery, gas_tank, {Prototype.Pipe, Prototype.UndergroundPipe})\nprint(f"Connected refinery to gas storage tank")\n\n# Wait for oil processing to start\nsleep(5)\n\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)

        test_string_1 = '# First fix power connection by creating a new connection from steam engine\nmove_to(steam_engine.position)\n# Create fresh power connection to pumpjack and refinery\npoles = connect_entities(steam_engine, pumpjack, Prototype.SmallElectricPole)\npoles = connect_entities(steam_engine, refinery, Prototype.SmallElectricPole)\nprint(f"Reconnected power to oil processing system")\n\n# Now set up iron plate production\n# Find iron ore\niron_pos = nearest(Resource.IronOre)\nmove_to(iron_pos)\n\n# Place electric mining drill\ndrill = place_entity(Prototype.ElectricMiningDrill, position=iron_pos, direction=Direction.DOWN)\nprint(f"Placed electric mining drill at {drill.position}")\n\n# Connect drill to power\npoles = connect_entities(steam_engine, drill, Prototype.SmallElectricPole)\nprint(f"Connected mining drill to power")\n\n# Place furnace below drill\nfurnace = place_entity_next_to(Prototype.ElectricFurnace, \n                              reference_position=drill.position,\n                              direction=Direction.DOWN,\n                              spacing=1)\nprint(f"Placed electric furnace at {furnace.position}")\n\n# Connect furnace to power\npoles = connect_entities(steam_engine, furnace, Prototype.SmallElectricPole)\nprint(f"Connected furnace to power")\n\n# Place storage tank for iron plates\niron_chest = place_entity_next_to(Prototype.WoodenChest,\n                                 reference_position=furnace.position,\n                                 direction=Direction.DOWN,\n                                 spacing=1)\nprint(f"Placed iron plate storage chest at {iron_chest.position}")\n\n# Add inserters\ninput_inserter = place_entity_next_to(Prototype.Inserter,\n                                     reference_position=drill.position,\n                                     direction=Direction.DOWN,\n                                     spacing=0)\nprint(f"Placed input inserter at {input_inserter.position}")\n\noutput_inserter = place_entity_next_to(Prototype.Inserter,\n                                      reference_position=furnace.position,\n                                      direction=Direction.DOWN,\n                                      spacing=0)\nprint(f"Placed output inserter at {output_inserter.position}")\n\n# Wait for system to start working\nsleep(5)\n\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)


        test_string_1 = '# First clean up existing setup\nmove_to(drill.position)\npickup_entity(drill)\npickup_entity(furnace)\npickup_entity(iron_chest)\n\n# Rebuild iron smelting with proper spacing\n# Place drill first\nmove_to(iron_pos)\ndrill = place_entity(Prototype.ElectricMiningDrill, position=iron_pos, direction=Direction.DOWN)\nprint(f"Placed electric mining drill at {drill.position}")\n\n# Place furnace with more spacing\nfurnace = place_entity_next_to(Prototype.ElectricFurnace, \n                              reference_position=drill.position,\n                              direction=Direction.DOWN,\n                              spacing=2)\nprint(f"Placed electric furnace at {furnace.position}")\n\n# Now add inserters with correct spacing\ninput_inserter = place_entity_next_to(Prototype.Inserter,\n                                     reference_position=drill.position,\n                                     direction=Direction.DOWN,\n                                     spacing=1)\nprint(f"Placed input inserter at {input_inserter.position}")\n\noutput_inserter = place_entity_next_to(Prototype.Inserter,\n                                      reference_position=furnace.position,\n                                      direction=Direction.DOWN,\n                                      spacing=1)\nprint(f"Placed output inserter at {output_inserter.position}")\n\n# Add output chest\niron_chest = place_entity_next_to(Prototype.WoodenChest,\n                                 reference_position=output_inserter.position,\n                                 direction=Direction.DOWN,\n                                 spacing=1)\nprint(f"Placed iron plate storage chest at {iron_chest.position}")\n\n# Connect everything to power\npoles = connect_entities(steam_engine, drill, Prototype.SmallElectricPole)\npoles = connect_entities(steam_engine, furnace, Prototype.SmallElectricPole)\nprint(f"Connected iron smelting to power")\n\n# Fix pumpjack power connection\npoles = connect_entities(steam_engine, pumpjack, Prototype.SmallElectricPole)\nprint(f"Reconnected pumpjack to power")\n\n# Wait for systems to start working\nsleep(5)\n\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = '# First add coal to boiler\nmove_to(boiler.position)\nboiler = insert_item(Prototype.Coal, boiler, 50)\nprint(f"Added coal to boiler")\n\n# Fix power connection to output inserter\npoles = connect_entities(steam_engine, output_inserter, Prototype.SmallElectricPole)\nprint(f"Connected output inserter to power")\n\n# Now let\'s set up the chemical plant for sulfur production\n# Place it between iron production and petroleum gas storage\nchemical_plant_pos = Position(x=gas_tank.position.x - 10, y=gas_tank.position.y)\nbuilding_box = BuildingBox(width=Prototype.ChemicalPlant.WIDTH + 4, height=Prototype.ChemicalPlant.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.ChemicalPlant, building_box, chemical_plant_pos)\nmove_to(coords.center)\n\n# Place and set up chemical plant\nchemical_plant = place_entity(Prototype.ChemicalPlant, position=coords.center)\nprint(f"Placed chemical plant at {chemical_plant.position}")\n\n# Set recipe to sulfur\nchemical_plant = set_entity_recipe(chemical_plant, Prototype.Sulfur)\nprint(f"Set chemical plant recipe to sulfur")\n\n# Connect to power\npoles = connect_entities(steam_engine, chemical_plant, Prototype.SmallElectricPole)\nprint(f"Connected chemical plant to power")\n\n# Connect water storage tank to chemical plant\npipes = connect_entities(water_tank, chemical_plant, {Prototype.Pipe, Prototype.UndergroundPipe})\nprint(f"Connected water to chemical plant")\n\n# Connect petroleum gas tank to chemical plant\npipes = connect_entities(gas_tank, chemical_plant, {Prototype.Pipe, Prototype.UndergroundPipe})\nprint(f"Connected petroleum gas to chemical plant")\n\n# Add output chest for sulfur\nsulfur_chest = place_entity_next_to(Prototype.WoodenChest,\n                                   reference_position=chemical_plant.position,\n                                   direction=Direction.RIGHT,\n                                   spacing=1)\nprint(f"Placed sulfur output chest at {sulfur_chest.position}")\n\n# Add output inserter\nsulfur_inserter = place_entity_next_to(Prototype.Inserter,\n                                      reference_position=chemical_plant.position,\n                                      direction=Direction.RIGHT,\n                                      spacing=0)\nprint(f"Placed sulfur output inserter at {sulfur_inserter.position}")\n\n# Connect inserter to power\npoles = connect_entities(steam_engine, sulfur_inserter, Prototype.SmallElectricPole)\nprint(f"Connected sulfur inserter to power")\n\n# Wait for system to start working\nsleep(5)\n\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


        test_string_1 = '# First create a comprehensive power network from steam engine\nmove_to(steam_engine.position)\n# Create fresh power connections to everything\npoles = connect_entities(steam_engine, pumpjack, Prototype.SmallElectricPole)\npoles = connect_entities(steam_engine, refinery, Prototype.SmallElectricPole)\npoles = connect_entities(steam_engine, chemical_plant, Prototype.SmallElectricPole)\npoles = connect_entities(steam_engine, drill, Prototype.SmallElectricPole)\npoles = connect_entities(steam_engine, furnace, Prototype.SmallElectricPole)\nprint(f"Rebuilt power network connections")\n\n# Fix iron plate backup - first clear the furnace\nmove_to(furnace.position)\nextract_item(Prototype.IronPlate, furnace, quantity=100)\nprint(f"Cleared iron plate backup from furnace")\n\n# Fix oil production - reconnect pumpjack to refinery\npipes = connect_entities(pumpjack, refinery, {Prototype.Pipe, Prototype.UndergroundPipe})\nprint(f"Reconnected oil production pipeline")\n\n# Wait for petroleum gas production\nprint(f"Waiting for petroleum gas production...")\nsleep(15)\n\n# Now try connecting chemical plant to petroleum gas\nmove_to(chemical_plant.position)\npipes = connect_entities(gas_tank, chemical_plant, {Prototype.Pipe, Prototype.UndergroundPipe})\nprint(f"Connected petroleum gas to chemical plant")\n\n# Add output chest and inserter for sulfur if not already placed\nsulfur_chest = place_entity_next_to(Prototype.WoodenChest,\n                                   reference_position=chemical_plant.position,\n                                   direction=Direction.RIGHT,\n                                   spacing=1)\nprint(f"Placed sulfur output chest at {sulfur_chest.position}")\n\nsulfur_inserter = place_entity_next_to(Prototype.Inserter,\n                                      reference_position=chemical_plant.position,\n                                      direction=Direction.RIGHT,\n                                      spacing=0)\nprint(f"Placed sulfur output inserter at {sulfur_inserter.position}")\n\n# Connect sulfur inserter to power\npoles = connect_entities(steam_engine, sulfur_inserter, Prototype.SmallElectricPole)\nprint(f"Connected sulfur inserter to power")\n\n# Wait for system to start working\nsleep(10)\n\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = '# First fix the oil production chain\nmove_to(refinery.position)\n# Set recipe again to ensure it\'s set\nrefinery = set_entity_recipe(refinery, RecipeName.BasicOilProcessing)\nprint(f"Reset refinery recipe to basic oil processing")\n\n# Now connect pumpjack to refinery\npipes = connect_entities(pumpjack, refinery, {Prototype.Pipe, Prototype.UndergroundPipe})\nprint(f"Connected pumpjack to refinery")\n\n# Clear iron plate backup from furnace and chest\nmove_to(furnace.position)\nextract_item(Prototype.IronPlate, furnace, quantity=100)\nprint(f"Cleared iron plate backup from furnace")\n\n# Fix iron plate output\nmove_to(iron_chest.position)\n# Remove existing inserter that might be blocked\npickup_entity(output_inserter)\n\n# Place new output inserter\noutput_inserter = place_entity_next_to(Prototype.Inserter,\n                                      reference_position=furnace.position,\n                                      direction=Direction.DOWN,\n                                      spacing=1)\nprint(f"Replaced output inserter")\n\n# Wait for oil production to start\nprint(f"Waiting for petroleum gas production...")\nsleep(15)\n\n# Now try connecting chemical plant to gas storage tank\nmove_to(chemical_plant.position)\npipes = connect_entities(gas_tank, chemical_plant, {Prototype.Pipe, Prototype.UndergroundPipe})\nprint(f"Connected petroleum gas to chemical plant")\n\n# Add output chest and inserter for sulfur if not already placed\nsulfur_chest = place_entity_next_to(Prototype.WoodenChest,\n                                   reference_position=chemical_plant.position,\n                                   direction=Direction.RIGHT,\n                                   spacing=1)\nprint(f"Placed sulfur output chest at {sulfur_chest.position}")\n\nsulfur_inserter = place_entity_next_to(Prototype.Inserter,\n                                      reference_position=chemical_plant.position,\n                                      direction=Direction.RIGHT,\n                                      spacing=0)\nprint(f"Placed sulfur output inserter at {sulfur_inserter.position}")\n\n# Connect sulfur inserter to power\npoles = connect_entities(steam_engine, sulfur_inserter, Prototype.SmallElectricPole)\nprint(f"Connected sulfur inserter to power")\n\n# Wait for system to start working\nsleep(10)\n\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


def test_error_pattern_58(): # DEMO
        from env.src.game_types import Prototype, Resource, Direction, Position, BuildingBox   
        
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 50, "wooden-chest": 10, "burner-inserter": 50,"inserter": 50, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 2, "offshore-pump": 2, "steam-engine": 2,
                                "electric-mining-drill": 50, "small-electric-pole": 500, "pipe": 500,
                                "assembling-machine-2": 10, "electric-furnace": 10, "pipe-to-ground": 100, "underground-belt": 100,
                                "pumpjack": 10, "oil-refinery": 5, "chemical-plant": 5, "storage-tank": 10,
                                #"solar-panel": 50,
                                }
        
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        #test_string_1 = 'refinery_pos = Position(x=47.5, y=49.5)\nmove_to(refinery_pos)\nrefinery = place_entity(Prototype.OilRefinery, position=refinery_pos)\nprint(f"Placed oil refinery at {refinery.position}")\n\n# Set recipe to basic oil processing\nrefinery = set_entity_recipe(refinery, RecipeName.BasicOilProcessing)\nprint(f"Set refinery recipe to basic oil processing")\ntank_pos = Position(x=57.5, y=49.5)\nmove_to(tank_pos)\nstorage_tank = place_entity(Prototype.StorageTank, position=tank_pos)\nprint(f"Placed storage tank at {storage_tank.position}")\n\n# Connect refinery to storage tank\npipes = connect_entities(refinery, storage_tank, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected refinery to storage tank")\n\n# Wait to check if everything is powered and connected\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)
        
        test_string_1 = '# First find water for power generation\nwater_pos = nearest(Resource.Water)\nprint(f"Found water at {water_pos}")\n\n# Place offshore pump\nmove_to(water_pos)\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {offshore_pump.position}")\n\n# Place boiler with space for connections\nbuilding_box = BuildingBox(width=Prototype.Boiler.WIDTH + 4, height=Prototype.Boiler.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.Boiler, building_box, offshore_pump.position)\nmove_to(coords.center)\nboiler = place_entity(Prototype.Boiler, position=coords.center)\nprint(f"Placed boiler at {boiler.position}")\n\n# Place steam engine\nbuilding_box = BuildingBox(width=Prototype.SteamEngine.WIDTH + 4, height=Prototype.SteamEngine.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.SteamEngine, building_box, boiler.position)\nmove_to(coords.center)\nsteam_engine = place_entity(Prototype.SteamEngine, position=coords.center)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect water system\nwater_pipes = connect_entities(offshore_pump, boiler, Prototype.Pipe)\nsteam_pipes = connect_entities(boiler, steam_engine, Prototype.Pipe)\nprint(f"Connected water and steam pipes")\n\n# Add fuel to boiler\nboiler = insert_item(Prototype.Coal, boiler, 50)\nprint(f"Added coal to boiler")\n\n# Wait for power generation\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")\n'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        #test_string_1 = '# First move to oil position\noil_pos = nearest(Resource.CrudeOil)\nmove_to(oil_pos)\nprint(f"Moved to oil at {oil_pos}")\n\n# Use larger building box for pumpjack\nbuilding_box = BuildingBox(width=Prototype.PumpJack.WIDTH + 8, height=Prototype.PumpJack.HEIGHT + 8)\ncoords = nearest_buildable(Prototype.PumpJack, building_box, oil_pos)\nmove_to(coords.center)\npumpjack = place_entity(Prototype.PumpJack, position=coords.center)\nprint(f"Placed pumpjack at {pumpjack.position}")\n\n# Connect power to pumpjack\npoles = connect_entities(steam_engine, pumpjack, Prototype.SmallElectricPole)\nprint(f"Connected power to pumpjack")\n\n# Place oil refinery with space for connections\n# Put it 20 spaces east of pumpjack to avoid water\nrefinery_pos = Position(x=pumpjack.position.x + 20, y=pumpjack.position.y)\nbuilding_box = BuildingBox(width=Prototype.OilRefinery.WIDTH + 8, height=Prototype.OilRefinery.HEIGHT + 8)\ncoords = nearest_buildable(Prototype.OilRefinery, building_box, refinery_pos)\nmove_to(coords.center)\nrefinery = place_entity(Prototype.OilRefinery, position=coords.center)\nprint(f"Placed oil refinery at {refinery.position}")\n\n# Set recipe to basic oil processing\nrefinery = set_entity_recipe(refinery, RecipeName.BasicOilProcessing)\nprint(f"Set refinery recipe to basic oil processing")\n\n# Connect power to refinery\npoles = connect_entities(pumpjack, refinery, Prototype.SmallElectricPole)\nprint(f"Connected power to refinery")\n\n# Connect pumpjack to refinery with pipes\npipes = connect_entities(pumpjack, refinery, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected pumpjack to refinery with pipes")\n\n# Place storage tank for petroleum gas output\ntank_pos = Position(x=refinery.position.x + 10, y=refinery.position.y)\nbuilding_box = BuildingBox(width=Prototype.StorageTank.WIDTH + 4, height=Prototype.StorageTank.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.StorageTank, building_box, tank_pos)\nmove_to(coords.center)\nstorage_tank = place_entity(Prototype.StorageTank, position=coords.center)\nprint(f"Placed storage tank at {storage_tank.position}")\n\n# Connect refinery to storage tank\npipes = connect_entities(refinery, storage_tank, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected refinery to storage tank")\n\n# Wait to check if everything is powered and connected\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)

        #test_string_1 = '# First move to oil position\noil_pos = nearest(Resource.CrudeOil)\nmove_to(oil_pos)\nprint(f"Moved to oil at {oil_pos}")\n\n# Use larger building box for pumpjack\nbuilding_box = BuildingBox(width=Prototype.PumpJack.WIDTH + 8, height=Prototype.PumpJack.HEIGHT + 8)\ncoords = nearest_buildable(Prototype.PumpJack, building_box, oil_pos)\nmove_to(coords.center)\npumpjack = place_entity(Prototype.PumpJack, position=coords.center)\nprint(f"Placed pumpjack at {pumpjack.position}")\n\n# Connect power to pumpjack\npoles = connect_entities(steam_engine, pumpjack, Prototype.SmallElectricPole)\nprint(f"Connected power to pumpjack")\n\n# Place oil refinery with space for connections\n# Put it 20 spaces east of pumpjack to avoid water\nrefinery_pos = Position(x=pumpjack.position.x + 20, y=pumpjack.position.y)\nbuilding_box = BuildingBox(width=Prototype.OilRefinery.WIDTH + 8, height=Prototype.OilRefinery.HEIGHT + 8)\ncoords = nearest_buildable(Prototype.OilRefinery, building_box, refinery_pos)\nmove_to(coords.center)\nrefinery = place_entity(Prototype.OilRefinery, position=coords.center)\nprint(f"Placed oil refinery at {refinery.position}")\n\n# Set recipe to basic oil processing\nrefinery = set_entity_recipe(refinery, RecipeName.BasicOilProcessing)\nprint(f"Set refinery recipe to basic oil processing")\n\n# Connect power to refinery\npoles = connect_entities(pumpjack, refinery, Prototype.SmallElectricPole)\nprint(f"Connected power to refinery")\n\n# Connect pumpjack to refinery with pipes\npipes = connect_entities(pumpjack, refinery, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected pumpjack to refinery with pipes")\n\n# Place storage tank for petroleum gas output\ntank_pos = Position(x=refinery.position.x + 10, y=refinery.position.y)\nbuilding_box = BuildingBox(width=Prototype.StorageTank.WIDTH + 4, height=Prototype.StorageTank.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.StorageTank, building_box, tank_pos)\nmove_to(coords.center)\nstorage_tank = place_entity(Prototype.StorageTank, position=coords.center)\nprint(f"Placed storage tank at {storage_tank.position}")\n\n# Connect refinery to storage tank\npipes = connect_entities(refinery, storage_tank, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected refinery to storage tank")\n\n# Wait to check if everything is powered and connected\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)

        #test_string_1 = '# Move to oil and place pumpjack directly\noil_pos = nearest(Resource.CrudeOil)\nmove_to(oil_pos)\npumpjack = place_entity(Prototype.PumpJack, position=oil_pos)\nprint(f"Placed pumpjack at {pumpjack.position}")\n\n# Connect power to pumpjack\npoles = connect_entities(steam_engine, pumpjack, Prototype.SmallElectricPole)\nprint(f"Connected power to pumpjack")\n\n# Place oil refinery 15 spaces east of pumpjack\nrefinery_pos = Position(x=pumpjack.position.x + 15, y=pumpjack.position.y)\nmove_to(refinery_pos)\nrefinery = place_entity(Prototype.OilRefinery, position=refinery_pos)\nprint(f"Placed oil refinery at {refinery.position}")\n\n# Set recipe to basic oil processing\nrefinery = set_entity_recipe(refinery, RecipeName.BasicOilProcessing)\nprint(f"Set refinery recipe to basic oil processing")\n\n# Connect power to refinery\npoles = connect_entities(pumpjack, refinery, Prototype.SmallElectricPole)\nprint(f"Connected power to refinery")\n\n# Connect pumpjack to refinery with pipes\npipes = connect_entities(pumpjack, refinery, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected pumpjack to refinery with pipes")\n\n# Place storage tank for petroleum gas output\n# Place it 10 spaces east of refinery\ntank_pos = Position(x=refinery.position.x + 10, y=refinery.position.y)\nmove_to(tank_pos)\nstorage_tank = place_entity(Prototype.StorageTank, position=tank_pos)\nprint(f"Placed storage tank at {storage_tank.position}")\n\n# Connect refinery to storage tank\npipes = connect_entities(refinery, storage_tank, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected refinery to storage tank")\n\n# Wait to check if everything is powered and connected\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)

        test_string_1 = '# Move to oil and place pumpjack directly\njack_pos = Position(x=32.5 ,y=49.5)\nmove_to(jack_pos)\npumpjack = place_entity(Prototype.PumpJack, position=jack_pos)\nprint(f"Placed pumpjack at {pumpjack.position}")\n\n# Connect power to pumpjack\npoles = connect_entities(steam_engine, pumpjack, Prototype.SmallElectricPole)\nprint(f"Connected power to pumpjack")\n\n# Place oil refinery 15 spaces east of pumpjack\nrefinery_pos = Position(x=pumpjack.position.x + 15, y=pumpjack.position.y)\nmove_to(refinery_pos)\nrefinery = place_entity(Prototype.OilRefinery, position=refinery_pos)\nprint(f"Placed oil refinery at {refinery.position}")\n\n# Set recipe to basic oil processing\nrefinery = set_entity_recipe(refinery, RecipeName.BasicOilProcessing)\nprint(f"Set refinery recipe to basic oil processing")\n\n# Connect power to refinery\npoles = connect_entities(pumpjack, refinery, Prototype.SmallElectricPole)\nprint(f"Connected power to refinery")\n\n# Connect pumpjack to refinery with pipes\npipes = connect_entities(pumpjack, refinery, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected pumpjack to refinery with pipes")\n\n# Place storage tank for petroleum gas output\n# Place it 10 spaces east of refinery\ntank_pos = Position(x=refinery.position.x + 10, y=refinery.position.y)\nmove_to(tank_pos)\nstorage_tank = place_entity(Prototype.StorageTank, position=tank_pos)\nprint(f"Placed storage tank at {storage_tank.position}")\n\n# Connect refinery to storage tank\npipes = connect_entities(refinery, storage_tank, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected refinery to storage tank")\n\n# Wait to check if everything is powered and connected\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


        test_string_1 = '# First fix refinery power by adding more poles\npoles = connect_entities(steam_engine, refinery, Prototype.SmallElectricPole)\nprint(f"Reconnected power to refinery")\n\n# Reconnect storage tank to refinery using regular pipes only first\n# Remove old storage tank\npickup_entity(storage_tank)\n# Place it closer to refinery\ntank_pos = Position(x=refinery.position.x + 5, y=refinery.position.y - 5)\nmove_to(tank_pos)\nstorage_tank = place_entity(Prototype.StorageTank, position=tank_pos)\nprint(f"Replaced storage tank at {storage_tank.position}")\n\n# Connect with regular pipes\npipes = connect_entities(refinery, storage_tank, Prototype.Pipe)\nprint(f"Connected refinery to storage tank")\n\n# Now let\'s set up the sulfur production\n# Place chemical plant for sulfur 15 spaces east of storage tank\nchem_pos = Position(x=storage_tank.position.x + 15, y=storage_tank.position.y)\nmove_to(chem_pos)\nchemical_plant = place_entity(Prototype.ChemicalPlant, position=chem_pos)\nprint(f"Placed chemical plant at {chemical_plant.position}")\n\n# Set recipe to sulfur\nchemical_plant = set_entity_recipe(chemical_plant, Prototype.Sulfur)\nprint(f"Set chemical plant recipe to sulfur")\n\n# Connect power to chemical plant\npoles = connect_entities(refinery, chemical_plant, Prototype.SmallElectricPole)\nprint(f"Connected power to chemical plant")\n\n# Connect petroleum gas from storage tank to chemical plant\npipes = connect_entities(storage_tank, chemical_plant, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected storage tank to chemical plant")\n\n# Find water for sulfur production\nwater_pos = nearest(Resource.Water)\nmove_to(water_pos)\nwater_pump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed water pump at {water_pump.position}")\n\n# Connect water to chemical plant\npipes = connect_entities(water_pump, chemical_plant, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected water to chemical plant")\n\n# Place chest for sulfur output\nchest_pos = Position(x=chemical_plant.position.x + 3, y=chemical_plant.position.y)\nmove_to(chest_pos)\noutput_chest = place_entity(Prototype.WoodenChest, position=chest_pos)\nprint(f"Placed output chest at {output_chest.position}")\n\n# Add inserter to move sulfur to chest\ninserter = place_entity_next_to(Prototype.Inserter, chemical_plant.position, Direction.RIGHT, spacing=0)\nprint(f"Placed output inserter at {inserter.position}")\n\n# Wait to check if everything is working\nsleep(10)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = '# First remove the incorrectly placed storage tank\npickup_entity(storage_tank)\n\n# Place storage tank near refinery\'s petroleum gas output point\n# The refinery\'s petroleum gas output is at (34.5, 37.5)\ntank_pos = Position(x=34.5, y=34.5)  # 3 tiles above output\nmove_to(tank_pos)\nstorage_tank = place_entity(Prototype.StorageTank, position=tank_pos)\nprint(f"Placed storage tank at {storage_tank.position}")\n\n# Connect refinery petroleum gas output to storage tank using specific connection points\npipes = connect_entities(\n    Position(x=34.5, y=37.5),  # Refinery petroleum gas output\n    storage_tank,\n    Prototype.Pipe\n)\nprint(f"Connected refinery petroleum gas output to storage tank")\n\n# Now let\'s set up the sulfur production\n# Place chemical plant for sulfur 10 spaces east of storage tank\nchem_pos = Position(x=storage_tank.position.x + 10, y=storage_tank.position.y)\nmove_to(chem_pos)\nchemical_plant = place_entity(Prototype.ChemicalPlant, position=chem_pos)\nprint(f"Placed chemical plant at {chemical_plant.position}")\n\n# Set recipe to sulfur\nchemical_plant = set_entity_recipe(chemical_plant, Prototype.Sulfur)\nprint(f"Set chemical plant recipe to sulfur")\n\n# Connect power to chemical plant\npoles = connect_entities(refinery, chemical_plant, Prototype.SmallElectricPole)\nprint(f"Connected power to chemical plant")\n\n# Find water for sulfur production\nwater_pos = nearest(Resource.Water)\nmove_to(water_pos)\nsulfur_water_pump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed water pump for sulfur at {sulfur_water_pump.position}")\n\n# Connect water to chemical plant\npipes = connect_entities(sulfur_water_pump, chemical_plant, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected water to chemical plant")\n\n# Connect petroleum gas from storage tank to chemical plant\npipes = connect_entities(storage_tank, chemical_plant, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected storage tank to chemical plant")\n\n# Place chest for sulfur output\nchest_pos = Position(x=chemical_plant.position.x + 3, y=chemical_plant.position.y)\nmove_to(chest_pos)\noutput_chest = place_entity(Prototype.WoodenChest, position=chest_pos)\nprint(f"Placed output chest at {output_chest.position}")\n\n# Add inserter to move sulfur to chest\ninserter = place_entity_next_to(Prototype.Inserter, chemical_plant.position, Direction.RIGHT, spacing=0)\nprint(f"Placed output inserter at {inserter.position}")\n\n# Wait to check if everything is working\nsleep(10)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


        test_string_1 = '# First let\'s place the storage tank in a better position relative to refinery\'s output point\n# The refinery\'s petroleum gas output is at (34.5, 37.5)\ntank_pos = Position(x=34.5, y=32.5)  # 5 tiles above output to leave room for pipes\nmove_to(tank_pos)\nstorage_tank = place_entity(Prototype.StorageTank, position=tank_pos, direction=Direction.RIGHT)\nprint(f"Placed storage tank at {storage_tank.position}")\n\n# Connect refinery petroleum gas output to storage tank with pipes\npipes = connect_entities(\n    Position(x=34.5, y=37.5),  # Refinery petroleum gas output position\n    storage_tank,\n    Prototype.Pipe\n)\nprint(f"Connected refinery petroleum gas output to storage tank")\n\n# Now let\'s set up the sulfur production\n# Place chemical plant 10 spaces east of storage tank\nchem_pos = Position(x=storage_tank.position.x + 10, y=storage_tank.position.y)\nmove_to(chem_pos)\nchemical_plant = place_entity(Prototype.ChemicalPlant, position=chem_pos)\nprint(f"Placed chemical plant at {chemical_plant.position}")\n\n# Set recipe to sulfur\nchemical_plant = set_entity_recipe(chemical_plant, Prototype.Sulfur)\nprint(f"Set chemical plant recipe to sulfur")\n\n# Connect power to chemical plant\npoles = connect_entities(refinery, chemical_plant, Prototype.SmallElectricPole)\nprint(f"Connected power to chemical plant")\n\n# Find water for sulfur production - use a different water position than power system\nwater_pos = Position(x=-11.0, y=5.0)  # Different position than first water pump\nmove_to(water_pos)\nsulfur_water_pump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed water pump for sulfur at {sulfur_water_pump.position}")\n\n# Connect water to chemical plant\npipes = connect_entities(sulfur_water_pump, chemical_plant, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected water to chemical plant")\n\n# Connect petroleum gas from storage tank to chemical plant\npipes = connect_entities(storage_tank, chemical_plant, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected storage tank to chemical plant")\n\n# Place chest for sulfur output\nchest_pos = Position(x=chemical_plant.position.x + 3, y=chemical_plant.position.y)\nmove_to(chest_pos)\noutput_chest = place_entity(Prototype.WoodenChest, position=chest_pos)\nprint(f"Placed output chest at {output_chest.position}")\n\n# Add inserter to move sulfur to chest\ninserter = place_entity_next_to(Prototype.Inserter, chemical_plant.position, Direction.RIGHT, spacing=0)\nprint(f"Placed output inserter at {inserter.position}")\n\n# Add coal back to boiler as it\'s out of fuel\nmove_to(Position(x=-4.5, y=3.0))  # Boiler position\nboiler = get_entity(Prototype.Boiler, Position(x=-4.5, y=3.0))\nboiler = insert_item(Prototype.Coal, boiler, 50)\nprint(f"Added coal to boiler")\n\n# Wait to check if everything is working\nsleep(10)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)

        test_string_1 = '# First fix power generation\n# Add coal to boiler\nmove_to(Position(x=-4.5, y=3.0))\nboiler = get_entity(Prototype.Boiler, Position(x=-4.5, y=3.0))\nboiler = insert_item(Prototype.Coal, boiler, 50)\nprint(f"Added coal to boiler")\n\n# Reconnect power network\npoles = connect_entities(steam_engine, pumpjack, Prototype.SmallElectricPole)\npoles = connect_entities(pumpjack, refinery, Prototype.SmallElectricPole)\npoles = connect_entities(refinery, chemical_plant, Prototype.SmallElectricPole)\nprint(f"Rebuilt power network")\n\n# Wait for power to stabilize\nsleep(5)\n\n# Now fix fluid connections\n# Get fresh references\nrefinery = get_entity(Prototype.OilRefinery, Position(x=32.5, y=40.5))\nstorage_tank = get_entity(Prototype.StorageTank, Position(x=34.5, y=32.5))\nchemical_plant = get_entity(Prototype.ChemicalPlant, Position(x=44.5, y=32.5))\n\n# Connect petroleum gas from storage tank to chemical plant\'s specific input\n# Chemical plant needs petroleum gas in the left input\npipes = connect_entities(\n    storage_tank,\n    chemical_plant.input_connection_points[1],  # petroleum-gas input\n    {Prototype.UndergroundPipe, Prototype.Pipe}\n)\nprint(f"Connected petroleum gas to chemical plant")\n\n# Place chest for sulfur output\nchest_pos = Position(x=chemical_plant.position.x + 3, y=chemical_plant.position.y)\nmove_to(chest_pos)\noutput_chest = place_entity(Prototype.WoodenChest, position=chest_pos)\nprint(f"Placed output chest at {output_chest.position}")\n\n# Add inserter to move sulfur to chest\ninserter = place_entity_next_to(Prototype.Inserter, chemical_plant.position, Direction.RIGHT, spacing=0)\nprint(f"Placed output inserter at {inserter.position}")\n\n# Wait to check if everything is working\nsleep(10)\n\n# Get fresh references to check status\nchemical_plant = get_entity(Prototype.ChemicalPlant, chemical_plant.position)\nrefinery = get_entity(Prototype.OilRefinery, refinery.position)\nstorage_tank = get_entity(Prototype.StorageTank, storage_tank.position)\n\nprint(f"Chemical plant status: {chemical_plant.status}")\nprint(f"Refinery status: {refinery.status}")\nprint(f"Storage tank contents: {storage_tank.fluid_box}")\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


def test_error_pattern_59(): # DEMO
        from env.src.game_types import Prototype, Resource, Direction, Position, BuildingBox   
        
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 50, "wooden-chest": 10, "burner-inserter": 50,"inserter": 50, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 2, "offshore-pump": 2, "steam-engine": 2,
                                "electric-mining-drill": 50, "small-electric-pole": 500, "pipe": 500,
                                "assembling-machine-2": 10, "electric-furnace": 10, "pipe-to-ground": 100, "underground-belt": 100,
                                "pumpjack": 10, "oil-refinery": 5, "chemical-plant": 5, "storage-tank": 10,
                                #"solar-panel": 50,
                                }
        
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 


        test_string_1 = '# First move to oil position\noil_pos = nearest(Resource.CrudeOil)\nmove_to(oil_pos)\nprint(f"Moved to oil at {oil_pos}")\n\n# Use larger building box for pumpjack\nbuilding_box = BuildingBox(width=Prototype.PumpJack.WIDTH + 8, height=Prototype.PumpJack.HEIGHT + 8)\ncoords = nearest_buildable(Prototype.PumpJack, building_box, oil_pos)\nmove_to(coords.center)\npumpjack = place_entity(Prototype.PumpJack, position=coords.center)\nprint(f"Placed pumpjack at {pumpjack.position}")\n\n# Connect power to pumpjack\npoles = connect_entities(steam_engine, pumpjack, Prototype.SmallElectricPole)\nprint(f"Connected power to pumpjack")\n\n# Place oil refinery with space for connections\n# Put it 20 spaces east of pumpjack to avoid water\nrefinery_pos = Position(x=pumpjack.position.x + 20, y=pumpjack.position.y)\nbuilding_box = BuildingBox(width=Prototype.OilRefinery.WIDTH + 8, height=Prototype.OilRefinery.HEIGHT + 8)\ncoords = nearest_buildable(Prototype.OilRefinery, building_box, refinery_pos)\nmove_to(coords.center)\nrefinery = place_entity(Prototype.OilRefinery, position=coords.center)\nprint(f"Placed oil refinery at {refinery.position}")\n\n# Set recipe to basic oil processing\nrefinery = set_entity_recipe(refinery, RecipeName.BasicOilProcessing)\nprint(f"Set refinery recipe to basic oil processing")\n\n# Connect power to refinery\npoles = connect_entities(pumpjack, refinery, Prototype.SmallElectricPole)\nprint(f"Connected power to refinery")\n\n# Connect pumpjack to refinery with pipes\npipes = connect_entities(pumpjack, refinery, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected pumpjack to refinery with pipes")\n\n# Place storage tank for petroleum gas output\ntank_pos = Position(x=refinery.position.x + 10, y=refinery.position.y)\nbuilding_box = BuildingBox(width=Prototype.StorageTank.WIDTH + 4, height=Prototype.StorageTank.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.StorageTank, building_box, tank_pos)\nmove_to(coords.center)\nstorage_tank = place_entity(Prototype.StorageTank, position=coords.center)\nprint(f"Placed storage tank at {storage_tank.position}")\n\n# Connect refinery to storage tank\npipes = connect_entities(refinery, storage_tank, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected refinery to storage tank")\n\n# Wait to check if everything is powered and connected\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


def test_error_pattern_60(): # DEMO
        from env.src.game_types import Prototype, Resource, Direction, Position, BuildingBox   
        
        LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 50, "wooden-chest": 10, "burner-inserter": 50,"inserter": 50, "transport-belt": 500,
                                "stone-furnace": 10, "boiler": 2, "offshore-pump": 2, "steam-engine": 2,
                                "electric-mining-drill": 50, "small-electric-pole": 500, "pipe": 500,
                                "assembling-machine-2": 10, "electric-furnace": 10, "pipe-to-ground": 100, "underground-belt": 100,
                                "pumpjack": 10, "oil-refinery": 5, "chemical-plant": 5, "storage-tank": 10,
                                #"solar-panel": 50,
                                }
        
        instance = FactorioInstance(address='localhost',
                                bounding_box=200,
                                tcp_port=27015,
                                fast=True,
                                #cache_scripts=False,
                                inventory=LAB_PLAY_POPULATED_STARTING_INVENTORY) 

        #test_string_1 = 'refinery_pos = Position(x=47.5, y=49.5)\nmove_to(refinery_pos)\nrefinery = place_entity(Prototype.OilRefinery, position=refinery_pos)\nprint(f"Placed oil refinery at {refinery.position}")\n\n# Set recipe to basic oil processing\nrefinery = set_entity_recipe(refinery, RecipeName.BasicOilProcessing)\nprint(f"Set refinery recipe to basic oil processing")\ntank_pos = Position(x=57.5, y=49.5)\nmove_to(tank_pos)\nstorage_tank = place_entity(Prototype.StorageTank, position=tank_pos)\nprint(f"Placed storage tank at {storage_tank.position}")\n\n# Connect refinery to storage tank\npipes = connect_entities(refinery, storage_tank, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected refinery to storage tank")\n\n# Wait to check if everything is powered and connected\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)
        
        #test_string_1 = '# First find water for power generation\nwater_pos = nearest(Resource.Water)\nprint(f"Found water at {water_pos}")\n\n# Place offshore pump\nmove_to(water_pos)\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {offshore_pump.position}")\n\n# Place boiler with space for connections\nbuilding_box = BuildingBox(width=Prototype.Boiler.WIDTH + 4, height=Prototype.Boiler.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.Boiler, building_box, offshore_pump.position)\nmove_to(coords.center)\nboiler = place_entity(Prototype.Boiler, position=coords.center)\nprint(f"Placed boiler at {boiler.position}")\n\n# Place steam engine\nbuilding_box = BuildingBox(width=Prototype.SteamEngine.WIDTH + 4, height=Prototype.SteamEngine.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.SteamEngine, building_box, boiler.position)\nmove_to(coords.center)\nsteam_engine = place_entity(Prototype.SteamEngine, position=coords.center)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect water system\nwater_pipes = connect_entities(offshore_pump, boiler, Prototype.Pipe)\nsteam_pipes = connect_entities(boiler, steam_engine, Prototype.Pipe)\nprint(f"Connected water and steam pipes")\n\n# Add fuel to boiler\nboiler = insert_item(Prototype.Coal, boiler, 50)\nprint(f"Added coal to boiler")\n\n# Wait for power generation\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")\n'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)

        #test_string_1 = '# First move to oil position\noil_pos = nearest(Resource.CrudeOil)\nmove_to(oil_pos)\nprint(f"Moved to oil at {oil_pos}")\n\n# Use larger building box for pumpjack\nbuilding_box = BuildingBox(width=Prototype.PumpJack.WIDTH + 8, height=Prototype.PumpJack.HEIGHT + 8)\ncoords = nearest_buildable(Prototype.PumpJack, building_box, oil_pos)\nmove_to(coords.center)\npumpjack = place_entity(Prototype.PumpJack, position=coords.center)\nprint(f"Placed pumpjack at {pumpjack.position}")\n\n# Connect power to pumpjack\npoles = connect_entities(steam_engine, pumpjack, Prototype.SmallElectricPole)\nprint(f"Connected power to pumpjack")\n\n# Place oil refinery with space for connections\n# Put it 20 spaces east of pumpjack to avoid water\nrefinery_pos = Position(x=pumpjack.position.x + 20, y=pumpjack.position.y)\nbuilding_box = BuildingBox(width=Prototype.OilRefinery.WIDTH + 8, height=Prototype.OilRefinery.HEIGHT + 8)\ncoords = nearest_buildable(Prototype.OilRefinery, building_box, refinery_pos)\nmove_to(coords.center)\nrefinery = place_entity(Prototype.OilRefinery, position=coords.center)\nprint(f"Placed oil refinery at {refinery.position}")\n\n# Set recipe to basic oil processing\nrefinery = set_entity_recipe(refinery, RecipeName.BasicOilProcessing)\nprint(f"Set refinery recipe to basic oil processing")\n\n# Connect power to refinery\npoles = connect_entities(pumpjack, refinery, Prototype.SmallElectricPole)\nprint(f"Connected power to refinery")\n\n# Connect pumpjack to refinery with pipes\npipes = connect_entities(pumpjack, refinery, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected pumpjack to refinery with pipes")\n\n# Place storage tank for petroleum gas output\ntank_pos = Position(x=refinery.position.x + 10, y=refinery.position.y)\nbuilding_box = BuildingBox(width=Prototype.StorageTank.WIDTH + 4, height=Prototype.StorageTank.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.StorageTank, building_box, tank_pos)\nmove_to(coords.center)\nstorage_tank = place_entity(Prototype.StorageTank, position=coords.center)\nprint(f"Placed storage tank at {storage_tank.position}")\n\n# Connect refinery to storage tank\npipes = connect_entities(refinery, storage_tank, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected refinery to storage tank")\n\n# Wait to check if everything is powered and connected\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)

        #test_string_1 = '# First move to oil position\noil_pos = nearest(Resource.CrudeOil)\nmove_to(oil_pos)\nprint(f"Moved to oil at {oil_pos}")\n\n# Use larger building box for pumpjack\nbuilding_box = BuildingBox(width=Prototype.PumpJack.WIDTH + 8, height=Prototype.PumpJack.HEIGHT + 8)\ncoords = nearest_buildable(Prototype.PumpJack, building_box, oil_pos)\nmove_to(coords.center)\npumpjack = place_entity(Prototype.PumpJack, position=coords.center)\nprint(f"Placed pumpjack at {pumpjack.position}")\n\n# Connect power to pumpjack\npoles = connect_entities(steam_engine, pumpjack, Prototype.SmallElectricPole)\nprint(f"Connected power to pumpjack")\n\n# Place oil refinery with space for connections\n# Put it 20 spaces east of pumpjack to avoid water\nrefinery_pos = Position(x=pumpjack.position.x + 20, y=pumpjack.position.y)\nbuilding_box = BuildingBox(width=Prototype.OilRefinery.WIDTH + 8, height=Prototype.OilRefinery.HEIGHT + 8)\ncoords = nearest_buildable(Prototype.OilRefinery, building_box, refinery_pos)\nmove_to(coords.center)\nrefinery = place_entity(Prototype.OilRefinery, position=coords.center)\nprint(f"Placed oil refinery at {refinery.position}")\n\n# Set recipe to basic oil processing\nrefinery = set_entity_recipe(refinery, RecipeName.BasicOilProcessing)\nprint(f"Set refinery recipe to basic oil processing")\n\n# Connect power to refinery\npoles = connect_entities(pumpjack, refinery, Prototype.SmallElectricPole)\nprint(f"Connected power to refinery")\n\n# Connect pumpjack to refinery with pipes\npipes = connect_entities(pumpjack, refinery, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected pumpjack to refinery with pipes")\n\n# Place storage tank for petroleum gas output\ntank_pos = Position(x=refinery.position.x + 10, y=refinery.position.y)\nbuilding_box = BuildingBox(width=Prototype.StorageTank.WIDTH + 4, height=Prototype.StorageTank.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.StorageTank, building_box, tank_pos)\nmove_to(coords.center)\nstorage_tank = place_entity(Prototype.StorageTank, position=coords.center)\nprint(f"Placed storage tank at {storage_tank.position}")\n\n# Connect refinery to storage tank\npipes = connect_entities(refinery, storage_tank, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected refinery to storage tank")\n\n# Wait to check if everything is powered and connected\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)

        #test_string_1 = '# Move to oil and place pumpjack directly\noil_pos = nearest(Resource.CrudeOil)\nmove_to(oil_pos)\npumpjack = place_entity(Prototype.PumpJack, position=oil_pos)\nprint(f"Placed pumpjack at {pumpjack.position}")\n\n# Connect power to pumpjack\npoles = connect_entities(steam_engine, pumpjack, Prototype.SmallElectricPole)\nprint(f"Connected power to pumpjack")\n\n# Place oil refinery 15 spaces east of pumpjack\nrefinery_pos = Position(x=pumpjack.position.x + 15, y=pumpjack.position.y)\nmove_to(refinery_pos)\nrefinery = place_entity(Prototype.OilRefinery, position=refinery_pos)\nprint(f"Placed oil refinery at {refinery.position}")\n\n# Set recipe to basic oil processing\nrefinery = set_entity_recipe(refinery, RecipeName.BasicOilProcessing)\nprint(f"Set refinery recipe to basic oil processing")\n\n# Connect power to refinery\npoles = connect_entities(pumpjack, refinery, Prototype.SmallElectricPole)\nprint(f"Connected power to refinery")\n\n# Connect pumpjack to refinery with pipes\npipes = connect_entities(pumpjack, refinery, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected pumpjack to refinery with pipes")\n\n# Place storage tank for petroleum gas output\n# Place it 10 spaces east of refinery\ntank_pos = Position(x=refinery.position.x + 10, y=refinery.position.y)\nmove_to(tank_pos)\nstorage_tank = place_entity(Prototype.StorageTank, position=tank_pos)\nprint(f"Placed storage tank at {storage_tank.position}")\n\n# Connect refinery to storage tank\npipes = connect_entities(refinery, storage_tank, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected refinery to storage tank")\n\n# Wait to check if everything is powered and connected\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)
        
        test_string_1 = '# First find water for power generation\nwater_pos = nearest(Resource.Water)\nprint(f"Found water at {water_pos}")\n\n# Place offshore pump\nmove_to(water_pos)\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {offshore_pump.position}")\n# Move to oil and place pumpjack directly\njack_pos = Position(x=32.5 ,y=49.5)\nmove_to(jack_pos)\npumpjack = place_entity(Prototype.PumpJack, position=jack_pos)\nprint(f"Placed pumpjack at {pumpjack.position}")\n\n# Connect power to pumpjack\n\n# Place oil refinery 15 spaces east of pumpjack\nrefinery_pos = Position(x=pumpjack.position.x + 15, y=pumpjack.position.y)\nmove_to(refinery_pos)\nrefinery = place_entity(Prototype.OilRefinery, position=refinery_pos)\nprint(f"Placed oil refinery at {refinery.position}")\n\n# Set recipe to basic oil processing\nrefinery = set_entity_recipe(refinery, RecipeName.AdvancedOilProcessing)\nprint(f"Set refinery recipe to basic oil processing")\npipes = connect_entities(pumpjack, refinery, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected pumpjack to refinery with pipes")\npipes = connect_entities(offshore_pump, refinery, {Prototype.UndergroundPipe, Prototype.Pipe})\nprint(f"Connected pumpjack to refinery with pipes")'
        output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        print(result)


        #test_string_1 = '# First find water for power generation\nwater_pos = nearest(Resource.Water)\nprint(f"Found water at {water_pos}")\n\n# Place offshore pump\nmove_to(water_pos)\noffshore_pump = place_entity(Prototype.OffshorePump, position=water_pos)\nprint(f"Placed offshore pump at {offshore_pump.position}")\n\n# Place boiler with space for connections\nbuilding_box = BuildingBox(width=Prototype.Boiler.WIDTH + 4, height=Prototype.Boiler.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.Boiler, building_box, offshore_pump.position)\nmove_to(coords.center)\nboiler = place_entity(Prototype.Boiler, position=coords.center)\nprint(f"Placed boiler at {boiler.position}")\n\n# Place steam engine\nbuilding_box = BuildingBox(width=Prototype.SteamEngine.WIDTH + 4, height=Prototype.SteamEngine.HEIGHT + 4)\ncoords = nearest_buildable(Prototype.SteamEngine, building_box, boiler.position)\nmove_to(coords.center)\nsteam_engine = place_entity(Prototype.SteamEngine, position=coords.center)\nprint(f"Placed steam engine at {steam_engine.position}")\n\n# Connect water system\nwater_pipes = connect_entities(offshore_pump, boiler, Prototype.Pipe)\nsteam_pipes = connect_entities(boiler, steam_engine, Prototype.Pipe)\nprint(f"Connected water and steam pipes")\n\n# Add fuel to boiler\nboiler = insert_item(Prototype.Coal, boiler, 50)\nprint(f"Added coal to boiler")\n\n# Wait for power generation\nsleep(5)\nprint(f"Current inventory {inspect_inventory()}")\nprint(f"Entities on the map: {get_entities()}")\nconnect_entities(steam_engine, pumpjack, Prototype.SmallElectricPole)\nconnect_entities(pumpjack, refinery, Prototype.SmallElectricPole)'
        #output_list, result, error, achievements = eval_program_with_achievements(instance, test_string_1)
        #print(result)


if __name__ == '__main__':
        
    #unittest.main()
    #create_nonliquid_items()
    test_error_pattern_60()
    #test_achievements_38()