class tic_tac_toe_board():
    def __init__(self,rows,columns):
        self.rows = rows
        self.columns = columns
        self.board = [[None for i in range(rows)] for j in range(columns)]


    def mark_board_at_location(self,x,y,player_marker):
        self.board[x][y] = player_marker
        self.print_board()

    def check_win_codition(self):
        pass

    def game_loop(self):
        game_rounds = ((self.rows)*(self.columns))

        for i in range(game_rounds):
            row = int(input("Select Row:")) - 1
            column = int(input("Select Column:")) - 1
            if row not in range(len(self.board)) or column not in range(len(self.board[0])):
                print("Input Too Large")
                continue
            if i % 2 == 0:
                player = "x"
            else:
                player = "o"

            self.mark_board_at_location(row,column,player)

    def print_board(self):
      for i, row in enumerate(self.board):
          current_row = (" | ".join(" " if cell is None else str(cell) for cell in row))
          print(current_row)
          #if i % 2 == 0:
          print((len(current_row)*"-"))

def main():
    my_board = tic_tac_toe_board(2,2)
    my_board.game_loop()


    



if __name__ == "__main__":
    main()
