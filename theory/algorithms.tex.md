# Algorithms

Typically, calculating summary statistics such as mean or standard deviation has complexity $O(n)$ for a sequence of $n$ elements. In SilverBullet, we repeatedly calculate summary statistics over a moving window with large $n$, but only a few elements changing every time. It is possible to avoid recalculating the mean, and instead update the old mean according to which elements are being added or removed. This results in a complexity of $O(1)$.

The underlying intuition is that each element in a sequence contributes to the summary statistic in a somewhat independent fashion, so given knowledge of the initial mean and the elements being added/removed, the final mean can be predicted without recalculating it over the whole window.

## Updating the mean

The mean is equal to the sum divided by the number of elements: $\mu = \frac{s}{n}$

If the initial sum of a sequence is known, the effect of adding an element $x$ is trivial to obtain: $s_f = s_i + x$. The same logic can be applied to removing an element.

The change in number of elements is likewise trivial. We can then derive the new mean from these two quantities.

### Adding an element

Given a vector of $n$ elements with mean $\mu_i$, let's say we add a single element $x$.

As noted earlier, finding the new sum is easy:

$s_i = n\mu_i$

$s_f = s_i + x$

We can then obtain the new mean:

$\mu_f = s_f/(n+1)$

It is sometimes useful to know the *change in mean*:

$\Delta = \mu_f - \mu_i = \frac{n\mu_i+x}{n+1}-\mu_i = \frac{n\mu_i+x-\mu_i(n+1)}{n+1}=\frac{n\mu_i + x- n\mu_i - \mu_i}{n+1} = \frac{x-\mu_i}{n+1}$

### Removing an element

Given a vector of $n+1$ elements with mean $\mu_i$, let's say we remove a single element $x$.

The process is very similar to adding an element. The sum:

$s_i = (n+1) \mu_i$

$s_f = s_i - x$

Mean:

$\mu_f = s_f/n$

Change in means:

$\Delta = \mu_f - \mu_i = \frac{(n+1)\mu_i - x}{n}-\mu_i = \frac{n\mu_i+\mu-x}{n}-\mu_i=\frac{n\mu_i+\mu-x-n\mu_i}{n} = \frac{x-\mu_i}{n}$

## Updating the variance

Variance is the sum of squared differences from the mean: $v = \frac{\sum (x_j-\mu)^2}{n}$

Variance can be thought of as "average error from the mean". It can be easier to work with "total error" $e = nv = \sum(x_j-\mu)^2$.

Because variance depends on the mean, calculating the new variance after adding an element is much easier if we also have access to the old and new mean. Luckily, in the previous section we have described such an algorithm.

### Adding an element

Given a vector of $n$ elements with mean $\mu_i$ and variance $v_i$, let's say we add a single element $x$.

We can calculate how the mean will change using the incremental mean method from before:

$\Delta = \mu_f - \mu_i = \frac{x-\mu_i}{n+1}$

Changing the mean will also change the contribution to variance from each existing element:

$e_j = (x_j - \mu_f)^2 = (x_j - \mu_i - \Delta)^2 = (x_j - \mu_i)^2 - 2\Delta(x_j-\mu_i) + \Delta^2 $

The first term is easy to recognize as the initial total error $e_i$. The second term disappears in the sum:

$\sum e_j = \sum (x_j - \mu_i)^2 - \sum 2\Delta(x_j-\mu_i) + \sum \Delta^2$

$\sum e_j = e_i - 2\Delta (\sum x_j- \sum\mu_i) + n \Delta^2$

$\sum e_j = e_i - 2\Delta (s_i- n\mu_i) + n \Delta^2$

$\sum e_j = e_i - 2\Delta (0) + n \Delta^2$

$\sum e_j = e_i + n \Delta^2$

The term $e_\Delta = n\Delta^2$ is the "change in total error due to change of mean".

The new element we add will also contribute to total error: 

$e_x = (x-\mu_f)^2$

We can now obtain the new total error: 

$e_f = e_i + e_\Delta + e_x = e_i + n\Delta^2 + (x-\mu_f)^2$

Variance is easy to calculate from this:

$v_f = \frac{e_f}{n+1}$

It is possible to obtain a closed form for this in terms of only $n$, $x$, $\mu_i$ and $\mu_f$. However the resulting equation is not easy to read. Implementing the stepwise approach also makes the algorithm easier to debug.

### Removing an element

The process is analogous to adding an element, but with a few important changes in the details. Given a vector of $n$ elements with mean $\mu_i$ and variance $v_i$, let's say we add a single element $x$.

The change in contribution to total error from existing elements is similar to the case of adding an element, except one of those elements will be removed and should not be included:

$e_\Delta= (n-1)\Delta^2$

The contribution of the element to be removed is straightforward:

$e_x = (x-\mu_i)^2$

Total error is now:

$e_f = e_i - e_\Delta - e_x$

And variance can be obtained with:

$v_f = \frac{e_f}{n-1}$
