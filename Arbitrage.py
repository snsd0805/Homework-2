liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25), }

class Queue():
    def __init__(self, init_values=[]):
        self.queue = init_values

    def push(self, value):
        self.queue.append(value)

    def pop(self):
        return self.queue.pop()

    def isEmpty(self):
        return len(self.queue) == 0

def getNext(token_in, pairs):
    ans = []
    for pair, value in pairs.items():
        token0, token1 = pair[0], pair[1]
        if token0 == token_in:
            ans.append((token1, pair))
        elif token1 == token_in:
            ans.append((token0, pair))
    ans.reverse()
    return ans

def findArb(pairs, token_in, token_out):
    queue = Queue([(token_in, [], pairs.copy())])
    circles = []
    tmp_token_in = token_in

    while not queue.isEmpty():
        tmp_token_out, path, new_pairs = queue.pop()
        # print(tmp_token_out, path, new_pairs)
        path = path + [tmp_token_out]
        if tmp_token_out == token_out and len(path) > 2:
            circles.append(path)
        else:
            nexts = getNext(tmp_token_out, new_pairs)
            for _token, _pair in nexts:
                # print("   ", _token, _pair)
                next_pairs = new_pairs.copy()
                next_pairs.pop(_pair)
                queue.push((_token, path, next_pairs))

    return circles

def calculate_new_token(path, number):
    previous_token = path[0]
    for token in path[1:]:
        if previous_token[5] < token[5]:
            token0, token1 = previous_token, token
            balance = liquidity[(token0, token1)]
            Rx, Ry = balance[0], balance[1]
        else:
            token0, token1 = token, previous_token
            balance = liquidity[(token0, token1)]
            Rx, Ry = balance[1], balance[0]
        number = (Ry * 0.997 * number) / (Rx + 0.997 * number)
        previous_token = token
    return number

circles = findArb(liquidity, 'tokenB', 'tokenB')
max_token = 0
max_path = []
for i in circles:
    new_token_number = calculate_new_token(i, 5)
    if new_token_number > max_token:
        max_token = new_token_number
        max_path = i

print("path: ", end='')
for i in max_path[:-1]:
    print(f"{i}->", end='')
print(f"{max_path[-1]}, tokenB balance={max_token}")

