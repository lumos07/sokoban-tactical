class Enemy:
    def __init__(self, position, enemy_type, health, damage, vision_range=2):
        self.position = position
        self.type = enemy_type
        self.health = health
        self.damage = damage
        self.vision_range = vision_range

    def take_damage(self, amount):
        self.health -= amount
        print(f"Ὦ1️ {self.type.title()} at {self.position} took {amount} damage. HP left: {self.health}")

    def is_alive(self):
        return self.health > 0

    def detect_player(self, player_pos):
        """Returns True if the player is within vision range (Manhattan distance)."""
        ex, ey = self.position
        px, py = player_pos
        distance = abs(ex - px) + abs(ey - py)
        return distance <= self.vision_range

    def attack(self, player):
        if player.isalive():
            print(f"⚔️ {self.type.title()} attacks! Deals {self.damage} damage.")
            player.take_damage(self.damage)

    def move_toward_player(self, player_pos, grid):
        """
        Determines a single step move towards the player
        Prefers the move that reduces Manhattan distance and is walkable.
        """
        ex, ey = self.position
        px, py = player_pos
        best_move = None
        min_dist = float('inf')

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = ex + dx, ey + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] in [' ', '.', 'R']:
                dist = abs(nx - px) + abs(ny - py)
                if dist < min_dist:
                    min_dist = dist
                    best_move = (nx, ny)

        return best_move
