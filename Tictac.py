#Python implementation of a Tic-Tac-Toe game that can be played by two players on the same computer

import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
BOARD_SIZE = 600
LINE_WIDTH = 10
CELL_SIZE = BOARD_SIZE // 3
O_COLOR = (0, 0, 255)  # Blue
X_COLOR = (255, 0, 0)   # Red
LINE_COLOR = (0, 0, 0)  # Black
BG_COLOR = (255, 255, 255)  # White
TEXT_COLOR = (0, 0, 0)  # Black

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
font = pygame.font.SysFont('Arial', 40)
score_font = pygame.font.SysFont('Arial', 30)

class TicTacToe:
    def __init__(self):
        self.board = [" "] * 9
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        self.scores = {"X": 0, "O": 0, "Tie": 0}
        self.reset_button = pygame.Rect(200, 620, 200, 50)
    
    def draw_board(self):
        # Draw the grid
        for i in range(1, 3):
            # Horizontal lines
            pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), 
                            (BOARD_SIZE, i * CELL_SIZE), LINE_WIDTH)
            # Vertical lines
            pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), 
                            (i * CELL_SIZE, BOARD_SIZE), LINE_WIDTH)
        
        # Draw X's and O's
        for i in range(9):
            row = i // 3
            col = i % 3
            center_x = col * CELL_SIZE + CELL_SIZE // 2
            center_y = row * CELL_SIZE + CELL_SIZE // 2
            
            if self.board[i] == "X":
                # Draw X
                pygame.draw.line(screen, X_COLOR, 
                                (center_x - 50, center_y - 50),
                                (center_x + 50, center_y + 50), 10)
                pygame.draw.line(screen, X_COLOR, 
                                (center_x + 50, center_y - 50),
                                (center_x - 50, center_y + 50), 10)
            elif self.board[i] == "O":
                # Draw O
                pygame.draw.circle(screen, O_COLOR, 
                                 (center_x, center_y), 50, 10)
        
        # Draw scores
        score_text = f"X: {self.scores['X']}  O: {self.scores['O']}  Ties: {self.scores['Tie']}"
        score_surface = score_font.render(score_text, True, TEXT_COLOR)
        screen.blit(score_surface, (20, BOARD_SIZE + 20))
        
        # Draw current player
        player_text = f"Current Player: {self.current_player}"
        player_surface = font.render(player_text, True, TEXT_COLOR)
        screen.blit(player_surface, (20, BOARD_SIZE + 60))
        
        # Draw reset button
        pygame.draw.rect(screen, (200, 200, 200), self.reset_button)
        reset_text = font.render("Reset Game", True, TEXT_COLOR)
        screen.blit(reset_text, (self.reset_button.x + 20, self.reset_button.y + 10))
    
    def check_winner(self):
        # Check rows
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != " ":
                return self.board[i]
        
        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != " ":
                return self.board[i]
        
        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] != " ":
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != " ":
            return self.board[2]
        
        # Check for tie
        if " " not in self.board:
            return "Tie"
        
        return None
    
    def make_move(self, pos):
        if self.game_over:
            return False
            
        row = pos[1] // CELL_SIZE
        col = pos[0] // CELL_SIZE
        index = row * 3 + col
        
        if 0 <= index <= 8 and self.board[index] == " ":
            self.board[index] = self.current_player
            self.winner = self.check_winner()
            
            if self.winner:
                self.game_over = True
                self.scores[self.winner] += 1
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False
    
    def reset_game(self):
        self.board = [" "] * 9
        self.current_player = "X"
        self.game_over = False
        self.winner = None

def main():
    game = TicTacToe()
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                # Check if reset button was clicked
                if game.reset_button.collidepoint(pos):
                    game.reset_game()
                elif not game.game_over and pos[1] < BOARD_SIZE:
                    game.make_move(pos)
        
        # Draw everything
        screen.fill(BG_COLOR)
        game.draw_board()
        
        # Display winner message if game is over
        if game.game_over and game.winner != "Tie":
            winner_text = f"Player {game.winner} wins!"
            text_surface = font.render(winner_text, True, TEXT_COLOR)
            screen.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, BOARD_SIZE + 120))
        elif game.game_over:
            text_surface = font.render("It's a tie!", True, TEXT_COLOR)
            screen.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, BOARD_SIZE + 120))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()


#Run the program in a Python environment

#Players take turns entering numbers 1-9 corresponding to board positions:

#Player X goes first, then Player O

#The first to get 3 in a row (horizontally, vertically, or diagonally) wins

#If all squares are filled with no winner, it's a tie