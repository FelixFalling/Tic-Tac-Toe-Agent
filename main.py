from enum import Enum
from abc import ABC, abstractmethod
import numpy as np
import random
import matplotlib.pyplot as plt

class GameState(Enum):
    PLAYING = 0
    WIN = 1
    DRAW = 2

class PlayType(Enum):
    PLAYER_VS_PLAYER = 0
    AGENT_VS_AGENT = 1
    AGENT_VS_PLAYER = 2

class BasePlayer(ABC):
    """
    Base Class for the different types of tic players that are used.
    """
    @abstractmethod
    def choose_action(self, state, valid_moves, epsilon):
        pass

    def update(self, state, action, reward, next_state, next_valid_moves):
        pass

class HumanPlayer(BasePlayer):
    def choose_action(self, state, valid_moves, epsilon):
        while True:
            try:
                row = int(input("Select Row: ")) - 1
                col = int(input("Select Column: ")) - 1
                action = row * 3 + col
                if action not in valid_moves:
                    print("Invalid move, try again")
                    continue
                return action
            except ValueError:
                print("Wrong input, try again")


class RandomAgent(BasePlayer):
    def choose_action(self, state, valid_moves, epsilon):
        return random.choice(valid_moves)


class QAgent(BasePlayer):
    def __init__(self, learning_rate=0.5, gamma=0.9):
        self.lr = learning_rate
        self.gamma = gamma
        self.q_table = np.zeros((3 ** 9, 9))

    def choose_action(self, state, valid_moves, epsilon):
        if random.random() < epsilon:
            return random.choice(valid_moves)
        return max(valid_moves, key=lambda a: self.q_table[state][a])

    def update(self, state, action, reward, next_state, next_valid_moves):
        # Q(s, a)
        current_q = self.q_table[state][action]
        if next_state is None or not next_valid_moves:
            # terminal state: target = r
            target = reward
        else:
            # max_a' Q(s', a')
            best_next = max(self.q_table[next_state][a] for a in next_valid_moves)
            # target = r + γ · max_a' Q(s', a')
            target = reward + self.gamma * best_next
        # Q(s, a) = Q(s, a) + η(target - Q(s, a))
        self.q_table[state][action] += self.lr * (target - current_q)


# Class for the state space
class tic_tac_toe_board():
    def __init__(self, rows, columns, play_type, player_x=None, player_o=None, verbose=True):
        self.rows = rows
        self.columns = columns
        self.board = [[None for _ in range(columns)] for _ in range(rows)]
        self.playing_type = play_type
        self.verbose = verbose

        # player_x / player_o are any object with choose_action() and update()
        # None means human input via HumanPlayer
        self.player_x = player_x if player_x is not None else HumanPlayer()
        self.player_o = player_o if player_o is not None else HumanPlayer()

        if verbose:
            if self.playing_type == PlayType.PLAYER_VS_PLAYER:
                print("Player vs Player")
            elif self.playing_type == PlayType.AGENT_VS_AGENT:
                print("Agent vs Agent")
            elif self.playing_type == PlayType.AGENT_VS_PLAYER:
                print("Agent vs Player")

    def reset(self):
        self.board = [[None for _ in range(self.columns)] for _ in range(self.rows)]

    def encode_state(self):
        val = {'x': 1, 'o': 2, None: 0}
        result = 0
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                result += val[cell] * (3 ** (i * 3 + j))
        return result

    def get_valid_moves(self):
        moves = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] is None:
                    moves.append(i * 3 + j)
        return moves

    def mark_board_at_location(self, x, y, player_marker):
        self.board[x][y] = player_marker
        self.print_board()

    def check_if_location_occupied(self, x, y):
        if self.board[x][y] is not None:
            if self.verbose:
                print("Location Occupied")
            return False
        return True

    def check_win_codition(self):
        num_rows = len(self.board)
        num_cols = len(self.board[0])

        for row in self.board:
            if row[0] is not None and all(cell == row[0] for cell in row):
                return GameState.WIN

        for col in range(num_cols):
            if self.board[0][col] is not None and all(self.board[row][col] == self.board[0][col] for row in range(num_rows)):
                return GameState.WIN

        if num_rows == num_cols:
            if self.board[0][0] is not None and all(self.board[i][i] == self.board[0][0] for i in range(num_rows)):
                return GameState.WIN
            if self.board[0][num_cols - 1] is not None and all(self.board[i][num_cols - 1 - i] == self.board[0][num_cols - 1] for i in range(num_rows)):
                return GameState.WIN

        if all(cell is not None for row in self.board for cell in row):
            return GameState.DRAW

        return GameState.PLAYING

    def input_type(self, state, valid_moves, epsilon, player):
        # Unified interface: calls choose_action on whichever player object is up
        agent = self.player_x if player == 'x' else self.player_o
        action = agent.choose_action(state, valid_moves, epsilon)
        return action // 3, action % 3

    def game_loop(self, epsilon=0.0, train=False):
        game_state = GameState.PLAYING
        current_round = 0
        prev = {'x': None, 'o': None}  # last (state, action) per player for Q-updates

        self.print_board()

        while game_state is GameState.PLAYING:
            player = 'x' if current_round % 2 == 0 else 'o'
            other  = 'o' if player == 'x' else 'x'
            agent  = self.player_x if player == 'x' else self.player_o
            other_agent = self.player_o if player == 'x' else self.player_x

            state       = self.encode_state()
            valid_moves = self.get_valid_moves()

            row, col = self.input_type(state, valid_moves, epsilon, player)
            action = row * 3 + col

            self.mark_board_at_location(row, col, player)
            game_state = self.check_win_codition()

            if train:
                if game_state == GameState.WIN:
                    agent.update(state, action, +1.0, None, [])
                    if prev[other]:
                        other_agent.update(prev[other][0], prev[other][1], -1.0, None, [])
                elif game_state == GameState.DRAW:
                    agent.update(state, action, +0.5, None, [])
                    if prev[other]:
                        other_agent.update(prev[other][0], prev[other][1], +0.5, None, [])
                else:
                    # mid-game: update this player's previous move now that we know what came next
                    if prev[player]:
                        agent.update(prev[player][0], prev[player][1], 0.0, state, valid_moves)

                prev[player] = (state, action)

            current_round += 1

        winner = player if game_state == GameState.WIN else None
        if self.verbose:
            if game_state == GameState.WIN:
                print(f"{winner.upper()} WINS!")
            elif game_state == GameState.DRAW:
                print("DRAW!")

        return game_state, winner

    def print_board(self) -> None:
        if not self.verbose:
            return

        col_count = len(self.board[0])
        header = "    " + " | ".join(str(c + 1) for c in range(col_count))
        separator = "  " + "-" * (len(header) - 2)
        print(header)
        print(separator)
        for i, row in enumerate(self.board):
            current_row = " | ".join(" " if cell is None else str(cell) for cell in row)
            print(f"{i + 1} | {current_row}")
            print(separator)


