# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1

Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

```
path: tokenB->tokenA->tokenD->tokenC->tokenB, tokenB balance=20.129888944077443
Starts with 5 tokenB
Execution result: 5 tokenB -> 5.655321988655322 tokenA
Execution result: 5.655321988655322 tokenA -> 2.4587813170979333 tokenD
Execution result: 2.4587813170979333 tokenD -> 5.0889272933015155 tokenC
Execution result: 5.0889272933015155 tokenC -> 20.129888944077443 tokenB
```

## Problem 2

What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Solution
> Slippage is the price difference between the actual execution price and the price we got by dividing two reserves in the pool,
> it happens because (X-dx)(Y+dy) = (X)(Y) = K, dy/dx will never be the same as Y/X, but increasing the X and Y value makes dy/dx closer to Y/X, thus
> decreasing the slippage in every swap, to increase X and Y, uniswap v2 has a functionality called add liquidity where people provide liquidity as X and Y and
> gain trading fees from it, sometimes even incentivicing the liquidity providors with governance tokens such as sushiswap.

## Problem 3

Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> Solution
> As the code I copied from the UniswapV2Pair.sol source code, it subtracts 10\**3 of the liquidity. The rationale is that you have to keep at least something larger than
> 0 in reserve. If they don't do so, when EVERY SINGLE liquidity provider pulled the liquidity out, they'll loss track of the X*Y=K value since 0 times 0 equals 0, if there's a
> little bit reserve left, they can still preserve the K state variable.

```solidity
 function mint(address to) external lock returns (uint liquidity) {
        (uint112 _reserve0, uint112 _reserve1,) = getReserves(); // gas savings
        uint balance0 = IERC20(token0).balanceOf(address(this));
        uint balance1 = IERC20(token1).balanceOf(address(this));
        uint amount0 = balance0.sub(_reserve0);
        uint amount1 = balance1.sub(_reserve1);

        bool feeOn = _mintFee(_reserve0, _reserve1);
        uint _totalSupply = totalSupply; // gas savings, must be defined here since totalSupply can update in _mintFee
        if (_totalSupply == 0) {
            liquidity = Math.sqrt(amount0.mul(amount1)).sub(MINIMUM_LIQUIDITY);
           _mint(address(0), MINIMUM_LIQUIDITY); // permanently lock the first MINIMUM_LIQUIDITY tokens
        } else {
            liquidity = Math.min(amount0.mul(_totalSupply) / _reserve0, amount1.mul(_totalSupply) / _reserve1);
        }
        require(liquidity > 0, 'UniswapV2: INSUFFICIENT_LIQUIDITY_MINTED');
        _mint(to, liquidity);

        _update(balance0, balance1, _reserve0, _reserve1);
        if (feeOn) kLast = uint(reserve0).mul(reserve1); // reserve0 and reserve1 are up-to-date
        emit Mint(msg.sender, amount0, amount1);
    }
```

## Problem 4

Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> Solution
> From the code I pasted above, it's basically the minimum of two reserve change percentage, since addking liquidity needs to
> fit the current ratio, so the change in two reserves needs to be the same percentage, they calculate the two new amounts delta and divide it with the original reserve
> for example if we get 0.001% change on token 0 vs 0.00095% token change on token 1, we can only take 0.0095% change on token 0 too, in order to not disrupt the original ratio
> after the calculation, they'll call mint function to finish the process.

## Problem 5

What is a sandwich attack, and how might it impact you when initiating a swap?

> Solution:
> Sandwich attack is a kind of onchain MEV attack where the attacker manipulates the price of the pair that the victim is trading, letting the victim's swap transaction incur more slippage than usual, extracting the value.
> Sandwich attack needs very fast computation and some bribing to the validators. Specifically here's how it often happens:
>
> 1. Victim sends a tx with the intention of swapping a token to another token with a MaxAmountIn or MinAmountOut parameter, indicating the tx's worst acceptable execution ptice.
> 2. The attacker sees the tx in the mempool before it got confirmed, generates another tx that pushes the price up/down against the victim, and bribe the validators to include that transaction before the victim's tx.
> 3. The attacker then generates their second tx and proceeds to flush out the holdings they just got, netting profits.
