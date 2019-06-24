from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class AssetStat(Model):
    asset = columns.Text(primary_key=True)
    time_collected = columns.Float()
    reward = columns.Float()
    risk = columns.Float()


class PortfolioStat(Model):
    id = columns.Integer(primary_key=True)
    reward = columns.Float()
    risk = columns.Float()
    time_evaluated = columns.Float()
    weights = columns.List(columns.Float())
