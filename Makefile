mm:
	alembic revision --autogenerate -m "$(c)"

up:
	alembic upgrade head

run:
	python3 run.py
	
test-info:
	pytest --cov=backend tests/