# Algorithms

Typically, calculating summary statistics such as mean or standard deviation has complexity <img src="/theory/tex/1f08ccc9cd7309ba1e756c3d9345ad9f.svg?invert_in_darkmode&sanitize=true" align=middle width=35.64773519999999pt height=24.65753399999998pt/> for a sequence of <img src="/theory/tex/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode&sanitize=true" align=middle width=9.86687624999999pt height=14.15524440000002pt/> elements. In SilverBullet, we repeatedly calculate summary statistics over a moving window with large <img src="/theory/tex/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode&sanitize=true" align=middle width=9.86687624999999pt height=14.15524440000002pt/>, but only a few elements changing every time. It is possible to avoid recalculating the mean, and instead update the old mean according to which elements are being added or removed. This results in a complexity of <img src="/theory/tex/1e2f931ee6c0b8e7a51a7b0d123d514f.svg?invert_in_darkmode&sanitize=true" align=middle width=34.00006829999999pt height=24.65753399999998pt/>.

The underlying intuition is that each element in a sequence contributes to the summary statistic in a somewhat independent fashion, so given knowledge of the initial mean and the elements being added/removed, the final mean can be predicted without recalculating it over the whole window.

## Updating the mean

The mean is equal to the sum divided by the number of elements: <img src="/theory/tex/b14cdbcd9377310f5989a6c57563667c.svg?invert_in_darkmode&sanitize=true" align=middle width=41.921175449999986pt height=22.853275500000024pt/>

If the initial sum of a sequence is known, the effect of adding an element <img src="/theory/tex/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode&sanitize=true" align=middle width=9.39498779999999pt height=14.15524440000002pt/> is trivial to obtain: <img src="/theory/tex/b4c607e24f0798171b1c4a4b24c8c103.svg?invert_in_darkmode&sanitize=true" align=middle width=80.80934399999998pt height=19.1781018pt/>. The same logic can be applied to removing an element.

The change in number of elements is likewise trivial. We can then derive the new mean from these two quantities.

### Adding an element

Given a vector of <img src="/theory/tex/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode&sanitize=true" align=middle width=9.86687624999999pt height=14.15524440000002pt/> elements with mean <img src="/theory/tex/ce9c41bf6906ffd46ac330f09cacc47f.svg?invert_in_darkmode&sanitize=true" align=middle width=14.555823149999991pt height=14.15524440000002pt/>, let's say we add a single element <img src="/theory/tex/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode&sanitize=true" align=middle width=9.39498779999999pt height=14.15524440000002pt/>.

As noted earlier, finding the new sum is easy:

<img src="/theory/tex/bd92343fd9cd8fe3d3c2dc6e7586033a.svg?invert_in_darkmode&sanitize=true" align=middle width=59.518606949999985pt height=14.15524440000002pt/>

<img src="/theory/tex/b4c607e24f0798171b1c4a4b24c8c103.svg?invert_in_darkmode&sanitize=true" align=middle width=80.80934399999998pt height=19.1781018pt/>

We can then obtain the new mean:

<img src="/theory/tex/d02eca73e3166161d03217e19d5a783e.svg?invert_in_darkmode&sanitize=true" align=middle width=115.75351094999998pt height=24.65753399999998pt/>

It is sometimes useful to know the *change in mean*:

<img src="/theory/tex/9cfc114e06f2106026bc28fd1b390272.svg?invert_in_darkmode&sanitize=true" align=middle width=487.59697965pt height=33.20539859999999pt/>

### Removing an element

Given a vector of <img src="/theory/tex/3f18d8f60c110e865571bba5ba67dcc6.svg?invert_in_darkmode&sanitize=true" align=middle width=38.17727759999999pt height=21.18721440000001pt/> elements with mean <img src="/theory/tex/ce9c41bf6906ffd46ac330f09cacc47f.svg?invert_in_darkmode&sanitize=true" align=middle width=14.555823149999991pt height=14.15524440000002pt/>, let's say we remove a single element <img src="/theory/tex/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode&sanitize=true" align=middle width=9.39498779999999pt height=14.15524440000002pt/>.

