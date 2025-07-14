from flask import render_template, request, redirect, url_for, Blueprint
from .models import Urls, db
import string
import random

bp = Blueprint("main", __name__)


def shorten_url():
    letters = string.ascii_letters  # characters to use
    while True:
        rand_letters = random.choices(letters, k=3)  # generate 3 random characters
        rand_letters = "".join(rand_letters)
        existing_url = Urls.query.filter_by(short=rand_letters).first()
        if not existing_url:  # if the random string is not in the database
            return rand_letters


@bp.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        url_received = request.form["orig_url"]
        # check if the URL is already in the database
        existing_url = Urls.query.filter_by(
            long=url_received
        ).first()  # filter in long column
        if existing_url:
            return redirect(url_for("main.display", url=existing_url.short))

        else:
            short_url = shorten_url()
            new_url = Urls(long=url_received, short=short_url)  # new url instance
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("main.display", url=short_url))

    else:  # GET method
        return render_template("home.html")


@bp.route("/display/<url>")  # <url> is a variable
def display(url):
    """
    Display the short URL.
    """
    full_url = url_for(
        "main.redirect_to_long", short_url=url, _external=True
    )  # absolute path of the short URL
    return render_template("shorturl.html", short_url_display=full_url)


@bp.route("/<short_url>")
def redirect_to_long(short_url):
    """
    Redirect to the long URL based on the short URL.
    """
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return "URL not found", 404
