from sqlalchemy import create_engine, Column, String, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="123456",
    host="localhost",
    port=5432,
    database="fingerprint"
)

engine = create_engine(url)

# Create a base class for declarative models
Base = declarative_base()


class DB_Finger_Win(Base):
    __tablename__ = 'finger_win'

    id = Column(String, primary_key=True)
    data = Column(String)
    hash = Column(String)
    os = Column(String)


def get_random_fingerprint() -> DB_Finger_Win:
    Session = sessionmaker(bind=engine)
    session = Session()

    sql_query = text("SELECT * FROM finger_win ORDER BY random() LIMIT 1")

    # Query and print all users in the database
    query_result = session.query(DB_Finger_Win).from_statement(sql_query)
    results = query_result.all()
    print("All fingerprints:")
    for fingerprint in results:
        print(f"ID: {fingerprint.id}, data: {fingerprint.data}, os: {fingerprint.os}")
    return results[0]
