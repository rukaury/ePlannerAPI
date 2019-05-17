from app import app, db
import datetime

class Ticket(db.Model):
    """
    Ticket model class
    """

    __tablename__ = 'tickets'

    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.guest_id'))
    qr_code_text = db.Column(db.Text, nullable=False)
    vvip = db.Column(db.Boolean, nullable=False)
    accepted = db.Column(db.Boolean, nullable=False)
    scanned = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Integer, nullable=True)
    ticket_created_on = db.Column(db.DateTime, nullable=False)
    ticket_updated_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, event_id, guest_id, qr_code_text, vvip, accepted, scanned):
        self.event_id = event_id
        self.guest_id = guest_id
        self.qr_code_text = qr_code_text
        self.vvip = vvip
        self.accepted = accepted
        self.scanned = scanned
        self.ticket_created_on = datetime.datetime.utcnow()
        self.ticket_updated_on = datetime.datetime.utcnow()

    def save(self):
        """
        Persist Ticket into the database
        :return:
        """
        db.session.add(self)
        db.session.commit()

    def update(self, scanned, accepted, vvip, comments):
        """
        Update data in the ticket
        :param name: Name
        :param description: Description
        :return:
        """

        self.scanned = scanned if scanned else self.scanned
        self.accepted = accepted if accepted else self.accepted
        self.vvip = vvip if vvip else self.vvip
        self.comments = comments if comments else self.comments
        
        db.session.commit()

    def delete(self):
        """
        Delete a ticket
        :return:
        """
        db.session.delete(self)
        db.session.commit()

    def json(self):
        """
        Json representation of the ticket model
        :return:
        """
        return {
            'ticket_id': self.ticket_id,
            'event_id': self.event_id,
            'guest_id': self.guest_id,
            'qr_code': self.qr_code_text,
            'vvip': self.vvip,
            'accepted': self.accepted,
            'scanned': self.scanned,
            'comments' : self.comments,
            'created_on': self.ticket_created_on.isoformat(),
            'modified_on': self.ticket_updated_on.isoformat()
        }