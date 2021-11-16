


upgrade:
	@echo "Running alembic upgrade to latest revision (head) ..."
	@alembic upgrade head

truncate:
	@echo "Initiating full db truncate (drop / create)"
	@alembic downgrade base
	# @alembic upgrade -1
	@alembic upgrade head

revision:
	alembic revision --autogenerate -m "$(NAME)"