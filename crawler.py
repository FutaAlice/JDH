import redis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
DB = [None for _ in range(4)] + [redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=i) for i in range(16)]

def init_once():
    for index in range(4, 20): DB[index].set('boardsize', index)

def check_at_start():
    print ('checking redis database...')
    for index in range(4, 20):
        print (DB[index].get('boardsize').decode())
        if DB[index].get('boardsize').decode() != str(index):
            print ('fail!')
            return
    print ('success')
        
# main
if __name__ == "__main__":
    check_at_start()
    pass
