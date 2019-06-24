from unittest import TestCase
from PriceQueue import *


class TestPriceQueue(TestCase):
    def test_increment_mean(self):
        u = [1, 2, 3]

        n = float(len(u))
        mu_i = sum(u) / n
        x = 4

        v = u + [x]
        mu_f_expected = sum(v) / (n + 1)

        mu_f_observed = incremental_mean(mu_i, n, x)

        self.assertLess(abs(mu_f_expected / mu_f_observed - 1), 0.001)

    def test_increment_mean_second(self):
        u = [0]

        n = float(len(u))
        mu_i = sum(u) / n
        x = 1

        v = u + [x]
        mu_f_expected = sum(v) / (n + 1)

        mu_f_observed = incremental_mean(mu_i, n, x)

        self.assertLess(abs(mu_f_expected / mu_f_observed - 1), 0.001)

    def test_decrement_mean(self):
        u = [1, 2, 3, 4]

        n = float(len(u))
        i = sum(u)
        mu_i = i / n
        x = u[0]

        v = u[1:]
        mu_f_expected = sum(v) / (n - 1)

        mu_f_observed = decremental_mean(mu_i, n, x)

        self.assertLess(abs(mu_f_expected / mu_f_observed - 1), 0.001)

    def test_increment_var(self):
        # u = [1, 2, 3]
        # x = 4
        u = [5, 6, 7]
        x = 8

        n = float(len(u))
        mu_i = sum(u) / n
        v_i = sum(map(lambda i: (i-mu_i)*(i-mu_i), u)) / n

        v = u + [x]
        mu_f = sum(v) / (n+1)
        v_f_expected = sum(map(lambda i: (i-mu_f)*(i-mu_f), v)) / (n+1)

        v_f_observed = incremental_var(mu_i, n, v_i, x)

        self.assertLess(abs(v_f_observed / v_f_expected - 1), 0.001)

    def test_decrement_var(self):
        # u = [1, 2, 3, 4]
        # x = u[0]
        u = [5, 6, 7, 8]
        x = u[0]

        n = float(len(u))
        mu_i = sum(u) / n
        v_i = sum(map(lambda i: (i-mu_i)*(i-mu_i), u)) / n

        v = u[1:]
        mu_f = sum(v) / (n - 1)
        v_f_expected = sum(map(lambda i: (i - mu_f) * (i - mu_f), v)) / (n-1)

        v_f_observed = decremental_var(mu_i, n, v_i, x)

        self.assertLess(abs(v_f_observed / v_f_expected - 1), 0.001)