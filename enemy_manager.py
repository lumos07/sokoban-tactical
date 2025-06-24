# import json
# import random
# from enemy import Enemy

# class EnemyManager:
#     def __init__(self, enemy_file="enemies/enemy_types.json"):
#         self.enemy_pool = self._load_enemy_types(enemy_file)
#         self.enemies = {}  # {(x, y): Enemy}

#     def _load_enemy_types(self, file_path):
#         try:
#             with open(file_path, 'r') as f:
#                 return json.load(f)
#         except FileNotFoundError:
#             print("⚠️ Enemy types file not found!")
#             return []

#     def spawn_enemy(self, pos, enemy_type_name=None):
#         """Spawn a specific or random enemy type at position."""
#         if not self.enemy_pool:
#             return None

#         if enemy_type_name:
#             enemy_data = next((e for e in self.enemy_pool if e["type"] == enemy_type_name), None)
#             if not enemy_data:
#                 print(f"⚠️ Unknown enemy type: {enemy_type_name}")
#                 return None
#         else:
#             enemy_data = random.choice(self.enemy_pool)

#         enemy = Enemy(
#             position=pos,
#             enemy_type=enemy_data["type"],
#             health=enemy_data["health"],
#             damage=enemy_data["damage"],
#             vision_range=enemy_data.get("vision_range", 2)
#         )
#         self.enemies[pos] = enemy
#         return enemy

#     def remove_enemy(self, pos):
#         if pos in self.enemies:
#             del self.enemies[pos]

#     def get_enemy(self, pos):
#         return self.enemies.get(pos, None)

#     def all_enemies(self):
#         return self.enemies


import json
import random
from enemy import Enemy

class EnemyManager:
    def __init__(self, enemy_file="enemies/enemy_types.json"):
        self.enemy_pool = self._load_enemy_types(enemy_file)
        self.enemies = {}  # {(x, y): Enemy}

    def _load_enemy_types(self, file_path):
        try:
            with open(file_path, 'r') as f:
                print(f"📂 Loading enemy types from {file_path}")
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ Enemy types file not found!")
            return []

    def spawn_enemy(self, pos, enemy_type_name=None):
        """Spawn an enemy at a position. If type is not given, randomize."""
        if not self.enemy_pool:
            print("⚠️ No enemy types available to spawn.")
            return None

        if enemy_type_name:
            enemy_data = next((e for e in self.enemy_pool if e["type"] == enemy_type_name), None)
            if not enemy_data:
                print(f"⚠️ Unknown enemy type: {enemy_type_name}")
                return None
        else:
            enemy_data = random.choice(self.enemy_pool)

        enemy = Enemy(
            position=pos,
            enemy_type=enemy_data["type"],
            health=enemy_data["health"],
            damage=enemy_data["damage"],
            vision_range=enemy_data.get("vision_range", 2)
        )
        self.enemies[pos] = enemy
        print(f"👹 Spawned {enemy.type} at {pos}")
        return enemy

    def remove_enemy(self, pos):
        if pos in self.enemies:
            print(f"🧹 Removed enemy at {pos}")
            del self.enemies[pos]

    def get_enemy(self, pos):
        return self.enemies.get(pos)

    def all_enemies(self):
        return self.enemies
