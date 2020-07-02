import pandas as pd
from galileodb.factory import create_experiment_database_from_env
from galileodb.sql.adapter import ExperimentSQLDatabase

from galileojp import env


def to_idlist(exp_ids):
    idlist = ', '.join([f'"{i}"' for i in exp_ids])
    return idlist


class ExperimentFrameGateway:

    def __init__(self, edb: ExperimentSQLDatabase) -> None:
        super().__init__()
        self.edb = edb

    @property
    def _con(self):
        return self.edb.db.connection

    def experiments(self) -> pd.DataFrame:
        return pd.read_sql(f'SELECT * FROM experiments', con=self._con)

    def nodeinfo(self, *exp_ids):
        if not exp_ids:
            raise ValueError

        idlist = to_idlist(exp_ids)

        df = pd.read_sql(f'SELECT * FROM nodeinfo WHERE exp_id in ({idlist})', con=self._con)
        return df

    def events(self, *exp_ids):
        if not exp_ids:
            raise ValueError

        idlist = to_idlist(exp_ids)

        df = pd.read_sql(f'SELECT * FROM events WHERE exp_id in ({idlist})', con=self._con)
        df.index = pd.DatetimeIndex(pd.to_datetime(df['TIMESTAMP'], unit='s'))
        return df

    def telemetry(self, *exp_ids) -> pd.DataFrame:
        if not exp_ids:
            raise ValueError

        idlist = to_idlist(exp_ids)

        df = pd.read_sql(f'SELECT * FROM telemetry WHERE exp_id in ({idlist})', con=self._con)
        df.index = pd.DatetimeIndex(pd.to_datetime(df['TIMESTAMP'], unit='s'))
        return df

    @staticmethod
    def from_env() -> 'ExperimentFrameGateway':
        env.load()
        return ExperimentFrameGateway(create_experiment_database_from_env())
