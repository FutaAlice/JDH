import pos
import zobrist

Pos     = pos.Pos
Color   = zobrist.Color
Board   = zobrist.Board

class DFS:
    def __init__(self, board, depth):
        self.__board = board
        self.__depth = depth
        
    def run(self):
        self.cnt = 0
        self.hash = set()
        self.__dfs(0, self.__board)
        
    def __dfs(self, current_depth, current_board):
        # set counter
        self.cnt += 1
    
        # do something.
        # print ('depth', current_depth, '/', self.__depth)
        # print (current_board)
        
        # check depth
        if current_depth >= self.__depth:
            return
        
        # for each empty position
        for point in current_board.empty_points():
            current_board.set(point.row, point.col)
            
            # check hash
            u32, u64 = current_board.hash()
            hashstr = str(u32) + '.' + str(u64)
            # print (hashstr)
            if hashstr in self.hash:
                # reset
                current_board.reset(point.row, point.col)
                continue
            else:
                self.hash.add(hashstr)
            
            # recursive
            self.__dfs(current_depth + 1, current_board)
            
            # reset
            current_board.reset(point.row, point.col)
        
# test
if __name__ == "__main__":
    b = Board(4)
    
    s = DFS(b, 99)
    s.run()
    print (s.cnt)
