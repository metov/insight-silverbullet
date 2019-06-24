import numpy as np
import time
import uuid
from pprint import pprint
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import create_keyspace_simple, sync_table, drop_table

from cassandra_models import AssetStat, PortfolioStat

n_portfolios = 10


def main():
    """
    Applies a Monte Carlo algorithm to probe portfolio space.

    :return:
    """

    # Connect to cassandra
    keyspace = 'silverbullet'
    connection.setup(['10.0.0.5'], keyspace)

    # Drop old table
    drop_table(PortfolioStat, keyspaces=[keyspace])

    # Create table for portfolio stats
    sync_table(PortfolioStat, keyspaces=[keyspace])

    # Start looping
    while True:
        # Get entire list of assets as a Python list with static order
        assets = [asset for asset in AssetStat.objects]

        # Generate random weights using the Dirichlet distribution (sums to 1)
        dirichlet_alpha = np.ones(len(assets))
        portfolio_weights = np.random.dirichlet(dirichlet_alpha, n_portfolios)

        # Evaluate portfolios
        portfolio_stat = []
        time_started = time.time()
        for i, p in enumerate(portfolio_weights):
            reward = 0
            risk = 0

            for j in range(len(assets)):
                reward += assets[j].reward * p[j]
                risk += assets[j].reward * p[j]

            portfolio_stat.append({'reward': reward, 'risk': risk})

            # Save to Cassandra
            PortfolioStat.create(id=i, reward=reward, risk=risk, time_evaluated=time.time(), weights=p)

        # Print some output so the user can tell the program is alive
        print(time.time())

        # Wait 1 second to avoid overloading the DB
        time.sleep(1)


if __name__ == "__main__":
    main()