# Factorio Implementation Guide

## Core Systems Implementation

### 1. Resource Mining Systems

#### Self-Fueling Coal Mining System
```python
def build_coal_mining_system(coal_patch_position):
    # Define building area
    building_box = BuildingBox(width=Prototype.BurnerMiningDrill.WIDTH, height=Prototype.BurnerMiningDrill.HEIGHT + Prototype.BurnerInserter.HEIGHT + Prototype.TransportBelt.HEIGHT)  #  drill width, drill + inserter + belt height
    buildable_coords = nearest_buildable(Prototype.BurnerMiningDrill, building_box, coal_patch_position)
    
    # Place drill
    move_to(buildable_coords.center())
    drill = place_entity(Prototype.BurnerMiningDrill, 
                            position=buildable_coords.center(),
                            direction=Direction.DOWN)
    print(f"Placed BurnerMiningDrill to mine coal at {drill.position}")
    
    # Place self-fueling inserter
    inserter = place_entity_next_to(Prototype.BurnerInserter,
                                        drill.position,
                                        direction=Direction.DOWN,
                                        spacing=0)
    inserter = rotate_entity(inserter, Direction.UP)
    print(f"Placed inserter at {inserter.position} to fuel the drill")
    
    # Connect with belts
    belts = connect_entities(drill.drop_position,
                                inserter.pickup_position,
                                Prototype.TransportBelt)
    print(f"Connected drill to inserter with transport belt")
    
    # Bootstrap system
    drill = insert_item(Prototype.Coal, drill, quantity=5)
    return drill, inserter, belts
```

#### Shared Resource Mining Line
```python
def build_shared_mining_line(ore_position, num_drills=5):
    # Calculate total width needed: drill * number of drills
    # Height needs: upper drill + belt + lower drill
    building_box = BuildingBox(width=Prototype.BurnerMiningDrill.WIDTH*num_drills, height=Prototype.BurnerMiningDrill.HEIGHT * 2 + Prototype.TransportBelt.Height)
    buildable_coords = nearest_buildable(Prototype.BurnerMiningDrill, 
                                            building_box, 
                                            ore_position)
    left_top = buildable_coords.left_top
    drills = []
    
    # Place upper drill line
    for i in range(num_drills):
        drill_pos = Position(x=left_top.x + i*2, y=left_top.y)
        move_to(drill_pos)
        drill = place_entity(Prototype.BurnerMiningDrill,
                                direction=Direction.DOWN,
                                position=drill_pos)
        drills.append(drill)
        print(f"Placed upper drill {i} at {drill.position}")
        
        # Place lower drill
        bottom_drill = place_entity_next_to(Prototype.BurnerMiningDrill,
                                               direction=Direction.DOWN,
                                               reference_position=drill.position,
                                               spacing=1)
        bottom_drill = rotate_entity(bottom_drill, Direction.UP)
        drills.append(bottom_drill)
        print(f"Placed bottom drill {i} at {bottom_drill.position}")
    
    # Create shared belt line
    x_coords = [drill.drop_position.x for drill in drills]
    belt_start = Position(x=min(x_coords), y=drills[0].drop_position.y)
    belt_end = Position(x=max(x_coords), y=drills[0].drop_position.y)
    
    main_belt = connect_entities(belt_start,
                                    belt_end,
                                    Prototype.TransportBelt)
    print(f"Created shared transport belt line for drills")
    
    return drills, main_belt
```

### 2. Smelting Systems

#### Basic automatic Smelting Line
Example: Create a copper plate mining line with 3 drills
```python
# log your general idea what you will do next
print(f"I will create a single line of 3 drills to mine copper ore")
# Find space for a line of 3 miners
move_to(source_position)
# define the BuildingBox for the drill. 
# We need 3 drills so width is 3*drill.WIDTH, height is drill.HEIGHT + furnace.HEIGHT, 3 for drill, one for furnace
building_box = BuildingBox(width = 3 * Prototype.ElectricMiningDrill.WIDTH, height = Prototype.ElectricMiningDrill.HEIGHT + Prototype.StoneFurnace.HEIGHT)
# get the nearest buildable area around the source_position
buildable_coordinates = nearest_buildable(Prototype.BurnerMiningDrill, building_box, source_position)

# Place miners in a line
# we first get the leftmost coordinate of the buildingbox to start building from
left_top = buildable_coordinates.left_top
# first lets move to the left_top to ensure building
move_to(left_top)
for i in range(3):
    # we now iterate from the leftmost point towards the right
    # take steps of drill.WIDTH
    drill_pos = Position(x=left_top.x + Prototype.ElectricMiningDrill.WIDTH*i, y=left_top.y)
    # Place the drill facing down as we start from top coordinate
    drill = place_entity(Prototype.ElectricMiningDrill, position=drill_pos, direction = Direction.DOWN)
    print(f"Placed ElectricMiningDrill {i} at {drill.position} to mine copper ore")
    # place a furnace to catch the ore
    # As a furnace has 2x2 dimensions, we need to use place_entity_next_to to ensure no overlap with drill
    # We use the drill.direction as the direction, which will place it next to the drill covering the drop position 
    furnace = place_entity_next_to(Prototype.StoneFurnace, reference_position=drill.position, direction = drill.direction)
    print(f"Placed furnace at {furnace.position} to smelt the copper ore for drill {i} at {drill.position}")
```

