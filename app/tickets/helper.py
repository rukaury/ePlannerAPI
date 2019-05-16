from flask import jsonify, make_response, request, url_for
from app import app
from functools import wraps
from app.models.users import User
from app.models.tickets import Ticket


def event_required(f):
    """
    Decorator to ensure that a valid event id is sent in the url path parameters
    :param f:
    :return:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        event_id = request.view_args['event_id']
        try:
            int(event_id)
        except ValueError:
            return response('failed', 'Provide a valid Event Id', 401)
        return f(*args, **kwargs)

    return decorated_function
    
def guest_required(f):
    """
    Decorator to ensure that a valid guest id is sent in the url path parameters
    :param f:
    :return:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        guest_id = request.view_args['guest_id']
        try:
            int(guest_id)
        except ValueError:
            return response('failed', 'Provide a valid Guest Id', 401)
        return f(*args, **kwargs)

    return decorated_function


def response(status, message, status_code):
    """
    Make an http response helper
    :param status: Status message
    :param message: Response Message
    :param status_code: Http response code
    :return:
    """
    return make_response(jsonify({
        'status': status,
        'message': message
    })), status_code


def response_with_event_ticket(status, ticket, status_code):
    """
    Http response for response with an event ticket.
    :param status: Status Message
    :param ticket: event ticket
    :param status_code: Http Status Code
    :return:
    """
    return make_response(jsonify({
        'status': status,
        'ticket': ticket.json()
    })), status_code


def response_with_pagination(tickets, previous, nex, count):
    """
    Get the Event tickets with the result paginated
    :param tickets: Tickets within the Event
    :param previous: Url to previous page if it exists
    :param nex: Url to next page if it exists
    :param count: Pagination total
    :return: Http Json response
    """
    return make_response(jsonify({
        'status': 'success',
        'previous': previous,
        'next': nex,
        'count': count,
        'tickets': tickets
    })), 200


def get_user_event(current_user, event_id):
    """
    Query the user to find and return the event specified by the event Id
    :param event_id: Event Id
    :param current_user: User
    :return:
    """
    user_event = User.get_by_id(current_user.id).events.filter_by(event_id=event_id).first()
    return user_event

def get_user_guest(current_user, guest_id):
    """
    Query the user to find and return the guest specified by the guest Id
    :param guest_id: Guest Id
    :param current_user: User
    :return:
    """
    user_guest = User.get_by_id(current_user.id).guests.filter_by(guest_id=guest_id).first()
    return user_guest

def get_user_ticket(current_user, event_id, guest_id):
    """
    Query the user to find and return the ticket specified by the event Id and guest Id
    :param event_id: Event Id
    :param guest_id: Guest Id
    :param current_user: User
    :return:
    """
    user_ticket = User.get_by_id(current_user.id).guests.filter_by(guest_id=guest_id).first().tickets.filter_by(event_id=event_id).first()
    return user_ticket


def get_paginated_tickets(event, event_id, page, q):
    """
    Get the tickets from the event and then paginate the results.
    Tickets can also be search when the query parameter is set.
    Construct the previous and next urls.
    :param q: Query parameter
    :param event: Event
    :param event_id: Event Id
    :param page: Page number
    :return:
    """

    if q:
        pagination = Ticket.query.filter(Ticket.qr_code_text.like("%" + q.lower().strip() + "%")) \
            .order_by(Ticket.ticket_created_on.desc()) \
            .filter_by(event_id=event_id) \
            .paginate(page=page, per_page=app.config['EVENTS_AND_TICKETS_PER_PAGE'], error_out=False)
    else:
        pagination = event.tickets.order_by(Ticket.ticket_created_on.desc()).paginate(page=page, per_page=app.config[
            'EVENTS_AND_TICKETS_PER_PAGE'], error_out=False)

    previous = None
    if pagination.has_prev:
        if q:
            previous = url_for('tickets.get_tickets', q=q, event_id=event_id, page=page - 1, _external=True)
        else:
            previous = url_for('tickets.get_tickets', event_id=event_id, page=page - 1, _external=True)
    nex = None
    if pagination.has_next:
        if q:
            nex = url_for('tickets.get_tickets', q=q, event_id=event_id, page=page + 1, _external=True)
        else:
            nex = url_for('tickets.get_tickets', event_id=event_id, page=page + 1, _external=True)
    return pagination.items, nex, pagination, previous
