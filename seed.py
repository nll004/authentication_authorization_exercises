from app import app
from models import Feedback, db, connect_db, User, hash_pwd

connect_db(app)
db.drop_all()
db.create_all()

user1 = User(
    first_name= 'Nathan',
    last_name = 'Ginter',
    username = 'user3',
    password = hash_pwd('hi'),
    email = 'fake@yahoo.com'
)

user2 = User(
    first_name= 'Chris',
    last_name = 'Jones',
    username = 'user1',
    password = hash_pwd('hi'),
    email = 'fake29@yahoo.com'
)

user3 = User(
    first_name = 'Jim',
    last_name = 'Yunce',
    username = 'user2',
    password = hash_pwd('hi'),
    email= 'tricky@yahoo.com'
 )

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.commit()

feed1 = Feedback(title="Post1", content='Post content', username='user1')
feed2 = Feedback(title="Post2", content='Post content', username='user1')
feed3 = Feedback(title="Post3", content='Post content', username='user1')
feed4 = Feedback(title="Post1", content='Post content', username='user2')
feed5 = Feedback(title="Post2", content='Post content', username='user2')
feed6 = Feedback(title="Post1", content='Post content', username='user3')

db.session.add(feed1)
db.session.add(feed2)
db.session.add(feed3)
db.session.add(feed4)
db.session.add(feed5)
db.session.add(feed6)
db.session.commit()
