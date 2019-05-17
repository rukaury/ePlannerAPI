from flask import make_response, jsonify, url_for
from app import app
from app.models.guests import Guest


def response_for_user_guest(user_guest):
    """
    Return the response for when a single guest was requested by the user.
    :param guest:
    :return:
    """
    return make_response(jsonify({
        'status': 'success',
        'guest': user_guest
    }))


def response_for_created_guest(guest, status_code):
    """
    Method returning the response when a guest has been successfully created.
    :param status_code:
    :param guest: Guest
    :return: Http Response
    """
    return make_response(jsonify({"guest" : {
        'status': 'success',
        'guest_id': guest.guest_id,
        'first_name': guest.first_name,
        'last_name': guest.last_name,
        'email': guest.email,
        'organization': guest.organization,
        'created_on': guest.guest_created_on,
        'modified_on': guest.guest_updated_on
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


def get_user_guests_json_list(user_guests):
    """
    Make json objects of the user guests and add them to a list.
    :param user_guests: Guest
    :return:
    """
    guests = []
    for user_guest in user_guests:
        guests.append(user_guest.json())
    return guests


def response_with_pagination(guests, previous, nex, count):
    """
    Make a http response for GuestList get requests.
    :param count: Pagination Total
    :param nex: Next page Url if it exists
    :param previous: Previous page Url if it exists
    :param guests: Guest
    :return: Http Json response
    """
    return make_response(jsonify({
        'status': 'success',
        'previous': previous,
        'next': nex,
        'count': count,
        'guests': guests
    })), 200


def paginate_guests(user_id, page, q, user):
    """
    Get a user by Id, then get hold of their guests and also paginate the results.
    There is also an option to search for a guest name if the query param is set.
    Generate previous and next pagination urls
    :param q: Query parameter
    :param user_id: User Id
    :param user: Current User
    :param page: Page number
    :return: Pagination next url, previous url and the user guests.
    """
    if q:
        pagination = Guest.query.filter(Guest.last_name.like("%" + q.lower().strip() + "%")).filter_by(user_id=user_id) \
            .paginate(page=page, per_page=app.config['EVENTS_AND_TICKETS_PER_PAGE'], error_out=False)
    else:
        pagination = user.guests.paginate(page=page, per_page=app.config['EVENTS_AND_TICKETS_PER_PAGE'],
                                           error_out=False)
    previous = None
    if pagination.has_prev:
        if q:
            previous = url_for('guests.guestlist', q=q, page=page - 1, _external=True)
        else:
            previous = url_for('guests.guestlist', page=page - 1, _external=True)
    nex = None
    if pagination.has_next:
        if q:
            nex = url_for('guests.guestlist', q=q, page=page + 1, _external=True)
        else:
            nex = url_for('guests.guestlist', page=page + 1, _external=True)
    items = pagination.items
    return items, nex, pagination, previous