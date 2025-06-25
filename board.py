from player import Player
from reward_manager import RewardManager
from enemy_manager import EnemyManager
from utils import is_walkable_for_enemy

class SokobanBoard:
    def __init__(self, filename):
        print("\U0001F4E5 Loading Sokoban level...")
        self.grid = self.load_level(filename)

        print("\U0001F4CF Grid loaded. Size:", len(self.grid), "rows")

        self.height = len(self.grid)
        self.width = max(len(row) for row in self.grid)
        self.turn = 0

        self.goals = set()
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == '.':
                    self.goals.add((i, j))

        player_pos = self.find_player()
        if player_pos is None:
            raise ValueError("❌ Player '@' not found in level file.")
        print("✅ Player found at:", player_pos)
        self.player = Player(player_pos)

        self.rewards = RewardManager()
        self.enemies = EnemyManager()
        self.load_enemies_from_grid()
        print("\U0001F3AE Board setup complete.")

    def load_level(self, filename):
        with open(filename) as f:
            lines = [list(line.rstrip('\n')) for line in f]
        print("\U0001F4C4 Level loaded:")
        for line in lines:
            print(''.join(line))
        return lines

    def find_player(self):
        print("\U0001F50D Searching for player '@' in grid...")
        for i, row in enumerate(self.grid):
            for j, ch in enumerate(row):
                if ch == '@':
                    print(f"✅ Found player at {(i, j)}")
                    return (i, j)
        print("❌ No player '@' found in the level.")
        return None

    def load_enemies_from_grid(self):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == 'E':
                    enemy = self.enemies.spawn_enemy((i, j))
                    if not enemy:
                        print(f"❌ Failed to spawn enemy at ({i},{j})")
                        continue
                    symbol = {
                        "grunt": 'G',
                        "brute": 'B',
                        "boss": 'X'
                    }.get(enemy.type, 'E')
                    self.grid[i][j] = symbol

    def display(self):
        for (x, y) in self.goals:
            if self.grid[x][y] == ' ':
                self.grid[x][y] = '.'

        for row in self.grid:
            print(''.join(row))
        print(f"❤️ Health: {self.player.health} | \U0001F6E1️ Shield: {self.player.shield} | \U0001F525 Burn: {self.player.burn_timer} | \U0001F553 Turn: {self.turn}")
        boxes = sum(row.count('$') for row in self.grid)
        goals = sum(row.count('.') for row in self.grid)
        print(f"\U0001F4E6 Boxes Remaining: {boxes} | \U0001F3AF Goals: {goals}")

    def _move(self, px, py, nx, ny):
        self.grid[px][py] = '.' if (px, py) in self.goals else ' '
        self.grid[nx][ny] = '@'
        self.player.set_position((nx, ny))

    def move(self, direction):
        dxdy = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
        if direction not in dxdy:
            return

        dx, dy = dxdy[direction]
        px, py = self.player.position
        nx, ny = px + dx, py + dy
        target = self.grid[nx][ny]

        self.turn += 1
        self.player.apply_decay()
        self.rewards.update(self.turn, self.grid)

        if target in ' .':
            self._move(px, py, nx, ny)
        elif target == '$':
            nnx, nny = nx + dx, ny + dy
            if self.grid[nnx][nny] in ' .':
                self.grid[nnx][nny] = '$'
                self._move(px, py, nx, ny)
        elif target in ['G', 'B', 'X']:
            print("❌ Enemy blocks your way! Use 'A' to attack if adjacent.")
            return
        elif target == 'R':
            print("\U0001F381 Reward collected!")
            self._move(px, py, nx, ny)
            self.rewards.collect_reward((nx, ny), self.player)

        self.enemy_turn()

    def enemy_turn(self):
        updated_enemies = {}
        for pos, enemy in list(self.enemies.all_enemies().items()):
            if not enemy.is_alive():
                self.grid[pos[0]][pos[1]] = ' '
                self.enemies.remove_enemy(pos)
                continue

            ex, ey = enemy.position
            px, py = self.player.position
            dist = abs(ex - px) + abs(ey - py)

            if dist <= enemy.vision_range:
                if dist == 1:
                    print(f"⚔️ {enemy.type.title()} at {enemy.position} attacks!")
                    enemy.attack(self.player)
                else:
                    dx = -1 if ex > px else (1 if ex < px else 0)
                    dy = -1 if ey > py else (1 if ey < py else 0)

                    move_order = [(dx, dy), (dx, 0), (0, dy)]
                    moved = False
                    for dxi, dyi in move_order:
                        nx, ny = ex + dxi, ey + dyi
                        if 0 <= nx < self.height and 0 <= ny < self.width and self.grid[nx][ny] in [' ', '.', 'R']:
                            self.grid[ex][ey] = '.' if (ex, ey) in self.goals else ' '
                            self.grid[nx][ny] = {
                                "grunt": 'G',
                                "brute": 'B',
                                "boss": 'X'
                            }.get(enemy.type, 'E')
                            enemy.position = (nx, ny)
                            updated_enemies[(nx, ny)] = enemy
                            moved = True
                            break

                    if not moved:
                        updated_enemies[(ex, ey)] = enemy
            else:
                updated_enemies[(ex, ey)] = enemy

        self.enemies.enemies = updated_enemies
        px, py = self.player.position
        if self.grid[px][py] != '@':
            self.grid[px][py] = '@'

        # Attack if still adjacent after move
        for pos, enemy in self.enemies.all_enemies().items():
            ex, ey = enemy.position
            px, py = self.player.position
            if abs(ex - px) + abs(ey - py) == 1:
                print(f"⚔️ {enemy.type.title()} at {enemy.position} attacks!")
                enemy.attack(self.player)

    def check_win(self):
        for (x, y) in self.goals:
            if self.grid[x][y] != '$':
                return False
        return True

    def player_attack(self):
        px, py = self.player.position
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = px + dx, py + dy
            enemy = self.enemies.get_enemy((nx, ny))
            if enemy and enemy.is_alive():
                self.player.attack(enemy)
                if not enemy.is_alive():
                    print(f"☠️ You defeated the {enemy.type}!")
                    self.grid[nx][ny] = '.' if (nx, ny) in self.goals else ' '
                    self.enemies.remove_enemy((nx, ny))
                return
        print("\U0001F645 No enemy to attack adjacent to you.")
