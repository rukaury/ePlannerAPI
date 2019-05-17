from flask import Blueprint, request, abort
from app.auth.helper import token_required
from app.tickets.helper import event_required, guest_required, response, get_user_event, get_user_ticket, get_user_guest, response_with_event_ticket, \
    response_with_pagination, get_paginated_tickets
from sqlalchemy import exc
from app.models.tickets import Ticket

tickets = Blueprint('tickets', __name__)


@tickets.route('/events/<event_id>/tickets', methods=['GET'])
@token_required
@event_required
def get_tickets(current_user, event_id):
    """
    A user's ticket belonging to an Event specified by the event_id are returned if the Event Id
    is valid and belongs to the user.
    An empty ticket list is returned if the event has no tickets.
    :param current_user: User
    :param event_id: Event Id
    :return: List of Tickets
    """
    # Get the user event
    event = get_user_event(current_user, event_id)
    if event is None:
        return response('failed', 'event not found', 404)

    # Get tickets in the event
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', None, type=str)
    tickets, nex, pagination, previous = get_paginated_tickets(event, event_id, page, q)

    # Make a list of tickets
    if tickets:
        result = []
        for ticket in tickets:
            result.append(ticket.json())
        return response_with_pagination(result, previous, nex, pagination.total)
    return response_with_pagination([], previous, nex, 0)


@tickets.route('/events/<event_id>/tickets/<ticket_id>/', methods=['GET'])
@token_required
@event_required
def get_ticket(current_user, event_id, ticket_id):
    """
    A ticket can be returned from the Event if the ticket and Event exist and below to the user.
    The event and ticket Ids must be valid.
    :param current_user: User
    :param event_id: event Id
    :param ticket_id: ticket Id
    :return:
    """
    # Check ticket id is an integer
    try:
        int(ticket_id)
    except ValueError:
        return response('failed', 'Provide a valid ticket Id', 202)

    # Get the user event
    event = get_user_event(current_user, event_id)
    if event is None:
        return response('failed', 'User has no event with Id ' + event_id, 404)

    # Get the ticket from the event
    ticket = event.tickets.filter_by(ticket_id=ticket_id).first()
    if not ticket:
        abort(404)
    return response_with_event_ticket('success', ticket, 200)

@tickets.route('/events/<event_id>/guests/<guest_id>/tickets', methods=['POST'])
@token_required
@guest_required
@event_required
def post(current_user, event_id, guest_id):
    """
    Storing a ticket into an event
    :param current_user: User
    :param event_id: event Id
    :return: Http Response
    """
    if not request.content_type == 'application/json':
        return response('failed', 'Content-type must be application/json', 401)

    data = request.get_json().get("ticket")
    ticket_qr_code = data.get('qr_code')
    ticket_vvip = int(data.get('vvip'))
    ticket_accepted = int(data.get('accepted'))
    ticket_scanned = int(data.get('scanned'))
    ticket_comments = data.get('comments') if data.get('comments') is not None else ""
    if not event_id and not guest_id and not ticket_qr_code and not ticket_vvip and not ticket_scanned and not ticket_accepted:
        return response('failed', 'No ticket value attribute found', 401)

    # Get the user event
    event = get_user_event(current_user, event_id)
    if event is None:
        return response('failed', 'User has no event with Id ' + event_id, 202)

    # Get the user guest
    guest = get_user_guest(current_user, guest_id)
    if guest is None:
        return response('failed', 'User has no guest with Id ' + guest_id, 202)

    # Check if ticket exists already
    ticket = get_user_ticket(current_user, event_id, guest_id)
    if ticket is not None:
        return response('failed', 'Ticket exists already for guest id ' + guest_id + ' participating at event id ' + event_id, 202)

    # Save the event ticket into the Database
    ticket = Ticket(event_id, guest_id, ticket_qr_code, ticket_vvip, ticket_accepted, ticket_scanned)
    ticket.comments = ticket_comments
    ticket.save()
    return response_with_event_ticket('success', ticket, 200)


@tickets.route('/events/<event_id>/tickets/<ticket_id>/', methods=['PUT'])
@token_required
@event_required
def edit_ticket(current_user, event_id, ticket_id):
    """
    Edit a ticket with a valid Id. The request content-type must be json and also the event
    in which the ticket belongs must be among the user`s events.
    The new data of the ticket must be present in the payload.
    :param current_user: User
    :param event_id: event Id
    :param ticket_id: ticket Id
    :return: Response of Edit ticket
    """
    if not request.content_type == 'application/json':
        return response('failed', 'Content-type must be application/json', 401)

    try:
        int(ticket_id)
    except ValueError:
        return response('failed', 'Provide a valid ticket Id', 202)

    # Get the user event
    event = get_user_event(current_user, event_id)
    if event is None:
        return response('failed', 'User has no event with Id ' + event_id, 202)

    # Get the ticket
    ticket = event.tickets.filter_by(ticket_id=ticket_id).first()
    if not ticket:
        abort(404)

    # Check for Json data
    request_json_data = request.get_json().get("ticket")
    scanned = request_json_data.get('scanned') if request_json_data.get('scanned') is not None else ""
    accepted = request_json_data.get('accepted') if request_json_data.get('accepted') is not None else ""
    vvip = request_json_data.get('vvip') if request_json_data.get('vvip') is not None else ""
    comments = request_json_data.get('comments') if request_json_data.get('comments') is not None else ""
    
    if not request_json_data:
        return response('failed', 'No attributes specified in the request', 401)

    if not scanned and not accepted and not vvip:
        return response('failed', 'No ticket data or value attribute found', 401)

    # Update the ticket record
    ticket.update(scanned, accepted, vvip, comments)
    return response_with_event_ticket('success', ticket, 200)


@tickets.route('/events/<event_id>/tickets/<ticket_id>/', methods=['DELETE'])
@token_required
@event_required
def delete(current_user, event_id, ticket_id):
    """
    Delete a ticket from the user's event.
    :param current_user: User
    :param event_id: event Id
    :param ticket_id: ticket Id
    :return: Http Response
    """
    # Check ticket id is an integer
    try:
        int(ticket_id)
    except ValueError:
        return response('failed', 'Provide a valid ticket Id', 202)

    # Get the user event
    event = get_user_event(current_user, event_id)
    if event is None:
        return response('failed', 'User has no event with Id ' + event_id, 202)

    # Delete the ticket from the event
    ticket = event.tickets.filter_by(ticket_id=ticket_id).first()
    if not ticket:
        abort(404)
    ticket.delete()
    return response('success', 'Successfully deleted the ticket from event with Id ' + event_id, 200)


@tickets.errorhandler(404)
def ticket_not_found(e):
    """
    Custom response to 404 errors.
    :param e:
    :return:
    """
    return response('failed', 'ticket not found', 404)


@tickets.errorhandler(400)
def bad_method(e):
    """
    Custom response to 400 errors.
    :param e:
    :return:
    """
    return response('failed', 'Bad request', 400)
