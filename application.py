import os
from flask import Flask, render_template
from twitch_wrapper import TwitchWrapper


application = Flask(__name__)
app = application
app.secret_key = os.environ.get('APP_SECRET_KEY')

twitch_wrapper = TwitchWrapper()
twitch_wrapper.start_chat()


@app.route('/')
def home():
    return render_template('home.html', title='Lxthul Chat')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html', title='404'), 404


if __name__ == '__main__':
    app.run(debug=True)
#     app.run()
