"""Podcast Storybook."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension

from model import Podcast, Event, connect_to_db, db
import json

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Prevent jinja from failing silently
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    podcasts = Podcast.query.all()

    return render_template("index.html", podcasts=podcasts)


@app.route('/<int:podcast_id>')
def podcast(podcast_id):
    """Show podcast user has selected"""

    events = Event.query.filter(Event.podcast_id==podcast_id)
    podcast = Podcast.query.get(podcast_id)

    carousel_images = db.session.query(Event.url).filter(Event.podcast_id==podcast_id).all()
    print carousel_images
    return render_template("podcast.html", events=events, podcast=podcast,
                            carousel_images=map(json.dumps, carousel_images))

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()