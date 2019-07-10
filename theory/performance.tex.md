# Performance

## Symbolic calculations

### Variable definitions

* The Spark job will run every $T$ seconds, therefore it will run $t$ times per second.
* There are *a* assets being considered.
* The Monte Carlo will probe *p* candidate portfolios at each trigger.

Asset price movements are assumed to be represented by a biased random walk with continuous values (percent change in price) and infinitely small step size. Under this model, the percent change of an asset after $\theta$ seconds will follow a normal distribution $N(\mu, \sigma)$ where $\mu \sim \theta$ and $\sigma \sim \sqrt{\theta}$. We normalize both to 1 a second interval, and get:

* Asset reward $g = \mu / \theta$, representing the average expected % increase in price after 1 second.
* Asset risk $r = \sigma / \sqrt{\theta}$, representing the average expected % spread of price after 1 second.
* Asset z-score $z = \frac{\mu / \theta}{\sigma / \sqrt(\theta)}$ representing normalized average expected change in price after 1 second.

### Asset summary

For a list $u$ containing $n$ prices, calculating the reward has complexity $O(n)$ - every element must be added up. However, if the initial mean $\mu_i$ of $u$  is known, pushing a new element $x$ does not necessitate redoing the entire calculation. We can calculate the new mean $\mu_f$ in $O(1)$ time:

$\mu_f = \frac{n \cdot \mu_i + x}{n+1}$

If $\mu_i$, $\mu_f$ and previous standard deviation $\sigma_i$ are known, we can also utilize a [fast algorithm](https://math.stackexchange.com/a/1362467) to obtain the new standard deviation:

$v_f = \frac{(x-\mu_f)^2}{n+1} + \frac{n\cdot v_i}{n+1} + \frac{n}{n+1}\delta^2 $ where $ v = \sigma ^2$ and $\delta=\mu_f-\mu_i$

Although the equation appears daunting, the running time is constant with respect to $n$.

For an entire universe of assets, we will make these calculations $a \cdot t$ times per second, and make $a \cdot t$ writes to Redis. During portfolio evaluation phase, every portfolio will need the entire table of asset summaries, generating $p \cdot t$ reads per second.

### Random portfolio generation

Generating a vector of weights will scale linearly with $a \cdot p$. Writing each portfolio vector separately will incur $p \cdot t$ writes per second. Evaluating the portfolios will incur $p\cdot t$ reads.

### Portfolio summary

For each portfolio, we will retrieve the entire asset summary table. This will generate $p \cdot t$ reads and $p \cdot t$ writes (to record portfolio summaries).

## Numeric examples

### Cryptocurrencies

If we take a reasonable estime of:

* Spark job 1/sec

* $a=100$ cryptocoins

* $p = 1000$ portfolios

Will result in the following load per second:

- Stock summary table:
  - 100 constant time calculations
  - 100 writes
  - 1000 reads
- Random portfolio table:
  - 1000 constant time calculations
  - 1000 writes
  - 1000 reads
- Portfolio summary table:
  - 1000 writes

### Stocks

If we take a reasonable estime of:

- Spark job 1/sec

- $a=4k$ stocks

- $p = 10k$ portfolios

Will result in the following load per second:

- Stock summary table:
  - 4k constant time calculations
  - 4k writes
  - 10k reads
- Random portfolio table:
  - 10k constant time calculations
  - 10k writes
  - 10k reads
- Portfolio summary table:
  - 10k writes


