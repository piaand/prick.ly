# Prick.ly - Hedgehog Petting Zoo
Project for Database application course in Helsinki University. See the live project [here](https://prickly.herokuapp.com/).

To log in to the service create your own credentials or use the following:\
username:<b> sonic</b>\
password:<b> hedgehog</b>

To log in to the service as admin use the following:\
username:<b> admin</b>\
password:<b> hogmaster</b>

Project under construction

## Project description
Pricky.ly is the world’s first hedgehog petting zoo. Hedgehog lovers may log into the service to reseach the wonderfull various kind of hedgehogs they would like to meet in person. User that is logged in may book a meeting time with one or more hedgehogs at the same time - given that the hedgehogs are available and not on holiday or booked by some other keen hogger. Prick.ly service administratives can add new hedgehogs to the service and make sure that the status of every hedgehog is correct.

## Service functionalities
With Prick.ly it is possible to
- Sign up and login to the service
- Find hedhogs by their various qualities (name, breed, age etc.)
- Sort by hedgehogs that are available on certain time and date
- Book one or more hedgehogs for a meetup
- Add more hedgehogs to the database (for admins)
- Set a status of a hedgehog as "unavailable" (for admins)
- Delete a hedgehog from the database (for admins)

To see the updated user stories documentation, visit [here](documentation/userstories.md).

## Database description
Below is a picture about the database plan for the Prick.ly service. More detailed SQL queries are documented with the [user stories](documentation/userstories.md).

![DB Prick.ly](documentation/prickly_db.png)

## Further development ideas
As with every project that has limited amount of resources and time not all the ideas get implemented. Here are few suggestions with no specific order:
- As of now, the user can only add more hedgehogs to their reserved time. However, removing hedgehogs from reservation could concidered as well. Now the solution is to delete the reservation and create it with correct hedgehog
- When admin needs to remove a hedgehog from the service it would be appropriate to notify all the users that have a booking with the specific hedgehog. This would be done by generating a list of users with the reservations in the future and extend the database with more user specific contact information such as email or phone numbers
- There is a "verified" column in the database in the reservation table. This could be taken into use to notify users about their bookings or pushing them to for example read the safety instructions and guidance before their reserved event
- One might say that one of the most important selection criteria for a visitor of a hedgehog petting zoo is the looks of a hedgehog. Pictures would definitely bring more visual aspect and appeal to the application and help users to compare hedgehogs and learn about their characteristics. This could be done by setting up a separate hedgehog picture server and linking the images there to the service.

