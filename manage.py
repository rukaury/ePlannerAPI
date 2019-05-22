from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db, models
from app.models.users import User
from app.models.events import Event
from app.models.guests import Guest
from app.models.tickets import Ticket
import unittest
import coverage
import os
import forgery_py as faker
from random import randint
from sqlalchemy.exc import IntegrityError

# Initializing the manager
manager = Manager(app)

# Initialize Flask Migrate
migrate = Migrate(app, db)

# Add the flask migrate
manager.add_command('db', MigrateCommand)

# Test coverage configuration
COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=[]
)
COV.start()


# Add test command
@manager.command
def test():
    """
    Run tests without coverage
    :return:
    """
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def dummy():
    # Create a user if they do not exist.
    user = User.query.filter_by(email="example@test.com").first()
    if not user:
        user = User("example@test.com", "123456")
        user.save()

    for i in range(100):
        # Add events to the database
        event = Event(faker.lorem_ipsum.title(words_quantity=10), faker.name.location(), faker.date.date(), user.id)
        event.save()

    for j in range(500):
        # Add guests to the database
        guest = Guest(faker.name.first_name(), faker.name.last_name(), faker.name.company_name(), 'email' + str(j) + '@test.ca', user.id)
        guest.save()

    for ev in range(1000):
        # Add tickets to the event
        event = Event.query.filter_by(event_id=randint(1, Event.query.count() - 1)).first()
        guest = Guest.query.filter_by(guest_id=randint(1, Guest.query.count() - 1)).first()
        ticket = Ticket(event.event_id, guest.guest_id, faker.lorem_ipsum.words(quantity=15, as_list=False), faker.basic.number(at_least=0, at_most=1), faker.basic.number(at_least=0, at_most=1), faker.basic.number(at_least=0, at_most=1000))
        db.session.add(ticket)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


# Run the manager
if __name__ == '__main__':
    manager.run()
