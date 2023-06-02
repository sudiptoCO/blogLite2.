from flask import Flask, jsonify, request, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, Text, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from flask_marshmallow import Marshmallow
from werkzeug.exceptions import abort
from flask_cors import CORS, cross_origin
from flask_login import UserMixin
from flask_login import LoginManager,login_user,logout_user,login_required,UserMixin,current_user
from werkzeug.security import check_password_hash
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_login import AnonymousUserMixin
from flask import session
from flask_jwt_extended import create_access_token
from datetime import timedelta
from flask_jwt_extended import jwt_required
import redis
import json
import os
import base64
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from celery import Celery
from celery.schedules import crontab
import jinja2




"""-----------------------------Set up--------------------------------"""
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://///home/sudipto/Desktop/NPTEL_IITM/BlogLite2/blog_app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
mm = Marshmallow(app)
login_manager = LoginManager()
login_manager.init_app(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
app.config['SECRET_KEY'] = 'mysecretkey'
jwt = JWTManager(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}
redis_client = redis.Redis(host='localhost', port=6379, db=0)
db = SQLAlchemy(app)
ma = Marshmallow(app)
SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "email@memail.com"
SENDER_PASSWORD = "123"
celery = Celery(app.name, broker='redis://localhost:6379/0',timezone = 'Asia/Kolkata')
celery.conf.update(app.config)
celery.conf.beat_schedule = {
    'send_daily': {
        'task': 'app.send_daily',
        'schedule': crontab(hour=00, minute=2),
    },
    'send_monthly': {
        'task': 'app.send_monthly',
        'schedule': crontab(day_of_month='1', hour=0, minute=0),
    },
}


'''@app.before_request
def before_request():
    # Create a Redis connection for the current request context
    g.redis = redis_client
'''


#Test the route
'''@app.route('/',methods=['GET'])
def get_hello():
    return jsonify({"hello":"world"})'''
"""-------------------------------Models----------------------------------"""
#Define the tables
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    num_followers = Column(Integer)
    num_followings = Column(Integer)
    num_posts = Column(Integer)

    posts = relationship('BlogPost', backref='author')

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', password='{self.password}', num_followers={self.num_followers}, num_posts={self.num_posts})"

    # Define a method to check the password hash against a plaintext password
    def check_password(self, password):
        #print(self.password, password)
        return(self.password == password)
    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False


class BlogPost(db.Model,UserMixin): #Stores the information about blog posts, images to included later
    __tablename__ = 'blog_posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    text = Column(Text)
    image_url = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self,title,text,image_url,auth):
        
        self.title = title
        self.text = text
        self.image_url = image_url
        self.author_id = auth

class Followers(db.Model,UserMixin):
    __tablename__ = 'followers'

    follower_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    followed_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    def __repr__(self):
        return f"Followers(follower_id={self.follower_id}, followed_id={self.followed_id})"


class PostSchema(mm.Schema):
    class Meta:
        fields = ('id','title','text','image')
post_schema = PostSchema()
posts_schema = PostSchema(many = True)

@login_manager.user_loader
def load_user(user_id):
    # Retrieve the user from your database or other data store
    print(current_user,"from load user")
    return User.query.get(int(user_id))



"""-------------------------------API----------------------------------"""
g_user = -1

@app.route('/login', methods=['POST'])
def login():
    global g_user  
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(name=username).first()

    if user is not None and user.check_password(password):
        login_user(user,remember=True,force=True,duration=timedelta(seconds=600))
        print(current_user,"from login")
        g_user = current_user.id
        access_token = create_access_token(identity=user.id,expires_delta = timedelta(seconds=600))
        return jsonify({'success': True, 'token': access_token})
    else:
        return jsonify({'success': False, 'error': 'Invalid username or password'})




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'success': True})







