# Dumps sqlite file to CSVs

import pandas as pd 
import sqlalchemy as db
import csv
import argparse

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("database", help="SQLite database file to dump", type=str)

    args = parser.parse_args()

    engine = db.create_engine("sqlite:///{}".format(args.database))
    meta = db.MetaData()
    meta.reflect(bind=engine)
    conn = engine.connect()

    for table_name in meta.tables:
        table = db.Table(table_name, meta, autoload=True, autoload_with=engine)
        query = db.select([table])
        ResultProxy = conn.execute(query)
        ResultSet = ResultProxy.fetchall()

        df = pd.DataFrame(ResultSet)
        df.to_csv(table_name + ".csv")

if __name__ == "__main__":
    main()