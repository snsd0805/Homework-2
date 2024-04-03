# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Solution

Profitable Path: 
```
tokenB->tokenA->tokenC->tokenE->tokenD->tokenC->tokenB
```

the amountIn, amountOut value for Each Swap:
```
5 tokenB ->
5.655321988655323 tokenA ->
2.372138936383089 tokenC ->
1.530137136963617 tokenE ->
3.4507414486197083 tokenD ->
6.684525579572587 tokenC ->
22.497221806974142 tokenB
```

My final Reward:
```
22.497221806974142 tokenB
```

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Solution

slippage 指的是交易時的預期價格跟實際成交時的價格之間的落差，通常是交易量較大且交易所流動性較低的情況或者交易市場屬於高波動性。
而 AMM 的交易價格是根據恆定乘積，例如 Uniswap: x*y=k 的方式定價，因此當某一方 token 被大量買入時，因為 x, y 數量變動，會造成其價格波動，因此實際交易價格跟你預期的價格不同，造成滑價。

從 [Uniswap Help Center](https://support.uniswap.org/hc/en-us/articles/7421987762829-Swap-errors-Advanced) 查詢到，如果在 Uniswap V2 中要避免 slippage，`The Uniswap protocol routers have a minimum output and a maximum input variable.`，因此我們可以在交易時在呼叫 router 時加入 minimum output 參數來要求若實際交易價格超出預期價格就 revert，例如在 [`UniswapV2Router02.sol`](https://github.com/Uniswap/v2-periphery/blob/0335e8f7e1bd1e8d8329fd300aea2ef2f36dd19f/contracts/UniswapV2Router02.sol#L224) 中的 `swapExactTokensForTokens()` 就有一個參數 `amountOutMin` 可以設定最小輸出 token 數量，在 line 232 有設定一個 require 要求由 `UniswapV2Library` 估算得到的量不能小於 `amountOutMin`。 

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> Solution

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> Solution

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> Solution

