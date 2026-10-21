from logging.config import fileConfig

from alembic import context

from database import engine
from models import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Give Alembic the table definitions from models.py.
target_metadata = Base.metadata


def run_migrations_offline():
    # Generate SQL without connecting to the database.
    context.configure(
        url=engine.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    # Use our existing database connection settings.
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()