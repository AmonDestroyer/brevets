# Brevet Time Calculator with API

Reimplementation of the
[RUSA ACP controle time calculator](https://rusa.org/octime_acp.html)
with flask, ajax, RESTful API service, and consumer website.

# Authors
* Michal Young: Initial version of this code.
* Ram Durairajan: Provision of the code and instruction for the project.
* Adam Case (acase@uoregon.edun): Implementation of the project.

# Brevet Controle Points
## Opening and Closing Time Calculation

The algorithm for calculating controle times is described [here](https://rusa.org/pages/acp-brevet-control-times-calculator). The table below is copied from associated link, the last row is not
included because brevets by acp are not greated than 1000km.

| Control Location (km) | Minimum Speed (km/hr)	| Maximum Speed (km/hr) |
|-----------------------|-----------------------|-----------------------|
|        (0 - 200]      |          15           |          34           |
|      (200 - 400]      |          15           |          32           |
|      (400 - 600]      |          15           |          30           |
|      (600 - 1000]     |        11.428         |          38           |
NOTE: ( and ] follow standard interval notation

Brevets are 200, 300, 400, 600, or 1000km in length. Controle points can be up
to 20% past the brevet distance, but never exceed 1000km.

 The controle point opening time is calculated by the sum time of distance traveled
 in a controle location range divided by the maximum speed, see Example 1.
 The time to open is rounded to the nearest minute.
 If the controle point is past the brevet length the opening time is calculated
 using the brevet length, see Example 2.


 The controle point closing time is the same as the opening time, just the
 minimum speed is used in place of the maximum speed. Except for the closing
 time for the final controle point will have the closing times following the
 table below.

 | Brevet Length (km) | Closing Time (hr)	|
 |--------------------|-------------------|
 |        200         |       13.5        |
 |        300         |       20.0        |
 |        400         |       27.0        |
 |        600         |       40.0        |
 |       1000         |       75.0        |


## Examples
In these examples opening times are calculated, but the same process is followed
for calculating closing times.
### Example 1 (Controle Point Covering Multiple Controle Ranges)

Let a brevet be 300km.

If a controle point is setup at 150km, then the opening time will be 150/34 =
4.411 hours = 264.7 minutes which will be rounded to 265 minutes from the start
of the brevet.

If a second controle point is setup at 220km, then the opening time will be
200/34 + 20/32 = 6.507 hours = 390.4 minutes which will be rounded to 390
minutes from the start of the brevet.

### Example 2 (Controle Point Beyone Brevet Distance)

Let a brevet be 200km.

If a final controle point is setup at 204km, 4km past the brevet distance, this
is okay, but the calculation is not the same as shown in Example 1.
The calculation for the opening time would be 204/34 = 6 hours = 360 minutes
from the start of the brevet.

## Guidence

It is not recommended to place a controle point at or before the 15 km mark of
the brevet as since the start of the brevet is typically open for 1 hour the
closing of the brevet start location will occur before the closure of the
first controle point.

# Developers
## Docker
All dependancies are in the `Dockerfile` and `docker-compose.yml`. The
website/service can be ran using `docker-compose up`. Mongo DB has issues
with Windows OS will sometimes run into a KeyError" so it is recommended to run
using Linux or Mac.

## Frontend
The front end is accessible using `localhost:6567`.

The template files can be found in `templates/`. `calc.html` contains
Javascript that automatically converts controle point entries from km to miles
and vise versa. The template will send the brevet length, controle point
distance, and date/time in ISO 8601 format to the backend where an ISO 8601
formatted date/time is returned by the backend and then populated in the
appropraite field.

## Backend
The backend consists of two main files `flask_brevets.py` and `acp_times.py`.

`flask_brevets.py`: Contains the flask microframework that manages routes when
navigating to the page, errors, and calls made by the frontend.

`acp_times.py`: Contains the individual calculations for opening and closing
times. This seperation is important for testing listed below.

## Considered Test Cases
Test cases were considered when implementing the two buttons. If the user is to click on the buttons the result will occur given the following situations.
### Submit
* An the data will not be submitted to the database and an error page will be presented...
  * If no controle points are entered
  * If the controle points are not provided in ascending order
  * If there are holes in the controle points
  * If the final controle point is 120% above the brevet distance

### Display
Display a page noting that there are no times in the database if nothing has been submitted.
Otherwise the display page will provide a list of all brevets and control points
in a list/table format.

## API
The API is accessible using `localhost:6568`.

There is an API service available to expose the database. An API call follows the
following format.
`http://<host:port>/LIST-TYPE/[FORMAT]?[TOP-K]`

Where:
* LIST-TYPE: Is one of the three below in JSON format
  * `listAll`: Returns all open and close times for control points
  * `listOpenOnly`: Returns all open times for control points
  * `listCloseOnly`: Returns all close times for control points
* `FORMAT`: Returns the desired format of the data
  * `json`: Returns the data in JSON format
  * `csv`: Returns the data in CSV format
* `TOP-K`: Returns the top "k" control points open and close times
  * `top=k`: Returns top k open and close times

The options can be combined as desired to get only open/close times, formatted
in a specific data style, and/or top "k" control points.

## Consumer Website
The consumer website is available using `localhost:6568`.

This provides a user friendly view of the API calls.


# Improvements
Many improvements can be made to this web application and mainly these lack of clarity or functionality is due to project or time constraints.

## input-form
* Currently the time will not recalculate when pressing the submission button. This results in the user needing to manually leave the field to ensure proper times are calculated prior to pressing the submission button. An update to automatically calculate the open and close times prior to submission should be done.
* There is no usage of the notes field, this might be good to let the user know of an error prior to them using the submit button.
* Indicating to the user when the submission has occured.

## API
* Currently all csv calls return a csv file while all json calls return a webpage. It would be best to make both of these outputs the same type, i.e. both present a file of the proper type or both get presented in the webpage.
* Due to the changes in the consumer website php file there is a call to no use top if top >= 9999. This should be removed and updated when the consumer website is addressed.
* The calls for each api resource is a bit messy, this can probably be cleaned up with in heritance.

## Consumer website
* The structure of the template files is messy, this is mainly due to my current lack of knowledge of apache and php. This can be improved by creating a general template file that will allow for the path to be pushed to the php template file and implemented for the appropriate function call.
* The use of a ridiculously high number if top was not provided is not great. This usage if changes were not made to the API will result in all returns being ordered by control opening time and not brevet. Future improvements will be to instead making the json call in php within the if statement and not outside.
* The website does not take into account an empty database, something needs to happen if null is returned for the api request.

# Update Information
Last Updated: 12/6/2021