# --- Training ---

def run_training(n_epochs=5000, epsilon_start=0.1, delta=0.001, m=50):
    agent = QAgent(learning_rate=0.5, gamma=0.9)
    random_opponent = RandomAgent()
    scores = []
    epsilon = epsilon_start

    for epoch in range(n_epochs):
        # self-play: agent trains as both X and O
        board = tic_tac_toe_board(3, 3, PlayType.AGENT_VS_AGENT,
                                  player_x=agent, player_o=agent, verbose=False)
        board.game_loop(epsilon=epsilon, train=True)

        if epoch % m == 0:
            epsilon = max(0.0, epsilon - delta)

        # test 10 games as X vs random O
        score = 0.0
        for _ in range(10):
            test_board = tic_tac_toe_board(3, 3, PlayType.AGENT_VS_AGENT,
                                           player_x=agent, player_o=random_opponent, verbose=False)
            result, winner = test_board.game_loop(epsilon=0.0, train=False)
            if result == GameState.WIN and winner == 'x':
                score += 1.0
            elif result == GameState.DRAW:
                score += 0.5
        scores.append(score / 10)

        if (epoch + 1) % 500 == 0:
            print(f"Epoch {epoch + 1}/{n_epochs}  score={scores[-1]:.2f}  epsilon={epsilon:.4f}")

    return agent, scores


def plot_training(scores):
    plt.figure(figsize=(10, 5))
    plt.plot(scores)
    plt.xlabel("Epoch")
    plt.ylabel("Score vs Random (out of 1.0)")
    plt.title("Q-Agent Training Progress")
    plt.tight_layout()
    plt.savefig("training_progress.png")
    #plt.show()


# --- Main ---

def main():
    print("1: Player vs Player")
    print("2: Train agent then play vs it")
    choice = input("Choose mode: ").strip()
    game_number = int(input("Number of games you want to play: ").strip())
    number_of_board_rows = 3
    number_of_board_columns = 3

    if choice == '1':
        board = tic_tac_toe_board(number_of_board_rows, number_of_board_columns, PlayType.PLAYER_VS_PLAYER)
        board.game_loop()

    elif choice == '2':
        print("Training agent (5000 epochs)...")
        agent, scores = run_training()
        plot_training(scores)

        print(f"\nNow play {game_number} games vs the trained agent (you are O, agent is X).")
        results = []
        for i in range(game_number):
            print(f"\n--- Game {i + 1} ---")
            board = tic_tac_toe_board(number_of_board_rows, number_of_board_columns, PlayType.AGENT_VS_PLAYER,
                                      player_x=agent, player_o=None, verbose=True)
            result, winner = board.game_loop(epsilon=0.0, train=False)
            results.append((result, winner))

        wins   = sum(1 for r, w in results if r == GameState.WIN and w == 'o')
        losses = sum(1 for r, w in results if r == GameState.WIN and w == 'x')
        draws  = sum(1 for r, _ in results if r == GameState.DRAW)
        print(f"\nYour results — Wins: {wins}  Losses: {losses}  Draws: {draws}")


if __name__ == "__main__":
    main()
