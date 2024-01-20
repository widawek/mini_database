import sqlalchemy
import pandas as pd  # intentionally ignore to_sql method in pandas
from sqlalchemy import create_engine, inspect
from sqlalchemy import Table, Column, MetaData, Integer, \
                        Float, String, ForeignKey


def show_table_columns(table):
    columns = inspector.get_columns(table)
    names = [column['name'] for column in columns]
    print(f"Table --{table}-- columns: ", names)


if __name__ == '__main__':

    clean_stations = pd.read_csv("csv/clean_stations.csv")
    clean_measure = pd.read_csv("csv/clean_measure.csv", )

    print(clean_stations.info())
    print(clean_measure.info())
    engine = create_engine('sqlite:///database.db', echo=True)
    meta = MetaData()
    inspector = inspect(engine)

    clean_stations_table = Table(
        'stations', meta,
        Column('station', String),
        Column('latitude', Float),
        Column('longitude', Float),
        Column('elevation', Float),
        Column('name', String),
        Column('country', String),
        Column('state', String),
    )

    clean_measure_table = Table(
        'measure', meta,
        Column('station', String,
               ForeignKey('stations.station')),
        Column('date', String),
        Column('precip', Float),
        Column('tobs', Integer)
    )

    meta.create_all(engine)
    print(inspector.get_table_names())

    for table in inspector.get_table_names():
        show_table_columns(table)

    # Add data to table measures from pandas
    ins = clean_stations_table.insert().values()
    with engine.connect() as conn:
        result = conn.execute(ins, clean_stations.to_dict(orient='records'))
        conn.commit()

    ins = clean_measure_table.insert().values()
    with engine.connect() as conn:
        result = conn.execute(ins, clean_measure.to_dict(orient='records'))
        conn.commit()
