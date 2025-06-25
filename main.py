import os
from board import SokobanBoard

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("🧠 Welcome to Sokoban Tactical Edition!")
    board = SokobanBoard("levels/level1.txt")
    
    print("✅ Board loaded successfully.")
    print("📍 Player position:", board.player.position)
    print("🧱 Grid size:", board.height, "x", board.width)
    print("📦 Boxes:", sum(row.count('$') for row in board.grid))
    print("🎯 Goals:", sum(row.count('.') for row in board.grid))
    print("❤️ Health:", board.player.health)

    print("🟢 Entering game loop...")

    while board.player.isalive():
        if board.check_win():
            clear_screen()
            board.display()
            print("🎉 You win! All boxes are on goals.")
            break

        clear_screen()
        board.display()
        print("➡️ Move (U/D/L/R), A to attack, Q to quit: ", end="")
        command = input().strip().upper()

        if command == 'Q':
            print("👋 Quitting the game. Bye!")
            break
        elif command in ['U', 'D', 'L', 'R']:
            board.move(command)
        elif command == 'A':
            board.player_attack()
        else:
            print("⚠️ Invalid input! Use U/D/L/R/A or Q.")

    if not board.player.isalive():
        print("\n💀 You died! Game over.")

    print("🎮 Game ended.")

if __name__ == "__main__":
    main()
