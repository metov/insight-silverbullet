"""
Evaluates random Monte Carlo portfolios. Run on Spark node.
"""

import numpy as np
import time
import uuid

from cassandra.cqlengine.management import sync_table, drop_table
from pyspark import SparkContext, SparkConf

from cassandra_models import AssetStat
from cassandra_models import PortfolioStat, PortfolioLatencyLog
from cassandra_utilities import *

n_portfolios = 1000


def main():
    """
    Applies a Monte Carlo algorithm to probe portfolio space.

    :return:
    """
    connect_to_cassandra()

    # Drop old table
    drop_table(PortfolioStat, keyspaces=[silverbullet_keyspace])

    # Create table for portfolio stats
    sync_table(PortfolioStat, keyspaces=[silverbullet_keyspace])
    sync_table(PortfolioLatencyLog, keyspaces=[silverbullet_keyspace])

    # Connect to Spark
    spark_config = SparkConf().setAppName('Monte Carlo portfolio optimizer')

    spark_context = SparkContext(conf=spark_config)

    # Start looping
    while True:
        t_start = time.time()

        # Get entire list of assets as a Python list with static order
        assets = [asset for asset in AssetStat.objects if asset.reward > 0]
        asset_names = [asset.asset for asset in assets]

        # Generate random weights using the Dirichlet distribution (sums to 1)
        dirichlet_alpha = np.ones(len(assets))
        portfolio_weights = np.random.dirichlet(dirichlet_alpha, n_portfolios)

        # Evaluate random portfolios on spark
        parallelized_weights = spark_context.parallelize(portfolio_weights)
        results = parallelized_weights.map(lambda w: dumb_portfolio_evaluate(assets, w)).collect()

        # Initialize latencies
        latency_min = 0
        latency_max = 0
        latency_sum = 0
        latency_n = 0

        # Write results to Cassandra
        for i, r in enumerate(results):
            t_end = time.time()
            latency = t_end - t_start

            PortfolioStat.create(id=i, reward=r['reward'], risk=r['risk'], time_evaluated=t_end,
                                 weights=r['weights'], weight_labels=asset_names, latency=latency)

            # Update latencies
            if latency_n == 0:
                latency_min = latency
                latency_max = latency
                latency_sum = latency
                latency_n = 1
            else:
                latency_max = max(latency, latency_max)
                latency_min = min(latency, latency_min)
                latency_n += 1
                latency_sum += latency

        # Record latency
        t = time.time()
        latency_mean = latency_sum / latency_n
        PortfolioLatencyLog.create(id=uuid.uuid1(),
                                   time_evaluated=int(t),
                                   latency_mean=latency_mean,
                                   latency_min=latency_min,
                                   latency_max=latency_max)

        # Print some output so the user can tell the program is alive
        print('{}\t{}\t{}\t{}'.format(t, latency_min, latency_max, latency_mean))

        # Wait 1 second to avoid overloading the DB
        time.sleep(1)


def dumb_portfolio_evaluate(assets, weights):
    """
    Takes weighted sum of asset reward and risk.
    :param assets: Cassandra ORM model for asset stat table.
    :param weights: Vector of weights for each asset (should sum to 1)
    :return: Dictionary containing portfolio reward, risk and weight vector.
    """

    reward = 0
    risk = 0
    for i in range(len(assets)):
        asset = assets[i]
        reward += asset.reward * weights[i]
        risk += asset.risk * weights[i] * weights[i]

    portfolio_stat = {'reward': reward, 'risk': risk, 'weights': weights}
    return portfolio_stat


if __name__ == "__main__":
    main()
