
def is_walkable_for_enemy(tile):
    """
    Determines if a tile is safe for an enemy to move into.
    Enemies should NOT overwrite walls, player, boxes, or other enemies.
    """
    return tile in [' ', '.', 'R']  # Empty space, goal, or reward
