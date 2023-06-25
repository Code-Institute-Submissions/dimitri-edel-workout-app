# workout-app
## Introduction
 If you work out, it is always good practice to keep a journal, so you can **keep track of your results** over
a given period of time. Many people will have a note pad, where they put everything down. But if you go to the gym and forget the note pad, then it might be difficult to memorize everything, so you can put it down in your workout journal. But for using this workout journal all you need is your smart phone with an internet connection, which you take everywhere with you anyway.
## Issues
Due to some misunderstandings along the way, less than three weeks before submission date, I learned that I had to use django and not Flask for this projects. Only because of how well documented and well organized django is, could I learn and develop at the same time. 
The actual problem, though, came up three days before submission, as I was already beginning to work on this README.MD file. Which, in turn, took away a huge chunk of the time that was planned on providing a good documentation. What happened was that I learned from my mentor, that the django adminstraion sites, do not count as the real admin sites. Thus, I have to implement my own admin interface. So, I whipped up an interface, that I would not put out in the real world. This interface merely serves as a means to show the assesment team, that if I had planned that in, it would not have been an issue.
## First design
### Wireframe
This was the initial thought. Yet, in the process I realized that I missed out a couple of views.
![First draft wireframe](static/img/first_design_wireframe.png)
### ERD
As mentioned before, I missed a few views in the intial wirefraem, which also means that the first ERD was missing one model class. However, this was the first draft.
![First draft ERD](static/img/first_erd.png)
## Final Design
### ERD
![Final draft ERD](static/img/erd-final.png)
## Use cases
## Testing
## Deployment
Before beginning with the project I had rented a Virtual Private Server at IONOS. The server comes with a plain Ubuntu operating system. Most Linux systems come with a pre-installed python interpreter and Ubuntu is one of them. 
1. Install an Apache2 Webserver and PostreSQL on the system. 
2. In order to run applications in their own python environment, it is mandatory to install virtual envireonment for python on the machine as well. 
3. Create a folder for the project.
4. Activate the virtual environment in that folder. 
5. With the virtual environment activated, pip3-install the required packages into the environment using the **requirements.txt**
6. Deactivate the virtual environment.
7. Copy the project files into that folder.
8. Create a configuaration file for the project folder in the Apache2 **conf-enabled** folder. The configuration file simply tells the webserver, which domain is to be acociated with the application, which will be used as the **ROOT_URL** by django. Secondly, it tells the server from where to load the application using the **wsgi.py** file, which is created by django as soon as you run <code>django-admin startproject</code> command. Thirdly, the configuration file tells the server which instance of python to use, so it is necessary to specify the path to the virtual environment folder of this project.
9. Create a Virtual Host for serving the static and media files.
10. Apply changes to **settings.py**, adding **ROOT_URL** and **STATIC_URL** as well as **STATIC_ROOT** .
11. Run the collect static command.

## Technologies
- Django
- Bootstrap
- Virtual Private Server
- PostgresSQL
- Visual Studio Code
- Python
- JavaScript
- HTML & CSS
## Credits
- Code Institute
- Django Documentation
- Bootstrap Documentation
- w3schools.com
- stackoverflow.com

