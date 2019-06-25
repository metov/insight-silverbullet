from cassandra.cqlengine import connection
from flask import Flask, jsonify, render_template
from cassandra_models import *
from cassandra_utilities import connect_to_cassandra, cassandra_configs

app = Flask(__name__)


@app.route('/')
def show_splash():
    s = 'SilverBullet<br/>' \
        '<a href=/api/asset_stat>API: Asset stats</a><br/>' \
        '<a href=/api/asset_stat>API: Asset stats</a><br/>'

    s = render_template('index.html')

    return s


@app.route('/api/asset_stat')
def asset_stats():
    connect_to_cassandra()

    # Get data from Cassandra as serializable dictionaries
    asset_stat = list(map(dict, AssetStat.objects.all()))

    # Serve JSON on API endpoint
    return jsonify(asset_stat)


@app.route('/api/portfolio_stat')
def portfolio_stat():
    # Connect to Cassandra
    connection.setup(cassandra_configs['ips'], cassandra_configs['keyspace'])

    # Get data from Cassandra as serializable dictionaries
    asset_stat = list(map(dict, PortfolioStat.objects.all()))

    # Serve JSON on API endpoint
    return jsonify(asset_stat)


if __name__ == "__main__":

    # Run app
    app.run('localhost:8000', debug=True)