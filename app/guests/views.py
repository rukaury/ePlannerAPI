from flask import Blueprint, request, abort
from app.auth.helper import token_required
from app.guests.helper import response, response_for_created_guest, response_for_user_guest, response_with_pagination, \
    get_user_guests_json_list, paginate_guests
from app.models.users import User
from app.models.guests import Guest
import re

# Initialize blueprint
guests = Blueprint('guests', __name__)


@guests.route('/guests/', methods=['GET'])
@token_required
def guestlist(current_user):
    """
    Return all the guests created by the user or limit them to 10.
    Return an empty guests object if user has no guests
    :param current_user:
    :return:
    """
    user = User.get_by_id(current_user.id)
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', None, type=str)

    items, nex, pagination, previous = paginate_guests(current_user.id, page, q, user)

    if items:
        return response_with_pagination(get_user_guests_json_list(items), previous, nex, pagination.total)
    return response_with_pagination([], previous, nex, 0)


@guests.route('/guests/', methods=['POST'])
@token_required
def create_guest(current_user):
    """
    Create a guest from the sent json data.
    :param current_user: Current User
    :return:
    """
    if request.content_type == 'application/json':
        data = request.get_json().get("guest")
        f_name = data.get('first_name')
        l_name = data.get('last_name')
        organization = data.get('organization')
        email = data.get('email')
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            if f_name and l_name and organization and email:
                user_guest = Guest(f_name, l_name, organization, email, current_user.id)
                user_guest.save()
                return response_for_created_guest(user_guest, 201)
            return response('failed', 'Missing some guest data', 400)
        return response('failed', 'Wrong email format', 401)        
    return response('failed', 'Content-type must be json', 202)


@guests.route('/guests/<guest_id>', methods=['GET'])
@token_required
def get_guest(current_user, guest_id):
    """
    Return a user guest with the supplied user Id.
    :param current_user: User
    :param guest_id: guest Id
    :return:
    """
    try:
        int(guest_id)
    except ValueError:
        return response('failed', 'Please provide a valid guest Id', 400)
    else:
        user_guest = User.get_by_id(current_user.id).guests.filter_by(guest_id=guest_id).first()
        if user_guest:
            return response_for_user_guest(user_guest.json())
        return response('failed', "Guest not found", 404)


@guests.route('/guests/<guest_id>', methods=['PUT'])
@token_required
def edit_guest(current_user, guest_id):
    """
    Validate the guest Id. Also check for the data in the json payload.
    If the data exists update the guest with the new data.
    :param current_user: Current User
    :param guest_id: guest Id
    :return: Http Json response
    """
    if request.content_type == 'application/json':
        data = request.get_json().get("guest")
        f_name = data.get('first_name') if data.get('first_name') is not None else ""
        l_name = data.get('last_name')  if data.get('last_name') is not None else ""
        organization = data.get('organization') if data.get('organization') is not None else ""
        email = data.get('email') if data.get('email') is not None else ""

        # Check email format
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return response('failed', 'Wrong email format', 401)

        updated_guest = Guest(f_name, l_name, organization, email, current_user.id)
        if f_name or l_name or organization or email:
            try:
                int(guest_id)
            except ValueError:
                return response('failed', 'Please provide a valid guest Id', 400)
            user_guest = User.get_by_id(current_user.id).guests.filter_by(guest_id=guest_id).first()
            if user_guest:
                user_guest.update(updated_guest)
                return response_for_created_guest(user_guest, 201)
            return response('failed', 'The guest with Id ' + guest_id + ' does not exist', 404)
        return response('failed', 'No attribute or value was specified, nothing was changed', 400)
    return response('failed', 'Content-type must be json', 202)


@guests.route('/guests/<guest_id>', methods=['DELETE'])
@token_required
def delete_guest(current_user, guest_id):
    """
    Deleting a User guest from the database if it exists.
    :param current_user:
    :param guest_id:
    :return:
    """
    try:
        int(guest_id)
    except ValueError:
        return response('failed', 'Please provide a valid guest Id', 400)
    user_guest = User.get_by_id(current_user.id).guests.filter_by(guest_id=guest_id).first()
    if not user_guest:
        abort(404)
    user_guest.delete()
    return response('success', 'Guest Deleted successfully', 200)


@guests.errorhandler(404)
def handle_404_error(e):
    """
    Return a custom message for 404 errors.
    :param e:
    :return:
    """
    return response('failed', 'Guest resource cannot be found', 404)


@guests.errorhandler(400)
def handle_400_errors(e):
    """
    Return a custom response for 400 errors.
    :param e:
    :return:
    """
    return response('failed', 'Bad Request', 400)
