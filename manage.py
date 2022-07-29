from src import create_app
from src.extensions import db
from src.tasks.models import Task

app = create_app()


@app.cli.command("db_create")
def db_create():
    db.create_all()
    print("Database created!")


@app.cli.command("db_drop")
def db_drop():
    db.drop_all()
    print("Database dropped!")


@app.cli.command("db_seed")
def db_seed():
    solve_first_kata = Task(
        title="Solve first kata",
        notes="Given two integers a and b, which can be positive or negative, "
        + "find the sum of all the integers between and including them and return it. "
        + "If the two numbers are equal return a or b.",
    )

    take_a_walk = Task(title="Take a walk")

    db.session.add(solve_first_kata)
    db.session.add(take_a_walk)
    db.session.commit()

    print("Database seeded!")
