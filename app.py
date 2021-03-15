from flask import ( Flask, render_template, session, redirect, request,
                    url_for, flash,abort,request,logging, jsonify )
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import BotForm, LoginForm, RegistrationForm
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import ( LoginManager, UserMixin, login_user, logout_user,
                          current_user, login_required )
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from rq import Queue
from rq.job import Job
from worker import conn
import stripe
import emoji
import os
import base64



#create the object of Flask
app  =  Flask(__name__)

db = SQLAlchemy(app)
Migrate(app,db)


app.config['SECRET_KEY'] = 'hardsecretkey'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


q = Queue(connection=conn)


#login code
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



##
## MY MODEL
##


class UserInfo(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password



class Bot(db.Model):

    __tablename__ = 'bots'

    id = db.Column(db.Integer, primary_key = True)
    insta_user = db.Column(db.String(20))
    insta_password = db.Column(db.String(20))
    img_data = db.Column(db.LargeBinary)

    bio = db.Column(db.Text)
    followers = db.Column(db.Integer)
    followees = db.Column(db.Integer)
    posts = db.Column(db.Integer)

    tags = db.Column(db.Text)
    comments = db.Column(db.Text)
    location = db.Column(db.String(20))
    radius = db.Column(db.Integer)
    #report = db.Column(db.PickleType)
    media = db.Column(db.String(20))
    created_dt = db.Column(db.DateTime())
    paid = db.Column(db.Boolean())
    status = db.Column(db.Text)
    end_dt = db.Column(db.DateTime())
    #results = db.Column(db.PickleType())
    results = db.Column(db.JSON())

    user_id = db.Column(db.Integer)

    def __init__(self, insta_user, insta_password,
                 img_data, bio, followers, followees, posts,
                 tags, comments, location, radius,
                 media, created_dt, paid, status, end_dt,
                 results, user_id ):

        self.insta_user = insta_user
        self.insta_password = insta_password

        self.img_data = img_data
        self.bio = bio
        self.followers = followers
        self.followees = followees
        self.posts = posts

        self.tags = tags
        self.comments = comments
        self.location = location
        self.radius = radius
        self.media = media
        self.created_dt = created_dt
        self.paid = paid
        self.status = status
        self.end_dt = end_dt
        self.results = results
        self.user_id = user_id





##
## Routing and Views
##


@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')




#login route
@app.route('/login' , methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = UserInfo.query.filter_by(username=form.username.data).first()

            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)

                    return redirect(url_for('profile'))

                flash("Invalid Credentials")

        flash("Succesfull log in champs!")

    return render_template('login.html', form = form)





@app.route('/logout')
@login_required
def logout():
    flash("Succesfull log out!")
    logout_user()
    return redirect(url_for('login'))





@app.route('/register' , methods = ['GET', 'POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data, method = 'sha256')
        username = form.username.data
        password = hashed_password
        email = form.email.data

        new_register =UserInfo(username=username,
                               password=password,
                               email=email)

        db.session.add(new_register)
        db.session.commit()

        flash("Registration was successfull, please login")

        return redirect(url_for('login'))

    return render_template('registration.html', form=form)




@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    import emoji

    bots = Bot.query.filter(Bot.user_id == current_user.get_id() ).all()
    cnt_bots = Bot.query.filter(Bot.user_id == current_user.get_id() ).count()

    return render_template("profile.html", bots=bots, cnt_bots=cnt_bots, emoji=emoji )







@app.route('/addbot',methods=['GET','POST'])
@login_required
def addbot():
    form = BotForm()
    if form.validate_on_submit():

        insta_user = form.insta_user.data
        insta_password = form.insta_password.data
        tags = form.tags.data
        comments = form.comments.data
        location = form.location.data
        radius = form.radius.data
        media = form.media.data

        created_dt = datetime.now()
        paid = False
        user_id = current_user.get_id()
        status = 'Created'
        end_dt = None
        results = None

        # Using INstaloader to get stats
        import instaloader
        import requests

        L = instaloader.Instaloader()
        L.login(insta_user, insta_password)
        profile = instaloader.Profile.from_username(L.context, insta_user)

        bio = profile.biography
        followers = profile.followers
        followees = profile.followees

        post_iterator = profile.get_posts()
        posts = post_iterator.count

        img = profile.get_profile_pic_url()
        response = requests.get(img)
        img_data =  response.content
        image_string = base64.b64encode(img_data)


        new_bot = Bot( insta_user, insta_password,
                       image_string,
                       bio, followers, followees, posts,
                       tags, comments, location,
                       radius, media, created_dt, paid,
                       status, end_dt, results, user_id )


        # Commit these changes to the database
        db.session.add(new_bot)
        db.session.commit()

        flash("Your Inst@Bot creation was successfull!")

        return redirect(url_for('profile'))

    return render_template('create_bot.html', form=form)







@app.route('/delete/<id>')
@login_required
def delete(id):

    bot = Bot.query.filter_by(id=id).first()
    db.session.delete(bot)
    db.session.commit()

    flash("Bot was deleted")

    return redirect(url_for('profile'))






@app.route('/qjob/<id>')
@login_required
def qjob(id):

    bot = Bot.query.filter_by(id=id).first()

    user_id = bot.user_id
    user = UserInfo.query.filter_by(id=user_id).first()

    Pinsta_user = bot.insta_user
    Pinsta_password = bot.insta_password
    Ptags = bot.tags
    Pcomments = bot.comments
    Plocation = bot.location
    Pradius = bot.radius
    Pmedia = bot.media
    Pemail = user.email
    Pbot_id = bot.id
    bot.paid = True
    bot.status = 'Running'

    db.session.commit()

    from utils import run_instapy_bot

    job = q.enqueue(run_instapy_bot, args=(Pemail, Pinsta_user, Pinsta_password, Ptags, Pcomments, Pmedia, Pbot_id) ,job_timeout=72000,
                    result_ttl=86400 )


    flash("Bot creation was successfull! your ID is {}".format(job.get_id()))

    return redirect(url_for('profile'))










#run flask app
if __name__ == "__main__":
    #app.run(debug=True)
    #app.run(host='0.0.0.0', port=80)
    app.debug = True
    app.run(host="0.0.0.0")
