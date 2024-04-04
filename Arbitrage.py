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
    ("tokenD", "tokenE"): (60, 25),
}
newLq = dict()
for x, y in liquidity.items():
    newLq[x] = y
    newLq[(x[1], x[0])] = (y[1], y[0])
# for x, y in newLq.items():
#     print(x, y)


def getAmountOut(amountIn, reserveIn, reserveOut):
    amountInWithFee = amountIn * 997
    numerator = amountInWithFee * reserveOut
    denominator = reserveIn * 1000 + amountInWithFee
    return numerator / denominator


def swap(tokenIn, tokenOut, amountIn, _liquidity):
    if (tokenIn == tokenOut):
        return amountIn
    amountOut = getAmountOut(amountIn, _liquidity[(
        tokenIn, tokenOut)][0], _liquidity[(tokenIn, tokenOut)][1])
    outFinal = _liquidity[(tokenIn, tokenOut)][1] - amountOut
    inFinal = _liquidity[(tokenIn, tokenOut)][0] + amountIn
    _liquidity[(tokenIn, tokenOut)] = (inFinal, outFinal)
    _liquidity[(tokenOut, tokenIn)] = (outFinal, inFinal)
    return amountOut

# performs a bfs search to all pairs


N = 1


def bfs(inputToken, currentAmountIn, path, liquidityState, res):
    global N
    if inputToken == "tokenB" and path:
        path = ["tokenB"] + path
        res.append((path, currentAmountIn))
        return
    for (ipt, opt) in liquidityState.keys():
        if ipt == inputToken and path.count(opt) < N:
            p = path.copy()
            l = liquidityState.copy()
            p.append(opt)
            outAmount = swap(ipt, opt, currentAmountIn, l)
            bfs(opt, outAmount, p, l, res)


def simulateSwap(path, amountIn, liquidity):
    print(f"Starts with {amountIn} {path[0]}")
    lastAmt = amountIn
    for i in range(len(path)-1):
        lastAmt = amountIn
        amountIn = swap(path[i], path[i+1], amountIn, liquidity)
        print(
            f"Execution result: {lastAmt } {path[i]} -> {amountIn} {path[i+1]}")


res = list()
bfs("tokenB", 5, [], newLq, res)
res.sort(key=lambda x: x[1], reverse=True)
bestRoute = res[0][0]
bestAmountOut = res[0][1]
print(f"path: {'->'.join(bestRoute)}, tokenB balance={bestAmountOut}")
# print(f"    address[] memory route = new address[]({len(bestRoute)});")
# for i in range(len(bestRoute)):
#     print(f"    route[{i}] = address({bestRoute[i]});")

# simulateSwap(bestRoute, 5, newLq.copy())
