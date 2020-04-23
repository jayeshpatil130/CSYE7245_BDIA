## Project
### Stock Prediction using Financial News Sentiment Analysis and Time Series Analysis

## Project Proposal:
https://codelabs-preview.appspot.com/?file_id=1TyFR1jlvE59nKuilDi-f81CGV9NqJZscQYVdNB1wxhE#0

## Project Structure
```
Project
├── README.md
├── Config file
├── Company Keywords
│   └── keywords to categorize the articles
├── Data: Scripts to scrape the data and api to get stock data
│   └── StockAPI_Alphavantage.py
│   └── WSJScrapper_Headline.py
│   └── WSJScrapper_Content.py
├── Dockerfile: instruction for docker image construction.
├── requirements.txt: dependencies.
```



## Getting Started

#### Prerequisites
1. Python3.5+
2. Docker
3. Flask
4. AWS


#### Configuring the AWS CLI
You need to retrieve AWS credentials that allow your AWS CLI to access AWS resources.

1. Sign into the AWS console. This simply requires that you sign in with the email and password you used to create your account. If you already have an AWS account, be sure to log in as the root user.
2. Choose your account name in the navigation bar at the top right, and then choose My Security Credentials.
3. Expand the Access keys (access key ID and secret access key) section.
4. Press Create New Access Key.
5. Press Download Key File to download a CSV file that contains your new AccessKeyId and SecretKey. Keep this file somewhere where you can find it easily
6. Get AWS Key and create a config file
7. Go to https://www.alphavantage.co and get API key to retrive the stock data and paste it in a config file.





## Authors
<b>[Sharvari Karnik](https://www.linkedin.com/in/sharvarikarnik25/)</b> 

<b>[Kunal Jaiswal](https://www.linkedin.com/in/kunaljaiswal4393/)</b> 

<b>[Jayesh Patil](https://www.linkedin.com/in/jayeshpatil130/)</b> 

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
