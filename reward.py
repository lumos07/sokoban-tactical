# class Reward:
#     def __init__(self, reward_type, value, spawn_turn, duration):
#         self.type = reward_type
#         self.value = value
#         self.spawn_turn = spawn_turn
#         self.duration = duration

#     def apply_to(self, player):
#         if self.type == 'health':
#             print(f"💊 +{self.value} Health")
#             player.heal(self.value)

#         elif self.type == 'shield':
#             print(f"🛡️ +{self.value} Shield")
#             if hasattr(player, 'shield'):
#                 player.shield += self.value
#             else:
#                 player.shield = self.value

#         elif self.type == 'extra_life':
#             print(f"❤️ +{self.value} Extra Life")
#             if hasattr(player, 'lives'):
#                 player.lives += self.value
#             else:
#                 player.lives = self.value

#         else:
#             print(f"⚠️ Unknown reward type: {self.type}")

class Reward:
    def __init__(self, reward_type, value, spawn_turn, duration):
        self.type = reward_type
        self.value = value
        self.spawn_turn = spawn_turn
        self.duration = duration

    def apply_to(self, player):
        if self.type == 'health':
            print(f"💊 +{self.value} Health")
            player.heal(self.value)

        elif self.type == 'shield':
            print(f"🛡️ +{self.value} Shield")
            if hasattr(player, 'shield'):
                player.shield += self.value
            else:
                player.shield = self.value

        elif self.type == 'extra_life':
            print(f"❤️ +{self.value} Extra Life")
            if hasattr(player, 'lives'):
                player.lives += self.value
            else:
                player.lives = self.value

        else:
            print(f"⚠️ Unknown reward type: {self.type}")
