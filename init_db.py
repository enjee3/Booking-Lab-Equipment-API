from pathlib import Path

from alembic import command
from alembic.config import Config


if __name__ == "__main__":
    config_path = Path(__file__).resolve().with_name("alembic.ini")
    config = Config(str(config_path))

    command.upgrade(config, "head")

    print("Database migrations are up to date.")