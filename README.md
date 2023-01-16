[![Dependencies][dependency-shield]][dependency-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

# Python App API example (Django)

Using SQLite as DB, backend based on  View-sets approach. 
JWT-token for authorization.
DRF for permissions setup
Based on API description (http://127.0.0.1:8000/redoc/)

Backend performs next modules:
* Post: can create new posts with images and text or edit/delete existing ones
* Group: can set post to specific group and render all posts from exact group
* Follow: can follow or unfollow author
* Comment: Can add comments on post and see all added posts


### Built With

* [![Python][Python.io]][Python-url]
* [![Django][Django.io]][Django-url]
* [![SqlLite][SqlLite.io]][SqlLite-url]


## Pre-installations

#### Clone the repo:

```sh
git clone https://github.com/Lesash13/api_python_app.git
```

#### Start and activate virtual environment:

```sh
python3 -m venv env
```

```sh
source env/bin/activate
```

#### Setup dependencies from requirements.txt file:

```sh
python3 -m pip install --upgrade pip
```

```sh
pip install -r requirements.txt
```

## Usage

#### Do migrations:

```sh
python3 manage.py migrate
```

#### Create superuser:

```sh
python3 manage.py createsuperuser
```

#### Run project:

Navigate to http://localhost:8000/


```sh
cd yatube_api
python3 manage.py runserver
```


## API example requests:

API documentation:
```
http://127.0.0.1:8000/redoc/
```

Get JWT-token request: 
```
http://127.0.0.1:8000/api/v1/jwt/create
```

Get post's request:

```
http://127.0.0.1:8000/api/v1/posts/
```

Get post's comments request: 

```
http://127.0.0.1:8000/api/v1/posts/1/comments/
```


<!-- MARKDOWN LINKS & IMAGES -->

[dependency-shield]: https://img.shields.io/badge/Dependency_Graph-darkgreen?style=for-the-badge

[dependency-url]: https://github.com/Lesash13/api_python_app/network/dependencies

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=darkblue

[linkedin-url]: https://www.linkedin.com/in/victoriya-mitrofanova-96839278/

[Python.io]: https://img.shields.io/badge/-Python-yellow?style=for-the-badge&logo=python

[Python-url]: https://www.python.org/

[Django.io]: https://img.shields.io/badge/-Django-darkgreen?style=for-the-badge&logo=django

[Django-url]: https://www.djangoproject.com/

[SqlLite.io]: https://img.shields.io/badge/-SQLite-blue?style=for-the-badge&logo=sqlite

[SqlLite-url]: https://www.sqlite.org/index.html