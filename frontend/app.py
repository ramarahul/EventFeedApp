import os
from flask import Flask, render_template, request, url_for, redirect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': 'roidtc-0323-attendee133',
})

db = firestore.client()
N = 7

app = Flask(__name__)

resultDict = {}
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] != 'password' or request.form['username'] != 'admin':
            error = 'Invalid Credentials'
            # return render_template('dashboard.html')
        else:
            # flash('wrong password!')
            return redirect(url_for('hello_world'))
    return render_template('login.html', error=error)


@app.route('/home')
def hello_world():
    return render_template('facebook.html')


@app.route('/post', methods=['POST', 'GET'])
def post_data():
    if request.method == 'POST':
        resultTitle = request.form['title']
        resultBody = request.form['event']
        data = {
            u'title': resultTitle,
            u'event': resultBody
        }
        db.collection(u'events').add(data)
        docs = db.collection(u'events').stream()
        firebaseDict = {}
        for doc in docs:
            firebaseDict[doc.to_dict()['title']] = doc.to_dict()['event']

        return render_template("facebook-post.html", firebaseDict=firebaseDict)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