@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form.get('title')
    text = request.form.get('text')
    auth = request.form.get('author_id')

    image = request.files.get('image')
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    else:
        image_url = None

    post = BlogPost(title=title, text=text, image_url=image_url,auth = g_user)
    user = User.query.filter_by(id=g_user).first()
    user.num_posts += 1
    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Post added successfully'})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']








@app.route('/add_user', methods=['POST']) #crosschecked
def add_user():
    json_payload = request.get_json(force=True)
    name = json_payload.get('name')
    password = json_payload.get('password')

    user = User(name=name, password=password, num_followers=0, num_posts=0,num_followings = 0)
    
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User added successfully'})





@app.route('/get_followers',methods= ['GET'])
def get_followers():
    

    # Retrieve the user with the given username
    print(g_user)
    user = User.query.filter_by(id=g_user).first()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    # Retrieve the list of followers for the user
    followers = Followers.query.filter_by(followed_id=user.id).all()

    follower_list = []
    for follower in followers:
        follower_info = {
            'id': follower.follower_id,
            'name': User.query.filter_by(id=follower.follower_id).first().name
        }
        follower_list.append(follower_info)

    return jsonify({'followers': follower_list})








@app.route('/get_followings')
def get_followings():
    username = g_user

    # Retrieve the user with the given username
    user = User.query.filter_by(id=username).first()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    # Retrieve the list of followings for the user
    followings = db.session.query(User).join(Followers, Followers.followed_id == User.id).filter(Followers.follower_id == user.id).all()

    # Create a list of dictionaries containing id and name of each followed user
    following_list = []
    for following in followings:
        following_info = {
            'id': following.id,
            'name': following.name
        }
        following_list.append(following_info)

    return jsonify({'followings': following_list})




@app.route('/get_posts')
def get_posts():
    # Retrieve the user with the given ID
    g.redis = redis_client
    user_id = g_user
    user = User.query.filter_by(id=user_id).first()
    print(user,"from get posts")
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    # Try to retrieve the list of posts from Redis cache
    redis_key = f"user:{user_id}:posts"
    post_dicts = g.redis.get(redis_key)
    if post_dicts:
        # If the data exists in cache, return it
        print('from cache')
        post_dicts = json.loads(post_dicts)
        print(len(post_dicts))
    else:
        # Otherwise, retrieve the list of posts from the database
        posts = BlogPost.query.filter_by(author_id=user.id).all()

        # Convert the posts to a list of dictionaries
        post_dicts = [post.__dict__ for post in posts]


        post_dicts = []
        for post in posts:
            post_dict = post.__dict__
            post_dict['timestamp'] = post.timestamp.isoformat() # Convert datetime to string
            del post_dict['_sa_instance_state']
            del post_dict['author_id']

            # If the post has an image, add a base64-encoded version to the dictionary
            if post_dict['image_url'] != "":
                with open(post_dict['image_url'], "rb") as f:
                    image_bytes = f.read()
                    base64_encoded = base64.b64encode(image_bytes).decode('utf-8')
                    post_dict['image_base64'] = 'data:image/jpeg;base64,' + base64_encoded

            post_dicts.append(post_dict)
            g.redis.set(redis_key, json.dumps(post_dicts),ex = 30)

    return jsonify({'posts': post_dicts})



def encode_image(url):
    if url != "":
        with open(url, "rb") as f:
            image_bytes = f.read()
            base64_encoded = base64.b64encode(image_bytes).decode('utf-8')
            return base64_encoded
    else:
        return ""







