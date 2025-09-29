'''
    This module implements maze_reader() function, contains main() function and provides taking input
    from command line. Additionally, this module handles all the thrown exceptions.

    Author: Rasul Abbaszada
'''


from maze import Maze
import argparse
from typing import Optional
import re
import matplotlib.pyplot as plt
import time
from runner import Runner


# raises Exception if something goes wrong when reading file
def get_file_content(file: str) -> list[str]:
    content: list[str] = []
    with open(file, 'r') as f:
        for line in f:
            content.append(line.strip())
    return content


# checks if dimensions, symbols etc. are correct, raises ValueError if not
def check_content(content: list[str]) -> None:
    # 1 cell in actual maze is represented by 3 x 3 array in maze file
    # that's why minimal size for columns and rows is 3
    if len(content) < 3:
        raise ValueError("Size of rows must be at least 3")

    # size of columns must be bigger than or equal to 3 and their lengths must be equal
    col_sz: int = len(content[0])
    for row in content:
        if len(row) < 3:
            raise ValueError("Size of column must be at least 3")
        if len(row) != col_sz:
            raise ValueError("Size of all columns must be equal")

    wall: str = "#"
    # check if external walls are all '#'
    for i in range(len(content)):
        for j in range(len(content[0])):
            if i == 0 or i + 1 == len(content):
                if (content[i][j] != wall):
                    raise ValueError("Incorrect character in external wall")
            if j == 0 or j + 1 == len(content[0]):
                if (content[i][j] != wall):
                    raise ValueError("Incorrect character in external wall")


def maze_reader(maze_file: str, stat_file: Optional[str]="statistics.txt") -> Maze:
    wall: str = "#"
    path: str = "."

    try:
        content: list[str] = get_file_content(maze_file)
    except Exception:
        raise IOError("Something happened when reading the file")

    # write the name of the file to the statistics file
    with open(stat_file, 'w', newline='') as st_f:
        st_f.writelines(maze_file + "\n")

    try:
        # checks content, raises Exception if anything illegal happens
        check_content(content)

        height: int = len(content) // 2  # height of the actual maze grid
        width: int = len(content[0]) // 2   # width of the actual maze grid
        maze: Maze = Maze(width, height)

        # read maze_file
        for i in range(len(content) - 2, 0, -2):
            for j in range(1, len(content[0]) - 1, 2):
                # check if there is an illegal symbol
                if content[i][j] != wall and content[i][j] != path \
                    or content[i - 1][j] != wall and content[i - 1][j] != path \
                    or content[i][j + 1] != wall and content[i][j + 1] != path \
                    or content[i + 1][j] != wall and content[i + 1][j] != path \
                    or content[i][j - 1] != wall and content[i][j - 1] != path:
                    raise ValueError("Incorrect character\n")


                # map the coordinates of maze in file to the coordinates of maze to be stored
                x: int = (j - 1) // 2
                y: int = (len(content) - (i + 2)) // 2

                # proceed adding the walls
                if content[i - 1][j] == wall:
                    maze.add_horizontal_wall(x, y + 1)
                if content[i][j + 1] == wall:
                    maze.add_vertical_wall(y, x + 1)
                if content[i + 1][j] == wall:
                    maze.add_horizontal_wall(x, y)
                if content[i][j - 1] == wall:
                    maze.add_vertical_wall(y, x)

        return maze

    except Exception as e:
        raise e

def is_in_dimension(content: list[str], starting: Optional[tuple[int, int]], goal: Optional[tuple[int , int]]) -> bool:
    height: int = len(content) // 2  # height of the maze
    width: int = len(content[0]) // 2   # width of the maze

    if goal != None:
        # check if out of dimension
        if goal[0] < 0 or goal[0] > width - 1\
        or goal[1] < 0 or goal[1] > height - 1:
            return False

    if starting != None:
        # check if out of dimension
        if starting[0] < 0 or starting[0] > width - 1 \
        or starting[1] < 0 or starting[1] > height - 1:
                return False

    return True


def str_to_tuple(s: str) -> tuple[int, int]:
    '''Firstly, we check if formatting is correct, then we return tuple that represents coordinates'''
    if s == None:
        return None

    expected_tokens = [",", " "] # order is important, we expect tokens in the order as they appear in the list

    for token in expected_tokens:
        if token not in s:
            raise ValueError(f"expected character: {token}")

    j = 0
    for i in range(0, len(s)):
        if i == 0 and not s[i].isdigit():
            raise ValueError("must be digit\n")

        if not s[i].isdigit():
            if j < len(expected_tokens):
                if s[i] == expected_tokens[j]:
                    j += 1
                    continue
                else:
                    raise ValueError(f"Incorrect token: {s[i]}")
            else:
                raise ValueError(f"extra tokens are not allowed\n")

    coordinates = re.findall(r'\d+', s)
    return (int(coordinates[0]), int(coordinates[1]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("maze", help="The name of the maze file, e.g., maze1.mz")
    parser.add_argument("--starting", type=str, help='The starting position, e.g., "2, 1"')
    parser.add_argument("--goal", type=str, help='The goal position, e.g., "4, 5"')

    args = parser.parse_args()

    try:
        content = get_file_content(args.maze)

        starting: tuple[int, int] = str_to_tuple(args.starting)
        goal: tuple[int, int] = str_to_tuple(args.goal)

        if not is_in_dimension(content, starting, goal):
            raise ValueError(f"{starting} or {goal} is/are out of dimension\n")

        # create maze and run shortest_path algorithm
        myMaze: Maze = maze_reader(args.maze)

        s_path: list[tuple[int, int]] = myMaze.shortest_path(starting, goal)

        # print the shortest path
        for pair in s_path:
            print(pair, end=" ")


        # visualize maze solving
        # if you want to disable me just comment me till the end of visualization
        fig, ax = plt.subplots()

        ax.set_xlim(0, myMaze.width)
        ax.set_ylim(0, myMaze.height)
        ax.set_aspect("equal")

        myMaze.plot(ax)
        plt.pause(0.2)
        for pair in myMaze.explored_coordinates:
            runner = Runner(pair[0], pair[1])
            runner.plot(ax, "green")
            plt.pause(0.2)
            runner.plot(ax, "red")

        plt.show()
        # end of visualization


    except Exception as e:
        print(e)




