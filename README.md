# diminuendo - A simple URL shortener API
---

### URLs:
- /&lt;hash&gt;
    - url redirector based on short url
- /shrink/
    - url shortener
    - returns json of url and its shortened form
    - POST request data format 
    ```
    {"u":"<url_to_be_shortened>"}
    ```
- /s/
    - search url using title
    - returns list of matching page titles
    - POST request data format 
    ```
    {"q":"<title_to_be_searched>"}
    ```
- /meta/
    - returns list metadata links for shourturls
- /meta/&lt;hash&gt;
    - returns a json of metadata of the short url

#### Prerequisites

- python3
- virtualenv==13.1.2

#### Setup

1. cd to the root of the project folder in the terminal
2. run the command to create a virtualenv for the project: `$ virtualenv -p python3 venv`
3. run the command to switch to virtualenv:
` $ source venv/bin/activate `
4. install required libraries to the using pip as follows:
` $ pip install -r requirements.pip `
5. run command to start server:
`$ python app.py `
6. goto http://localhost:8888/ to access the API
    
    
