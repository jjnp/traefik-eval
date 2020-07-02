galileo-jupyter
===============

Tools for analyzing galileo experiments.

Configuration
-------------

Create a `$HOME/.galileojp` and fill with environment variables that configure the database access to galileo-db.
For example:

```
galileo_expdb_driver=mysql

galileo_expdb_mysql_host=localhost
galileo_expdb_mysql_port=3307
galileo_expdb_mysql_db=galileo
galileo_expdb_mysql_user=galileo
galileo_expdb_mysql_password=mypassword
```

Usage
-----

Then you can run

```python
from galileojp.frames import ExperimentFrameGateway

efg = ExperimentFrameGateway.from_env()
efg.telemetry('my-exp-id') # returns a dataframe containing the telemetry for the given experiment
```
