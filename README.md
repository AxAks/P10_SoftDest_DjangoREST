# P10_SoftDesk_DjangoREST
Study project for Django REST API Framework

#(A RÉDIGER !!!)

## Chapters

1. [Presentation](#presentation)
2. [Prerequisites (for developers)](#prerequisites)
3. [Installation](#installation)
4. [Execution](#execution)
5. [Usage](#usage)
***

## 1. Presentation <a name="presentation"></a>
This Project is a Django REST API providing a per-project ticketing system.
It can be accessed via requests.
***

## 2. Prerequisites (for developers) <a name="prerequisites"></a>
This program runs under python 3.9 in a virtual environment.  
Thus, it is usable on Windows, Unix-based operating systems
insofar as the followings are installed:
- python 3.9 (including pip3)
- virtualenv

__Linux__  
_installation of python3.9:_    
$ sudo add-apt-repository ppa:deadsnakes/ppa    
$ sudo apt update     
$ sudo apt install python3.9    
_installation of pip3:_     
$ wget https://bootstrap.pypa.io/get-pip.py     
$ python3.9 get-pip.py    
$ pip --version    
_Installation of virtualenv :_      
$ sudo apt install virtualenv    

__Mac__  
_installation of python3.9 and pip3:_  
$ brew install python@3.9    
(pip3 comes along with it) 
if not, download and install the file get-pip.py from https://bootstrap.pypa.io/get-pip.py    
$ py get-pip.py       
_Installation of virtualenv :_    
$ pip3 install virtualenv
  
__Windows__     
_installation of python3.9 and pip3:_  
Download and install python 3.9 for windows from python.org    
(pip3 comes along with it)     
if not, download and install the file get-pip.py from https://bootstrap.pypa.io/get-pip.py    
$ py get-pip.py     
_Installation of virtualenv :_   
$ pip install virtualenv    
***

## 3. Installation <a name="installation"></a>

__Download the project:__    
_Via Git_      
$ git clone https://github.com/AxAks/P10_SoftDest_DjangoREST.git   
    
_Via the Web_     
- Visit the page : https://github.com/AxAks/P10_SoftDest_DjangoREST.git    
- Click on the button "Code"     
- Download the project     

__Linux / Mac__       
in the project directory in a shell:       
_create the virtual environment_       
$ python3.9 -m virtualenv 'venv_name'        
_activate the environment:_        
$ source 'venv_name'/bin/activate         
_install project requirements:_       
$ pip install -r requirements.txt         
  
__Windows__    
in the project directory in a shell:        
_create the virtual environment_      
$ virtualenv 'venv_name'      
_activate the environment:_     
$ C:\Users\'Username'\'venv_name'\Scripts\activate.bat       
_install project requirements:_            
$ pip install -r requirements.txt
***

## 4. Execution <a name="execution"></a>
from the terminal, in the root directory of the project:

_activate the environment:_    
$ source 'venv_name'/bin/activate        
_launch the Django server_       
$ python SoftDesk/manage.py runserver    
-> The Server is ready  
***

## 5. Usage <a name="usage"></a>

Definition of Endpoints:

Users:
- user registration (POST)
URL -> /signup/ 
- login (POST)
URL -> /login/
- user listing (GET)
URL -> /users/

Projects:
- create project (POST)
URL -> /projects/
- list projects (GET)
URL -> /projects/
- find project (GET)
URL -> /projects/{id_project}
- edit project (PUT)
URL -> /projects/{id_project}
- delete project (DELETE)
URL -> /projects/{id_project}

Contributors:
- add contributor (POST)
URL -> /projects/{id_project}/users/
- list project contributors (GET)
URL -> /projects/{id_project}/users/
- find contributor (GET)
URL -> /projects/{id_project}/users/{id_user}
- edit contributor (PUT)
URL -> /projects/{id_project}/users/{id_user}
- remove contributor (DELETE)
URL -> /projects/{id_project}/users/{id_user}

Issues:
- create issue (POST)
URL -> /projects/{id_project}/issues/
- list project issues (GET)
URL -> /projects/{id_project}/issues/
- find issue (GET)
URL -> /projects/{id_project}/issues/{id_issue}
- edit issue (PUT)
URL -> /projects/{id_project}/issues/{id_issue}
- delete issue (DELETE)
URL -> /projects/{id_project}/issues/{id_issue}

Comments:
- create comment (POST)
URL -> /projects/{id_project}/issues/{id_issue}/comments/
- list issue comments (GET)
URL -> /projects/{id_project}/issues/{id_issue}/comments/
- find comment (GET)
URL -> /projects/{id_project}/issues/{id_issue}/comments/{id_comment}
- edit comment (PUT)
URL -> /projects/{id_project}/issues/{id_issue}/comments/{id_comment}
- delete comment (DELETE)
URL -> /projects/{id_project}/issues/{id_issue}/comments/{id_comment}
***
