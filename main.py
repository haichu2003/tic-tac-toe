class Player:

    def __init__(self, name, character):
        """
        :param name: str, the player's name
        :param character: str, the player's character
        """
        self.__name = name
        self.__char = character

    def get_character(self):
        """
        function to get a player's character ('x' or 'o')
        :return: str, player's character
        """
        return self.__char

    def get_name(self):
        """
        function to get a player's name
        :return: str, player's name
        """
        return self.__name

    def __str__(self):
        """
        :return: str, format:
        Name: player's name
        Character: player's character
        """
        return f'Name: {self.__name}' + '\n' + f'Character: {self.__char}'


class Box:
    def __init__(self):
        self.__is_ticked = " "

    def is_ticked(self):
        """
        if the box is not ticked, return ' ', else return the character within the box ('x' or 'o')
        :return: str (' ', 'x' or 'o')
        """
        return self.__is_ticked

    def tick(self, player):
        """
        set a box as ticked by the player
        :param player: Player, one of the players
        :return: bool, True if the box is not ticked, otherwise False
        """
        if self.__is_ticked != " ":
            return False
        self.__is_ticked = player.get_character()
        return True

    def __str__(self):
        """
        :return: str, format:
        " ": the box is not ticked
        "x" or "y": the box is ticked by one of the players
        """
        return self.__is_ticked


class Map:
    def __init__(self, size=10):
        self.__col = size
        self.__row = size
        self.__map = [[Box() for i in range(self.__col)] for j in range(self.__row)]

    def tick(self, player, x, y):
        return self.__map[x][y].tick(player)

    def get_map_size(self):
        """
        function to get the map size
        :return: (since the map is a square) an int, the length of one row
        """
        return self.__row

    def get_horizontal(self):
        """
        function to get a list of horizontal lines of the map
        :return: list of horizontal lines
        """
        return self.__map

    def get_vertical(self):
        """
        function to get a list of vertical lines of the map
        :return: list of vertical lines
        """
        to_return = []
        for i in range(self.__row):
            temp = []
            for j in range(self.__row):
                temp.append(self.__map[j][i])
            to_return.append(temp)
        return to_return

    def get_right_diagonal(self):
        """
        function to get a list of right-diagonal lines of the map
        :return: list of diagonal lines
        """
        to_return = []
        for i in range(self.__row):
            temp = []
            for x in range(0, i + 1):
                y = i - x
                temp.append(self.__map[x][y])
            to_return.append(temp)
        for i in range(1, self.__row):
            temp = []
            check = i + self.__col - 1
            for x in range(i, self.__col):
                y = check - x
                temp.append(self.__map[x][y])
            to_return.append(temp)
        return to_return

    def get_left_diagonal(self):
        """
        function to get a list of left-diagonal lines of the map
        :return: list of diagonal lines
        """
        to_return = []
        for i in range(self.__row - 1, -1, -1):
            temp = []
            for x in range(self.__col - 1, i - 1, -1):
                y = x - i
                temp.append(self.__map[x][y])
            to_return.append(temp)
        for i in range(1, self.__row + 1):
            temp = []
            for y in range(self.__col - 1, i - 1, -1):
                x = y - i
                temp.append(self.__map[x][y])
            to_return.append(temp)
        return to_return

    def __str__(self):
        to_return = '  '
        for i in range(self.__col):
            to_return += f' {i} '
        to_return += '\n'
        for i in range(self.__col):
            to_return += f'{i} '
            for j in range(self.__row):
                to_return += '[' + str(self.__map[i][j]) + ']'
            to_return += '\n'
        return to_return


def check_win(lines, map_size):
    """
    function to check if there are 5 (or 3, if the map is small) consecutive ticks of the same player on the same line
    :param lines: the line to be checked
    :param map_size: the size of the map
    :return: list of two character, "1" and the winner's character or "0" and ""
    """
    temp = ''
    for line in lines:
        temp += str(line)
#    temp = temp.strip()
    if len(temp) < map_size:
        return False, ""
    else:
        temp = temp.strip()
        check = []
        for i in range(len(temp)):
            if len(check) > 0 and temp[i] != check[-1]:
                check = []
            check.append(temp[i])
            if len(check) >= (3 if map_size <= 5 else 5):
                return True, check[0]

        return False, ""


def print_map(map1):
    to_return = ""
    for i in range(len(map1)):
        for j in range(len(map1[i])):
            to_return += '[' + str(map1[i][j]) + ']'
        to_return += '\n'
    print(to_return)


def main():
    map1 = Map(3)
    p1 = Player('Hai', 'x')
    p2 = Player('Ha', 'o')

    winner = ""
    break_condition = False
    turn_count = 0
    while True:
        if turn_count % 2 == 0:
            player = p1
        else:
            player = p2
        turn_count += 1
        print(map1)
        user_input = input(f"{player.get_name()} box: ")
        try:
            x, y = user_input.split()
        except ValueError:
            break
        map1.tick(player, int(x), int(y))

        # check if there is any winner
        for line in map1.get_horizontal():
            check, c = check_win(line, map1.get_map_size())
            if check:
                winner = c
                break_condition = check
                break
        for line in map1.get_vertical():
            check, c = check_win(line, map1.get_map_size())
            if check:
                winner = c
                break_condition = check
                break
        for line in map1.get_left_diagonal():
            check, c = check_win(line, map1.get_map_size())
            if check:
                winner = c
                break_condition = check
                break
        for line in map1.get_right_diagonal():
            check, c = check_win(line, map1.get_map_size())
            if check:
                winner = c
                break_condition = check
                break
        if break_condition:
            break

    if p1.get_character() == winner:
        print(f"Winner:\n{p1}")
    elif p2.get_character() == winner:
        print(f"Winner:\n{p2}")
    else:
        print("Tie")


if __name__ == '__main__':
    main()
