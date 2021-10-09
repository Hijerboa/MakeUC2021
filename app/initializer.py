import alembic.config
import os, os.path, time

os.chdir(os.path.join(os.path.dirname(__file__), "db"))

time.sleep(2)

alembic.config.main(
    argv=[
        "--raiseerr",
        "upgrade",
        "head"
    ]
)
