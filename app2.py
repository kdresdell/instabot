from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_script import Manager



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config['SECRET_KEY'] = "765765675"

db = SQLAlchemy(app)
migrate = Migrate(app,db) #Initializing migrate.
manager = Manager(app)
# set FLASK_APP=app






@app.route('/')
def index():
    return render_template('index2.html')

@app.route("/ajaxprogressbar", methods=["POST","GET"])
def ajaxprogressbar():
    if request.method == 'POST':
        username = request.form['username']
        useremail = request.form['useremail']
        print(username)
        #cursor = mysql.connection.cursor()
        #cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cur.execute("INSERT INTO tbl_user (username, useremail) VALUES (%s, %s)",[username, useremail])
        #mysql.connection.commit()
        #cur.close()
        msg = 'New record created successfully'
    return jsonify(msg)

if __name__ == "__main__":
    app.run(debug=True)
