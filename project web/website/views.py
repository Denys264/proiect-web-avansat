from flask import Blueprint, flash, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from .models import Post, User
from . import db
import time

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    message = None

    if request.method == "GET":
        mesaje = Post.query.order_by(Post.date_created.desc()).all()

    if request.method == "POST":
        message = request.form.get('message')
        if not message:
            flash('Message is empty', category='error')
        else:
            new_message = Post(text=message, author=current_user.id)
            db.session.add(new_message)
            db.session.commit()
            flash('Message sent')

            return redirect(url_for('views.home'))

    return render_template("home.html", user=current_user, mesaje=mesaje)

@views.route("/poll", methods=["GET"])
def poll():
    timeout = 30  # Timeout pentru long polling
    start_time = time.time()

    last_message_time = float(request.args.get("last_message_time", 0))

    while time.time() - start_time < timeout:
        latest_message = Post.query.order_by(Post.date_created.desc()).first()
        if latest_message and latest_message.date_created.timestamp() > last_message_time:
            return jsonify({
                "message": latest_message.text,
                "author": latest_message.user.username,
                "timestamp": latest_message.date_created.timestamp()
            }), 200

        time.sleep(1)  # Așteaptă un moment înainte de a verifica din nou

    return jsonify({"message": None}), 204

@views.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == "GET":
        user = User.query.all()
    return render_template("admin.html", users=user)

@views.route("/delete_user", methods=['GET', 'POST'])
def delete_user():
    username = request.form.get("username")
    user_exists = User.query.filter_by(username=username).first()
    if user_exists:
        db.session.delete(user_exists)
        db.session.commit()
        return redirect(url_for("views.admin"))
    else:
        return "User not found"

@views.route("/change_user", methods=['GET', 'POST'])
def change_user():
    username = request.form.get("usernamechange")
    new_username = request.form.get("newusername")
    user_exists = User.query.filter_by(username=username).first()
    if user_exists:
        user_exists.username = new_username
        db.session.commit()
        return redirect(url_for("views.admin"))
    else:
        return "User not found"
