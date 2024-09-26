# Imports
from flask import Flask, render_template, redirect, request, flash
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


# My App
app = Flask(__name__)
app.secret_key = "your_secret_key"
Scss(app)


# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)


# Task model
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"Task {self.id}: {self.content}"


with app.app_context():
    db.create_all()


@app.route("/", methods=["POST", "GET"])
def index():
    # Add task
    if request.method == "POST":
        current_task = request.form['content']
        if not current_task.strip():
            flash("Task content cannot be empty!", "error")
            return redirect("/")

        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully!", "success")
            return redirect("/")
        except Exception as e:
            flash(f"An error occurred while adding the task: {e}", "error")
            return redirect("/")

    # Retrieve all tasks
    tasks = MyTask.query.order_by(MyTask.created).all()
    return render_template('index.html', tasks=tasks)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