@app.route('/follow', methods=['POST'])
def follow():
    # Retrieve the IDs of the follower and the followed users from the request body
    data = request.get_json(force=True)
    follower_id = g_user
    followed_id = data.get('followed_id')

    # Make sure both IDs are present
    if follower_id is None or followed_id is None:
        return jsonify({'error': 'Missing follower or followed ID'}), 400

    # Make sure both IDs correspond to valid users
    follower = User.query.filter_by(id=follower_id).first()
    followed = User.query.filter_by(id=followed_id).first()

    if follower is None or followed is None:
        return jsonify({'error': 'Invalid follower or followed ID'}), 400

    # Check if the follower is already following the followed user
    if Followers.query.filter_by(follower_id=follower_id, followed_id=followed_id).first() is not None:
        return jsonify({'error': 'User already followed'}), 400

    # Create a new follower relationship
    new_followership = Followers(follower_id=follower_id, followed_id=followed_id)
    db.session.add(new_followership)

    # Update the follower and followed user's num_followers and num_followings
    follower.num_followings += 1
    followed.num_followers += 1

    db.session.commit()

    return jsonify({'message': 'User followed successfully'}), 200




@app.route('/unfollow', methods=['POST'])
def unfollow():
    # Retrieve the IDs of the follower and the followed users from the request body
    data = request.get_json(force=True)
    follower_id = g_user
    followed_id = data.get('followed_id')
    print(followed_id,follower_id , "from unfollow")
    # Make sure both IDs are present
    if follower_id is None or followed_id is None:
        return jsonify({'error': 'Missing follower or followed ID'}), 400

    # Make sure both IDs correspond to valid users
    follower = User.query.filter_by(id=follower_id).first()
    followed = User.query.filter_by(id=followed_id).first()
    print(follower,followed,'from unfollow')
    if follower is None or followed is None:
        return jsonify({'error': 'Invalid follower or followed ID'}), 400

    # Check if the follower is currently following the followed user
    followership = Followers.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()
    if followership is None:
        return jsonify({'error': 'User not followed'}), 400

    # Delete the follower relationship
    db.session.delete(followership)
    follower.num_followings -= 1
    followed.num_followers -= 1
    db.session.commit()

    return jsonify({'message': 'User unfollowed successfully'}), 200


