.PHONY: run test pipeline clean install

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

pipeline:
	python -m scripts.daily_pipeline

seed:
	python -m scripts.seed_historical

test:
	pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
	find . -type f -name "*.pyc" -delete

docker-build:
	docker build -t nifty-brief-api .

docker-run:
	docker run -p 8080:8000 -e SUPABASE_URL= -e SUPABASE_SERVICE_KEY= -e SUPABASE_ANON_KEY= -e HF_API_TOKEN= nifty-brief-api
