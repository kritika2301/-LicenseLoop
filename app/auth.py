
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)
from werkzeug.security import check_password_hash
from app.db import get_db_connection


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if session.get("user_id"):
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT user_id, full_name, email, password_hash
                FROM users
                WHERE LOWER(email) = %s;
            """, (email,))

            user = cursor.fetchone()

        finally:
            cursor.close()
            connection.close()

        if user and check_password_hash(user[3], password):

            session.clear()
            session["user_id"] = user[0]
            session["full_name"] = user[1]
            session.permanent = True

            return redirect(url_for("main.dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@auth.route("/logout", methods=["POST"])
def logout():

    session.clear()

    flash("You have been logged out successfully.", "success")

    return redirect(url_for("auth.login"))
