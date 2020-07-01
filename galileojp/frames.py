import pandas as pd
from galileodb.sql.adapter import ExperimentSQLDatabase


class ExperimentFrameGateway:

    def __init__(self, edb: ExperimentSQLDatabase) -> None:
        super().__init__()
        self.edb = edb
        self.exp_id = None

    def load_experiment(self, exp_id) -> pd.DataFrame:
        exp = self.edb.get_experiment(exp_id)
        if not exp:
            raise ValueError('no such experiment')

        self.exp_id = exp_id

        return pd.read_sql(f'SELECT * FROM experiments WHERE exp_id = "{exp_id}"', con=self.edb.db.connection)

    def events(self):
        return pd.read_sql(f'SELECT * FROM events WHERE exp_id = "{self.exp_id}"', con=self.edb.db.connection)

    def telemetry(self):
        return pd.read_sql(f'SELECT * FROM telemetry WHERE exp_id = "{self.exp_id}"', con=self.edb.db.connection)
