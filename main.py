class tic_tac_toe_board():
    def __init__(self):
        #self.board[3][3] = None
        self.board = [[None for i in range(3)] for j in range(3)]


    def mark_board_at_location(self,x,y,player_marker):
        self.board[x][y] = player_marker
        self.print_board()

    def check_win_codition(self):
        pass

    def print_board(self):
      for i, row in enumerate(self.board):
          print(" | ".join(" " if cell is None else str(cell) for cell in row))
          if i < 2:
              print("---------")
def main():
    my_board = tic_tac_toe_board()
    #my_board.mark_board_at_location(1,1,"x")

    for i in range(10):
        row = int(input("Select Row:"))
        column = int(input("Select Column:"))
        if i % 2 == 0:
            player = "x"
        else:
            player = "o"

        my_board.mark_board_at_location(row,column,player)


    



if __name__ == "__main__":
    main()
