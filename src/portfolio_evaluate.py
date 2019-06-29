"""
Evaluates random Monte Carlo portfolios. Run on Spark node.
"""

import time
import uuid

import numpy as np
from cassandra.cqlengine.management import sync_table, drop_table
from cassandra_models import AssetStat, PortfolioStat, PortfolioLatencyLog
from cassandra_utilities import connect_to_cassandra, silverbullet_keyspace

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

    # Start looping
    while True:
        t = time.time()

        # Get entire list of assets as a Python list with static order
        assets = [asset for asset in AssetStat.objects if asset.reward > 0]
        asset_names = [asset.asset for asset in assets]

        # Generate random weights using the Dirichlet distribution (sums to 1)
        dirichlet_alpha = np.ones(len(assets))
        portfolio_weights = np.random.dirichlet(dirichlet_alpha, n_portfolios)

        # Evaluate portfolios
        portfolio_stat = []

        latency_min = 0
        latency_max = 0
        latency_sum = 0
        latency_n = 0

        for i, p in enumerate(portfolio_weights):
            reward = 0
            risk = 0

            for j in range(len(assets)):
                asset = assets[j]
                reward += asset.reward * p[j]
                risk += asset.risk * p[j]

            portfolio_stat.append({'reward': reward, 'risk': risk})

            # Save to Cassandra
            dt = time.time() - t
            PortfolioStat.create(id=i, reward=reward, risk=risk, time_evaluated=t,
                                 weights=p, weight_labels=asset_names, latency=dt)

            # Update latencies
            if latency_n == 0:
                latency_min = dt
                latency_max = dt
                latency_sum = dt
                latency_n = 1
            else:
                latency_max = max(dt, latency_max)
                latency_min = min(dt, latency_min)
                latency_n += 1
                latency_sum += dt

        # Record latencies for this message
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


if __name__ == "__main__":
    main()
