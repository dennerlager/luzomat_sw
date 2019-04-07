import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy import Table, Column, Integer, String, MetaData

class Counter():
    def __init__(self, name):
        self.dbConnection = DbConnection()
        self.name = name
        self.count = self.dbConnection.getCounter(self.name)

    def __add__(self, other):
        self.count += other
        self.dbConnection.writeCounter(self.name, self.count)
        return self

    def __repr__(self):
        return 'counter {}: {}'.format(self.name, self.count)

    def increase(self):
        self += 1

    def getCount(self):
        return self.count

class DbConnection:
    def __init__(self):
        self.engine = sqlalchemy.create_engine('sqlite:///db.db')
        self.connection = self.engine.connect()
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    def getCounter(self, name):
        counters = self.getCountersTable()
        statement = select([counters.c.count]).where(
            counters.c.name == name)
        result = self.connection.execute(statement).fetchone()
        if result:
            return result[0]
        self.createCounter(name)
        return self.getCounter(name)

    def getCountersTable(self):
        try:
            return self.metadata.tables['counters']
        except KeyError:
            self.createCountersTable()
        return self.getCountersTable()

    def createCountersTable(self):
        Table('counters', self.metadata,
              Column('pkey', Integer, primary_key=True),
              Column('name', String, unique=True),
              Column('count', Integer))
        self.metadata.create_all(self.engine)

    def createCounter(self, name):
        counters = self.getCountersTable()
        self.connection.execute(counters.insert().values(name=name, count=0))

    def writeCounter(self, name, count):
        counters = self.getCountersTable()
        self.connection.execute(counters.update().values(name=name, count=count))

if __name__ == '__main__':
    c = Counter('luz')
    c.increase()
    print(c)
