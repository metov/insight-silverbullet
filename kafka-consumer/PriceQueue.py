class PriceData:
    """
    Stores entire dataset of all asset prices.
    """

    def __init__(self, n):
        self.data = {}
        self.n = n

    def push_price(self, asset, price, timestamp):
        if asset not in self.data:
            self.data[asset] = PriceQueue(self.n, price, timestamp)
        else:
            self.data[asset].push_price(price, timestamp)

    def print_summary_table(self):
        for asset, pq in self.data.items():
            s = '\t{}: {} / {} ({})'.format(asset, pq.reward, pq.risk, len(pq.price_data))
            print(s)


class PriceQueue:
    """
    Stores information about prices of one asset.
    """

    def __init__(self, n, price, timestamp):
        self.max_length = n

        pd = PriceDatum(price, timestamp)
        self.price_data = [pd]

        self.reward = 0
        self.risk = 0

    def push_price(self, price, timestamp):
        if len(self.price_data) == self.max_length:
            self.pop_oldest_price()

        pd = PriceDatum(price, timestamp)
        pd.update_relative(self.price_data[-1])
        self.push_new_price(pd)

    def push_new_price(self, incoming):
        # Update reward
        x = incoming.normalized_change
        n = len(self.price_data)
        mu_i = self.reward
        mu_f = incremental_mean(mu_i, n, x)

        self.reward = mu_f

        # Update risk
        v_i = self.risk
        v_f = incremental_var(mu_i, n, v_i, x)

        self.risk = v_f

        # Update price list
        self.price_data.append(incoming)

    def pop_oldest_price(self):
        # Learn the price we are about to remove
        outgoing = self.price_data[0]

        # Update reward
        x = outgoing.normalized_change
        n = len(self.price_data)
        mu_i = self.reward
        mu_f = decremental_mean(mu_i, n, x)

        self.reward = mu_f

        # Update risk
        v_i = self.risk
        v_f = decremental_var(mu_i, n, v_i, x)

        self.risk = v_f

        # Update price list
        outgoing = self.price_data.pop(0)

    def __repr__(self):
        s = 'reward: {}, risk: {}, prices: {}'

        sp = ''
        for p in self.price_data:
            sp += '{}, '.format(p.normalized_change)

        t = s.format(self.reward, self.risk, sp)

        return t


class PriceDatum:
    """
    Represents a single tick of a single asset.
    """

    def __init__(self, price, timestamp):
        self.price = price
        self.timestamp = timestamp

        self.relative_change = 0
        self.time_interval = 0
        self.normalized_change = 0

    def update_relative(self, basis):
        """
        Calculates relative statistics using the provided datum as a basis.
        """

        dp = self.price / basis.price - 1
        dt = self.timestamp - basis.timestamp

        self.relative_change = dp
        self.time_interval = dt
        self.normalized_change = dp / dt

    def __repr__(self):
        s = 'price={}, time_interval={}, normalized_change={}'
        t = s.format(self.price, self.time_interval, self.normalized_change)

        return t


def incremental_mean(mu_i, n, x):
    """
    Calculates the mean after adding x to a vector with given mean and size.

    :param mu_i: Mean before adding x.
    :param n: Number of elements before adding x.
    :param x: Element to be added.
    :return: New mean.
    """

    delta = (x - mu_i) / float(n + 1)
    mu_f = mu_i + delta

    return mu_f


def decremental_mean(mu_i, n, x):
    """
    Calculates the mean after removing x from a vector with given mean and size.

    :param mu_i: Mean before removing x.
    :param n: Number of elements before removing x.
    :param x: Element to be removed.
    :return: New mean.
    """

    delta = (mu_i - x) / float(n - 1)
    mu_f = mu_i + delta

    return mu_f


def incremental_var(mu_i, n, v_i, x):
    """
    Calculates the variance after adding x to a vector with given mean and size.

    :param mu_i: Mean before adding x.
    :param n: Number of elements before adding x.
    :param v_i: Variance before adding x.
    :param x: Element to be added.
    :return: New variance.
    """

    mu_f = incremental_mean(mu_i, n, x)
    delta = mu_f - mu_i
    e_i = v_i * n

    e_x = (x - mu_f)*(x - mu_f)
    e_delta = n * delta * delta

    e_f = e_i + e_x + e_delta

    v_f = e_f / float(n+1)

    return v_f


def decremental_var(mu_i, n, v_i, x):
    """
    Calculates the variance after removing x to a vector with given mean and size.

    :param mu_i: Mean before removing x.
    :param n: Number of elements before removing x.
    :param v_i: Variance before removing x.
    :param x: Element to be removed.
    :return: New variance.
    """

    mu_f = decremental_mean(mu_i, n, x)
    delta = mu_f - mu_i
    e_i = v_i * n

    e_x = (x - mu_i)*(x - mu_i)
    e_delta = (n - 1) * delta * delta

    e_f = e_i - e_x - e_delta

    v_f = e_f / float(n-1)

    return v_f
