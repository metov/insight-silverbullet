"""
Evaluates random Monte Carlo portfolios. Run on Spark node.
"""

import time

import numpy as np
from cassandra.cqlengine.management import sync_table, drop_table
from cassandra_models import AssetStat, PortfolioStat
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

    # Start looping
    while True:
        # Get entire list of assets as a Python list with static order
        assets = [asset for asset in AssetStat.objects]
        asset_names = [asset.asset for asset in assets]

        # Generate random weights using the Dirichlet distribution (sums to 1)
        dirichlet_alpha = np.ones(len(assets))
        portfolio_weights = np.random.dirichlet(dirichlet_alpha, n_portfolios)

        # Evaluate portfolios
        portfolio_stat = []
        for i, p in enumerate(portfolio_weights):
            reward = 0
            risk = 0
            last_asset = 0

            for j in range(len(assets)):
                asset = assets[j]
                reward += asset.reward * p[j]
                risk += asset.risk * p[j]
                last_asset = max(last_asset, asset.time_evaluated)

            portfolio_stat.append({'reward': reward, 'risk': risk})

            # Save to Cassandra
            t = time.time()
            dt = t - last_asset
            PortfolioStat.create(id=i, reward=reward, risk=risk, time_evaluated=t,
                                 weights=p, weight_labels=asset_names, latency=dt)

        # Print some output so the user can tell the program is alive
        print(time.time())

        # Wait 1 second to avoid overloading the DB
        time.sleep(1)


if __name__ == "__main__":
    main()
