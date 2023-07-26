# IMC's Prosperity Trading Challenge

Welcome to the official GitHub repository of team Shiro!

*Highest rank: 45th of 7007 teams*

Prosperity is a 10-day global trading challenge, consisting of 5 rounds, hosted by IMC Trading. For each round, a new product is released with its own characteristics and price action that guide profitable strategies. Teams are challenged to combine Python skills, strategic insight, and analytics to trade on a virtual market and bring their island to prosperity.

We, a team of three penultimate students, managed to reach our final rank of 79th among 7007 global teams. We would love to present our strategies and analysis across this challenging competition.

### Team member:
- Dat Su depzai
- Long bu c thang duoi
- Moe bi thang tren bu

<br>

## Round 1

Pearls and Bananas are two products introduced in the first round and we work on them separately.

For Pearls, it always stays in a range of [9995, 10000] and has a stable mean of 10000. There are times when the best bid is 10002 or the best ask is 9998. Therefore we market-take any ask below 10000, and accept any bid above 10000.

<p align="center">
  <span style="display: inline-block; border: 1px solid #ccc; border-radius: 8px;">
    <img src="analysis/Pearls.png" alt="Pearls" width="700">
  </span>
</p>

For Bananas, the bid and ask price always have a consistent gap and some spikes occur occasionally. We use a method that tracks a simple exponential smoothing (unlike a moving average, the weights attached to the observations decrease exponentially as we go back in time) and cut through the spikes. Whenever it cut a spike, we enter a trade.

Midpoint price is defined by:
$$price_t = \frac{bestask_t + bestbid_t}{2}$$

Simple Exponential Smoothing Equation:
$$l_t = a*mid_t + (1-a)*l_{t-1},$$
<p align="center"> where $a = 0.077$, $l_0 = 4950$ </p>

The rate at which the weights decrease is controlled by the parameter $a$, which is chosen by running simulated tests to maximise profit. We market-take orders with prices that pass through the SEM line plus an additional range (avoid some spikes that barely pass). This results in a high-frequency trading strategy.

<p align="center">
  <span style="display: inline-block; border: 1px solid #ccc; border-radius: 8px;">
    <img src="analysis/bananas.png" alt="Bananas" width="700">
  </span>
</p>



<br>

## Round 2

New products in this round are Coconuts and Pina Coladas. Unlike round 1, Coconuts and Pina Coladas are pair-traded as they are correlated with each other. Our volatility-based pair-trading strategy begins with standardising their price (midpoint of bid and ask) and their variance.

Standardising equation:
$$z_t=\frac{price_t + \overline{price}}{\sigma} \sim (0,1)$$

Next, we compute the 20-step moving average for each product and use it to identify any widened gap larger than 0.3. The moving average helps smooth out volatility-induced fluctuations.

$$| MA20_{coco, t} - MA20_{pina, t} | > 0.3$$

We also calculate the percentage change of the 200-step moving average at time $t$ with time $t-j$ for $j = 20, 40,..., 200$. The $MA200$ has been averaged between Coconuts and Pina Coladas. These percentage changes are then used to determine the number of intervals with increasing and decreasing trends.

$$Percentage Change_{t,j} = \frac{MA200_{t} - MA200_{t-j}}{MA200_{t-j}}$$

$$N_{increase} = \sum_{j=20, 40, \ldots, 200} \mathbb{I}({Percentage Change}_{t,j} > 0)$$

$$N_{decrease} = \sum_{j=20, 40, \ldots, 200} \mathbb{I}({Percentage Change}_{t,j} < 0)$$

<p align="center">
  where $\mathbb{I}(x)$ is the indicator function, which returns 1 if the condition $x$ is met, and 0 otherwise.
</p>

The trend is identified as bullish when $N_{increase}>6$, and as bearish when $N_{decrease}>6$.

In simple pair trading, whenever the gap is observed, we long the product with a higher price and short the other. However, in this case, we implement a trend indication as an additional condition. Now, we only go long if the trend is upward and go short if the trend is downward.



<br>

## Round 3



<br>

## Round 4



<br>

## Round 5



<br>

