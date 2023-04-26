## Requirements
Step 1. ensure you already have Python3 installed.  
Step 2. Install Django:  
```
python3 -m pip install --upgrade pip  
python3 -m pip install django
```
Step 3. Get `config.ini` file from author, put it under the root directory.  

Or you can register for your own API key and write it into 'config.ini'. At the same time, you need a django secrete. 

## Local Deployment
Step 1. run the following commands:
```
python3 manage.py migrate
python3 manage.py runserver
```
Step 2. In your browser, visit: http://localhost:8000/

## APIs
One Call API 3.0: https://openweathermap.org/api/one-call-3  
Geocoding API: https://openweathermap.org/api/geocoding-api

## UI
![start page](imgs/start_page.JPG)

![search page](imgs/search_page.JPG)