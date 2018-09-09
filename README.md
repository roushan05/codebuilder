A Django app to automatically process your pull requests.
Uses Ngrok to interact with your local port.
If any syntax issues are found in the PR, the app automatically declines the PR.
Otherwise it merges the PR and creates a tag on it
The whole series of events are logged in the Events.txt file.

Reqirements:
->>Django
->>Ngrok
->>Requests
->>Urllib2

Steps :
->> Kindly download the codebuilder app from the github repository.
->> Install the requirements as stated in this file.
->> Install Ngrok.
->> Create a webhook from your bitbucket repository.
->> Enter the url supplied from Ngrok.
->> Start the django server by entering the command below. 
python manage.py runserver
->> Visit localhost:8000 or the url supplied by Ngrok.
->> Please enter your bitbucket account username and password and the path to your local repository on your computer. 
->> Create a PR for the your repository. 
