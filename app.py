"""Cricbuzz LiveStats: Flask application entry point."""
import os
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from dotenv import load_dotenv

from utils.api_client import (
    fetch_women_odi_batter_rankings, fetch_live_matches, fetch_upcoming_matches, fetch_recent_matches
)
from utils.db_connection import get_db, init_db, register_app
from utils.queries import SQL_QUESTIONS

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-development-secret")
app.config["DATABASE"] = os.getenv("DATABASE_PATH", "cricbuzz.db")
register_app(app)


@app.context_processor
def inject_site_name():
    return {"site_name": "Cricbuzz LiveStats"}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/rankings")
def rankings():
    result = fetch_women_odi_batter_rankings()
    return render_template("rankings.html", result=result)


@app.route("/live-matches")
def live_matches():
    result = fetch_live_matches()
    return render_template("live_matches.html", result=result)


@app.route("/upcoming-matches")
def upcoming_matches():
    result = fetch_upcoming_matches()
    return render_template("upcoming_matches.html", result=result)


@app.route("/recent-matches")
def recent_matches():
    result = fetch_recent_matches()
    return render_template("upcoming_matches.html", result=result)


@app.route("/player-analytics")
def player_analytics():
    db = get_db()
    players = db.execute(
        "SELECT id, name, country, role, runs, wickets, matches FROM players ORDER BY runs DESC"
    ).fetchall()
    return render_template("player_analytics.html", players=players)


@app.route("/sql-analytics", methods=["GET", "POST"])
def sql_analytics():
    rows, columns, selected = [], [], 1
    error = None
    if request.method == "POST":
        try:
            selected = int(request.form.get("question_id", "1"))
            if selected not in SQL_QUESTIONS:
                raise ValueError("Select a valid SQL practice question.")
            query = SQL_QUESTIONS[selected]
            db = get_db()
            cursor = db.execute(query["sql"])
            rows = cursor.fetchall()
            columns = [item[0] for item in cursor.description] if cursor.description else []
        except (ValueError, KeyError, sqlite3.Error) as exc:
            error = f"Could not run this query: {exc}"
            if selected not in SQL_QUESTIONS:
                selected = 1
    return render_template(
        "sql_analytics.html", questions=SQL_QUESTIONS, rows=rows,
        columns=columns, selected=selected, error=error
    )


@app.route("/crud", methods=["GET", "POST"])
def crud():
    db = get_db()
    if request.method == "POST":
        action = request.form.get("action")
        try:
            if action == "create":
                db.execute(
                    """INSERT INTO players(name,country,role,runs,wickets,matches)
                       VALUES(?,?,?,?,?,?)""",
                    (request.form["name"].strip(), request.form["country"].strip(),
                     request.form["role"].strip(), int(request.form["runs"]),
                     int(request.form["wickets"]), int(request.form["matches"]))
                )
                db.commit()
                flash("Player record created.", "success")
            elif action == "update":
                db.execute(
                    """UPDATE players SET name=?,country=?,role=?,runs=?,wickets=?,matches=?
                       WHERE id=?""",
                    (request.form["name"].strip(), request.form["country"].strip(),
                     request.form["role"].strip(), int(request.form["runs"]),
                     int(request.form["wickets"]), int(request.form["matches"]),
                     int(request.form["id"]))
                )
                db.commit()
                flash("Player record updated.", "success")
            elif action == "delete":
                db.execute("DELETE FROM players WHERE id=?", (int(request.form["id"]),))
                db.commit()
                flash("Player record deleted.", "success")
        except (ValueError, sqlite3.Error, KeyError) as exc:
            db.rollback()
            flash(f"Operation failed: {exc}", "error")
        return redirect(url_for("crud"))

    players = db.execute("SELECT * FROM players ORDER BY id DESC").fetchall()
    return render_template("crud.html", players=players)


@app.route("/api/rankings")
def api_rankings():
    """JSON endpoint for the rankings data."""
    return jsonify(fetch_women_odi_batter_rankings())


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
