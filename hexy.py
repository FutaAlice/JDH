import requests

class Pos:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def __str__(self):
        return 'Pos{row: %d, row: %d}' % (self.row, self.col)
    __repr__ = __str__

class Hexy:
    """
Usage:

h = Hexy('localhost', '8080')   # Create an instance of hexy handler

print (h.init())                # Initialize

print (h.msg_size(11))          # Specific boardsize: 11
print (h.msg_newgame())         # Start a new game

print (h.set_piece(5, 5))       # Set a hex piece at row: 5 col: 5, color red
print (h.set_and_wait(6, 5))    # Set a hex piece at row: 6 col: 5, color blue, wait for hexy move

print (h.get_gameoverflag())    # Whether game is over
print (h.get_boardsize())       # Current boardsize
print (h.get_pawnnum())         # Count of pieces on current board
print (h.get_rec())             # Query position of pieces on current board

    """
    timeout = 5
    def __init__(self, srv_host, srv_port):
        self.__host = str(srv_host)
        self.__port = str(srv_port)
        
    def __url(self, path):
        return 'http://' + self.__host + ':' + self.__port + str(path)
        
    def __log(self, response):
        print ('')
        print (response.request.method, response.url)
        if response.request.method == 'POST':
            print (response.request.body)
        print (response.status_code, response.reason)
        print (response.json())
        
    def __success(self, response):
        return response.status_code == 200 and response.json()['errCode'] == 200
        
    def init(self):
        r = requests.get(self.__url('/init'), timeout=self.timeout)
        self.__log(r)
        return self.__success(r)
        
    def set_piece(self, row, col):
        r = requests.post(self.__url('/set/piece'), json={
            'row': row,
            'col': col,
        }, timeout=self.timeout)
        self.__log(r)
        return self.__success(r)
        
    def set_and_wait(self, row, col):
        r = requests.post(self.__url('/set/wait'), json={
            'row': row,
            'col': col,
        }, timeout=self.timeout)
        self.__log(r)
        return self.__success(r), Pos(r.json()['row'], r.json()['col'])
        
    def get_rec(self):
        r = requests.get(self.__url('/get/rec'), timeout=self.timeout)
        self.__log(r)
        return self.__success(r), [Pos(x['row'], x['col']) for x in r.json()['records']]
        
    def get_pawnnum(self):
        r = requests.get(self.__url('/get/pawnnum'), timeout=self.timeout)
        self.__log(r)
        return self.__success(r), r.json()['num']
        
    def get_boardsize(self):
        r = requests.get(self.__url('/get/boardsize'), timeout=self.timeout)
        self.__log(r)
        return self.__success(r), r.json()['boardsize']
        
    def get_gameoverflag(self):
        r = requests.get(self.__url('/get/gameoverflag'), timeout=self.timeout)
        self.__log(r)
        return self.__success(r), r.json()['gameover']
        
    def msg_newgame(self):
        r = requests.get(self.__url('/msg/newgame'), timeout=self.timeout)
        self.__log(r)
        return self.__success(r)
        
    def msg_newgame(self):
        r = requests.get(self.__url('/msg/newgame'), timeout=self.timeout)
        self.__log(r)
        return self.__success(r)
        
    def msg_size(self, size):
        r = requests.post(self.__url('/msg/size'), json={
            'size': size,
        }, timeout=self.timeout)
        self.__log(r)
        return self.__success(r)
        
    
# test
if __name__ == "__main__":
    print (Hexy.__doc__)
    
    h = Hexy('localhost', '8080')   # Create an instance of hexy handler

    print (h.init())                # Initialize

    print (h.msg_size(11))          # Specific boardsize: 11
    print (h.msg_newgame())         # Start a new game

    print (h.set_piece(5, 5))       # Set a hex piece at row: 5 col: 5, color red
    print (h.set_and_wait(6, 5))    # Set a hex piece at row: 6 col: 5, color blue, wait for hexy move

    print (h.get_gameoverflag())    # Whether game is over
    print (h.get_boardsize())       # Current boardsize
    print (h.get_pawnnum())         # Count of pieces on current board
    print (h.get_rec())             # Query position of pieces on current board
    