@jwt_required
@app.route('/delete_post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = BlogPost.query.get(post_id)
    if not post:
        abort(404, description=f"Post with ID {post_id} not found")

    user = User.query.get(g_user)
    if not user:
        abort(404, description=f"User with ID { g_user } not found")

    user.num_posts -= 1

    db.session.delete(post)
    db.session.commit()

    return post_schema.jsonify(post)



@app.route('/edit/<int:post_id>', methods=['PUT'])
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    if not post:
        abort(404, description='Post not found')

    json_payload = request.get_json(force=True)
    title = json_payload.get('title', post.title)
    text = json_payload.get('text', post.text)
    
    post.title = title
    post.text = text
    

    db.session.commit()

    return post_schema.jsonify(post)

###################Fix IT##########################3
@app.route('/pdit/<int:post_id>')
def pdit(post_id):
    post = BlogPost.query.get_or_404(post_id)
    post_data = {'title': post.title, 'text': post.text, 'id':post.id}
    return jsonify(post_data)


@app.route('/users/<int:user_id>')
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(404)  # Return a 404 error if the user isn't found
    num_followers = Followers.query.filter_by(followed_id=user_id).count()
    num_following = Followers.query.filter_by(follower_id=user_id).count()
    return jsonify({
        'id': user.id,
        'name': user.name,
        'num_followers': num_followers,
        'num_followings': num_following,
        'num_posts': user.num_posts
    })



@jwt_required
@app.route('/get_user_posts/<int:user_id>')
def get_user_posts(user_id):
    # Retrieve the user with the given ID
    user = User.query.filter_by(id=user_id).first()
    print(user,"from get posts")
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    # Try to retrieve the list of posts from Redis cache
    redis_key = f"user:{user_id}:posts"
    post_dicts = redis_client.get(redis_key)
    if post_dicts:
        # If the data exists in cache, return it
        print('get_user_post responding from from cache')
        post_dicts = json.loads(post_dicts)
        print(len(post_dicts))
    else:
        # Otherwise, retrieve the list of posts from the database
        posts = BlogPost.query.filter_by(author_id=user.id).all()

        # Convert the posts to a list of dictionaries
        post_dicts = []
        for post in posts:
            post_dict = post.__dict__
            post_dict['timestamp'] = post.timestamp.isoformat() # Convert datetime to string
            del post_dict['_sa_instance_state']
            del post_dict['author_id']

            # If the post has an image, add a base64-encoded version to the dictionary
            if post_dict['image_url'] != "":
                with open(post_dict['image_url'], "rb") as f:
                    image_bytes = f.read()
                    base64_encoded = base64.b64encode(image_bytes).decode('utf-8')
                    post_dict['image_base64'] = 'data:image/jpeg;base64,' + base64_encoded

            post_dicts.append(post_dict)
        # Set the data in Redis cache with an expiration time of 30 seconds
        redis_client.set(redis_key, json.dumps(post_dicts), ex=30)

    return jsonify({'posts': post_dicts})

@app.route('/search')
def search_users():
    print('activate')
    # Get the search query from the request arguments
    search_query = request.args.get('q')

    # Perform a case-insensitive search for users matching the search query
    matching_users = User.query.filter(User.name.ilike(f'{search_query}%')).all()

    # Convert the matching users to a list of dictionaries
    user_dicts = [user.__dict__ for user in matching_users]

    # Remove the attributes that we don't want to expose in the API
    for user_dict in user_dicts:
        del user_dict['_sa_instance_state']
        del user_dict['password']

    # Return the list of matching users
    return jsonify({'users': user_dicts})














@app.route('/get_feed', methods=['GET', 'POST'])
def get_feed():
    result = db.engine.execute(f"SELECT followed_id FROM followers WHERE follower_id={g_user}")
    followers_list = [row[0] for row in result]

    posts = []
    for person in followers_list:
        post_objs = BlogPost.query.filter_by(author_id=person).all()
        for post in post_objs:
            usr = User.query.get(post.author_id)
            name = usr.name
            encoded_img = encode_image(post.image_url)

            post_dict = {
                'post_id': post.id,
                'post_title': post.title,
                'post_text': post.text,
                'author_id': post.author_id,
                'name' : name,
                'image64': 'data:image/jpeg;base64,'+encoded_img,
                'timestamp': post.timestamp



            }
            posts.append(post_dict)

    #print(post_dict,"printing post dict")
    feed_dict = {}
    for person in followers_list:
        feed_dict[person] = [post_dict for post_dict in posts if post_dict['author_id'] == person]
    #print(feed_dict)
    return jsonify(feed_dict)


###Fix the issue here



@app.route('/getmyinfo',methods= ['GET','POST'])
@jwt_required()
def get_my_info():

    print(current_user)
    user_id = g_user
    print(user_id,"from getmyinfo")
    user = User.query.get(user_id)
    num_followers = Followers.query.filter_by(followed_id=user_id).count()
    num_following = Followers.query.filter_by(follower_id=user_id).count()

    return jsonify(name=user.name, followers= num_followers,posts=user.num_posts,followings = num_following)

@app.route('/isfollowed', methods=['GET','POST'])
def is_followed():
    # Retrieve the IDs of the follower and the followed users from the request body
    data = request.get_json(force=True)
    follower_id = g_user
    followed_id = data.get('followed_id')

    # Make sure both IDs are present
    if follower_id is None or followed_id is None:
        return jsonify({'error': 'Missing follower or followed ID'}), 400

    # Make sure both IDs correspond to valid users
    follower = User.query.filter_by(id=follower_id).first()
    followed = User.query.filter_by(id=followed_id).first()

    if follower is None or followed is None:
        return jsonify({'error': 'Invalid follower or followed ID'}), 400

    # Check if the follower is already following the followed user
    if Followers.query.filter_by(follower_id=follower_id, followed_id=followed_id).first() is not None:
        return jsonify({'is_followed': True}), 200
    else:
        return jsonify({'is_followed': False}), 200

"""-----------------------------Backend Jobs----------------------------------"""
import jinja2

def render_without_request(template_name, **template_vars):

    env = jinja2.Environment(
        loader=jinja2.PackageLoader('backend','templates')
    )
    template = env.get_template(template_name)
    return template.render(**template_vars)





def send_email(to_addr, subject, message):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_ADDRESS
        msg['To'] = to_addr
        msg["Subject"] = subject
        msg.attach(message)

        s = smtplib.SMTP(host=SMTP_SERVER_HOST,port=SMTP_SERVER_PORT)
        s.login(SENDER_ADDRESS,SENDER_PASSWORD)
        s.send_message(msg)
        s.quit()
        return True
    except Exception as e:
        print("An error occurred while sending email: ", str(e))
        return False


from datetime import datetime, date
from flask import render_template
def check_last_upload_today(user_id):
    user = User.query.get(user_id)
    if user:
        last_post = BlogPost.query.filter_by(author_id=user_id).order_by(BlogPost.timestamp.desc()).first()
        if last_post:
            last_post_date = last_post.timestamp.date()
            today_date = date.today()
            if last_post_date == today_date:
                return True
    return False






def get_user_stats(user_id):
    user = User.query.filter_by(id=user_id).first()
    num_posts = len(user.posts)
    num_followers = Followers.query.filter_by(followed_id=user_id).count()
    num_following = Followers.query.filter_by(follower_id=user_id).count()
    name = user.name
    return num_posts, num_followers, num_following,name


@celery.task
def send_monthly():
    # Query all users from the User table
    users = db.session.query(User).all()
    
    # Extract the names of all users
    user_ids = [user.id for user in users]
    
    for i in user_ids:
        num_posts, num_followers, num_following,name = get_user_stats(i)
        subject = "Monthly Reminder"
        to_addr = name+"@mymail.com"
        html = render_without_request("monthly.html",num_posts = num_posts, num_followers = num_followers, num_followings = num_following,name = name)
        message = MIMEText(html, "html")
                
        send_email(to_addr, subject, message)
    print('monthly email sent')
    return True
@celery.task
def send_daily():
    print('daily email entered')
    # Query all users from the User table
    users = db.session.query(User).all()
    
    # Extract the names of all users
    user_names = [user.name for user in users]
    
    for i in user_names:
        if not check_last_upload_today(i):
            subject = "Daily Reminder"
            to_addr = i+"@mymail.com"
            with app.app_context(), app.test_request_context():
                html = render_template("daily.html", uname=i)
                message = MIMEText(html, "html")
            
            send_email(to_addr, subject, message)
    print('daily email sent')
    return True




@app.route('/email_test_monthly')
def email_test_monthly():
    send_monthly()
    return jsonify({'true':'true'})

@app.route('/email_test_daily')
def email_test_daily():
    send_daily()
    return jsonify({'true':'true'})

import pandas as pd
from flask import make_response

@app.route('/export')
def export():
    # Retrieve all posts of the given user from the database
    user = User.query.get(g_user)
    posts = user.posts

    # Convert the posts to a list of dictionaries
    post_list = []
    for post in posts:
        post_dict = post_schema.dump(post)
        post_list.append(post_dict)

    # Create a Pandas DataFrame from the post list
    df = pd.DataFrame(post_list)

    # Convert the DataFrame to a CSV file
    csv = df.to_csv(index=False)

    # Create a response object for downloading the CSV file
    response = make_response(csv)
    response.headers['Content-Disposition'] = f'attachment; filename={user.name}_posts.csv'
    response.headers['Content-Type'] = 'text/csv'

    return response
















'''
@app.route('/test',methods=['POST'])
def dubg():
    print(request.json)
    return jsonify({"testing":"debug"})'''


if __name__ == "__main__":
    db.create_all()  # create all the tables defined in your models
    app.run(debug=True,port=5001)
