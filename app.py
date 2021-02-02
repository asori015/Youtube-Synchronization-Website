from flask import Flask, render_template, url_for, request, redirect
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from datetime import datetime
import re

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#sqlite initalization
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#socketio initialization
app.config['SECRET_KEY'] = 'vajiralongko1232#'
socketio = SocketIO(app)

currentSeconds = {'seconds': 0.0}
currentURL = 'M7lc1UVf-VE'
currentPlayState = False

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    print("in index")
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    print("in delete")
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task.'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    print("in update")
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task.' 
    else:
        return render_template('update.html', task=task_to_update)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    print(request.sid)
    socketio.emit('my response', json, callback=messageReceived)

@socketio.on('new url')
def setYoutubeURL(json):
    x = re.findall(r'(http://)?(https://)?www\.youtube\.com/watch\?v=([a-zA-Z0-9_]+)(&list=)?([a-zA-z0-9_]+)?(&index=)?([0-9])?', json['url'])
    print('got new url' + str(json))
    print(x)
    if len(x) > 0:
        currentURL = x[0][2]
        socketio.emit('new url', {"new url" : x[0][2]})
    elif len(x) == 0:
        socketio.emit('new url', {"new url" : ""})

@socketio.on('play')
def playYoutube():
    print('playing video')
    currentPlayState = True
    socketio.emit('play', currentSeconds)

@socketio.on('pause')
def pauseYoutube(json):
    print('pausing video')
    print(json['seconds'])
    currentSeconds['seconds'] = json['seconds']
    currentPlayState = False
    socketio.emit('pause')

@socketio.on('connect')
def log_connect():
    print("new user connected")
    # print(request)
    # print(request.sid)
    # print(request.namespace)
    # print(request.namespace.socket)
    # print(request.namespace.socket.sessid)
    # socketio.
    # socketio.emit('startup', {
    #     'url' : currentURL,
    #     'seconds' : str(currentSeconds['seconds']),
    #     'state' : str(currentPlayState)
    # }, broadcast=False)

@socketio.on('disconnect')
def log_disconnect():
    print("user disconnected")

if __name__  == "__main__":
    socketio.run(app, debug=True)
