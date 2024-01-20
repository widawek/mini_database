from sqlalchemy import create_engine, text


engine = create_engine('sqlite:///database.db', echo=True)
conn = engine.connect()
query = text("SELECT * FROM stations LIMIT 5")
result = conn.execute(query)

for row in result:
    print(row)
