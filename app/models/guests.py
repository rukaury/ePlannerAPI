from app import app, db
import datetime

class Guest(db.Model):
    """
    Class to represent the Guest model
    """
    __tablename__ = 'guests'

    guest_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    organization = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    guest_created_on = db.Column(db.DateTime, nullable=False)
    guest_created_on = db.Column(db.DateTime, nullable=False)
    guest_updated_on = db.Column(db.DateTime, nullable=False)
    tickets = db.relationship('Ticket', backref='guest_tickets', lazy='dynamic')

    def __init__(self, f_name, l_name, organization, email, user_id):
        self.first_name = f_name
        self.last_name = l_name
        self.organization = organization
        self.email = email
        self.user_id = user_id
        self.guest_created_on = datetime.datetime.utcnow()
        self.guest_updated_on = datetime.datetime.utcnow()

    def save(self):
        """
        Persist a guest in the database
        :return:
        """
        db.session.add(self)
        db.session.commit()

    def update(self, guest):
        """
        Update some guest data
        :param guest: Guest
        :return:
        """

        self.first_name = guest.first_name if guest.first_name else self.first_name
        self.last_name = guest.last_name if guest.last_name else self.last_name
        self.organization = guest.organization if guest.organization else self.organization
        self.email = guest.email if guest.email else self.email
        self.guest_updated_on = datetime.datetime.utcnow()

        db.session.commit()

    def delete(self):
        """
        Delete a guest from the database
        :return:
        """
        db.session.delete(self)
        db.session.commit()

    def json(self):
        """
        Json representation of the guest model.
        :return:
        """
        return {
            'guest_id': self.guest_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'organization': self.organization,
            'email': self.email,
            'created_on': self.guest_created_on.isoformat(),
            'modified_on': self.guest_updated_on.isoformat()
        }