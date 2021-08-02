'''

扫雷

扫雷是一款单人益智游戏。游戏的目标是清除
包含隐藏的“地雷”或炸弹的矩形板，而不引爆其中
任何一个，借助每个区域中相邻地雷数量的线索。


'''

# 导入库

import itertools
import random


class Minesweeper():
    

    """
    扫雷游戏表示
    
    """

    def __init__(self, height=8, width=8, mines=8):

        
        # 设置初始宽度、高度和地雷数量
        
        self.height = height
        self.width = width
        self.mines = set()

        # 初始化一个没有地雷的空字段
        
        self.board = []
        
        for i in range(self.height):
            row = []
            
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # 随机添加地雷
        
        while len(self.mines) != mines:
            
            i = random.randrange(height)
            j = random.randrange(width)
            
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # 最开始，玩家没有发现地雷
        
        self.mines_found = set()

    def print(self):
        
        """
        输出地雷所在位置的基于文本的表示。
        
        """
        
        for i in range(self.height):
            print("--" * self.width + "-")
            
            for j in range(self.width):
                
                if self.board[i][j]:
                    print("|X", end="")
                
                else:
                    print("| ", end="")
            print("|")
        
        print("--" * self.width + "-")

    
    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        返回给定单元格的一行和一列内的地雷数，不包括单元格本身。
        """

        # 保持附近地雷的数量
        count = 0

        # 遍历一行和一列内的所有单元格
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # 忽略单元格本身
                if (i, j) == cell:
                    continue

                # 如果单元格在边界内并且是地雷，则更新计数
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        检查是否已标记所有地雷。
        """
        return self.mines_found == self.mines


class Sentence():
    
    """
    关于扫雷游戏的逻辑语句 
    一个句子由一组棋盘单元和这些单元格的数量组成。
    
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        
        """
        返回 self.cells 中已知为地雷的所有单元格的集合。
        
        """
        
        if len(self.cells) == self.count:
            return self.cells

    def known_safes(self):
        
        """
        返回 self.cells 中已知安全的所有单元格的集合。
        
        """
        
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        
        """
        鉴于已知单元格是地雷，更新内部知识表示。
        
        """
        
        if cell in self.cells:
            self.cells.discard(cell)
            self.count -= 1

    def mark_safe(self, cell):
        
        """
        鉴于已知单元格是安全的，更新内部知识表示。
        
        """
        
        if cell in self.cells:
            self.cells.discard(cell)
 

class MinesweeperAI():
   
    """
    扫雷游戏玩家
    
    """

    def __init__(self, height=8, width=8):

        # 设置初始高度和宽度
        
        self.height = height
        self.width = width

        # 跟踪点击了哪些单元格
        
        self.moves_made = set()

        # 跟踪已知安全或地雷的细胞
        
        self.mines = set()
        self.safes = set()

        # 关于已知为真游戏的句子列表
        
        self.knowledge = []


    def mark_mine(self, cell):
        
        """
        将一个单元格标记为地雷，并更新所有知识以将该单元格也标记为地雷。
        
        """
        
        self.mines.add(cell)
        
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        
        """
        将一个单元格标记为安全，并更新所有知识以将该单元格也标记为安全。
        
        """
        
        self.safes.add(cell)
        
        for sentence in self.knowledge:
            sentence.mark_safe(cell)


    def nearby_cells(self, cell):
        
        """
        用于获取所有附近的单元格
        
        """
        cells = set()

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                if (i, j) == cell:
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:
                    cells.add((i, j))

        return cells

    def add_knowledge(self, cell, count):
        
        """
        
        当扫雷板告诉我们，对于给定的安全单元，有多少相邻单元中有地雷时调用。

         这个功能应该：
             1）将单元格标记为已进行的移动
             2）将单元格标记为安全
             3）在AI的知识库中增加一个新的句子
                基于 `cell` 和 `count` 的值
             4）将任何额外的细胞标记为安全或地雷
                如果可以根据人工智能的知识库得出结论
             5) 将任何新句子添加到 AI 的知识库中
                如果它们可以从现有知识中推断出来
        
        """
        
        self.moves_made.add(cell)

        # 标记单元格安全

        if cell not in self.safes:    
            self.mark_safe(cell)

        
        # 获取所有附近的单元格

        nearby = self.nearby_cells(cell)       

        nearby -= self.safes | self.moves_made     

        new_sentence = Sentence(nearby, count)

        self.knowledge.append(new_sentence)

        new_safes = set()
        new_mines = set()

        for sentence in self.knowledge:
            
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)
            
            else:
                tmp_new_safes = sentence.known_safes()
                tmp_new_mines = sentence.known_mines()

                
                if type(tmp_new_safes) is set:
                    new_safes |= tmp_new_safes

                
                if type(tmp_new_mines) is set:
                    new_mines |= tmp_new_mines

        
        for safe in new_safes:
            self.mark_safe(safe)

        
        for mine in new_mines:
            self.mark_mine(mine)

        

        prev_sentence = new_sentence

        new_inferences = []

        for sentence in self.knowledge:
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)

            elif prev_sentence == sentence:
                break
            elif prev_sentence.cells <= sentence.cells:
                inf_cells = sentence.cells - prev_sentence.cells
                inf_count = sentence.count - prev_sentence.count

                new_inferences.append(Sentence(inf_cells, inf_count))

            prev_sentence = sentence

        self.knowledge += new_inferences

    def make_safe_move(self):
        

        """
        返回一个安全的单元格以在扫雷板上选择。
         必须知道移动是安全的，而不是已经移动
         那已经完成了。

         这个函数可能会用到self.mines、self.safes中的知识
         和 self.moves_made，但不应修改任何这些值。
        """
        
        safe_moves = self.safes.copy()

        safe_moves -= self.moves_made

        if len(safe_moves) == 0:
            return None

        return safe_moves.pop()


    def make_random_move(self):
        

        """
        
        返回要在扫雷板上进行的移动。
         应该在以下单元格中随机选择：
             1) 尚未被选中，并且
             2) 不知道是地雷
        

        """
        

        if len(self.moves_made) == 56:
            return None

        random_move = random.randrange(self.height), random.randrange(self.height)

        not_safe_moves = self.moves_made | self.mines

        while random_move in not_safe_moves:
            random_move = random.randrange(self.height), random.randrange(self.height)

        return random_move
