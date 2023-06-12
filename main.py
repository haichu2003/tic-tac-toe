from tkinter import *


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

    def set_name(self, name):
        """
        set the player's name
        :param name: player's name
        :return: None
        """
        self.__name = name

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

    def reset(self):
        """
        reset the box to its original state
        """
        self.__is_ticked = ' '

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
        return self.__map[y][x].tick(player)

    def get_map_size(self):
        """
        function to get the map size
        :return: (since the map is a square) an int, the length of one row
        """
        return self.__row

    def get_map(self):
        """
        function to get the __map
        :return: self.__map
        """
        return self.__map

    def reset(self):
        """
        reset the map to its original state
        """
        for i in range(self.__row):
            for j in range(self.__col):
                self.__map[i][j].reset()

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


class GUI:
    def __init__(self, game_map, p1, p2):
        """
        GUI constructor
        :param game_map: a Map object, the map to be used
        :param p1: player 1
        :param p2: player 2
        """
        # "Welcome" window configuration
        self.__map_size_input = None
        self.__welcome_window = None

        self.__player1_input = None
        self.__player2_input = None

        self.__map = game_map
        self.__buttons = [[0 for i in range(self.__map.get_map_size())] for j in range(self.__map.get_map_size())]
        self.__turn_count = 0
        self.__p1 = p1
        self.__p2 = p2

        self.__game_window = None
        self.__text_box = None

        self.start_welcome_window()

    def start_welcome_window(self):
        """
        start the welcome window, which will be shown when the game is started or new player(s) is introduced
        :return: None
        """
        self.__welcome_window = Tk()

        Label(self.__welcome_window, text="Enter map size:").grid(row=0, column=0)
        Label(self.__welcome_window, text="Enter player 1's name:").grid(row=1, column=0)
        Label(self.__welcome_window, text="Enter player 2's name:").grid(row=2, column=0)

        self.__map_size_input = Entry(self.__welcome_window)
        self.__player1_input = Entry(self.__welcome_window)
        self.__player2_input = Entry(self.__welcome_window)

        menu_bar = Menu(self.__welcome_window)
        menu_bar.add_command(label="Start game", command=self.start_game_window)
        menu_bar.add_command(label="Quit", command=self.quit)

        self.__map_size_input.grid(row=0, column=1, columnspan=3)
        self.__player1_input.grid(row=1, column=1, columnspan=3)
        self.__player2_input.grid(row=2, column=1, columnspan=3)

        self.__welcome_window.config(menu=menu_bar)

        if self.__game_window is not None:
            self.__game_window.withdraw()

    def update_map(self, x, y):
        """
        function to update the game window
        :param x: location of box
        :param y: location of box
        :return: None
        """
        if self.__turn_count % 2 == 0:
            player = self.__p1
            self.__text_box.configure(text=f"{self.__p2.get_name()}'s turn. ({self.__p2.get_character()})")
        else:
            player = self.__p2
            self.__text_box.configure(text=f"{self.__p1.get_name()}'s turn. ({self.__p1.get_character()})")
        valid_move = self.__map.tick(player, x, y)
        check = False
        # print(self.__map)
        if valid_move:
            self.__turn_count += 1
            self.__buttons[x][y].configure(text=player.get_character())
        else:
            self.__text_box.configure(text="Invalid move! Please choose again.")
        for line in self.__map.get_horizontal():
            temp, c = check_win(line, self.__map.get_map_size())
            check ^= temp
        for line in self.__map.get_vertical():
            temp, c = check_win(line, self.__map.get_map_size())
            check ^= temp
        for line in self.__map.get_left_diagonal():
            temp, c = check_win(line, self.__map.get_map_size())
            check ^= temp
        for line in self.__map.get_right_diagonal():
            temp, c = check_win(line, self.__map.get_map_size())
            check ^= temp
        if check:
            self.__text_box.configure(text=f"{player.get_name()} has won the match.")
            self.reset()
            self.__text_box.configure(text=f"{self.__p1.get_name()}'s turn. ({self.__p1.get_character()})")

    def start_game_window(self):
        """
        start the game
        :return: None
        """
        # test
        self.__welcome_window.withdraw()
        if self.__map_size_input.get() != '':
            try:
                map_size = int(self.__map_size_input.get())
                self.__map = Map(map_size)
            except ValueError:
                print("Must be int")
        if self.__player1_input.get() != '':
            self.__p1.set_name(self.__player1_input.get())
        if self.__player1_input.get() != '':
            self.__p2.set_name(self.__player2_input.get())

        # game window configuration

        self.__game_window = Toplevel(self.__welcome_window)
        self.__text_box = Label(self.__game_window, text="Tic Tac Toe", font=("Helvetica", "10"))
        self.__text_box.configure(text=f"{self.__p1.get_name()}'s turn. ({self.__p1.get_character()})")

        self.reset()

        menu_bar = Menu(self.__game_window)
        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Reset game", command=self.reset)
        edit_menu.add_command(label="Quit", command=self.quit)
        edit_menu.add_command(label="New player", command=self.start_welcome_window)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.__game_window.config(menu=menu_bar)

        self.__game_window.title("Tic Tac Toe")
        self.__game_window.resizable(True, True)

        # game window structure
        self.__text_box.grid(row=0, column=0, columnspan=self.__map.get_map_size())
#        for i in range(self.__map.get_map_size()):
#            for j in range(self.__map.get_map_size()):
#                self.__buttons[j][i] = Button(self.__game_window, height=1, width=3,
#                                              font=("Helvetica", "20"),
#                                              command=lambda x=j, y=i: self.update_map(x, y))
#                self.__buttons[j][i].grid(row=i + 1, column=j)

    def reset(self):
        """
        reset the map to its initial status
        :return: None
        """
        self.__map.reset()
        self.__turn_count = 0
        for i in range(self.__map.get_map_size()):
            for j in range(self.__map.get_map_size()):
                self.__buttons[i][j] = Button(self.__game_window, height=1, width=3,
                                              font=("Helvetica", "20"),
                                              command=lambda x=i, y=j: self.update_map(x, y))
                self.__buttons[i][j].grid(row=i + 2, column=j)

    def start(self):
        """
        start the game
        :return: None
        """
        self.__welcome_window.mainloop()

    def quit(self):
        """
        quit the game
        :return: None
        """
        self.__welcome_window.quit()


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


def command_line_game():
    map1 = Map(4)
    p1 = Player('Hai', 'X')
    p2 = Player('Ha', 'O')
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
        check = map1.tick(player, int(x), int(y))
        while not check:
            user_input = input(f"{player.get_name()} box: ")
            try:
                x, y = user_input.split()
            except ValueError:
                break
            check = map1.tick(player, int(x), int(y))

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


def main():
    map1 = Map()
    p1 = Player('Player1', 'X')
    p2 = Player('Player2', 'O')
    gui = GUI(map1, p1, p2)
    gui.start()


if __name__ == '__main__':
    # command_line_game()
    main()
