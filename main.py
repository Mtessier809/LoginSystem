from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


def addUser(name, email):
    # connecting to database#
    cnx = mysql.connector.connect(user='mtessier', password='Apple123!', host='localhost', port=3306,
                                  database='flaskapp')
    # creating new cursor
    cursor = cnx.cursor(buffered=True)
    # check if user already has an account with email
    check_user = ("SELECT email FROM users WHERE email = '{}'".format(email))
    cursor.execute(check_user)
    # if no user is found then create a new account
    if cursor.rowcount == 0:
        add_user = ("INSERT INTO users(email,name) VALUES('{}','{}');".format(email, name))
        cursor.execute(add_user)
    else:
        print("A user under the email {} already exists.".format(email))
    # committing change
    cnx.commit()
    # closing cursor and database connection
    cursor.close()
    cnx.close()


@app.route("/", methods=['GET', 'POST'])
def home():
    # creating new user in database if a form was submitted
    if request.method == 'POST':
        # fetching user info from form
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        addUser(name, email)

    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
