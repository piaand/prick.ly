# User stories
In this document all the planned user stories are listed. In addition all SQL queries related to the user stories are listed.

## List of stories
- As a user I want login to service to see my bookings with the hedgehogs (done)
- As a user I want to inspect all the details of a specific hedgehog at one view so that I can see all the information that may impact my decision (done)
- As a user I want to search hedgehogs by their individual attributes, such as age, so that I can pick the one I want to meet
- As a user I want to filter out those hedgehogs that are not available at the time I suggest (done)
- As a user I want to book a meetup with one or several hedgehogs (done)
- As the admin I want to add and remove hedgehogs from the listing so that the listing remains up to date (done)
- As the admin I want to set hedgehogs on or off duty so that hedgehogs get a decent rest and are not overworked (done)
- As the admin I need to know that no one else than admins can update the information about the hedgehogs (done)
- As the admin I want to see all hedgehogs in the service (done)
- As the admin I need to see all booked hedgehogs at a given timespan (certain date, a week etc) so that I can follow the demand for hedgehogs

## Create database schemas
Below is the current (in production) schema about the Prick.ly database

CREATE TABLE hog (\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;id INTEGER NOT NULL,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;date_created DATETIME,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;date_modified DATETIME,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;name VARCHAR(144) NOT NULL,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;onduty BOOLEAN NOT NULL,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PRIMARY KEY (id),\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CHECK (onduty IN (0, 1))\
)

CREATE TABLE account (\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;id INTEGER NOT NULL,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;date_created DATETIME,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;date_modified DATETIME,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;name VARCHAR(144) NOT NULL,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;username VARCHAR(144) NOT NULL,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;password VARCHAR(144) NOT NULL,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;access VARCHAR(144) NOT NULL,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PRIMARY KEY (id)\
)

CREATE TABLE reservation (\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;id INTEGER NOT NULL,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;date_created DATETIME,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;date_modified DATETIME,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;start_time DATETIME NOT NULL,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;duration_min INTEGER NOT NULL,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;account_id INTEGER NOT NULL,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;verified BOOLEAN NOT NULL,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PRIMARY KEY (id),\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;FOREIGN KEY(account_id) REFERENCES account (id),\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CHECK (verified IN (0, 1))\
)

CREATE TABLE hog_identifier (\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;reservation_id INTEGER,\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hog_id INTEGER, \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;FOREIGN KEY(reservation_id) REFERENCES reservation (id), \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;FOREIGN KEY(hog_id) REFERENCES hog (id)\
)


## SQL queries
Below are the in production SQL queries and their respective user stories:

- As the admin I want to see all hedgehogs in the service\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SELECT hog.id AS hog_id, hog.date_created AS hog_date_created, hog.date_modified AS hog_date_modified, hog.name AS hog_name, hog.onduty AS hog_onduty
- As the admin I want to add and remove hedgehogs to the listing so that the listing remains up to date\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; INSERT INTO Hog (date_created, date_modified, name, onduty) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; DELETE FROM hog WHERE hog.id = ?
- As the admin I want to set hedgehogs on or off duty so that hedgehogs get a decent rest and are not overworked\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;UPDATE Hog SET date_modified=CURRENT_TIMESTAMP, onduty=? WHERE hog.id = ?
- As a user I want to inspect all the details of a specific hedgehog at one view so that I can see all the information that may impact my decision\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SELECT hog.name AS name, COALESCE(total, 0), hog.onduty AS onduty, hog.id AS id FROM hog\
LEFT JOIN ( SELECT SUM(reservation.duration_min) AS total, hog_identifier.hog_id AS identify FROM reservation\
LEFT JOIN hog_identifier ON hog_identifier.reservation_id = reservation.id GROUP BY identify) AS derivedtable\
ON identify = id ORDER BY total DESC
- As a user I want login to service to see my bookings with the hedgehogs\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SELECT reservation.id, reservation.date_created, reservation.date_modified, reservation_start_time, reservation_duration_min, reservation_account_id, reservation_verified FROM reservation\
WHERE reservation.account_id = ?
- As a user I want to filter out those hedgehogs that are not available at the time I suggest\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SELECT hog.name AS name, hog.id AS id FROM hog WHERE id NOT IN\
(SELECT hog.id AS id_booked FROM hog LEFT JOIN (\
SELECT hog_identifier.hog_id AS identify, reservation.start_time AS start_time FROM reservation\
LEFT JOIN hog_identifier ON hog_identifier.reservation_id = reservation.id) AS derivedtable\
ON identify = hog.id WHERE NOT (start_time < ? OR start_time > ?))\
AND (hog.onduty = True)
- As a user I want to book a meetup with one or several hedgehogs\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;INSERT INTO reservation (date_created, date_modified, start_time, duration_min, account_id, verified) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?, ?)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;INSERT INTO hog_identifier (reservation_id, hog_id) VALUES (?, ?)
- As the admin I need to know that no one else than admins can update the information about the hedgehogs
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Implementation of this functionality was not done in database level but as several secured checks before execution of the request

