import pygit2
import os


class DataModelError(Exception):
    pass


def mk_commit(message="Oh sinner why don't you answer"):
    repo_path = None
    if "WIKI_DIR" in os.environ:
        repo_path = os.environ["WIKI_DIR"]
    else:
        raise DataModelError("No repo found")
    if "WIKI_NAME" in os.environ:
        username = os.environ["WIKI_NAME"]
    else:
        username = "Sakura"
    if "WIKI_EMAIL" in os.environ:
        user_email = os.environ["WIKI_EMAIL"]
    else:
        user_email = "sakura@clowcards.localhost"

    repo = pygit2.Repository(repo_path)

    # Step 2: Stage changes
    # You can stage specific files or all files
    index = repo.index
    index.add_all()  # Stage all changes
    index.write()  # Write changes to the index

    # Step 3: Prepare a commit
    author = pygit2.Signature(username, user_email)
    committer = pygit2.Signature("Wiki Kero", "system@mwiki.localhost")
    tree = index.write_tree()  # Create a tree object from the index

    # Step 4: Create a commit
    if repo.head_is_unborn:
        # This means there's no initial commit yet
        commit_id = repo.create_commit(
            "refs/heads/main",  # Reference to update (branch to commit to)
            author,  # Author list
            committer,  # Committer list
            message,  # Commit message
            tree,  # New tree object
            [],  # Parents list (empty for the initial commit)
        )
    else:
        parent_commit = repo.head.peel()  # Get the current tip of the branch
        commit_id = repo.create_commit(
            "refs/heads/main",
            author,
            committer,
            message,
            tree,
            [parent_commit.id],  # Parent commit
        )
    return commit_id
