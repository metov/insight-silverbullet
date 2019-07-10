# Performance

## Symbolic calculations

### Variable definitions

* The Spark job will run every <img src="/theory/tex/2f118ee06d05f3c2d98361d9c30e38ce.svg?invert_in_darkmode&sanitize=true" align=middle width=11.889314249999991pt height=22.465723500000017pt/> seconds, therefore it will run <img src="/theory/tex/4f4f4e395762a3af4575de74c019ebb5.svg?invert_in_darkmode&sanitize=true" align=middle width=5.936097749999991pt height=20.221802699999984pt/> times per second.
* There are *a* assets being considered.
* The Monte Carlo will probe *p* candidate portfolios at each trigger.

Asset price movements are assumed to be represented by a biased random walk with continuous values (percent change in price) and infinitely small step size. Under this model, the percent change of an asset after <img src="/theory/tex/27e556cf3caa0673ac49a8f0de3c73ca.svg?invert_in_darkmode&sanitize=true" align=middle width=8.17352744999999pt height=22.831056599999986pt/> seconds will follow a normal distribution <img src="/theory/tex/5593b1fc0a9439a54b6c249d7447253e.svg?invert_in_darkmode&sanitize=true" align=middle width=54.97909064999999pt height=24.65753399999998pt/> where <img src="/theory/tex/08720488029202e91f3ff86e693cd774.svg?invert_in_darkmode&sanitize=true" align=middle width=39.996082499999986pt height=22.831056599999986pt/> and <img src="/theory/tex/b76a3e9fe25f7be6ef6bac54dec2d872.svg?invert_in_darkmode&sanitize=true" align=middle width=53.77271129999999pt height=29.33328419999998pt/>. We normalize both to 1 a second interval, and get:

* Asset reward <img src="/theory/tex/4763bba02fb819c29b9081a819487bb5.svg?invert_in_darkmode&sanitize=true" align=middle width=56.64564839999999pt height=24.65753399999998pt/>, representing the average expected % increase in price after 1 second.
* Asset risk <img src="/theory/tex/c606aeb5d3b6bcd522cf3ae73ddde654.svg?invert_in_darkmode&sanitize=true" align=middle width=69.86487584999998pt height=29.33328419999998pt/>, representing the average expected % spread of price after 1 second.
* Asset z-score <img src="/theory/tex/30f2ae010b51428846f856c61835a1ed.svg?invert_in_darkmode&sanitize=true" align=middle width=77.61132059999998pt height=33.20539859999999pt/> representing normalized average expected change in price after 1 second.

### Asset summary

For a list <img src="/theory/tex/6dbb78540bd76da3f1625782d42d6d16.svg?invert_in_darkmode&sanitize=true" align=middle width=9.41027339999999pt height=14.15524440000002pt/> containing <img src="/theory/tex/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode&sanitize=true" align=middle width=9.86687624999999pt height=14.15524440000002pt/> prices, calculating the reward has complexity <img src="/theory/tex/1f08ccc9cd7309ba1e756c3d9345ad9f.svg?invert_in_darkmode&sanitize=true" align=middle width=35.64773519999999pt height=24.65753399999998pt/> - every element must be added up. However, if the initial mean <img src="/theory/tex/ce9c41bf6906ffd46ac330f09cacc47f.svg?invert_in_darkmode&sanitize=true" align=middle width=14.555823149999991pt height=14.15524440000002pt/> of <img src="/theory/tex/6dbb78540bd76da3f1625782d42d6d16.svg?invert_in_darkmode&sanitize=true" align=middle width=9.41027339999999pt height=14.15524440000002pt/>  is known, pushing a new element <img src="/theory/tex/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode&sanitize=true" align=middle width=9.39498779999999pt height=14.15524440000002pt/> does not necessitate redoing the entire calculation. We can calculate the new mean <img src="/theory/tex/a5d5b14c3616c4fa018839d0842ae295.svg?invert_in_darkmode&sanitize=true" align=middle width=17.60479214999999pt height=14.15524440000002pt/> in <img src="/theory/tex/1e2f931ee6c0b8e7a51a7b0d123d514f.svg?invert_in_darkmode&sanitize=true" align=middle width=34.00006829999999pt height=24.65753399999998pt/> time:

<img src="/theory/tex/e07ccfe935c343ceb3d22a5ba77ac6ae.svg?invert_in_darkmode&sanitize=true" align=middle width=85.09310864999999pt height=28.913154600000016pt/>

