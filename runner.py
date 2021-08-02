
import pygame
import sys
import time

from minesweeper import Minesweeper, MinesweeperAI

HEIGHT = 8
WIDTH = 8
MINES = 8

# 颜色

BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)


# 创建游戏

pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)
 

# 字体

OPEN_SANS = "assets/fonts/simkai.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)


# 计算面板尺寸

BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)


# 添加图片

flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))


# 创建游戏和 AI 代理

game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)


# 跟踪显示的单元格、标记的单元格以及是否被地雷击中

revealed = set()
flags = set()
lost = False


# 最初显示说明

instructions = True

while True:

    # 检查游戏是否退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)

    # 显示游戏说明

    if instructions:

        # 标题
        title = largeFont.render("海拥 | 扫雷", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Rules
        rules = [
            "单击一个单元格以显示它",
            "右键单击一个单元格以将其标记为地雷",
            "成功标记所有地雷以获胜！"
        ]
        for i, rule in enumerate(rules):
            line = smallFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)

        # 开始游戏按钮
        
        buttonRect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
        buttonText = mediumFont.render("开始游戏", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        # 检查是否点击播放按钮
        
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse):
                instructions = False
                time.sleep(0.3)

        pygame.display.flip()
        continue

    # 画板
    
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # 为单元格绘制矩形
            
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 3)

            # 如果需要，添加地雷、旗帜或数字
            
            if game.is_mine((i, j)) and lost:
                screen.blit(mine, rect)
            elif (i, j) in flags:
                screen.blit(flag, rect)
            elif (i, j) in revealed:
                neighbors = smallFont.render(
                    str(game.nearby_mines((i, j))),
                    True, BLACK
                )
                neighborsTextRect = neighbors.get_rect()
                neighborsTextRect.center = rect.center
                screen.blit(neighbors, neighborsTextRect)

            row.append(rect)
        cells.append(row)

    
    # AI 移动按钮
    
    aiButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 50,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("AI 移动", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = aiButton.center
    pygame.draw.rect(screen, WHITE, aiButton)
    screen.blit(buttonText, buttonRect)

    
    # 重置按钮
    
    resetButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("重置", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = resetButton.center
    pygame.draw.rect(screen, WHITE, resetButton)
    screen.blit(buttonText, buttonRect)

    
    # 显示文字
    
    text = "失败" if lost else "获胜" if game.mines == flags else ""
    text = mediumFont.render(text, True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((5 / 6) * width, (2 / 3) * height)
    screen.blit(text, textRect)

    move = None

    left, _, right = pygame.mouse.get_pressed()

    
    # 检查右键单击以切换标记
    
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

        

        # 如果单击 AI 按钮，则进行 AI 移动
        
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

        # 重置游戏状态
        
        elif resetButton.collidepoint(mouse):
            
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
            revealed = set()
            flags = set()
            lost = False
            continue

        # 用户自定义动作
        
        elif not lost:
            
            for i in range(HEIGHT):
                
                for j in range(WIDTH):
                    
                    if (cells[i][j].collidepoint(mouse)
                            and (i, j) not in flags
                            and (i, j) not in revealed):
                        move = (i, j)

    # 行动起来，更新AI知识
    
    if move:
        
        if game.is_mine(move):
            lost = True
        
        else:
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)

    
    pygame.display.flip()
