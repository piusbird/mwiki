from flask import Flask, render_template, request, redirect, url_for, Response
import os
import sys
import glob

from flask_misaka import Misaka
from beemovie import BEE_MOVIE
from gitops import mk_commit, DataModelError


def chdir_to_wiki():
    if "WIKI_DIR" in os.environ:
        print(os.environ["WIKI_DIR"])
        os.chdir(os.environ["WIKI_DIR"])
    else:
        print("not wiki dir`")


# UGLY HACK ALERT

ourfile = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.normpath(os.path.join(ourfile, "../static"))

TEMPLATES_DIR = os.path.normpath(os.path.join(ourfile, "../templates"))
md = Misaka(fenced_code=True, underline=True, math=True)
app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)
md.init_app(app)


@app.route("/")
def index():
    """List all markdown files in the current directory"""
    md_files = glob.glob("*.md")
    txt_files = glob.glob("*.txt")
    md_files.extend(txt_files)
    md_files.sort()
    if os.path.isfile("README.md"):
        with open("README.md", "r") as rme:
            readme = rme.read()
    else:
        readme = None
    return render_template("index.html", files=md_files, readme=readme)


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
    cmsg = "this is bad shouldn't be here"
    """Edit a markdown file"""
    if not (filename.endswith(".md") or filename.endswith(".txt")):
        return "Invalid file type", 400

    if request.method == "POST":
        saved = request.form["saved"]
        cmsg = request.form["cmsg"]

        with open(filename, "w", encoding="utf-8") as f:
            f.write(saved)

        try:
            _ = mk_commit(message=cmsg)
        except DataModelError as e:
            print(e)
            sys.exit(1)
        return redirect(url_for("view_file", filename=filename))
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            saved = f.read()
    else:
        saved = BEE_MOVIE

    return render_template("edit.html", filename=filename, saved=saved)


@app.route("/api/hello")
def api_stub():
    """don't know why the frontend is making this request
    but let's not segfault the container on the server shall we
    """
    user = request.args.get("name")
    return "Greetz " + user


@app.route("/raw/<filename>")
def raw_file(filename):
    """View a markdown file"""
    if not (filename.endswith(".md") or filename.endswith(".txt")):
        return "Invalid file type", 400

    if not os.path.exists(filename):
        return "file not found\n", 404

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    return Response(content, content_type="text/plain; charset=utf-8", status=201)


@app.errorhandler(404)
def not_found(e):
    # Add guard clause here to prevent nested links
    if request.path.count("/") != 1:
        return render_template("404.html")
    if request.path.endswith(".md") or request.path.endswith(".txt"):
        return redirect(url_for("view_file", filename=request.path))
    else:
        render_template("404.html")