The process is very similar to adding an element. The sum:

<img src="/theory/tex/a68b6a05ef8f1e22f879063197b35bf2.svg?invert_in_darkmode&sanitize=true" align=middle width=100.61444085pt height=24.65753399999998pt/>

<img src="/theory/tex/a7712ecc4de6a5ad0140131edc826020.svg?invert_in_darkmode&sanitize=true" align=middle width=80.80934399999998pt height=19.1781018pt/>

Mean:

<img src="/theory/tex/3cf2104a116a8858f60c08e9fd38afea.svg?invert_in_darkmode&sanitize=true" align=middle width=74.65767704999999pt height=24.65753399999998pt/>

Change in means:

<img src="/theory/tex/71ed0d558a4f6a79dac5da0ee1ded1bd.svg?invert_in_darkmode&sanitize=true" align=middle width=504.70766280000004pt height=33.20539859999999pt/>

## Updating the variance

Variance is the sum of squared differences from the mean: <img src="/theory/tex/c0e30db7cb3106f100a7dbe114aa6437.svg?invert_in_darkmode&sanitize=true" align=middle width=94.81286429999999pt height=37.19082179999999pt/>

Variance can be thought of as "average error from the mean". It can be easier to work with "total error" <img src="/theory/tex/6a539dc75ba20fd8bafe2a2db9c8e01e.svg?invert_in_darkmode&sanitize=true" align=middle width=152.9212542pt height=26.76175259999998pt/>.

Because variance depends on the mean, calculating the new variance after adding an element is much easier if we also have access to the old and new mean. Luckily, in the previous section we have described such an algorithm.

### Adding an element

Given a vector of <img src="/theory/tex/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode&sanitize=true" align=middle width=9.86687624999999pt height=14.15524440000002pt/> elements with mean <img src="/theory/tex/ce9c41bf6906ffd46ac330f09cacc47f.svg?invert_in_darkmode&sanitize=true" align=middle width=14.555823149999991pt height=14.15524440000002pt/> and variance <img src="/theory/tex/9f7365802167fff585175c1750674d42.svg?invert_in_darkmode&sanitize=true" align=middle width=12.61896569999999pt height=14.15524440000002pt/>, let's say we add a single element <img src="/theory/tex/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode&sanitize=true" align=middle width=9.39498779999999pt height=14.15524440000002pt/>.

We can calculate how the mean will change using the incremental mean method from before:

<img src="/theory/tex/8e7cd5b6663276d5fd6736a4e271a275.svg?invert_in_darkmode&sanitize=true" align=middle width=144.3307668pt height=28.913154600000016pt/>

Changing the mean will also change the contribution to variance from each existing element:

<img src="/theory/tex/771cee8c42fe25f78516d1905494e8f2.svg?invert_in_darkmode&sanitize=true" align=middle width=479.950086pt height=26.76175259999998pt/>

The first term is easy to recognize as the initial total error <img src="/theory/tex/b95c2b0aab2482e5bebd25332a4bbde0.svg?invert_in_darkmode&sanitize=true" align=middle width=12.30503669999999pt height=14.15524440000002pt/>. The second term disappears in the sum:

<img src="/theory/tex/205cd891e3a64c3e8fbfee872cd2bd89.svg?invert_in_darkmode&sanitize=true" align=middle width=333.0011685pt height=26.76175259999998pt/>

<img src="/theory/tex/5a5730a6fa8ce095c5f3a9f90f76592d.svg?invert_in_darkmode&sanitize=true" align=middle width=266.6931333pt height=26.76175259999998pt/>

<img src="/theory/tex/57a23c245b7c9c456941a39e8c0b96bf.svg?invert_in_darkmode&sanitize=true" align=middle width=233.23427325pt height=26.76175259999998pt/>

