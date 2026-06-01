class tic_tac_toe_board():
    def __init__(self,rows,columns):
        self.rows = rows
        self.columns = columns
        self.board = [[None for i in range(rows)] for j in range(columns)]


    def mark_board_at_location(self,x,y,player_marker):
        self.board[x][y] = player_marker
        self.print_board()

    def check_win_codition(self) -> bool:
        num_rows = len(self.board)
        num_cols = len(self.board[0])

        # check rows
        for row in self.board:
            if row[0] is not None and all(cell == row[0] for cell in row):
                return True

        # check columns
        for col in range(num_cols):
            if self.board[0][col] is not None and all(self.board[row][col] == self.board[0][col] for row in range(num_rows)):
                return True

        # check diagonals (only valid on square boards)
        if num_rows == num_cols:
            if self.board[0][0] is not None and all(self.board[i][i] == self.board[0][0] for i in range(num_rows)):
                return True
            if self.board[0][num_cols - 1] is not None and all(self.board[i][num_cols - 1 - i] == self.board[0][num_cols - 1] for i in range(num_rows)):
                return True

        return False

    def game_loop(self):
        game_won = False
        current_round = 0

        self.print_board()


        while (game_won is False):
            try:
                row = int(input("Select Row:")) - 1
                column = int(input("Select Column:")) - 1
                current_round += 1
                if row not in range(len(self.board)) or column not in range(len(self.board[0])):
                    print("Input Too Large")
                    continue
                if current_round % 2 == 0:
                    player = "x"
                else:
                    player = "o"

                self.mark_board_at_location(row,column,player)
                if(self.check_win_codition()):
                    game_won = True
                    print("Game Won!")
            except ValueError:
                print("Wrong input try again")


    def print_board(self) -> None:
      for i, row in enumerate(self.board):
          current_row = (" | ".join(" " if cell is None else str(cell) for cell in row))
          print(current_row)
          print((len(current_row)*"-"))

def main():
    my_board = tic_tac_toe_board(3,3)
    my_board.game_loop()


if __name__ == "__main__":
    main()
