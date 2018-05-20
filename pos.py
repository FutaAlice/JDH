
class Pos:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def __str__(self):
        return 'Pos{row: %d, row: %d}' % (self.row, self.col)
    __repr__ = __str__
