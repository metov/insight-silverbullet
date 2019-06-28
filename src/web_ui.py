from cassandra.cqlengine import connection
from flask import Flask, jsonify, render_template
from cassandra_models import *
from cassandra_utilities import connect_to_cassandra, cassandra_configs


# Setup flask app
flask_app = Flask(__name__)

@flask_app.route('/')
def show_splash():
    s = render_template('index.html')

    return s


@flask_app.route('/api/asset_stat')
def asset_stats():
    connect_to_cassandra()

    # Get data from Cassandra as serializable dictionaries
    asset_stat = list(map(dict, AssetStat.objects.all()))

    # Serve JSON on API endpoint
    return jsonify(asset_stat)


@flask_app.route('/api/portfolio_stat')
def portfolio_stat():
    # Connect to Cassandra
    connection.setup(cassandra_configs['ips'], cassandra_configs['keyspace'])

    # Get data from Cassandra as serializable dictionaries
    asset_stat = list(map(dict, PortfolioStat.objects.all()))

    # Serve JSON on API endpoint
    return jsonify(asset_stat)


if __name__ == "__main__":
    flask_app.run(host='0.0.0.0', port='80', debug=True)