### 3. Power Systems

**Power Infrastructure with steam engine**

Power typically involves:
-> Water Source + OffshorePump
-> Boiler (burning coal)
-> SteamEngine

IMPORTANT: We also need to be very careful and check where we can place boiler and steam engine as they cannot be on water
```python
# log your general idea what you will do next
print(f"I will create a power generation setup with a steam engine")
# Power system pattern
move_to(water_position)
# first place offshore pump on the water system
offshore_pump = place_entity(Prototype.OffshorePump, position=water_position)
print(f"Placed offshore pump to get water at {offshore_pump.position}")
# Then place the boiler close to the offshore pump
# IMPORTANT: We need to be careful as there is water nearby which is unplaceable,
# We do not know where the water is so we will use nearest_buildable for safety and place the entity at the center of the boundingbox
# We will also need to be atleast 4 tiles away from the offshore-pump and otherwise won't have room for connections. Therefore the nearest_buildable buildingbox will have width and length of added 4 so the center is 4 tiles away from all borders

# first get the width and height of a BurnerMiningDrill
print(f"Boiler width: {Prototype.Boiler.WIDTH}, height: {Prototype.Boiler.HEIGHT}") # width 3, height 2
# use the prototype width and height attributes 
# add 4 to ensure no overlap
building_box = BuildingBox(width = Prototype.Boiler.WIDTH + 4, height = Prototype.Boiler.HEIGHT + 4)

coords = nearest_buildable(Prototype.Boiler,building_box,offshore_pump.position)
# place the boiler at the centre coordinate
boiler = place_entity(Prototype.Boiler, position = coords.center)
print(f"Placed boiler to generate steam at {boiler.position}. This will be connected to the offshore pump at {offshore_pump.position}")
# add coal to boiler to start the power generation
boiler = insert_item(Prototype.Coal, boiler, 10)

# Finally we need to place the steam engine close to the boiler
# Need to add 4 again as there is water nearby and room for connections
print(f"SteamEngine width: {Prototype.SteamEngine.WIDTH}, height: {Prototype.SteamEngine.HEIGHT}") # width 5, height 3
# use the prototype width and height attributes 
# add 4 to ensure no overlap
building_box = BuildingBox(width = Prototype.SteamEngine.WIDTH + 4, height = Prototype.SteamEngine.HEIGHT + 4)

coords = nearest_buildable(Prototype.SteamEngine,bbox,boiler.position)
# move to the centre coordinate
move_to(coords.center)
# place the steam engine on the centre coordinate
steam_engine = place_entity(Prototype.SteamEngine, position = coords.center)

print(f"Placed steam_engine to generate electricity at {steam_engine.position}. This will be connected to the boiler at {boiler.position} to generate electricity")

# Connect entities in order
water_pipes = connect_entities(offshore_pump, boiler, Prototype.Pipe)
print(f"Connected offshore pump at {offshore_pump.position} to boiler at {boiler.position} with pipes {water_pipes}")
steam_pipes = connect_entities(boiler, steam_engine, Prototype.Pipe)
print(f"Connected boiler at {boiler.position} to steam_engine at {steam_engine.position} with pipes {water_pipes}")

# check that it has power
# sleep for 5 seconds to ensure flow
sleep(5)
# update the entity
steam_engine = get_entity(Prototype.SteamEngine, position = steam_engine.position)
# check that the steam engine is generating power
assert steam_engine.energy > 0, f"Steam engine is not generating power"
print(f"Steam engine at {steam_engine.position} is generating power!")
```

### 4. Automated Assembly Systems

