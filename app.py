import query_on_whoosh
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config.update(dict(JSONIFY_PRETTYPRINT_REGULAR=True))

@app.route("/")
def handle_slash():
    username = request.args.get("name")
    return render_template("index.html", name=username)

@app.route("/query/")
def handle_query():
    search_term = request.args.get("q")
    page_num = int(request.args.get("p"))
    return jsonify(query_on_whoosh.query(search_term, 10, page_num))

