
# can_place_entity

## Overview
`can_place_entity` is a utility function that checks whether an entity can be placed at a specific position in Factorio. It verifies various placement conditions including:
- Player reach distance
- Entity existence in inventory
- Collision with other entities
- Terrain compatibility (e.g., water for offshore pumps)
- Space requirements

## Basic Usage

```python
# Basic syntax
can_place = can_place_entity(
    entity: Prototype,  # The entity type to place
    direction: Direction = Direction.UP,  # Optional direction
    position: Position = Position(x=0, y=0)  # Position to check
) -> bool
```

## Examples

1. Basic placement check:
```python
# Check before attempting to place large entities
target_pos = Position(x=10, y=10)
move_to(target_pos)
if can_place_entity(Prototype.SteamEngine, position=target_pos):
    place_entity(Prototype.SteamEngine, position=target_pos)
else:
    print("Cannot place steam engine at target position")
```

2. Check with direction:
```python
# Check if we can place a mining drill facing down
can_place = can_place_entity(
    Prototype.BurnerMiningDrill,
    direction=Direction.DOWN,
    position=Position(x=0, y=0)
)
```

## Important Considerations

1. Player Distance
- Checks fail if the target position is beyond the player's reach
- Always move close enough before checking placement

2. Entity Collisions
- Checks for existing entities in the target area
- Returns False if there would be a collision

3. Special Cases
- Offshore pumps require water tiles
- Some entities have specific placement requirements