<img src="/theory/tex/e8efaa09341f6999c7fa6bb55b3816d5.svg?invert_in_darkmode&sanitize=true" align=middle width=182.93941875pt height=26.76175259999998pt/>

<img src="/theory/tex/53544930c3f25479cf181978e2a8955a.svg?invert_in_darkmode&sanitize=true" align=middle width=119.9257026pt height=26.76175259999998pt/>

The term <img src="/theory/tex/b8de696693304c743506c921f9b3d8df.svg?invert_in_darkmode&sanitize=true" align=middle width=71.31091604999999pt height=26.76175259999998pt/> is the "change in total error due to change of mean".

The new element we add will also contribute to total error: 

<img src="/theory/tex/c98cc14175fe605aa4ade678fc484dcf.svg?invert_in_darkmode&sanitize=true" align=middle width=105.09889664999999pt height=26.76175259999998pt/>

We can now obtain the new total error: 

<img src="/theory/tex/1e16d781569a81c9eea6a0f6e4f2338d.svg?invert_in_darkmode&sanitize=true" align=middle width=300.02627655000003pt height=26.76175259999998pt/>

Variance is easy to calculate from this:

<img src="/theory/tex/f8f859842186628c401ccadd67d19f15.svg?invert_in_darkmode&sanitize=true" align=middle width=65.15001734999998pt height=26.78527500000001pt/>

It is possible to obtain a closed form for this in terms of only <img src="/theory/tex/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode&sanitize=true" align=middle width=9.86687624999999pt height=14.15524440000002pt/>, <img src="/theory/tex/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode&sanitize=true" align=middle width=9.39498779999999pt height=14.15524440000002pt/>, <img src="/theory/tex/ce9c41bf6906ffd46ac330f09cacc47f.svg?invert_in_darkmode&sanitize=true" align=middle width=14.555823149999991pt height=14.15524440000002pt/> and <img src="/theory/tex/a5d5b14c3616c4fa018839d0842ae295.svg?invert_in_darkmode&sanitize=true" align=middle width=17.60479214999999pt height=14.15524440000002pt/>. However the resulting equation is not easy to read. Implementing the stepwise approach also makes the algorithm easier to debug.

### Removing an element

The process is analogous to adding an element, but with a few important changes in the details. Given a vector of <img src="/theory/tex/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode&sanitize=true" align=middle width=9.86687624999999pt height=14.15524440000002pt/> elements with mean <img src="/theory/tex/ce9c41bf6906ffd46ac330f09cacc47f.svg?invert_in_darkmode&sanitize=true" align=middle width=14.555823149999991pt height=14.15524440000002pt/> and variance <img src="/theory/tex/9f7365802167fff585175c1750674d42.svg?invert_in_darkmode&sanitize=true" align=middle width=12.61896569999999pt height=14.15524440000002pt/>, let's say we add a single element <img src="/theory/tex/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode&sanitize=true" align=middle width=9.39498779999999pt height=14.15524440000002pt/>.

The change in contribution to total error from existing elements is similar to the case of adding an element, except one of those elements will be removed and should not be included:

<img src="/theory/tex/953c37a233673c3dc16803303b416010.svg?invert_in_darkmode&sanitize=true" align=middle width=112.40674994999998pt height=26.76175259999998pt/>

The contribution of the element to be removed is straightforward:

<img src="/theory/tex/c39b24d5ee2e73df20187b92a65f45c8.svg?invert_in_darkmode&sanitize=true" align=middle width=102.04991609999999pt height=26.76175259999998pt/>

Total error is now:

<img src="/theory/tex/1c17f8df636e927514313d763266657b.svg?invert_in_darkmode&sanitize=true" align=middle width=125.78656364999999pt height=19.1781018pt/>

And variance can be obtained with:

<img src="/theory/tex/5b3b9ac2b6c7ac28a60f7dfad23d0f96.svg?invert_in_darkmode&sanitize=true" align=middle width=65.33266409999999pt height=26.78527500000001pt/>
