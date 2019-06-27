"""
Models for accessing data on Cassandra. Required for all Cassandra-related scripts.
"""

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class AssetStat(Model):
    asset = columns.Text(primary_key=True)
    reward = columns.Float()
    risk = columns.Float()
    latency = columns.Float()
    time_evaluated = columns.Float()


class PortfolioStat(Model):
    id = columns.Integer(primary_key=True)
    reward = columns.Float()
    risk = columns.Float()
    time_evaluated = columns.Float()
    latency = columns.Float()
    weights = columns.List(columns.Float())
    weight_labels = columns.List(columns.Text())
