import collections

import pandas as pd
from galileodb.factory import create_experiment_database_from_env, create_experiment_database
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

    def traces(self, *exp_ids):
        if not exp_ids:
            raise ValueError

        idlist = to_idlist(exp_ids)

        df = pd.read_sql(f'SELECT * FROM traces WHERE exp_id in ({idlist})', con=self._con)
        df['RTT'] = df['DONE'] - df['SENT']
        df['SENT'] = df['SENT'].apply(lambda d: pd.to_datetime(d, unit='s'))
        df['DONE'] = df['DONE'].apply(lambda d: pd.to_datetime(d, unit='s'))
        df['RTT'] = df['RTT'].apply(lambda d: d * 1000)

        return df

    def traces_with_telemetry(self, *exp_ids):
        if not exp_ids:
            raise ValueError

        idlist = to_idlist(exp_ids)
        db_str = "SELECT j1.rid as rid, j1.sent as sent, j1.done as done, round((j1.done - j1.sent) * 1000) as rtt, j1.node as node, j1.cpu as cpu, j1.cputs as cputs, j2.ram as ram, j2.ramts as ramts, j1.cputs - j2.ramts as metric_ts_delta FROM (SELECT tr.EXP_ID as exp_id, tr.REQUEST_ID as rid, tr.SENT as sent, tr.DONE as done, te.VALUE as cpu, te.TIMESTAMP as cputs, te.NODE as node FROM traces tr LEFT OUTER JOIN telemetry te ON abs(tr.DONE - te.TIMESTAMP) < 0.5 AND te.METRIC = 'cpu' AND te.EXP_ID = tr.EXP_ID WHERE te.exp_id  IN ({idlist})) j1 JOIN (SELECT tr.REQUEST_ID as rid, tr.SENT as sent, tr.DONE as done, te.VALUE as ram, te.TIMESTAMP as ramts, te.NODE as node FROM traces tr LEFT OUTER JOIN telemetry te ON abs(tr.DONE - te.TIMESTAMP) < 0.5 AND te.METRIC = 'ram' AND te.EXP_ID = tr.EXP_ID WHERE te.exp_id  IN ({idlist})) j2 ON j1.rid = j2.rid AND j1.node = j2.node WHERE j1.exp_id  IN ({idlist})".format(idlist=idlist)
        df = pd.read_sql(db_str, con=self._con)
        # df = pd.read_sql(f'SELECT * FROM traces trac WHERE trac.exp_id in ({idlist}) JOIN telemetry tel ON abs(trac.CREATED - tel.TIMESTAMP) < 1 WHERE tel.EXP_ID in ({idlist})', con=self._con)
        # df['RTT'] = df['DONE'] - df['SENT']
        df['sent'] = df['sent'].apply(lambda d: pd.to_datetime(d, unit='s'))
        df['done'] = df['done'].apply(lambda d: pd.to_datetime(d, unit='s'))
        # df['RTT'] = df['RTT'].apply(lambda d: d * 1000)
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

    @staticmethod
    def from_file(filename) -> 'ExperimentFrameGateway':
        artificial_environment = {}
        artificial_environment.setdefault("galileo_expdb_sqlite_path", filename)
        artificial_environment.setdefault("galileo_expdb_driver", "sqlite")
        return ExperimentFrameGateway(create_experiment_database('sqlite', env=artificial_environment))

