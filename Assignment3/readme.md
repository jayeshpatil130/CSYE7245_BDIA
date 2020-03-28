## Data pipeline to train and benchmark multiple Synthetic data generators and then deploy them in production

## Report
https://codelabs-preview.appspot.com/?file_id=1YfTvWj234H7i01qs1_KezlwoYNQkogpDJkHWnCldXmM#0

# Prerequisites
Things you need to install:

Python3.5+\
Celery\
Streamlit \
Docker\
Postman\
Flask

## Setup For Running this Project:
### Step 1:

Clone this repo and setup celery http://docs.celeryproject.org/en/latest/index.html <br>
Run this using command: celery -A proj worker -l info and run the tasks.

### Step 2:

Build an API service using Flask (app) and create a docker image that will take an input json

### Step 3:

You can unit test this using streamlit https://docs.streamlit.io/ . We have a file called streamlit which takes and input and run the command streamlit run filename.py


## Collaborators
<b>[Sharvari Karnik](https://www.linkedin.com/in/sharvarikarnik25/)</b> 

<b>[Kunal Jaiswal](https://www.linkedin.com/in/kunaljaiswal4393/)</b> 

<b>[Jayesh Patil](https://www.linkedin.com/in/jayeshpatil130/)</b> 