If <img src="/theory/tex/ce9c41bf6906ffd46ac330f09cacc47f.svg?invert_in_darkmode&sanitize=true" align=middle width=14.555823149999991pt height=14.15524440000002pt/>, <img src="/theory/tex/a5d5b14c3616c4fa018839d0842ae295.svg?invert_in_darkmode&sanitize=true" align=middle width=17.60479214999999pt height=14.15524440000002pt/> and previous standard deviation <img src="/theory/tex/e61ae7f2cb94c8418c30517775fde77d.svg?invert_in_darkmode&sanitize=true" align=middle width=14.04400634999999pt height=14.15524440000002pt/> are known, we can also utilize a [fast algorithm](https://math.stackexchange.com/a/1362467) to obtain the new standard deviation:

<img src="/theory/tex/10f3de854b8e18788f4abc7426b7f71f.svg?invert_in_darkmode&sanitize=true" align=middle width=204.27120449999998pt height=37.39173569999998pt/> where <img src="/theory/tex/548f7489617ac8969b8f66a4147dd4ae.svg?invert_in_darkmode&sanitize=true" align=middle width=47.01090074999999pt height=26.76175259999998pt/> and <img src="/theory/tex/128d13f5f892b4c9189f05110c447c26.svg?invert_in_darkmode&sanitize=true" align=middle width=82.91942009999998pt height=22.831056599999986pt/>

Although the equation appears daunting, the running time is constant with respect to <img src="/theory/tex/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode&sanitize=true" align=middle width=9.86687624999999pt height=14.15524440000002pt/>.

For an entire universe of assets, we will make these calculations <img src="/theory/tex/1886855f46fb1b3c79645aa86858ebe3.svg?invert_in_darkmode&sanitize=true" align=middle width=26.497232849999993pt height=20.221802699999984pt/> times per second, and make <img src="/theory/tex/1886855f46fb1b3c79645aa86858ebe3.svg?invert_in_darkmode&sanitize=true" align=middle width=26.497232849999993pt height=20.221802699999984pt/> writes to Redis. During portfolio evaluation phase, every portfolio will need the entire table of asset summaries, generating <img src="/theory/tex/c7de704e6d83251e78f9bd0855a2ddae.svg?invert_in_darkmode&sanitize=true" align=middle width=26.07864599999999pt height=20.221802699999984pt/> reads per second.

### Random portfolio generation

Generating a vector of weights will scale linearly with <img src="/theory/tex/a852d50348282cefd8687a58a0c8e76f.svg?invert_in_darkmode&sanitize=true" align=middle width=28.83170234999999pt height=14.611911599999981pt/>. Writing each portfolio vector separately will incur <img src="/theory/tex/c7de704e6d83251e78f9bd0855a2ddae.svg?invert_in_darkmode&sanitize=true" align=middle width=26.07864599999999pt height=20.221802699999984pt/> writes per second. Evaluating the portfolios will incur <img src="/theory/tex/592f13e119f252b775fd3f9b415294a0.svg?invert_in_darkmode&sanitize=true" align=middle width=26.07864599999999pt height=20.221802699999984pt/> reads.

### Portfolio summary

For each portfolio, we will retrieve the entire asset summary table. This will generate <img src="/theory/tex/c7de704e6d83251e78f9bd0855a2ddae.svg?invert_in_darkmode&sanitize=true" align=middle width=26.07864599999999pt height=20.221802699999984pt/> reads and <img src="/theory/tex/c7de704e6d83251e78f9bd0855a2ddae.svg?invert_in_darkmode&sanitize=true" align=middle width=26.07864599999999pt height=20.221802699999984pt/> writes (to record portfolio summaries).

## Numeric examples

### Cryptocurrencies

If we take a reasonable estime of:

* Spark job 1/sec

* <img src="/theory/tex/9e0807da26fc99a2ff66b35f5fb022e7.svg?invert_in_darkmode&sanitize=true" align=middle width=55.26441359999998pt height=21.18721440000001pt/> cryptocoins

* <img src="/theory/tex/bd850c33ea00460961b3aff78e9e78ef.svg?invert_in_darkmode&sanitize=true" align=middle width=63.06503444999999pt height=21.18721440000001pt/> portfolios

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

- <img src="/theory/tex/a55eeb657f1762b24665eb549043cc88.svg?invert_in_darkmode&sanitize=true" align=middle width=47.901362849999984pt height=22.831056599999986pt/> stocks

- <img src="/theory/tex/135afde7bda3c75dcf546007b2597f44.svg?invert_in_darkmode&sanitize=true" align=middle width=55.701985349999994pt height=22.831056599999986pt/> portfolios

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


