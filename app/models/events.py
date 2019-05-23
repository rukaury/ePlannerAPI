from app import app, db
import datetime

class Event(db.Model):
    """
    Class to represent the Event model
    """
    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_name = db.Column(db.Text, nullable=False)
    event_location = db.Column(db.Text, nullable=False)
    event_eval_link = db.Column(db.Text, nullable=True)
    event_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_created_on = db.Column(db.DateTime, nullable=False)
    event_updated_on = db.Column(db.DateTime, nullable=False)
    tickets = db.relationship('Ticket', backref='event_tickets', lazy='dynamic')

    def __init__(self, name, location, time, user_id):
        self.event_name = name
        self.user_id = user_id
        self.event_location = location
        self.event_time = time
        self.event_created_on = datetime.datetime.utcnow()
        self.event_updated_on = datetime.datetime.utcnow()

    def save(self):
        """
        Persist an event in the database
        :return:
        """
        db.session.add(self)
        db.session.commit()

    def update(self, an_event):
        """
        Update some event data
        :param an_event: Event
        :return:
        """

        self.event_name = an_event.event_name if an_event.event_name else self.event_name
        self.event_location = an_event.event_location if an_event.event_location else self.event_location
        self.event_time = an_event.event_time if an_event.event_time else self.event_time
        self.event_eval_link = an_event.event_eval_link if an_event.event_eval_link else self.event_eval_link
        self.event_updated_on = datetime.datetime.utcnow()

        db.session.commit()

    def delete(self):
        """
        Delete an event from the database
        :return:
        """
        db.session.delete(self)
        db.session.commit()

    def json(self):
        """
        Json representation of the event model.
        :return:
        """
        return {
            'event_id': self.event_id,
            'event_name': self.event_name,
            'event_location': self.event_location,
            'event_eval_link': self.event_eval_link,
            'event_time': self.event_time.isoformat(),
            'created_on': self.event_created_on.isoformat(),
            'modified_on': self.event_updated_on.isoformat()
        }