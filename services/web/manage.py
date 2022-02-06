import random

from flask.cli import FlaskGroup
from project import app, db, SuperHeroes, Chronicles


cli = FlaskGroup(app)


@cli.command('create_db')
def create_db():
    """
    Create project db
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('seed_db')
def seed_db():
    """
    Populate db with data
    """
    if db.session.query(SuperHeroes).count() == 0:
        for _ in range(2):
            db.session.add(SuperHeroes(name='Positive Hero', power=random.randint(1, 10), is_villain=False))
            db.session.add(SuperHeroes(name='Negative Hero', power=random.randint(1, 10), is_villain=True))
        db.session.commit()

    if db.session.query(Chronicles).count() == 0:
        heroes = db.session.query(SuperHeroes).all()
        for hero in heroes:
            for _ in range(random.randint(1, 3)):
                db.session.add(
                    Chronicles(
                        hero_id=hero.id,
                        year=random.randint(2000, 2100),
                        text=f"Some text for {hero.name} number {hero.id}",
                    )
                )
        db.session.commit()


if __name__ == "__main__":
    cli()
