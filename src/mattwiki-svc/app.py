from flask import Flask, render_template, request, redirect, url_for
import os
import glob

from flask_misaka import Misaka
from beemovie import BEE_MOVIE

# UGLY HACK ALERT

ourfile = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.normpath(os.path.join(ourfile, "../static") )

TEMPLATES_DIR = os.path.normpath(os.path.join(ourfile, "../templates") )
app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)
Misaka(app)
if "WIKI_DIR" in os.environ:
    os.chdir(os.environ["WIKI_DIR"])

@app.route("/")
def index():
    """List all markdown files in the current directory"""
    md_files = glob.glob("*.md")
    txt_files = glob.glob("*.txt")
    md_files.extend(txt_files)
    md_files.sort()
    return render_template("index.html", files=md_files)


@app.route("/view/<filename>")
def view_file(filename):
    """View a markdown file"""
    if not (filename.endswith(".md") or filename.endswith(".txt")):
        return "Invalid file type", 400

    if not os.path.exists(filename):
        return render_template("fourorcreate.html", filename=filename), 404

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    return render_template("view.html", filename=filename, mkd=content)


@app.route("/edit/<filename>", methods=["GET", "POST"])
def edit_file(filename):
    """Edit a markdown file"""
    if not (filename.endswith(".md") or filename.endswith(".txt")):
        return "Invalid file type", 400

    if request.method == "POST":
        saved = request.form["saved"]
        with open(filename, "w", encoding="utf-8") as f:
            f.write(saved)
        return redirect(url_for("view_file", filename=filename))
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            saved = f.read()
    else:
        saved = BEE_MOVIE

    return render_template("edit.html", filename=filename, saved=saved)


#if __name__ == "__main__":
#    app.run(debug=True, port=5042)

