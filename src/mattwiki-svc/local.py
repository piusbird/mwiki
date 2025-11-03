
import os
import sys

from app import app

if __name__ == '__main__':
    if 1 < len(sys.argv):
        wiki_files_dir = sys.argv[1] 
        if not os.path.isabs(wiki_files_dir):
            if wiki_files_dir.startswith("~"):
                wiki_files_dir = os.path.normpath(os.path.expanduser(wiki_files_dir))
            else:
                wiki_files_dir = os.path.abspath(wiki_files_dir)
        if os.path.isdir(wiki_files_dir):
            os.environ["WIKI_DIR"] = wiki_files_dir
        else:
            os.environ["WIKI_DIR"] = os.getcwd()
    app.run(port=5042)