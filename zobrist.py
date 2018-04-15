import enum
import json

import generator

with open(generator.FILE_NAME) as f:
    contents = f.read()
JSON_OBJ = json.loads(contents)

# Color = enum.Enum('Color', ('Empty', 'Red', 'Blue'))
class Color(enum.Enum):
    Empty = 0
    Red = 1
    Blue = 2

"""
Usage

# Create an empty 5*5 hex board
b = Board(5)

# next player's color
color = b.next

# next player set a piece at (row:0, col:2)
b.set(0, 2)

# specific piece color
b.force_set(2, 2, Color.Red)

# withdraw
b.reset(0, 2)

"""
class Board:
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
                
                red32.append(JSON_OBJ[key_red]['u32'])
                red64.append(JSON_OBJ[key_red]['u64'])
                blue32.append(JSON_OBJ[key_blue]['u32'])
                blue64.append(JSON_OBJ[key_blue]['u64'])
                
            self.__hashtable32[Color.Red].append(red32)
            self.__hashtable64[Color.Red].append(red64)
            self.__hashtable32[Color.Blue].append(blue32)
            self.__hashtable64[Color.Blue].append(blue64)
            
        print (self.__hashtable32, self.__hashtable64)
        
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
        
    def hash32(self):
        hash = 0
        for row in range(self.__size):
            for col in range(self.__size):
                color = self.status[row][col]
                if not color is Color.Empty:
                    hash ^= self.__hashtable32[color][row][col]
        return hash
        
    def hash64(self):
        hash = 0
        for row in range(self.__size):
            for col in range(self.__size):
                color = self.status[row][col]
                if not color is Color.Empty:
                    hash ^= self.__hashtable64[color][row][col]
        return hash
        
# test
if __name__ == "__main__":

    fuck = Board(5)
    print (fuck.hash32())
    fuck.force_set(0, 3, Color.Red)
    fuck.set(0, 0)
    print (fuck.hash32(), fuck.hash64())
    print (fuck)
