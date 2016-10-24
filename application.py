import os
import time
from flask import Flask, render_template, Response, request
from twitch_wrapper import TwitchWrapper


application = Flask(__name__)
app = application
app.secret_key = os.environ.get('APP_SECRET_KEY')

twitch_wrapper = TwitchWrapper()
# twitch_wrapper.start_chat()


@app.route('/')
def home():
    # streaming: http://flask.pocoo.org/docs/0.11/patterns/streaming/
    if request.headers.get('accept') == 'text/event-stream':
        def events():
            for i in range(0, 10):
                print('doing the thing')
                yield ('data: %d\n' % i)
                time.sleep(1)
        # https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
        return Response(events(), content_type='text/event-stream')
    return render_template('home.html', title='Lxthul Chat')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html', title='404'), 404


if __name__ == '__main__':
    app.run(debug=True)
#     app.run()
