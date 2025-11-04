# sync uv.lock
sync:
	uv sync
# run with default wiki_dir
run-default:
	uv run src/mattwiki-svc/local.py 
# run with wikidir supplied
run DIR:
	uv run src/mattwiki-svc/local.py {{DIR}}
