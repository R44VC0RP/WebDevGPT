from flask import Flask, render_template
from flask_socketio import SocketIO
import webgen

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webpreview/<filename>')
def webpreview(filename):
    # This will return the image file for the given filename.
    # The filename should be the name of a file in the webpreview folder.
    # For example, if the file is '/Users/ryanvogel/Desktop/WebDevGPT/flask/webpreview/websiteSaved.png', the filename should be 'websiteSaved.png'.
    return app.send_static_file(filename)



def updateWebClient(assistant, message):
    socketio.emit('update_status', {'assistant': assistant, 'message': message})

@socketio.on('connect')
def on_connect():
    # This could be triggered by the client sending its initial prompt.
    # For now, it just prints to the server console.
    print('Client connected')

@socketio.on('send_prompt')
def handle_prompt(data):
    print('Received prompt: ' + data['prompt'])
    webgen.main(data['prompt'])
    # updateWebClient('DevAI', 'Starting processing...')

if __name__ == '__main__':
    socketio.run(app, debug=True)
