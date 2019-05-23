from flask import Blueprint, request, abort
from app.auth.helper import token_required
from app.events.helper import response, response_for_created_event, response_for_user_event, response_with_pagination, \
    get_user_events_json_list, paginate_events
from app.models.users import User
from app.models.events import Event

# Initialize blueprint
events = Blueprint('events', __name__)


@events.route('/events/', methods=['GET'])
@token_required
def eventlist(current_user):
    """
    Return all the events created by the user or limit them to 10.
    Return an empty events object if user has no events
    :param current_user:
    :return:
    """
    user = User.get_by_id(current_user.id)
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', None, type=str)

    items, nex, pagination, previous = paginate_events(current_user.id, page, q, user)

    if items:
        return response_with_pagination(get_user_events_json_list(items), previous, nex, pagination.total)
    return response_with_pagination([], previous, nex, 0)


@events.route('/events/', methods=['POST'])
@token_required
def create_event(current_user):
    """
    Create an event from the sent json data.
    :param current_user: Current User
    :return:
    """
    if request.content_type == 'application/json':
        data = request.get_json().get("event")
        name = data.get('name') if data.get('name') is not None else None
        location = data.get('location') if data.get('location') is not None else None
        time = data.get('time') if data.get('time') is not None else None 
        eval_link = data.get('eval_link') if data.get('eval_link') is not None else None
        if name and location and time:
            user_event = Event(name, location, time, current_user.id)
            user_event.event_eval_link = eval_link
            user_event.save()
            return response_for_created_event(user_event, 201)
        return response('failed', 'Missing some event data, nothing was changed', 400)
    return response('failed', 'Content-type must be json', 202)


@events.route('/events/<event_id>', methods=['GET'])
@token_required
def get_event(current_user, event_id):
    """
    Return a user event with the supplied user Id.
    :param current_user: User
    :param event_id: Event Id
    :return:
    """
    try:
        int(event_id)
    except ValueError:
        return response('failed', 'Please provide a valid Event Id', 400)
    else:
        user_event = User.get_by_id(current_user.id).events.filter_by(event_id=event_id).first()
        if user_event:
            return response_for_user_event(user_event.json())
        return response('failed', "Event not found", 404)


@events.route('/events/<event_id>', methods=['PUT'])
@token_required
def edit_event(current_user, event_id):
    """
    Validate the event Id. Also check for the data in the json payload.
    If the data exists update the event with the new data.
    :param current_user: Current User
    :param event_id: Event Id
    :return: Http Json response
    """
    if request.content_type == 'application/json':
        data = request.get_json().get("event")
        name = data.get('name') if data.get("name") is not None else ""
        location = data.get('location') if data.get("location") is not None else ""
        time = data.get('time') if data.get("time") is not None else ""
        eval_link = data.get('eval_link') if data.get("eval_link") is not None else ""
        updated_event = Event(name, location, time, current_user.id)
        updated_event.event_eval_link = eval_link
        if name or location or time or eval_link:
            try:
                int(event_id)
            except ValueError:
                return response('failed', 'Please provide a valid Event Id', 400)
            user_event = User.get_by_id(current_user.id).events.filter_by(event_id=event_id).first()
            if user_event:
                user_event.update(updated_event)
                return response_for_created_event(user_event, 201)
            return response('failed', 'The Event with Id ' + event_id + ' does not exist', 404)
        return response('failed', 'No attribute or value was specified, nothing was changed', 400)
    return response('failed', 'Content-type must be json', 202)


@events.route('/events/<event_id>', methods=['DELETE'])
@token_required
def delete_event(current_user, event_id):
    """
    Deleting a User Event from the database if it exists.
    :param current_user:
    :param event_id:
    :return:
    """
    try:
        int(event_id)
    except ValueError:
        return response('failed', 'Please provide a valid Event Id', 400)
    user_event = User.get_by_id(current_user.id).events.filter_by(event_id=event_id).first()
    if not user_event:
        abort(404)
    user_event.delete()
    return response('success', 'Event Deleted successfully', 200)


@events.errorhandler(404)
def handle_404_error(e):
    """
    Return a custom message for 404 errors.
    :param e:
    :return:
    """
    return response('failed', 'Event resource cannot be found', 404)


@events.errorhandler(400)
def handle_400_errors(e):
    """
    Return a custom response for 400 errors.
    :param e:
    :return:
    """
    return response('failed', 'Bad Request', 400)
