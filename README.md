# MakeUC2021
This project brought to you by The Meme Men.

## Inspiration
This project was inspired by a dataset we discovered created by the Global Terror Database.
The dataset can be found [here](https://www.kaggle.com/START-UMD/gtd).
## What it does
This project allows the user to view all terror events that take place between a pair of specified dates on an interactive map of the world.
Each act of terrorism will be displayed as a dot on the map, colored according to if any casualties were reported from the attack.
Each dot can be selected and viewed, and additional information about that terror act displayed. This information includes the number of killed, wounded, monetary damage, whether a ransom was demanded, and a brief summary of the attack.
The user is able to select a range of dates to display terror acts from. By default, this is from 1970 to 2017, but the user is able to select these dates as they wish.
Each terrorism act is assigned to one of 13 regions in the world. At the bottom, a graph of monetary damage by region for the selected is displayed on the screen, as well as reported casualties. These graphs are automatically updated when the user changes their selected date range.
## How we built it
The fundamentals of this app are the Dash webpage, as well as the Postgres database. 
The dash web page renders all of the components, then sends the information over to the user. It allows for a "low code" style solution to developing the data visualization on the front end.
The data prepropocessing was handled using Alembic (for automatic database migrations), and SQL Alchemy as an ORM. A series of scripts were used to break up the csv file into a variety of data tables. These tables were created with the philosophy of using Postgres as a data warehouse.
## Challenges we ran into
- As with any hackathon, sleep was a challenge.
- As any good web developer would say: CSS stands for Completely Stupid Styling
- We ran into some issues with getting all of the data collected to be utilized and displayed on the page, as we ran out of time for adding more fields.

## Accomplishments that we're proud of
For some of us, this is our first time working on a data visualization, especially of this scale, so merit of having a data visualization capable of displaying over 150,000 data points on a web page is a major accomplishment.
We're also particularly proud of the dynamic nature of this data visualization, as a user can move through the world and easily see information about any of the terror act listed.
## What we learned
We learned a great deal about dash in the course of this project, as well as about bootstrap, which was used for the styling. 
We also learned a lot about data processing and how to best store that data in a database.
## What's next for Terrorism Tracker
We want to add more filters to the data, such as listings for different types of attacks using different types of weapons or different target types. Dash allows for easy filtering based on these, and we have the information stored in our database as a part of our data model, but we simply did not have time to implement more of these filters.