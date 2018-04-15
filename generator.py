import json
import random
import time

FILE_NAME = 'config.json'

record = set()
def rand_unique(l, r):
    while True:
        time.sleep(0.003)
        random.seed(time.time() * 1000)
        num = random.randint(l, r)
        if not num in record:
            break    
    record.add(num)
    return num
    
def check():
    with open(FILE_NAME) as f:
        contents = f.read()
    json_obj = json.loads(contents)
    unique = set()
    for k, v in json_obj.items():
        u64, u32 = v['u64'], v['u32']
        if u64 in unique or u32 in unique or u64 == u32:
            print (k)
            return False
    return True
    
# main
if __name__ == "__main__":
    data = dict()
    for i in range(0, 1000):
        item = {
            'u32': rand_unique(0, 0xFFFF),
            'u64': rand_unique(0, 0xFFFFFFFF),
        }
        data[str(i).zfill(3)] = item

    json_str = json.dumps(data, sort_keys=True, indent=4)

    print ('Writting to output file:', FILE_NAME)
    with open(FILE_NAME, 'w') as f:
        f.write(json_str)
        
print ('Checking data:', check())