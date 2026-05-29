class tic_tac_toe_board():
    def __init__(self):
        #self.board[3][3] = None
        self.board = [[None for i in range(3)] for j in range(3)]


    def mark_board_at_location(self,x,y,player_marker):
        self.board[x][y] = player_marker
        self.print_board()

    def print_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                print(self.board[i][j])





def main():
    my_board = tic_tac_toe_board()
    my_board.mark_board_at_location(2,2,"x")


    



if __name__ == "__main__":
    main()
