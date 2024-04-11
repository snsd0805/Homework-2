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

這是為了避免早期 LP 惡意抬高流動性價格，造成他人沒有能力參與提供 liquidity，舉個例子：在 ETH/DAI 流動池中，若最早的 LP 放入 1 wei + 價值 2000 ether 的 DAI，則流動性單價會高達 (1+2000*10^18)，約為 2000 eth，因此散戶若只想提供很小的流動性 1 wei，就要付出價值 2000 ether 的 DAI。這會造成流動性不足，因此價格波動會非常劇烈。

因此 Uniswap V2 限制 pool 中至少存在 MINIMUM_LIQUIDITY 流動性，因此第一次 mint LP token 時必須扣掉 MINIMUM_LIQUIDITY。

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> Solution

在 [UniswapV2Pair](https://github.com/Uniswap/v2-core/blob/ee547b17853e71ed4e0101ccfd52e70d5acded58/contracts/UniswapV2Pair.sol#L123) 的 line 123 的公式中，如果先都把 `totalSupply` 一起提出來，可以看到他要設定的 liquidity 是取 min( amount0/reserv0, amount1/reserv1)，也就是可以計算出你現在存入的 token0 是池裡所有 token0 的多少佔比，以及 token1 的佔比，最後的 liquidity 會取最小佔比的數值，例如今天存入的 token0 佔 10%、token1 佔 20 %，最終取得的 liquidity 會只有 10%。

這麼設計是因為在 uniswap 中會希望池中的兩個 token 的比例要保持恆定，例如如果是 50/50 的池就希望能一直保持 50/50 的比例。而且這樣的機制不會把多投入的 token 轉回，因此使用者必須在 mint 前事先計算好要投入的 token0, token1，以保持池中比例恆定。

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> Solution

當使用者要買入時，會把價格拉高（尤其是量大的時候），這時如果攻擊者搶先在你的訂單前先買入來拉高價格，因此你的訂單買入時會是相較更高一點的價格，而因為你買入時又把價格又拉高，此時攻擊者就可以在此時將剛剛買入的部份賣掉，因此攻擊者就能賺到中間差。

這會導致使用者實際買入的價格因為這種攻擊方式而以比預期更差的價格成交，造成額外成本，而因為攻擊者搶先在訂單前介入，因此使用者的交易也可能因此被延遲。