#### Basic Assembly Line
```python
def build_assembly_line( recipe_prototype, power_source, input_belt):
    # Plan space for assembler and inserters
    building_box = BuildingBox(width=Prototype.AssemblingMachine1.WIDTH + 2*Prototype.BurnerInserter.WIDTH, height=Prototype.AssemblingMachine1.HEIGHT)
    buildable_coords = nearest_buildable(Prototype.AssemblingMachine1,
                                            building_box,
                                            input_belt.position.right(10))
    
    # Place assembling machine
    move_to(buildable_coords.center())
    assembler = place_entity(Prototype.AssemblingMachine1,
                                position=buildable_coords.center())
    print(f"Placed assembling machine at {assembler.position}")
    
    # Set recipe
    set_entity_recipe(assembler, recipe_prototype)
    
    # Add input inserter
    # place it to the right as we added to the width of the building box
    input_inserter = place_entity_next_to(Prototype.BurnerInserter,
                                              assembler.position,
                                              direction=Direction.RIGHT,
                                              spacing=0)
    # rotate it to input items into the assembling machine                                          
    input_inserter = rotate_entity(input_inserter, Direction.LEFT)
    
    # Add output inserter
    # put it on the other side of assembling machine
    output_inserter = place_entity_next_to(Prototype.BurnerInserter,
                                               assembler.position,
                                               direction=Direction.LEFT,
                                               spacing=0)
    # add coal to inserters
    output_inserter = insert_item(Prototype.Coal, output_inserter, quantity = 5)
    input_inserter = insert_item(Prototype.Coal, input_inserter, quantity = 5)
    # Connect power
    poles = connect_entities(power_source,
                         assembler,
                         Prototype.SmallElectricPole)
    print(f"Powered assembling machine at {assembler.position} with {poles}")
    # wait for 5 seconds to check power
    sleep(5)
    assembler = get_entity(Prototype.AssemblingMachine1,assembler.position)
    assert assembler.energy > 0, f"Assembling machine at {assembler.position} is not receiving power" 
    # Connect input belt
    belts = connect_entities(input_belt,
                         input_inserter,
                         Prototype.TransportBelt)
    print(f"Connected assembling machine at {assembler.position} to input belt with {belts}")
    return assembler, input_inserter, output_inserter
```

### 5. Research Systems

#### Basic Research Setup
```python
def build_research_facility( power_source):
    # Plan space for lab, chest and inserter
    building_box = BuildingBox(width=Prototype.Lab.WIDTH + Prototype.BurnerInserter.WIDTH + Prototype.WoodenChest.WIDTH, height=Prototype.Lab.HEIGHT)
    buildable_coords = nearest_buildable(Prototype.Lab,
                                            building_box,
                                            power_source.position.right(10))
    
    # Place lab
    move_to(buildable_coords.center())
    lab = place_entity(Prototype.Lab,
                          position=buildable_coords.center())
    print(f"Placed lab at {lab.position}")
    
    # Connect power
    poles = connect_entities(power_source,
                         lab,
                         Prototype.SmallElectricPole)
    print(f"Powered lab at {lab.position} with {poles}")
    # Add science pack inserter
    inserter = place_entity_next_to(Prototype.BurnerInserter,
                                        lab.position,
                                        direction=Direction.LEFT,
                                        spacing=0)
    # rotate it to input items into the lab                                          
    inserter = rotate_entity(inserter, Direction.RIGHT)
    # Place input chest
    chest = place_entity(Prototype.WoodenChest,
                                     inserter.pickup_position,
                                     direction=Direction.UP)
    print(f"Placed chest at {chest.position} to input automation packs to lab at {lab.position}")
    
    return lab, inserter, chest
```

## Key Implementation Patterns


### 1. Power Connection Verification
```python
def verify_power_connection( entity, retry_attempts=3):
    for _ in range(retry_attempts):
        sleep(5)
        entity = get_entity(entity.prototype, entity.position)
        if entity.energy > 0:
            return True
    return False
```

## Error Handling and Recovery

### 1. Entity Status Monitoring
```python
def monitor_entity_status(entity, expected_status):
    entity = get_entity(entity.prototype, entity.position)
    if entity.status != expected_status:
        print(f"Entity at {entity.position} has unexpected status: {entity.status}")
        return False
    return True
```

## Factory Expansion Patterns

### 1. Resource Network Extension
```python
def extend_resource_network(existing_belt_end, new_consumers):
    for consumer in new_consumers:
        # Add inserter for the consumer
        inserter = place_entity_next_to(Prototype.BurnerInserter,
                                           consumer.position,
                                           direction=Direction.UP,
                                           spacing=0)
        if not inserter:
            return False
        # rotate it to input items into the the new consumer                                          
        inserter = rotate_entity(inserter, Direction.RIGHT)
        # Connect the existing belt to the inserter
        branch = connect_entities(existing_belt_end,
                                     inserter,
                                     Prototype.TransportBelt)
        print(f"Connected new consumer at {consumer.position} with {branch}")
        if not branch:
            return False
    return True
```

## TIPS WHEN CREATING STRUCTURES
- When a entity has status "WAITING_FOR_SPACE_IN_DESTINATION", it means the there is no space in the drop position. For instance, a mining drill will have status WAITING_FOR_SPACE_IN_DESTINATION when the entities it mines are not being properly collected by a furnace or a chest or transported away from drop position with transport belts
- Make sure to always put enough fuel into all entities that require fuel. It's easy to mine more coal, so it's better to insert in abundance 
- Keep it simple! Minimise the usage of transport belts if you don't need them. Use chests and furnaces to catch the ore directly from drills
- Inserters put items into entities or take items away from entities. You need to add inserters when items need to be automatically put into entities like chests, assembling machines, furnaces, boilers etc. The only exception is you can put a furnace or a chest directly at drills drop position, that catches the ore directly