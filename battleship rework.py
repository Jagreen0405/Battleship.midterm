from random import randrange

ship_initial = ["B", "C", "F", "A", "S"]
ship_names = ["Battleship", "Cruiser", "Frigate", "Aircraft Carrier", "Submarine"]
ship_lengths = [4, 3, 2, 5, 2]
map_size = 10

def get_usernames():
    """
    Function getting usernames for two players.
    """
    while True:
        player1_name = input("Player 1, enter your name: ")
        if player1_name:
            break
        else:
            print("Please enter your name.")

    while True:
        player2_name = input("Player 2, enter your name: ")
        if player2_name and player2_name != player1_name:
            break
        else:
            print("Please enter a valid name, and it cannot be the same as Player 1.")

    print(f"Welcome {player1_name} and {player2_name} to the Battleship game!")
    return player1_name, player2_name

def create_battlefield(map_size):
    """
    Function to create a map based on size.
    """
    return [["_"] * map_size for _ in range(map_size)]

def display_battlefield(board):
    """
    Function to display the current state of the map.
    """
    for row in board:
        print(" ".join(row))

def is_valid_placement(board, row, col, length, orientation, occupied):
    """
    Check if a ship can be placed at the given coordinates with the specified orientation.
    """
    if orientation == "H":  # Horizontal placement
        if col + length > map_size:  # Check if it goes out of bounds
            return False
        for i in range(length):
            if (row, col + i) in occupied:
                return False  # Check if it overlaps with another ship
    elif orientation == "V":  # Vertical placement
        if row + length > map_size:  # Check if it goes out of bounds
            return False
        for i in range(length):
            if (row + i, col) in occupied:
                return False  # Check if it overlaps with another ship
    return True

def place_ship_on_board(board, row, col, length, orientation, symbol, occupied):
    """
    Place the ship on the board and update the occupied set.
    """
    if orientation == "H":
        for i in range(length):
            board[row][col + i] = symbol
            occupied.add((row, col + i))
    elif orientation == "V":
        for i in range(length):
            board[row + i][col] = symbol
            occupied.add((row + i, col))
    return board, occupied

def player_ship_coordinate(player_board, occupied, player_name):
    """
    Function for player ship placement.
    """
    print(f"{player_name}, place your ships.")

    for ship_symbol, ship_name, ship_length in zip(ship_initial, ship_names, ship_lengths):
        while True:
            try:
                print(f"Placing {ship_name} ({ship_length} cells).")
                row = int(input(f"Enter the starting row for {ship_name}: "))
                col = int(input(f"Enter the starting column for {ship_name}: "))
                orientation = input("Enter orientation (H for horizontal, V for vertical): ").upper()

                if 0 <= row < map_size and 0 <= col < map_size and orientation in ["H", "V"]:
                    if is_valid_placement(player_board, row, col, ship_length, orientation, occupied):
                        player_board, occupied = place_ship_on_board(player_board, row, col, ship_length, orientation, ship_symbol, occupied)
                        break
                    else:
                        print("Invalid placement. Please ensure the ship is within bounds and does not overlap.")
                else:
                    print("Invalid input. Please enter correct values.")
            except ValueError:
                print("Invalid input. Please enter valid integers.")

    return player_board, occupied

def check_player_hit(opponent_board, dummy_board, player_name):
    """
    Function for checking if the player hit or missed on opponent's ships.
    """
    print(f"{player_name}, it's your turn to attack.")
    while True:
        try:
            row = int(input("Enter the row to attack: "))
            col = int(input("Enter the column to attack: "))
            if 0 <= row < map_size and 0 <= col < map_size:
                break
            else:
                print("Invalid coordinates. Please enter correct values.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    if opponent_board[row][col] in ship_initial:
        print(f"Hit! {player_name} hit a ship!")
        dummy_board[row][col] = "X"  # 'X' marks a hit
        opponent_board[row][col] = opponent_board[row][col].lower()  # Mark hit ships with lowercase
        return 1
    else:
        print(f"Miss! {player_name} missed.")
        dummy_board[row][col] = "*"  # '*' marks a miss
        return 0

def multiplayer_battle():
    """
    Main function to run the multiplayer battleship game.
    """
    player1_name, player2_name = get_usernames()

    # Create boards for each player
    player1_board = create_battlefield(map_size)
    player2_board = create_battlefield(map_size)
    player1_dummy_board = create_battlefield(map_size)
    player2_dummy_board = create_battlefield(map_size)

    player1_occupied = set()
    player2_occupied = set()

    # Player 1 places their ships
    print(f"\n{player1_name}'s turn to place ships.")
    player_ship_coordinate(player1_board, player1_occupied, player1_name)
    display_battlefield(player1_board)

    input("\nPress Enter to let Player 2 place their ships...")

    # Player 2 places their ships
    print(f"\n{player2_name}'s turn to place ships.")
    player_ship_coordinate(player2_board, player2_occupied, player2_name)
    display_battlefield(player2_board)

    input("\nPress Enter to start the game...")

    # Initialize hit counts for both players
    player1_hits = 0
    player2_hits = 0

    # Total ship cells: B (4), C (3), F (2), A (5), S (2) = 16 total cells
    total_ship_cells = 16

    # Alternate turns between Player 1 and Player 2
    while True:
        # Player 1's turn to attack
        print(f"\n{player1_name}'s turn to attack!")
        player1_hits += check_player_hit(player2_board, player1_dummy_board, player1_name)
        display_battlefield(player1_dummy_board)

        if player1_hits == total_ship_cells:  # Player 1 sinks all of Player 2's ships
            print(f"{player1_name} has won! Game over!")
            break

        # Player 2's turn to attack
        print(f"\n{player2_name}'s turn to attack!")
        player2_hits += check_player_hit(player1_board, player2_dummy_board, player2_name)
        display_battlefield(player2_dummy_board)

        if player2_hits == total_ship_cells:  # Player 2 sinks all of Player 1's ships
            print(f"{player2_name} has won! Game over!")
            break

        # Show both player boards (for testing purposes or debugging)
        print(f"\n{player1_name}'s board:")
        display_battlefield(player1_board)

        print(f"\n{player2_name}'s board:")
        display_battlefield(player2_board)

if __name__ == "__main__":
    multiplayer_battle()
