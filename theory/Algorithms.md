# Algorithms

## Updating mean

### Adding element

Given a vector of $n$ elements with mean $\mu_1$, let's say we add a single element $x$:

$s_1 = n\cdot \mu_1$, $s_2 = s_1 + x$, $\mu_2 = s_2/(n+1)$

$\mu_2 - \mu_1 = \frac{n\mu_1+x}{n+1}-\mu_1 = \frac{n\mu_1+x-\mu_1(n+1)}{n+1}=\frac{n\mu_1 + x- n\mu_1 - \mu_1}{n+1} = \frac{x-\mu_1}{n+1}$

### Removing element

Given a vector of n+1 elements with mean \mu_1, let's say we remove a single element x:

$s_1 = (n+1)\cdot \mu_1, s_2 = s_1 - x, \mu_2 = s_2/n$

$\mu_2 - \mu_1 = \frac{(n+1)\mu_1 - x}{n}-\mu_1 = \frac{n\mu_1+\mu-x}{n}-\mu_1=\frac{n\mu_1+\mu-x-n\mu_1}{n} = \frac{x-\mu_1}{n}$


