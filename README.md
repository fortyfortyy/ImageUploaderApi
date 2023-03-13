# Image Uploader API
<div id="top"></div>

> Live Project Link: https://dev-imageuploadapi.up.railway.app/api/v1/accounts/register/

This is based on the **Django Rest Framework** application that implements the all necessary logic to work with **GSC** (**Google Cloud Storage**), **Redis**, **Celery** and **PostgreSQL**.
It does provide ONLY Django Rest Framework UI, so please follow the docs to see available URLS. 
I hope you not gonna spam my bucket :)

## Table of contents
* [Technologies Used](#technologies-used)
* [Features implemented](#features-implemented)
* [Available Urls](#available-urls)
* [How To Set Up Locally](#how-to-set-up-locally)

## Technologies Used
* Python 3.10
* Django 4.1.7
* Redis 
* Celery
* Django REST 3.14
* Google Cloud Storage 2.7.0
* PostgreSQL 2.9.5
* Docker-compose
* Django-Alluth

## Features Implemented
- users can upload images via HTTP request
- users can list their uploaded images
- three builtin `account tiers Basic, Premium and Enterprise`
  - users that have a `"Basic"` plan after uploading an image get: 
    - a link to a thumbnail that's 200px in height
  - users that have a `"Premium"` plan get:
    - a link to a thumbnail that's 200px in height
  - a link to a thumbnail that's 400px in height
    - a link to the originally uploaded image
  - users that have a `"Enterprise"` plan get
    - a link to a thumbnail that's 200px in height
    - a link to a thumbnail that's 400px in height
    - a link to the originally uploaded image
    - the ability to fetch a link to the (binary) image that **expires** after several seconds (user can specify any number between 300 and 30000) and download it
- apart from the builtin tiers, admins can create arbitrary tiers with the following things configurable:
  - `arbitrary thumbnail sizes`
  - `presence of the link to the originally uploaded file`
  - `ability to generate expiring links`
- admin UI has been done via django-admin
- tests validation of the image and account tiers
- `performance considerations`(implemented basic cache for _**15 seconds**_, distributed task queue to be able to process a lot of images)

<p align="right">(<a href="#top">back to top</a>)</p>

## Available Urls
PUBLIC URLS
- https://dev-imageuploadapi.up.railway.app/api/v1/accounts/register/
- https://dev-imageuploadapi.up.railway.app/api/v1/accounts/login/

ADMIN URLS
- https://dev-imageuploadapi.up.railway.app/admin/

AUTHENTICATED USERS
- https://dev-imageuploadapi.up.railway.app/api/v1/images/
- https://dev-imageuploadapi.up.railway.app/api/v1/images/upload/
- https://dev-imageuploadapi.up.railway.app/api/v1/images/expiring-links/ (only Premium+ Account Tier)

ADVANCED API DOCS 
- https://dev-imageuploadapi.up.railway.app/api/swagger/
- https://dev-imageuploadapi.up.railway.app/api/redoc/

<p align="right">(<a href="#top">back to top</a>)</p>

## How To Set Up Locally
> First of all, you need to:
> - Create a **bucket in GCS <a href="https://console.cloud.google.com/storage/create-bucket">link </a>**, with the name of your desire. 
> - Create **IAM Policy <a href="https://console.cloud.google.com/iam-admin/serviceaccounts"> link </a>**, GENERATE A KEY and download *.json file with the credentials. 
> - PUT YOUR CREDENTIALS TO THE SOURCE OF THIS PROJECT AND CHANGE THE NAME TO "private-credentials.json"


The easiest approach is to run docker-compose. It should work without any problems.
The docker-compose approach is based on google cloud storage. If you have the desire to save locally 
the images and thumbnails please, visit <a href="https://github.com/fortyfortyy/ImageUploadApi/pull/6"> this PR </a> and see the changes.

- clone the repo 
- go to the project folder
- run `docker-compose up -d --build`
- create a test super account with `docker-compose exec backend python manage.py create_test_superuser`
- visit (try both URLs in case the error occurred) `localhost:8000/admin/` or `127.0.0.1:8000/admin/` and paste the generated credentials

<br />

If you have any questions, let me know at `d.pacek1@gmail.com`
<p align="right">(<a href="#top">back to top</a>)</p>
