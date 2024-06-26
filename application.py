import os
from queue import Queue
from threading import Thread
from flask import Flask, render_template, Response, request
from twitch_wrapper import TwitchWrapper


application = Flask(__name__)
app = application
app.secret_key = os.environ.get('APP_SECRET_KEY')

msg_queue = Queue()
twitch_wrapper = TwitchWrapper(msg_queue)


@app.route('/')
def home():
    # streaming: http://flask.pocoo.org/docs/0.11/patterns/streaming/
    if request.headers.get('accept') == 'text/event-stream':
        return Response(events(), content_type='text/event-stream')
    return render_template('home.html', title='Lxthul Chat')


def events():
    while True:
        msg = msg_queue.get()
        # this format is REQUIRED. 'data: blah\n\n'
        # https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
        yield ('data: %s\n\n' % msg)


@app.route('/about/')
def about():
    return render_template('about.html', title='About')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html', title='404'), 404


if __name__ == '__main__':
    twitch_thread = Thread(target=twitch_wrapper.start_chat)
    twitch_thread.start()
    app.run()
