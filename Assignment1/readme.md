# Assignment 1
## Developed a data pipeline to accomplish a scraping task and the goal was to ingest, process and store it into google buckets.


### Report
https://codelabs-preview.appspot.com/?file_id=1WNt8YYhNIGRSNJVnYj8dVWI6AlLNzXr-WEkgTjDtDdM#0

### Required Installation-
Run the requirements.txt file using pip install

### Steps to run this project
1. Using GCP shell run the requirements.txt on shell and it will install all the required dependenices 
2. run the .py file using command:
python Assignment1-Final.py --project assignment1bdia --runner DataflowRunner--temp_location gs://assignment1csye7245/temp/

Here, we need to specify the runner from apache beam supporeted runners and temp location to store temp log files.
