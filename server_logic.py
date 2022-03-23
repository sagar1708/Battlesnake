import random
from typing import List, Dict
from scipy import spatial
"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""


def avoid_my_body(my_body, possible_moves):
    """
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """

    remove = []

    for direction, location in possible_moves.items():
        if location in my_body:
            remove.append(direction)

    for direction in remove:
        del possible_moves[direction]

    return possible_moves


def avoid_walls(board_width, board_height, possible_moves):
    remove = []

    for direction, location in possible_moves.items():
        x_out_range = (location["x"] < 0 or location["x"] == board_width)
        y_out_range = (location["y"] < 0 or location["y"] == board_height)

        if x_out_range or y_out_range:
            remove.append(direction)

    for direction in remove:
        del possible_moves[direction]

    return possible_moves


def avoid_snakes(snakes, mySnakeLength, possible_moves):
    remove = []

    for snake in snakes:
        for direction, location in possible_moves.items():
            if location in snake["body"]:
                remove.append(direction)
    remove = set(remove)
    for direction in remove:
        del possible_moves[direction]

    return possible_moves


def get_target_close(snakes, mySnakeLength, foods, my_head):
    coordinates = []

    if len(foods) == 0:
        return None

    for food in foods:
        coordinates.append((food["x"], food["y"]))

    for snake in snakes:
        if snake["length"] < mySnakeLength: 
            print(snake["head"]["x"], snake["head"]["y"])
            coordinates.append((snake["head"]["x"], snake["head"]["y"]))

    tree = spatial.KDTree(coordinates)

    results = tree.query([(my_head["x"], my_head["y"])])[1]

    return foods[results[0]]


def move_target(possible_moves, my_head, target):
    distance_x = abs(my_head["x"] - target["x"])
    distance_y = abs(my_head["y"] - target["y"])

    for direction, location in possible_moves.items():
        new_distance_x = abs(location["x"] - target["x"])
        new_distance_y = abs(location["y"] - target["y"])

        if new_distance_x < distance_x or new_distance_y < distance_y:
            return direction

    return list(possible_moves.keys())[0]


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """

    my_head = data["you"][
        "head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"][
        "body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    board_height = data["board"]["height"]
    board_width = data["board"]["width"]
    snakes = data["board"]["snakes"]
    foods = data["board"]["food"]

    mySnakeLength = data["you"]["length"]

    # TODO: uncomment the lines below so you can see what this data looks like in your output!
    #print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    #print(f"All board data this turn: {data}")
    #print(f"My Battlesnakes head this turn is: {my_head}")
    #print(f"My Battlesnakes body this turn is: {my_body}")

    #possible_moves = ["up", "down", "left", "right"]

    possible_moves = {
        "up": {
            "x": my_head["x"],
            "y": my_head["y"] + 1,
        },
        "down": {
            "x": my_head["x"],
            "y": my_head["y"] - 1,
        },
        "left": {
            "x": my_head["x"] - 1,
            "y": my_head["y"],
        },
        "right": {
            "x": my_head["x"] + 1,
            "y": my_head["y"],
        }
    }

    # Don't allow your Battlesnake to move back in on it's own neck
    possible_moves = avoid_my_body(my_body, possible_moves)
    possible_moves = avoid_walls(board_width, board_height, possible_moves)
    possible_moves = avoid_snakes(snakes, mySnakeLength, possible_moves)

    target = get_target_close(snakes, mySnakeLength, foods, my_head)

    if len(possible_moves) > 0:
        if target is not None:
            move = move_target(possible_moves, my_head, target)
        else:
            possible_moves = list(possible_moves.keys())
            move = random.choice(possible_moves)
    else:
        move = "up"
        print("GOING TO LOSE!!!!!!!!!!")
    # TODO: Explore new strategies for picking a move that are better than random

    #print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
