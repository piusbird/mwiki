
import os
import sys

from app import app, chdir_to_wiki

if __name__ == '__main__':
    # we only set the env var if the commandline indicates
    # we should otherwise we go with what the user already has set
    # failing that we go with cwd
    if len(sys.argv) > 1:
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
        print(wiki_files_dir)
    chdir_to_wiki()
    app.run(port=5042)