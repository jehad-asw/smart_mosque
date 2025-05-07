import os
import subprocess

def run_alembic():
    print("Running Alembic revision and upgrade...")

    # Apply migrations
    #subprocess.run([
    #    "alembic", "upgrade", "head"
    #], check=True)

    # Generate revision
    subprocess.run([
        "alembic", "revision", "--autogenerate", "-m", "Auto migration"
    ], check=True)

    # Apply migrations
    subprocess.run([
        "alembic", "upgrade", "head"
    ], check=True)

if __name__ == "__main__":
    run_alembic()