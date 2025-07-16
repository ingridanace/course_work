"""
Important: We assume that upper side of the board belongs to black, and bottom side is white
1. Input of a letter and a digit +
2. Choose between 2 options +
3. After piece is input, ask to input black pieces at least 1, to 16. +
4. User inputs 'done' and program for inputs ends there +
5. If user inputs 'done' before first input, do not end, throw an error +
6. Confirmation after adding all pieces or an error with whats wrong +
7. Print out what black pieces if any the white piece can take
a-h and 1-8
"""

from tabulate import tabulate
import csv

piece = ""  # Global argument concept
clear_board = [
    ["", "a", "b", "c", "d", "e", "f", "g", "h"],
    [1, "", "", "", "", "", "", "", ""],
    [2, "", "", "", "", "", "", "", ""],
    [3, "", "", "", "", "", "", "", ""],
    [4, "", "", "", "", "", "", "", ""],
    [5, "", "", "", "", "", "", "", ""],
    [6, "", "", "", "", "", "", "", ""],
    [7, "", "", "", "", "", "", "", ""],
    [8, "", "", "", "", "", "", "", ""],
]

# Creating CSV file
def create_board():
    with open("chess_board.csv", "w", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerows(clear_board)
create_board()

# Reading the CSV
def read_board():
    with open("chess_board.csv", "r") as file:
        reader = csv.reader(file, delimiter=",")
        rows = list(reader)
        return rows

# Printing the board in CSV
def print_board():
    rows = read_board()
    headers = rows[0]
    data = rows[1:]
    print(tabulate(data, headers=headers, tablefmt="grid"))

# The input of chess pieces
def white_piece_input():

    global piece
    rows = read_board()
    headers = rows[0]
    data = rows[1:]
    print_board()
    white_piece = input(
        "Please input coordinates for a white piece King or Pawn in letter + digit format e.g. 'King a5' or 'Pawn c2': ")
    # I will use split from fuel lesson
    try:
        piece, position = white_piece.split(" ")
        piece_column_letter = position[0]
        piece_row = int(position[1:])-1
        column_map = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5,
                      "f": 6, "g": 7, "h": 8}  # Mapping column letters to int

        if piece_row < 0:
            raise IndexError("Row must be a number between 1 to 8")

        # This converts letter to int
        piece_column = column_map[piece_column_letter]

        # Marks an empty slot with W for white, K for king and p for pawn
        if piece == "King":
            data[piece_row][piece_column] = "WK"
        elif piece == "Pawn":
            data[piece_row][piece_column] = "WP"
        else:
            raise ValueError("Invalid chess piece name")

        # Board updated after white piece entry:
        with open("chess_board.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows([headers] + data)
        print("White piece successfully added")

        return piece_row, piece_column

    except ValueError as e:
        print(f"Wrong input! {e}")
        return white_piece_input()  # If bad input - try again with recursion
    except IndexError as e:
        print(f"Wrong coordinates! {e}")
        return white_piece_input()  # If bad input - try again with recursion


def black_pieces_input():
    rows = read_board()
    headers = rows[0]
    data = rows[1:]

    black_count = 0
    while True:
        print_board()
        black_cell = input(
            "Input coordinates for a black pawn (e.g., 'b3') or type 'done' to finish: ")

        if black_cell.lower() == "done":
            if black_count == 0:
                print("Error: At least one black piece is required!")
                continue
            break

        try:
            piece_column_letter = black_cell[0]
            piece_row = int(black_cell[1:])

            piece_row = int(piece_row) - 1  # Convert row (number) to int
            column_map = {"a": 1, "b": 2, "c": 3, "d": 4,
                          "e": 5, "f": 6, "g": 7, "h": 8}

            # Convert column letter to int
            piece_column = column_map[piece_column_letter]

            if data[piece_row][piece_column]:
                print("This slot is taken! Choose another slot.")
                continue

            # Place black piece
            data[piece_row][piece_column] = "BP"
            black_count += 1
            print(f"Black piece was added successfully!")

            if black_count > 16:
                print("No more black pieces can be added")
                continue

            # Update and print the board with new black piecces
            with open("chess_board.csv", "w", newline="") as file:
                writer = csv.writer(file, delimiter=",")
                writer.writerows([headers] + data)

        except IndexError as e:
            print(f"Wrong coordinates! {e}")

    # Save updated board
    with open("chess_board.csv", "w", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerows([headers] + data)
    print("All black pieces added with success!")

# Module to find what pieces can white piece take
def the_move(saved_board):
    global piece  # this will use the input from white_piece_position()

    if piece == "King":
        # A King piece can takeall surrounding squeres by 1
        possible_moves = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        check_can_piece_take(saved_board, possible_moves, "King")
        # A Pawn piece can take only 2 diagonal pieces in front (we are looking only at white piece)
    elif piece == "Pawn":
        possible_moves = [
            (-1, -1), (-1, 1)
        ]
        check_can_piece_take(saved_board, possible_moves, "Pawn")


def check_can_piece_take(saved_board, possible_moves, piece_name):
    piece_row, piece_column = white_piece_position

    can_piece_take = False  # I use flag, so it would find at least one match

    def transform_row(val):
        return val + 1
    def transform_column(val):
        mapc = {
            1:"a", 2:"b", 3:"c", 4:"d",
            5:"e", 6:"f", 7:"g", 8:"h"
        }
        return mapc[val]

    white_chess_row = transform_row(piece_row)
    white_chess_column = transform_column(piece_column)
    print(f"Pawn at {white_chess_column}{white_chess_row}")

    for move in possible_moves:
        black_row = piece_row + move[0]
        black_column = piece_column + move[1]

        # Make sure the move does not go outside the board
        black_chess_row = transform_row(black_row)
        black_chess_column = transform_column(black_column)

        if 0 <= black_row < len(saved_board) and 0 <= black_column < len(saved_board[0]):
            cell = saved_board[black_row][black_column]
            if cell == "BP":
                print(f"{piece_name} can take this black piece! ({
                      black_chess_column}{black_chess_row})")
                can_piece_take = True

    if not can_piece_take:
        print(f"The white {piece_name} cannot capture any black pieces.")

white_piece_position = white_piece_input()
balck_pieces_positions = black_pieces_input()
saved_board = read_board()
headers = saved_board[0]
data = saved_board[1:]
the_move(data)


# https://github.com/TuringCollegeSubmissions/inacec-DS.v3.1.1.6
