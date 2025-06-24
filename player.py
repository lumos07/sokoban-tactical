# class Player:
#     def __init__(self, position):
#         self.position = position
#         self.health = 100
#         self.shield = 0          
#         self.lives = 1
#         self.burn_timer = 0
#         self.decay_rate = 5

#     def apply_decay(self):
#         if self.burn_timer > 0:
#             self.health -= self.decay_rate
#             self.burn_timer -= 1

#     def trigger_burn(self, turns=5):
#         self.burn_timer = turns

#     def heal(self, amount):
#         self.health = min(100, self.health + amount)

#     def set_position(self, new_pos):
#         self.position = new_pos

#     def isalive(self):
#         return self.health > 0
    
#     def move(self, dx, dy):
#         x, y = self.position
#         self.position = (x + dx, y + dy)

#     def attack(self, target):
#         # Basic example: fixed damage
#         damage = 10
#         if hasattr(target, 'take_damage'):
#             target.take_damage(damage)
            
#     def take_damage(self, amount):
#         # Optional shield logic
#         if hasattr(self, 'shield') and self.shield > 0:
#             absorbed = min(self.shield, amount)
#             self.shield -= absorbed
#             amount -= absorbed
#             print(f"🛡️ Shield absorbed {absorbed} damage.")

#         self.health -= amount
#         print(f"💔 Player took {amount} damage! Current HP: {self.health}")

class Player:
    def __init__(self, position):
        self.position = position
        self.health = 100
        self.shield = 0          
        self.lives = 1
        self.burn_timer = 0
        self.decay_rate = 5

    def apply_decay(self):
        if self.burn_timer > 0:
            self.health -= self.decay_rate
            self.burn_timer -= 1
            print(f"🔥 Burn effect: {self.decay_rate} damage. Burn timer: {self.burn_timer}")

    def trigger_burn(self, turns=5):
        self.burn_timer = turns
        print(f"🔥 Player is burning for {turns} turns!")

    def heal(self, amount):
        old_health = self.health
        self.health = min(100, self.health + amount)
        print(f"💊 Healed from {old_health} to {self.health}")

    def set_position(self, new_pos):
        self.position = new_pos

    def isalive(self):
        return self.health > 0

    def move(self, dx, dy):
        x, y = self.position
        self.position = (x + dx, y + dy)

    def attack(self, target):
        damage = 10
        print(f"🗡️ Player attacks {target.type} for {damage} damage.")
        if hasattr(target, 'take_damage'):
            target.take_damage(damage)

    def take_damage(self, amount):
        if self.shield > 0:
            absorbed = min(self.shield, amount)
            self.shield -= absorbed
            amount -= absorbed
            print(f"🛡️ Shield absorbed {absorbed} damage.")

        self.health -= amount
        print(f"💔 Player took {amount} damage! Current HP: {self.health}")
