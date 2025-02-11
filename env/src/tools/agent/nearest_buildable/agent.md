# nearest_buildable

The `nearest_buildable` tool helps find valid positions to place entities while respecting space requirements and resource coverage. This guide explains how to use it effectively.

## Basic Usage

```python
nearest_buildable(
    entity: Prototype,
    building_box: BuildingBox,
    center_position: Position
) -> BoundingBox
```

The function returns a BoundingBox object containing buildable area coordinates.

### Parameters
- `entity`: Prototype of entity to place
- `building_box`: BuildingBox defining required area dimensions
- `center_position`: Position to search around

### Return Value
Returns a BoundingBox with these attributes:
- `left_top`: Top-left corner Position
- `right_bottom`: Bottom-right corner Position
- `left_bottom`: Bottom-left corner Position
- `right_top`: Top-right corner Position
- `center()`: Method to get center Position

## Building Box Usage

```python
# Simple 1x1 box for chests
chest_box = BuildingBox(height=1, width=1)

# 3x3 box for mining drills
drill_box = BuildingBox(height=3, width=3)

# Larger box for multiple entities
factory_box = BuildingBox(height=5, width=10)
```

## Common Use Cases

### 1. Basic Entity Placement
```python
# Find place for chest near the origin
chest_box = BuildingBox(height=Prototype.WoodenChest.HEIGHT, width=Prototype.WoodenChest.WIDTH)
buildable_area = nearest_buildable(
    Prototype.WoodenChest,
    chest_box,
    Position(x=0, y=0)
)

# Place at center of buildable area
move_to(buildable_area.center())
chest = place_entity(Prototype.WoodenChest, position=buildable_area.center())
```

### 2. Mining Drill Placement
```python
# Setup mining drill on ore patch
resource_pos = nearest(Resource.IronOre)
# Define area for drill
drill_box = BuildingBox(height=Prototype.ElectricMiningDrill.HEIGHT, width=Prototype.ElectricMiningDrill.WIDTH)

# Find buildable area
buildable_area = nearest_buildable(
    Prototype.ElectricMiningDrill,
    drill_box,
    resource_pos
)

# Place drill
move_to(buildable_area.center())
drill = place_entity(
    Prototype.ElectricMiningDrill,
    position=buildable_area.center()
)
```

### 3. Power Infrastructure
```python
# Setup boiler near a offshore_pump
# assume a offshore pump exists at Position(15,8)
offshore_pump = get_entity(Prototype.OffshorePump, Position(x = 15, y = 8))
# add 4 to ensure no overlap
building_box = BuildingBox(width = Prototype.Boiler.WIDTH + 4, height = Prototype.Boiler.HEIGHT + 4)

coords = nearest_buildable(Prototype.Boiler, building_box, offshore_pump.position)
# place the boiler at the centre coordinate
boiler = place_entity(Prototype.Boiler, position = coords.center)
print(f"Placed boiler to generate steam at {boiler.position}. This will be connected to the offshore pump at {offshore_pump.position}")
```

## Common Patterns

1. **Factory Section Planning**
```python
def plan_factory_section(center: Position, width: int, height: int):
    box = BuildingBox(width=width, height=height)
    try:
        area = nearest_buildable(
            Prototype.AssemblingMachine1,
            box,
            center
        )
        return area
    except Exception:
        print("Cannot fit factory section")
        return None
```

2. **Multiple Entity Placement**
```python
def setup_mining_outpost(ore_pos: Position):
    # Find area for multiple drills (3)
    drill_line = BuildingBox(width=Prototype.ElectricMiningDrill.WIDTH * 3, height=Prototype.ElectricMiningDrill.HEIGHT)  # Space for 3 drills
    
    area = nearest_buildable(
        Prototype.ElectricMiningDrill,
        drill_line,
        ore_pos
    )
    
    # Place drills along the line
    drills = []
    for x in range(3):
        pos = Position(
            x=area.left_top.x + (x * Prototype.ElectricMiningDrill.WIDTH),
            y=area.left_top.y
        )
        move_to(pos)
        drill = place_entity(
            Prototype.ElectricMiningDrill,
            position=pos
        )
        drills.append(drill)
    
    return drills
```

## Best practices
- Always use Prototype.X.WIDTH and .HEIGHT to plan the buildingboxes
- When doing power setups or setups with inserters, ensure the buildingbox is large enough to have room for connection types

## Troubleshooting

1. "No buildable position found"
   - Check building box size is appropriate
   - Verify resource coverage for miners