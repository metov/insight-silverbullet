from unittest import TestCase

from PriceQueue import PriceData


class TestPriceData(TestCase):
    def test_push_price_second(self):
        pd = PriceData(3)

        pd.push_price('test', 1, 1)
        pd.push_price('test', 2, 2)

        reward_observed = pd.data['test'].reward
        reward_expected = 0.5

        self.assertLess(abs(reward_observed / reward_expected - 1), 0.001)

    def test_push_price_last(self):
        pd = PriceData(4)

        pd.push_price('test', 1.0, 1.0)
        pd.push_price('test', 2.0, 2.0)
        pd.push_price('test', 1.0, 3.0)
        pd.push_price('test', 2.0, 4.0)
        pd.push_price('test', 1.0, 5.0)

        reward_observed = pd.data['test'].reward
        reward_expected = 0.25

        self.assertLess(abs(reward_observed / reward_expected - 1), 0.001)
