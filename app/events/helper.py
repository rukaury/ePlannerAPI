from flask import make_response, jsonify, url_for
from app import app
from app.models.events import Event


def response_for_user_event(user_event):
    """
    Return the response for when a single event was requested by the user.
    :param event:
    :return:
    """
    return make_response(jsonify({
        'status': 'success',
        'event': user_event
    }))


def response_for_created_event(event, status_code):
    """
    Method returning the response when an event has been successfully created.
    :param status_code:
    :param event: Event
    :return: Http Response
    """
    return make_response(jsonify({'event' : {
        'status': 'success',
        'event_id': event.event_id,
        'event_name': event.event_name,
        'event_location': event.event_location,
        'event_eval_link': event.event_eval_link,
        'event_time': event.event_time,
        'created_on': event.event_created_on,
        'modified_on': event.event_updated_on
    }})), status_code


def response(status, message, code):
    """
    Helper method to make a http response
    :param status: Status message
    :param message: Response message
    :param code: Response status code
    :return: Http Response
    """
    return make_response(jsonify({
        'status': status,
        'message': message
    })), code


def get_user_events_json_list(user_events):
    """
    Make json objects of the user events and add them to a list.
    :param user_events: Event
    :return:
    """
    events = []
    for user_event in user_events:
        events.append(user_event.json())
    return events


def response_with_pagination(events, previous, nex, count):
    """
    Make a http response for EventList get requests.
    :param count: Pagination Total
    :param nex: Next page Url if it exists
    :param previous: Previous page Url if it exists
    :param events: Event
    :return: Http Json response
    """
    return make_response(jsonify({
        'status': 'success',
        'previous': previous,
        'next': nex,
        'count': count,
        'events': events
    })), 200


def paginate_events(user_id, page, q, user):
    """
    Get a user by Id, then get hold of their events and also paginate the results.
    There is also an option to search for an event name if the query param is set.
    Generate previous and next pagination urls
    :param q: Query parameter
    :param user_id: User Id
    :param user: Current User
    :param page: Page number
    :return: Pagination next url, previous url and the user events.
    """
    if q:
        pagination = Event.query.filter(Event.event_name.like("%" + q.lower().strip() + "%")).filter_by(user_id=user_id) \
            .paginate(page=page, per_page=app.config['EVENTS_AND_TICKETS_PER_PAGE'], error_out=False)
    else:
        pagination = user.events.paginate(page=page, per_page=app.config['EVENTS_AND_TICKETS_PER_PAGE'],
                                           error_out=False)
    previous = None
    if pagination.has_prev:
        if q:
            previous = url_for('events.eventlist', q=q, page=page - 1, _external=True)
        else:
            previous = url_for('events.eventlist', page=page - 1, _external=True)
    nex = None
    if pagination.has_next:
        if q:
            nex = url_for('events.eventlist', q=q, page=page + 1, _external=True)
        else:
            nex = url_for('events.eventlist', page=page + 1, _external=True)
    items = pagination.items
    return items, nex, pagination, previous