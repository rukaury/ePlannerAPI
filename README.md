# ePlanner REST API

API used for the ePlanner system (QR code reader and TicketViewer). The API should allow users to register, login, logout and list or add necessary information regarding events, tickets and guests.


## Usage
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
    - [Users](#users)
    - [Events](#events)
    - [Tickets](#tickets)
    - [Guests](#guests)
- [Running the tests](#running-the-tests)
- [Deployment](#deployment)
- [Built with](#built-with)
- [Contributing](#contributing)
- [Versioning](#versioning)
- [Authors](#authors)
- [License](#license)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The API is built using a small python-based framework called Flask, therefore will require python to be installed.

### Installing

Once python is installed, a virtual environment can be used for development. 

These steps can be used to install a virtual environment: 

1. Install a virtual environment (Mac OS X): `sudo easy_install virtualenv` 

2. Activate the environment by running: `venv/Scripts/activate`

Creating a virtual environment for each application ensures that applications have access to only the packages that they use.

## API Documentation

### Users

#### User Registration [/auth/register]

##### Register a user [POST]

You can create a user by sending a json request with an email and password. The
password must be at least four(4) characters.

+ Request (application/json)

        {
            "email": "example@gmail.com",
            "password": "123456"
        }

+ Response 201 (application/json)

        {
            "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MDM0ODQ5OTYsImlhdCI6MTUwMzM5ODU4Niwic3ViIjo1fQ.GC6IEOohdo_xrz9__UeugIlir0qtJdKbEzBtLgqjt5A",
            "message": "Successfully registered",
            "status": "success"
        }

+ Response 202 (application/json)

        {
            "message": "Missing or wrong email format or password",
            "status": "failed"
        }

+ Response 202 (application/json)

        {
            "message": "Failed, User already exists, Please sign In",
            "status": "failed"
        }

+ Response 202 (application/json)

        {
          "message": "Content-type must be json",
          "status": "failed"
        }

#### Login [/auth/login]

##### Login a user [POST]

You can login a user by sending their email and password. Please take note
of the auth token for you will need it for all user requests.

+ Request (application/json)

        {
            "email": "example@gmail.com",
            "password": "123456"
        }

+ Response 201 (application/json)

        {
            "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MDM0ODQ5OTYsImlhdCI6MTUwMzM5ODU4Niwic3ViIjo1fQ.GC6IEOohdo_xrz9__UeugIlir0qtJdKbEzBtLgqjt5A",
            "message": "Successfully registered",
            "status": "success"
        }

+ Response 202 (application/json)

        {
          "message": "Content-type must be json",
          "status": "failed"
        }

+ Response 401 (application/json)

        {
          "message": "Missing or wrong email format or password is less than four characters",
          "status": "failed"
        }

+ Response 401 (application/json)

        {
          "message": "User does not exist or password is incorrect",
          "status": "failed"
        }

#### Logout [/auth/logout]

##### Log out a user [POST]

You can log out a user by sending a request with their email and address. The
auth token will then be invalidated (blacklisted).

+ Request (application/json)

    + Headers

            Authorization: Bearer JWT Token

+ Response 200 (application/json)

        {
            "message": "Successfully logged out",
            "status": "success"
        }

+ Response 403 (application/json)

        {
          "message": "Provide a valid auth token",
          "status": "failed"
        }

+ Response 403 (application/json)

        {
          "message": "Provide an authorization header",
          "status": "failed"
        }

+ Response 401 (application/json)

        {
          "message": "Signature expired, Please sign in again",
          "status": "failed"
        }

+ Response 401 (application/json)

        {
          "message": "Invalid token. Please sign in again",
          "status": "failed"
        }

### Events

#### Event Resources [/events{?page}{?q}]

You can create, read, update and delete events.

NOTE: A valid token should be present in the header else a 401 or 403 response
will be returned as seen in the log out section.

+ Parameters
    + page(optional, number, `1`) - The page number
    + q(optional, string) - Search query

##### Create an Event [POST]
    Add a new Event attached to the user

+ name (required, string) -  Name of the Event
+ location (required, string) -  Location of the Event
+ eval_link (optional, string) -  Evaluation of the Event
+ time (required, date) -  Time when the event will happen

+ Request (application/json)


    + Headers

            Authorization: Bearer JWT Token

    + Body

            {
                "event" : 
                {
                    "name" : "DIS retreat (CI / CD)",
                    "location" : "Bayview Yards, 7 Bayview Rd, Ottawa, ON K1Y 2C5",
                    "time" : "2019-05-19 15:00",
                    "eval_link": "https://en.busrides-trajetsenbus.ca/",
                }
            }

+ Response 201 (application/json)

        {
            "event": {
                "created_on": "Fri, 17 May 2019 14:44:21 GMT",
                "event_eval_link": "https://en.busrides-trajetsenbus.ca/",
                "event_id": 8,
                "event_location": "Bayview Yards, 7 Bayview Rd, Ottawa, ON K1Y 2C5",
                "event_name": "DIS retreat (CI / CD)",
                "event_time": "Sun, 19 May 2019 15:00:00 GMT",
                "modified_on": "Fri, 17 May 2019 14:44:21 GMT",
                "status": "success"
            }
        }

+ Response 202 (application/json)

        {
          "message": "Content-type must be json",
          "status": "failed"
        }

+ Response 400 (application/json)

        {
          "message": "Missing some event data",
          "status": "failed"
        }

##### List all Events [GET]

You can get a list of all the Events that belong to a user. The results are
paginated with the previous and next url.

You can also search for an Event by its name using the q query parameter.


+ Request (application/json)


    + Headers

            Authorization: Bearer JWT Token

+ Response 200 (application/json)

        {
            "count": 4,
            "events": [
                {
                    "created_on": "2019-05-16T19:10:25.138377",
                    "event_id": 5,
                    "event_location": "Bayview Yards, 7 Bayview Rd, Ottawa, ON K1Y 2C5",
                    "event_name": "DIS retreat (CI / CD)",
                    "event_time": "2019-05-19T15:00:00",
                    "modified_on": "2019-05-16T19:14:38.530211"
                },
                {
                    "created_on": "2019-05-17T14:36:02.839747",
                    "event_id": 6,
                    "event_location": "Bayview Yards, 7 Bayview Rd, Ottawa, ON K1Y 2C5",
                    "event_name": "DIS retreat (CI / CD)",
                    "event_time": "2019-05-19T15:00:00",
                    "modified_on": "2019-05-17T14:36:02.839747"
                },
                {
                    "created_on": "2019-05-17T14:41:57.123927",
                    "event_id": 7,
                    "event_location": "Bayview Yards, 7 Bayview Rd, Ottawa, ON K1Y 2C5",
                    "event_name": "DIS retreat (CI / CD)",
                    "event_time": "2019-05-19T15:00:00",
                    "modified_on": "2019-05-17T14:41:57.123927"
                }
            ],
            "next": "http://localhost:5000/v1/events/?page=2",
            "previous": null,
            "status
        }

+ Response 200 (application/json)

        {
            "count": 0,
            "events": [],
            "next": null,
            "previous": null,
            "status : "success"
        }

#### Single Event Resources [/events/{event_id}]

+ Parameters
    + event_id (required,number) - Id of the event to be returned

##### Get an Event [GET]

You get a single event by specifying its Id.

+ Request (application/json)


    + Headers

            Authorization: Bearer JWT Token

+ Response 200 (application/json)

        {
            "event": {
                "created_on": "2019-05-17T14:44:21.585719",
                "event_id": 8,
                "event_location": "Bayview Yards, 7 Bayview Rd, Ottawa, ON K1Y 2C5",
                "event_name": "DIS retreat (CI / CD)",
                "event_time": "2019-05-19T15:00:00",
                "modified_on": "2019-05-17T14:44:21.585719"
            },
            "status": "success"
        }

+ Response 400 (application/json)

        {
          "message": "Please provide a valid Event Id",
          "status": "failed"
        }

+ Response 404 (application/json)

        {
          "message": "Event not found",
          "status": "failed"
        }

##### Edit an event [PUT]

You can update the name, location, time and evaluation link of the Event. 

At least one data attribute and value need to be provided.

+ name (optional, string) -  Name of the Event
+ location (optional, string) -  Location of the Event
+ eval_link (optional, string) -  Evaluation of the Event
+ time (optional, date) -  Time when the event will happen

+ Request (application/json)


    + Headers

            Authorization: Bearer JWT Token

    + Body

            {
                "event" : 
                {
                    "location" : "La Salle Academy, 373 Sussex Dr, Ottawa, ON K1N 6Z2
                }
            }

+ Response 201 (application/json)

        {
            "event": {
                "created_on": "Fri, 17 May 2019 14:44:21 GMT",
                "event_eval_link": "https://en.busrides-trajetsenbus.ca/",
                "event_id": 8,
                "event_location": "La Salle Academy, 373 Sussex Dr, Ottawa, ON K1N 6Z2",
                "event_name": "DIS retreat (CI / CD)",
                "event_time": "Sun, 19 May 2019 15:00:00 GMT",
                "modified_on": "Fri, 17 May 2019 15:27:14 GMT",
                "status": "success"
            }
        }

+ Response 202 (application/json)

        {
          "message": "Content-type must be json",
          "status": "failed"
        }

+ Response 400 (application/json)

        {
          "message": "Please provide a valid Event Id",
          "status": "failed"
        }

+ Response 400 (application/json)

        {
          "message": "No attribute or value was specified, nothing was changed",
          "status": "failed"
        }

+ Response 404 (application/json)

        {
          "message": "The Event with Id does not exist",
          "status": "failed"
        }

##### Delete an event [DELETE]

+ Request (application/json)


    + Headers

            Authorization: Bearer JWT Token

+ Response 200 (application/json)

        {
            "message": "Event Deleted successfully",
            "status": "success"
        }

+ Response 400 (application/json)

        {
          "message": "Please provide a valid Event Id",
          "status": "failed"
        }

+ Response 404 (application/json)

        {
          "message": "Event resource cannot be found",
          "status": "failed"
        }

### Tickets

#### Event Ticket Resources [/events/{event_id}/tickets{?page}/{?q}] or [/events/{event_id}/guests/{guest_id}/tickets] 

You can create, read, update and delete event tickets.

NOTE: A valid token should be present in the header else a 401 or 403 response
will be returned as seen in the log out section.

The Event Id must be valid else a response with code status 401 will be returned

The Guest Id must be valid only for creating a ticket else a response with code status 401 will be returned

+ Parameters
    + event_id (required, number) - Id of the Event
    + guest_id (required, number) - Id of the Guest
    + page (optional, number, `1`) - Page to return
    + q (optional, string) - Search query string

##### Get all tickets within an event [GET]

You can get all the tickets within the event if they exist, otherwise the tickets
list will be empty.

You can also use the query parameter q to search for a ticket qr code text within the Ticket as showm below (Qr code contains guest name for example)

+ Request (application/json)


    + Headers

            Authorization: Bearer JWT Token

+ Response 200 (application/json)

        {
            "count": 2,
            "next": null,
            "previous": null,
            "status": "success",
            "tickets": [
                {
                    "accepted": false,
                    "comments": "Guest needs an elevator",
                    "created_on": "2019-05-17T16:41:45.099966",
                    "event_id": 8,
                    "guest_id": 3,
                    "modified_on": "2019-05-17T16:41:45.099966",
                    "qr_code": "qrcodetext",
                    "scanned": 0,
                    "ticket_id": 5,
                    "vvip": false
                },
                {
                    "accepted": true,
                    "comments": null,
                    "created_on": "2019-05-16T15:43:27.647366",
                    "event_id": 8,
                    "guest_id": 2,
                    "modified_on": "2019-05-16T15:43:27.647366",
                    "qr_code": "qrcode",
                    "scanned": 3,
                    "ticket_id": 1,
                    "vvip": true
                }
            ]
        }

+ Response 200 (application/json)

        {
            "count": 0,
            "next": null,
            "previous": null,
            "status": "success",
            "tickets": []
        }

+ Response 401 (application/json)

        {
          "message": "Provide a valid Event Id",
          "status": "failed"
        }

##### Add a ticket to the Event [POST]

You can also add a ticket to the Event by sending a qr code text, vvip, accepted, scanned and an optional
comments.

+ qr_code (required, string) - Qr code text of the ticket
+ vvip (required, Boolean) - Vvip info of the guest
+ accepted (required, Boolean) - Invitation acceptance of the guest
+ scanned (required, Integer) - How many times the ticket was scanned
+ comments (optional, string) - Comments on the ticket

+ Request (application/json)


    + Headers

            Authorization: Bearer JWT Token

    + Body

            {
                "ticket" : 
                {
                    "qr_code" : "qrcodetext",
                    "vvip" : "0",
                    "accepted" : "0",
                    "scanned" : "0", 
                    "comments" : "Guest needs an elevator"
                }
            }

+ Response 201 (application/json)

        {
            "status": "success",
            "ticket": {
                "accepted": false,
                "comments": "Guest needs an elevator",
                "created_on": "2019-05-17T16:41:45.099966",
                "event_id": 8,
                "guest_id": 3,
                "modified_on": "2019-05-17T16:41:45.099966",
                "qr_code": "qrcodetext",
                "scanned": 0,
                "ticket_id": 5,
                "vvip": false
            }
        }

+ Response 202 (application/json)

        {
          "message": "User has no Event with Id",
          "status": "failed"
        }

+ Response 202 (application/json)

    {
        "message": "Ticket exists already for guest id 2 participating at event id 1",
        "status": "failed"
    }

+ Response 401 (application/json)

        {
          "message": "No ticket value attribute found",
          "status": "failed"
        }

+ Response 401 (application/json)

        {
          "message": "Content-type must be application/json",
          "status": "failed"
        }

#### Single Event Tickets Resource [/events/{event_id}/tickets/{ticket_id}]

NOTE: A valid token should be present in the header else a 401 or 403 response
will be returned as seen in the log out section.

The Event Id must be valid else a response with code status 401 will be returned

+ Parameters
    + event_id (required, number) - Id of the Event
    + ticket_id (required, number) - Id of the ticket

##### Get a Ticket from the Event [GET]

You can get a Ticket from the Event by specifying the Event Id and Ticket Id

+ Request (application/json)


    + Headers

            Authorization: Bearer JWT Token

+ Response 201 (application/json)

        {
            "status": "success",
            "ticket": {
                "accepted": false,
                "comments": "Guest needs an elevator",
                "created_on": "2019-05-17T16:41:45.099966",
                "event_id": 8,
                "guest_id": 3,
                "modified_on": "2019-05-17T16:41:45.099966",
                "qr_code": "qrcodetext",
                "scanned": 0,
                "ticket_id": 5,
                "vvip": false
            }
        }

+ Response 202 (application/json)

        {
          "message": "Provide a valid ticket Id",
          "status": "failed"
        }

+ Response 202 (application/json)

        {
          "message": "User has no Event with Id",
          "status": "failed"
        }


##### Edit a Ticket within a Event [PUT]

You can also edit a ticket within the Event.

At least one data attribute and value need to be provided.

+ vvip (optional, Boolean) - Vvip info of the guest
+ accepted (optional, Boolean) - Invitation acceptance of the guest
+ scanned (optional, Integer) - How many times the ticket was scanned
+ comments (optional, string) - Comments on the ticket

+ Request (application/json)


    + Headers

            Authorization: Bearer JWT Token

    + Body

            {
                "ticket" : 
                {
                    "scanned" : "1"
                }
            }

+ Response 200 (application/json)

        {
            "status": "success",
            "ticket": {
                "accepted": false,
                "comments": "Guest needs an elevator",
                "created_on": "2019-05-17T16:41:45.099966",
                "event_id": 8,
                "guest_id": 3,
                "modified_on": "2019-05-17T16:41:45.099966",
                "qr_code": "qrcodetext",
                "scanned": 1,
                "ticket_id": 5,
                "vvip": false
            }
        }

+ Response 401 (application/json)

        {
          "message": "No ticket data or value attribute found",
          "status": "failed"
        }

+ Response 401 (application/json)

        {
          "message": "No attributes specified in the request",
          "status": "failed"
        }

##### Delete a ticket from the Event [DELETE]

You can delete a ticket from an Event by sending a delete request, by specifying
the event Id and ticket Id.

+ Request (application/json)


    + Headers

            Authorization: Bearer JWT Token

+ Response 200 (application/json)

        {
            "message": "Successfully deleted the ticket from event with Id 8",
            "status": "success"
        }

+ Response 404 (application/json)

        {
          "message": "Ticket not found",
          "status": "failed"
        }

### Guests

#### Guest Resources [/guests{?page}{?q}]

You can create, read, update and delete guests.

NOTE: A valid token should be present in the header else a 401 or 403 response
will be returned as seen in the log out section.

+ Parameters
    + page(optional, number, `1`) - The page number
    + q(optional, string) - Search query

##### Create a Guest [POST]
    Add a new Guest attached to the user

+ first_name (required, string) -  First name of the Guest
+ last_name (required, string) -  Last name of the Guest
+ organization (required, string) -  Organization of the Guest
+ email (required, string) -  Email of the Guest

+ Request (application/json)


    + Headers

            Authorization: Bearer JWT Token

    + Body

            {
                "guest" : 
                {
                    "first_name" : "Nikola",
                    "last_name" : "Tesla",
                    "organization" : "CSPS",
                    "email" : "nikola.tesla@canada.ca"
                }
            }

+ Response 201 (application/json)

        {
            "guest": {
                "created_on": "Fri, 17 May 2019 18:05:58 GMT",
                "email": "nikola.tesla@canada.ca",
                "first_name": "Nikola",
                "guest_id": 6,
                "last_name": "Tesla",
                "modified_on": "Fri, 17 May 2019 18:05:58 GMT",
                "organization": "CSPS",
                "status": "success"
            }
        }

+ Response 202 (application/json)

        {
          "message": "Content-type must be json",
          "status": "failed"
        }

+ Response 400 (application/json)

        {
          "message": "Missing some guest data",
          "status": "failed"
        }

+ Response 401 (application/json)

        {
          "message": "Wrong email format",
          "status": "failed"
        }

##### List all Guest [GET]

You can get a list of all the guests that belong to a user. The results are
paginated with the previous and next url.

You can also search for a Guest by its name using the q query parameter.


+ Request (application/json)


    + Headers

            Authorization: Bearer JWT Token

+ Response 200 (application/json)

        {
            "count": 3,
            "guests": [
                {
                    "created_on": "2019-05-16T15:23:45.073426",
                    "email": "test@name.ca",
                    "first_name": "Test",
                    "id": 2,
                    "last_name": "Name",
                    "modified_on": "2019-05-16T15:23:45.073426",
                    "organization": "CSPS"
                },
                {
                    "created_on": "2019-05-16T19:32:06.527834",
                    "email": "donald.trump@us.gov",
                    "first_name": "Donald",
                    "id": 3,
                    "last_name": "Trump",
                    "modified_on": "2019-05-16T19:45:05.339792",
                    "organization": "UPS"
                },
                {
                    "created_on": "2019-05-17T18:05:58.613725",
                    "email": "nikola.tesla@canada.ca",
                    "first_name": "Nikola",
                    "id": 6,
                    "last_name": "Tesla",
                    "modified_on": "2019-05-17T18:05:58.613725",
                    "organization": "CSPS"
                }
            ],
            "next": null,
            "previous": null,
            "status": "success"
        }

+ Response 200 (application/json)

        {
            "count": 0,
            "guests": [],
            "next": null,
            "previous": null,
            "status : "success"
        }

#### Single Guest Resources [/guests/{guest_id}]

+ Parameters
    + guest_id (required,number) - Id of the guest to be returned

##### Get a Guest [GET]

You get a single guest by specifying its Id.

+ Request (application/json)


    + Headers

            Authorization: Bearer JWT Token

+ Response 200 (application/json)

        {
            "guest": {
                "created_on": "2019-05-16T15:23:45.073426",
                "email": "test@name.ca",
                "first_name": "Test",
                "id": 2,
                "last_name": "Name",
                "modified_on": "2019-05-16T15:23:45.073426",
                "organization": "CSPS"
            },
            "status": "success"
        }

+ Response 400 (application/json)

        {
          "message": "Please provide a valid Guest Id",
          "status": "failed"
        }

+ Response 404 (application/json)

        {
          "message": "Guest not found",
          "status": "failed"
        }

##### Edit a guest [PUT]

You can update the first name, last name, organization and email of the Guest. 

At least one data attribute and value need to be provided.

+ first_name (optional, string) -  First name of the Guest
+ last_name (optional, string) -  Last name of the Guest
+ organization (optional, string) -  Organization of the Guest
+ email (optional, string) -  Email of the Guest

+ Request (application/json)


    + Headers

            Authorization: Bearer JWT Token

    + Body

            {
                "guest" : 
                {
                    "email" : "nikola.tesla@states.com"
                }
            }

+ Response 201 (application/json)

        {
            "guest": {
                "created_on": "Fri, 17 May 2019 18:05:58 GMT",
                "email": "nikola.tesla@states.com",
                "first_name": "Nikola",
                "guest_id": 6,
                "last_name": "Tesla",
                "modified_on": "Fri, 17 May 2019 18:26:43 GMT",
                "organization": "CSPS",
                "status": "success"
            }
        }

+ Response 202 (application/json)

        {
          "message": "Content-type must be json",
          "status": "failed"
        }

+ Response 400 (application/json)

        {
          "message": "Please provide a valid Guest Id",
          "status": "failed"
        }

+ Response 400 (application/json)

        {
          "message": "No attribute or value was specified, nothing was changed",
          "status": "failed"
        }

+ Response 401 (application/json)

        {
          "message": "Wrong email format",
          "status": "failed"
        }

+ Response 404 (application/json)

        {
          "message": "The Guest with Id does not exist",
          "status": "failed"
        }

##### Delete a guest [DELETE]

+ Request (application/json)


    + Headers

            Authorization: Bearer JWT Token

+ Response 200 (application/json)

        {
            "message": "Guest Deleted successfully",
            "status": "success"
        }

+ Response 400 (application/json)

        {
          "message": "Please provide a valid Guest Id",
          "status": "failed"
        }

+ Response 404 (application/json)

        {
          "message": "Guest resource cannot be found",
          "status": "failed"
        }

## Running the tests

Tests have not been implemented yet.

## Deployment

Not ready for deployment yet.

## Built with

* [Flask](http://flask.pocoo.org) - Web framework used
* [SQLAlchemy](https://www.sqlalchemy.org/) - SQL Toolkit and ORM

## Contributing

Decisions has not been made yet on who can contribute to this repository.

## Versioning

Thinking of using semantic versioning, but decision has not been made yet. 

## Authors

* **Aury Rukazana** - *Initial work*

## License

This project is licensed under the MIT License.