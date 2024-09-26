# Imports
from flask import Flask, render_template, redirect, request, flash
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


# My App
app = Flask(__name__)


@app.route("/")
def index():
    return " TESTING  12345 "


if __name__ == "__main__":
    app.run(debug=True)
