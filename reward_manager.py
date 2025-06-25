import json
import random
from reward import Reward

class RewardManager:
    def __init__(self, reward_file="rewards/reward_types.json"):
        self.rewards = {}  # {(x, y): Reward}
        self.reward_pool = self._load_reward_types(reward_file)

    def _load_reward_types(self, file_path):
        try:
            with open(file_path, 'r') as f:
                print(f"📦 Loading rewards from {file_path}")
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ Reward file not found!")
            return []

    def spawn_random_reward(self, pos, current_turn):
        """Spawn a reward of random type at the given position."""
        if not self.reward_pool:
            print("⚠️ No rewards to spawn.")
            return None

        reward_data = random.choice(self.reward_pool)
        reward = Reward(
            reward_type=reward_data["type"],
            value=reward_data["value"],
            spawn_turn=current_turn,
            duration=reward_data.get("duration", 5)
        )
        self.rewards[pos] = reward
        print(f"🎁 Spawned {reward.type} at {pos} (Duration: {reward.duration})")
        return reward

    def update(self, current_turn, grid):
        """Expire rewards after their duration ends."""
        expired = []
        for pos, reward in list(self.rewards.items()):
            if current_turn - reward.spawn_turn >= reward.duration:
                x, y = pos
                if grid[x][y] == 'R':
                    grid[x][y] = ' '  # Clear from board
                expired.append(pos)

        for pos in expired:
            del self.rewards[pos]
            print(f"🗑️ Reward at {pos} expired")

    def collect_reward(self, pos, player):
        """Apply the reward to the player and remove it from board."""
        if pos in self.rewards:
            reward = self.rewards[pos]
            reward.apply_to(player)
            del self.rewards[pos]
            print(f"✅ Reward at {pos} collected")

    def reward_exists_at(self, pos):
        return pos in self.rewards
