
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, jsonify
from dbconnect import connection
from show_users import show_users
from MySQLdb import escape_string as thwart
import gc
import random

app = Flask(__name__)
# my random string
app.config['SECRET_KEY'] = 'refd2334d402'

# MAIN route
@app.route('/')
def hello_world():
    return render_template('main.html')

# route for SELECT all users
@app.route('/_get_users', methods=['GET', 'POST'])
def _get_user():
    try:
        users = show_users()
        return jsonify(users = users)
    except Exception as e:
        return (str(e))

# route for adding new users
@app.route('/_reg_users', methods=['GET', 'POST'])
def _reg_user():
    try:
        name = request.args.get('name')
        # My own rule. Simle validation by length
        if len(str(name))>=3:
            c, conn = connection()
            c.execute("SELECT * FROM users WHERE username = %s",(thwart(name),))
            rows = c.fetchall()
            if len(rows)>0:
                return jsonify(result = "This user ({}) has already registrated".format(name))
            else:
                c.execute("INSERT INTO users (username) VALUES (%s)",(thwart(name),))
                conn.commit()
                c.close()
                conn.close()
                # optimisation
                gc.collect()
                return jsonify(result = "Thank you for registration {}!".format(name))
        else:
            return jsonify(result = "This name ({}) is too short".format(name))

    except Exception as e:
        return(str(e))

# route for deleting of users
@app.route('/_del_user', methods=['GET', 'POST'])
def _del_users():
    try:
        name = request.args.get('name')
        c, conn = connection()
        c.execute("DELETE FROM users WHERE username = %s",(thwart(name),))
        conn.commit()
        c.close()
        conn.close()
        # optimisation
        gc.collect()
        return jsonify(result = '{} was deleted'.format(name))
    except Exception as e:
        return(str(e))

# additional route fot async getting of "LUCKY LIST"
@app.route('/_random', methods=['GET', 'POST'])
def _random():
    try:
        # I don't want to make a new request with specific WHERE statement
        users = show_users()
        # We need at least 4 users (if we have only 3 they are all will be "LUCKY" )
        if len(users)>3:
            numbers = list(range(0,len(users)))
            lucky_num = random.sample(numbers,3)
            lucky_rows =[]
            for i in range(0,len(users)):
                if i in lucky_num:
                    lucky_rows.append(users[i])
            return jsonify(result = lucky_rows)
        else:
            return jsonify(result = 'You have not enough users to do this')
    except Exception as e:
        return(str(e))

if __name__ == "__main__":
    app.run()
