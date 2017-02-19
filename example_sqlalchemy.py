from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:')

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

session.add_all([
    User(name='ed', fullname='Ed Jones', password='edspassword'),
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')
])
session.commit()

# typical usage
users = session.query(User).filter(User.name == 'fred').all()
print('Users', users)

# explained
my_query = session.query(User)
print('Base query:', my_query, repr(my_query))
my_filter = User.name == 'fred'
print('Base filter:', my_filter, repr(my_filter))
filtered_query = my_query.filter(my_filter)
print('Query with filter:', filtered_query, repr(filtered_query))
filtered_users = filtered_query.all()
print('Filtered users:', filtered_users)
