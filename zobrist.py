import enum
import json

import generator
import pos

with open(generator.FILE_NAME) as f:
    contents = f.read()
JSON_OBJ = json.loads(contents)

Pos = pos.Pos

# Color = enum.Enum('Color', ('Empty', 'Red', 'Blue'))
class Color(enum.Enum):
    Empty = 0
    Red = 1
    Blue = 2

class Board:
    """
Usage

b = Board(5)                    # Create an empty 5*5 hex board
color = b.color()               # Get next player's color
b.set(0, 2)                     # Next player set a piece at (row:0, col:2)
b.reset(0, 2)                   # Withdraw
b.force_set(2, 2, Color.Red)    # Specific piece color
u32, u64 = b.hash()             # 32bit Zobrist-Hashing of current status
    
    """
    def __init__(self, size):
        self.status = [[Color.Empty for _ in range(size)] for _ in range(size)]
        self.__size = size
        
        self.__hashtable32 = { Color.Red: [], Color.Blue: [] }
        self.__hashtable64 = { Color.Red: [], Color.Blue: [] }
        
        for row in range(size):
            red32, red64, blue32, blue64 = [], [], [], []
            for col in range(size):
                index = row * size + col
                
                key_red  = str(index * 2 + 0).zfill(3)
                key_blue = str(index * 2 + 1).zfill(3)
                
                red32.append(int(JSON_OBJ[key_red]['u32']))
                red64.append(int(JSON_OBJ[key_red]['u64']))
                blue32.append(int(JSON_OBJ[key_blue]['u32']))
                blue64.append(int(JSON_OBJ[key_blue]['u64']))
                
            self.__hashtable32[Color.Red].append(red32)
            self.__hashtable64[Color.Red].append(red64)
            self.__hashtable32[Color.Blue].append(blue32)
            self.__hashtable64[Color.Blue].append(blue64)
            
        # print ("red:")
        # for line in self.__hashtable64[Color.Red]:
        #     print (line)
        # print ("blue:")
        # for line in self.__hashtable64[Color.Blue]:
        #     print (line)
        
    def __str__(self):
        charset = { Color.Blue: 'b', Color.Red: 'r', Color.Empty: '_' }
        ret = ''
        for line in self.status:
            for color in line:
                ret += charset[color]
                ret += ' '
            ret += '\n'
        return ret
        
    __repr__ = __str__
        
    def color(self):
        cnt = 0
        for line in self.status:
            for color in line:
                if not color is Color.Empty: cnt += 1
        return cnt % 2 and Color.Blue or Color.Red
        
    def reset(self, row, col):
        self.status[row][col] = Color.Empty
        
    def set(self, row, col):
        if not self.status[row][col] is Color.Empty:
            raise RuntimeError('pos(row:%2d, col:%2d) not empty.' % (row, col))
        self.status[row][col] = self.color()
        
    def force_set(self, row, col, color):
        if not isinstance(color, Color):
            raise TypeError('type of color:', type(color), 'unexpected.')
        self.status[row][col] = color
        
    def hash(self):
        hash32, hash64 = 0, 0
        for row in range(self.__size):
            for col in range(self.__size):
                color = self.status[row][col]
                if not color is Color.Empty:
                    hash32 ^= self.__hashtable32[color][row][col]
                    hash64 ^= self.__hashtable64[color][row][col]
        return hash32, hash64
        
    def empty_points(self):
        points = list()
        for row in range(self.__size):
            for col in range(self.__size):
                color = self.status[row][col]
                if color is Color.Empty:
                    points.append(Pos(row, col))
        return points
        
# test
if __name__ == "__main__":

    b = Board(5)                    # Create an empty 5*5 hex board
    color = b.color()                  # Get next player's color
    b.set(0, 2)                     # Next player set a piece at (row:0, col:2)
    b.reset(0, 2)                   # Withdraw
    b.force_set(2, 2, Color.Red)    # Specific piece color
    u32, u64 = b.hash()             # 32bit Zobrist-Hashing of current status
    print (u32, u64)
    
    print (b.empty_points())
    
    print (b)
