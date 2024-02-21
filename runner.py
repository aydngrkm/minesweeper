import pygame
import sys
import time

from minesweeper import Minesweeper, MinesweeperAI

HEIGHT = 8
WIDTH = 8
MINES = 8

# Colors
ZEROBLACK = (0, 0, 0)
BLACK = (30, 30, 30)
GRAY = (180, 180, 180)
WHITE = (230, 230, 230)
RED = (200, 0, 0)
GREEN = (0, 160, 0)
BLUE = (0, 0, 200)
DARKBLUE = (0, 0, 110)
CLARETRED = (128, 0, 0)
TURQUOISE = (48, 213, 200)
DARKGRAY = (100, 100, 100)


# Create game
pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Minesweeper")
icon = pygame.image.load("assets/images/minesweeper.png")
pygame.display.set_icon(icon)

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)
rulesFont = pygame.font.Font(OPEN_SANS, 20)
rulesFont.italic = True

# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Add images
flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))

# Create game and AI agent
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

# Keep track of revealed cells, flagged cells, and if a mine was hit
revealed = set()
flags = set()
lost = False

# Show instructions initially
instructions = True

def decideColor(game, i, j):
    nearby_mines = game.nearby_mines((i, j))
    if nearby_mines == 0:
        return ZEROBLACK
    elif nearby_mines == 1:
        return BLUE
    elif nearby_mines == 2:
        return GREEN
    elif nearby_mines == 3:
        return RED
    elif nearby_mines == 4:
        return DARKBLUE
    elif nearby_mines == 5:
        return CLARETRED
    elif nearby_mines == 6:
        return TURQUOISE
    elif nearby_mines == 7:
        return BLACK
    elif nearby_mines == 8:
        return DARKGRAY

while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)

    # Show game instructions
    if instructions:
        # Title
        title = largeFont.render("Play Minesweeper", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Rules
        rules = [
            "Click a cell to reveal it.",
            "Right-click a cell to mark it as a mine.",
            "Reveal all mine-free cells without opening a mine to win!"
        ]

        for i, rule in enumerate(rules):
            line = rulesFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)

        # Play game button
        buttonRect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
        buttonText = mediumFont.render("Play Game", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        mouse = pygame.mouse.get_pos()
        if buttonRect.collidepoint(mouse):
            pygame.draw.rect(screen, GRAY, buttonRect)
            screen.blit(buttonText, buttonTextRect)


        # Check if play button clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            if buttonRect.collidepoint(mouse):
                instructions = False
                time.sleep(0.3)
                startTime = time.time()

        pygame.display.flip()
        continue

    # Draw board
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 3)

            # Add a mine, flag, or number if needed
            if game.is_mine((i, j)) and lost:
                screen.blit(mine, rect)
            elif (i, j) in flags:
                screen.blit(flag, rect)
            elif (i, j) in revealed:
                numColor = decideColor(game, i, j)
                neighbors = smallFont.render(
                    str(game.nearby_mines((i, j))),
                    True, numColor
                )
                neighborsTextRect = neighbors.get_rect()
                neighborsTextRect.center = rect.center
                screen.blit(neighbors, neighborsTextRect)

            row.append(rect)
        cells.append(row)

    # AI Move button
    aiButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 50,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    aiButtonText = mediumFont.render("AI Move", True, BLACK)
    aiButtonRect = aiButtonText.get_rect()
    aiButtonRect.center = aiButton.center
    pygame.draw.rect(screen, WHITE, aiButton)
    screen.blit(aiButtonText, aiButtonRect)

    mouse = pygame.mouse.get_pos()
    if aiButton.collidepoint(mouse):
        pygame.draw.rect(screen, GRAY, aiButton)
        screen.blit(aiButtonText, aiButtonRect)

    # Reset button
    resButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    resButtonText = mediumFont.render("Reset", True, BLACK)
    resButtonRect = resButtonText.get_rect()
    resButtonRect.center = resButton.center
    pygame.draw.rect(screen, WHITE, resButton)
    screen.blit(resButtonText, resButtonRect)

    if resButton.collidepoint(mouse):
        pygame.draw.rect(screen, GRAY, resButton)
        screen.blit(resButtonText, resButtonRect)

    # Display text
    won = True
    if lost:
        text = "Lost"
    else:
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if not(game.is_mine((i, j))) and not((i, j) in revealed):
                    won = False
                    break
        if won:
            text = "Won"
        else:
            text = ""
    text = mediumFont.render(text, True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((5 / 6) * width, resButton.bottom + 40)
    screen.blit(text, textRect)

    # Display Time
    if not lost and not won:
        timeSoFar = time.time() - startTime
    timer = mediumFont.render(f"Time: {timeSoFar: .0f}s", True, WHITE)
    timerRect = timer.get_rect()
    timerRect.center = (5 * width / 6, textRect.bottom + 40)
    screen.blit(timer, timerRect)

    move = None

    mouse = pygame.mouse.get_pos()

    for i in range(HEIGHT):
        for j in range(WIDTH):
            if cells[i][j].collidepoint(mouse):
                pygame.draw.rect(screen, GRAY, cells[i][j])
                if (i, j) in revealed:
                    numColor = decideColor(game, i, j)
                    neighbors = smallFont.render(
                    str(game.nearby_mines((i, j))),
                    True, numColor
                    )
                    neighborsTextRect = neighbors.get_rect()
                    neighborsTextRect.center = cells[i][j].center
                    screen.blit(neighbors, neighborsTextRect)
                if (i, j) in flags:
                    screen.blit(flag, cells[i][j])
                if game.is_mine((i, j)) and lost:
                    screen.blit(mine, cells[i][j])

    left, _, right = pygame.mouse.get_pressed()

    # Check for a right-click to toggle flagging
    if right == 1 and not lost:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                    if (i, j) in flags:
                        flags.remove((i, j))
                    else:
                        flags.add((i, j))
                    time.sleep(0.2)

    elif left == 1:
        mouse = pygame.mouse.get_pos()

        # If AI button clicked, make an AI move
        if aiButton.collidepoint(mouse) and not lost:
            move = ai.make_safe_move()
            if move is None:
                move = ai.make_random_move()
                if move is None:
                    flags = ai.mines.copy()
                    print("No moves left to make.")
                else:
                    print("No known safe moves, AI making random move.")
            else:
                print("AI making safe move.")
            time.sleep(0.2)

        # Reset game state
        elif resButton.collidepoint(mouse):
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
            revealed = set()
            flags = set()
            startTime = time.time()
            lost = False
            continue

        # User-made move
        elif not lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse)
                            and (i, j) not in flags
                            and (i, j) not in revealed):
                        move = (i, j)

    # Make move and update AI knowledge
    if move:
        if game.is_mine(move):
            lost = True
        else:
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)

    pygame.display.flip()
