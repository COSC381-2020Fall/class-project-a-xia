import math
import smtplib
import sqlite3
from flask import Flask, render_template, request, jsonify

import query_on_whoosh
import config

app = Flask(__name__)
app.config.update(dict(JSONIFY_PRETTYPRINT_REGULAR=True))

@app.route("/", strict_slashes=False)
def handle_slash():
    username = request.args.get("name")
    return render_template("index.html", name=username)

@app.route("/about", strict_slashes=False)
def handle_about():
    return render_template("about.html")

@app.route("/query_view", strict_slashes=False)
def handle_query_view():
    query_term = request.args.get("q")
    if not query_term:
        query_term = ""
    
    p = request.args.get("p")
    if p:
        page_num = int(p)
    else:
        page_num = 1
    
    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO search_terms (term, search_time) VALUES (?, strftime('%s', 'now'));", (query_term,))
    c.execute("SELECT * FROM search_terms;")
    rows = c.fetchall()
    conn.commit()
    conn.close()
    
    query_results = query_on_whoosh.query(query_term, 10, page_num)
    search_results = query_results[0]
    results_num = int(query_results[1])
    page_count = math.ceil(results_num/10)
    return render_template("query.html",
                           results=search_results,
                           query_term=query_term,
                           page_count=page_count,
                           history=rows)

@app.route("/feedback", strict_slashes=False)
def handle_feedback():
    return render_template("feedback.html")

@app.route("/submit", methods=['POST'], strict_slashes=False)
def handle_request():
    subject = request.form["subject"]
    body = request.form["body"]
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("axia@emich.edu", config.gmail_pw)
    
    # check if an email was submitted
    if request.form["email"] != "":
        message = 'Subject: {}\n\n{}'.format("Your feedback", "Subject: " + subject + "\n\nMessage: " + body)
        server.sendmail("axia@emich.edu", request.form["email"], message)
    
    message = 'Subject: {}\n\n{}'.format("Feedback: " + subject, body)
    server.sendmail("axia@emich.edu", "axia@emich.edu", message)
    return render_template("submitted.html")

