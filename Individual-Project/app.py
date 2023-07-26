from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
config = {
  'apiKey': "AIzaSyCBgTfrTSzGdL2nNbFpA8Pq45-pB8wdXPg",
  'authDomain': "individual-project-nada.firebaseapp.com",
  'projectId': "individual-project-nada",
  'storageBucket': "individual-project-nada.appspot.com",
  'messagingSenderId': "782047104386",
  'appId': "1:782047104386:web:9012c6d78b06996731d39b",
  'measurementId': "G-ENGYJWWPW7",
  'databaseURL':'https://individual-project-nada-default-rtdb.europe-west1.firebasedatabase.app/'
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()


@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=''
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        full_name=request.form['full_name']
        username=request.form['username']
        try:
            login_session['user']=auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user={'email':email, 'password':password, 'full_name':full_name, 'username':username, 'bio':'','rating':'','location':'','music_type':'','link':''}
            print("meow2")
            db.child('Users').child(UID).set(user)
            return redirect (url_for('next'))
        except:
            error='Authentication failed'
            return render_template('signup.html')
    else:
        return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error=''
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        try:
            login_session['user']=auth.sign_in_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            return redirect (url_for('home'))
        except:
            error='Authentication failed'
            return render_template('signin.html')
    else:
        return render_template('signin.html')

@app.route('/next', methods=['POST','GET'])
def next():
    error=''
    if request.method=='POST':
        bio=request.form['bio']
        rating=request.form['rating']
        location=request.form['location']
        music_type=request.form['music_type']
        link=request.form['link']
        artist=request.form['artist']
        insta_link=request.form['insta_link']

        try:
            UID=login_session['user']['localId']
            db.child('Users').child(UID).update({'bio':bio,'rating':rating,'location':location,'music_type':music_type,'link':link,"artist":artist,'insta_link':insta_link})
            return redirect(url_for('home'))
        except Exception as e:
            error='idk'
            print(e)
            return render_template('next.html')
    else:
        return render_template('next.html')

@app.route('/home', methods=['POST','GET'])
def home():
    users=db.child('Users').get().val()
    current_user=login_session['user']['localId']
    return render_template("home.html", users=users, current_user=current_user)


@app.route('/artist/<string:i>')
def artist(i):
    artist= db.child('Users').child(i).get().val()
    return render_template('artist.html', artist=artist)


@app.route('/logout')
def logout():
    login_session['user'] =None
    auth.current_user=None
    return redirect (url_for('intro'))



#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)