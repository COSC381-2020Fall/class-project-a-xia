import math
import smtplib
import sqlite3
from datetime import datetime, timezone, timedelta
from flask import Flask, render_template, request, session, jsonify

import query_on_whoosh
import config

app = Flask(__name__)
app.secret_key = b'KJ)as!9Eca?n/2ad*-S'

@app.route("/", methods=['GET', 'POST'], strict_slashes=False)
def handle_slash():
    try:
        request.form['change']
        del session['name']
    except:
        pass
    
    if 'name' not in session:
        try:
            username = request.form['name']
            session['name'] = username
        except:
            username = False
    else:
        username = session['name']
    
    return render_template("index.html", name=username)

@app.route("/about", strict_slashes=False)
def handle_about():
    return render_template("about.html")

@app.route("/query_view", strict_slashes=False)
def handle_query_view():
    if 'history_enabled' not in session:
        session['history_enabled'] = True

    query_term = request.args.get("q")
    if not query_term:
        query_term = ''
    
    topic = request.args.get("topic")
    if not topic:
        topic = ''

    p = request.args.get("p")
    if p:
        page_num = int(p)
    else:
        page_num = 1
    
    # only adds to history db if not empty and if search history is enabled
    if query_term and topic and not p and session['history_enabled']:
        conn = sqlite3.connect('search_history.db')
        c = conn.cursor()
        c.execute("INSERT INTO search_terms (term, search_time, search_topic) VALUES (?, strftime('%s', 'now'), ?);", (query_term, topic))
        conn.commit()
        conn.close()
    
    query_results = query_on_whoosh.query(query_term, topic, 10, page_num)
    search_results = query_results[0]
    results_num = int(query_results[1])
    page_count = math.ceil(results_num/10)
    return render_template("query.html",
                           results=search_results,
                           query_term=query_term,
                           topic=topic,
                           page_count=page_count,
                           topic_list=config.topic_list)

@app.route("/history", methods=['GET', 'POST'], strict_slashes=False)
def handle_history():
    if 'timezone' not in session:
        session['timezone'] = -5
    
    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()

    deleted = False
    if request.method == 'POST':
        search_id = request.form['id']
        c.execute("DELETE FROM search_terms WHERE id = ?;", (search_id,))
        conn.commit()
        deleted = True

    c.execute("SELECT * FROM search_terms ORDER BY id DESC;")
    rows = c.fetchall()
    conn.close()

    for i in range(len(rows)):
        rows[i] = list(rows[i])
        timestamp = datetime.fromtimestamp(rows[i][2], timezone(timedelta(hours=int(session['timezone']))))
        rows[i][2] = str(timestamp.month) + '/' + str(timestamp.day) + timestamp.strftime('/%Y %I:%M %p')
        rows[i] = tuple(rows[i])
    
    return render_template("history.html", history=rows, deleted=deleted)

@app.route("/settings", methods=['GET', 'POST'], strict_slashes=False)
def handle_settings():
    if 'history_enabled' not in session:
        session['history_enabled'] = True
    if 'timezone' not in session:
        session['timezone'] = -5
    
    submitted = False
    if request.method == 'POST':
        try:
            search_hist = request.form['search_history']
            session['history_enabled'] = True
        except:
            session['history_enabled'] = False
        
        session['timezone'] = request.form['timezone']

        submitted = True

    return render_template("settings.html",
                           history_enabled=session['history_enabled'],
                           timezone=session['timezone'],
                           submitted=submitted)

@app.route("/feedback", strict_slashes=False)
def handle_feedback():
    return render_template("feedback.html")

@app.route("/submitted", methods=['POST'], strict_slashes=False)
def handle_request():
    subject = request.form['subject']
    body = request.form['body']
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

