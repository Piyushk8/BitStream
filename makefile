dev:
	uv run uvicorn app.main:app --reload

prod:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

worker:
	uv run python worker.py


docker run -p 6379:6379 redis    

uv run dramatiq app.queue.task  