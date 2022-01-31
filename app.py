from flask import Flask, render_template, url_for, request, redirect
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from datetime import datetime
import re

# flask initialization
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# sqlite initalization
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# socketio initialization
app.config['SECRET_KEY'] = 'vajiralongko1232#'
socketio = SocketIO(app)

# Global variables
currentSeconds = {'seconds': 0.0}       # Current time in seconds of YT video
currentTimestamp = {'timestamp': 0}     # Current timestamp of most recent 'play' event emitted
currentURL = {'url': 'M7lc1UVf-VE'}     # Current url of YT video
currentIP = {'ip': '0.0.0.0'}           # Current IP address of livestream
currentPlayState = {'state': False}     # Is YT video playing?
currentSIDs = {}                        # socket IDs of currently connected clients

# SQL schema
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# index.html route
@app.route('/', methods=['POST', 'GET'])
def index():
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

# delete task route
@app.route('/delete/<int:id>')
def delete(id):
    print("in delete") # debug
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task.'

# update task route
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    print("in update") # debug
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

# 'chat message' event
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json)) # debug
    socketio.emit('my response', json)

# 'play YT video for all clients' event
@socketio.on('play')
def playYoutube(json):
    print('playing video') # debug
    currentTimestamp['timestamp'] = json['timestamp']
    currentPlayState['state'] = True
    socketio.emit('play', {**currentSeconds, **currentTimestamp})

# 'pause YT video for all clients' event
@socketio.on('pause')
def pauseYoutube(json):
    print('pausing video') # debug
    currentSeconds['seconds'] = json['seconds']
    currentPlayState['state'] = False
    socketio.emit('pause')

# 'update YT video url' event
@socketio.on('new url')
def setYoutubeURL(json):
    print('got new url' + str(json)) # debug
    urls = re.findall(r'(http:\/\/|https:\/\/)?(www\.)?youtu(be\.com\/watch\?v=|\.be\/|be\.com\/embed\/)([a-zA-Z0-9_-]+)(&list=)?([a-zA-z0-9_-]+)?(&index=)?([0-9])?', json['url'])
    if len(urls) > 0:
        currentURL['url'] = urls[0][3]
        socketio.emit('new url', {"new url" : urls[0][3]})
    elif len(urls) == 0:
        socketio.emit('new url', {"new url" : ""})

# 'update livestream IP address' event
@socketio.on('new ip')
def setLivestreamIP(json):
    print('got new ip' + str(json)) # debug
    ip = re.findall(r'[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}', json['ip'])
    if len(ip) > 0:
        currentIP['ip'] = ip[0]
        socketio.emit('new ip', {"new ip" : ip[0]})
    elif len(ip) == 0:
        socketio.emit('new ip', {"new ip" : ""})

# 'debug' event
@socketio.on('debug')
def debugServer():
    print("Debug information:")
    print(currentURL)
    print(currentSeconds)
    print(currentPlayState)

# default connection event for new clients
@socketio.on('connect')
def log_connect():
    print("new user connected")  # debug
    currentSIDs[request.sid] = [0,0]
    print(currentSIDs)  # debug
    socketio.emit('startup', {
        'url' : currentURL['url'],
        'seconds' : str(currentSeconds['seconds']),
        'state' : str(currentPlayState['state'])
    }, room=request.sid)

# default disconnection event for clients
@socketio.on('disconnect')
def log_disconnect():
    print("user disconnected")  # debug
    currentSIDs.pop(request.sid)

# start server
if __name__  == "__main__":
    socketio.run(app, debug=True)
