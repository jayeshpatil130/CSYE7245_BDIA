import scrapy
from scrapy.crawler import CrawlerProcess   # Programmatically execute scrapy
from urllib.parse import urlparse
from slugify import slugify
import re

# RANDOMIZE USER AGENTS ON EACH REQUEST:
import random
# SRC: https://developers.whatismybrowser.com/useragents/explore/
user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]
debug_mode = True

class QuotesSpider(scrapy.Spider):

    name = "quotes"
    custom_settings = {
            # 'LOG_LEVEL': 'CRITICAL', # 'DEBUG'
            'LOG_ENABLED': False,
            'DOWNLOAD_DELAY': 4 # 0.25 == 250 ms of delay, 1 == 1000ms of delay, etc.
    }

    def start_requests(self):
        # GET LAST INDEX PAGE NUMBER
        urls = [ 'https://seekingalpha.com/earnings/earnings-call-transcripts/9999' ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_last_page)

    def parse_last_page(self, response):
        import pandas as pd
        from io import StringIO

        import boto3
        from botocore.exceptions import NoCredentialsError
        ACCESS_KEY = ''
        SECRET_KEY = ''
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY)
        csv_obj = s3.get_object(Bucket= 'team2bdia', Key= 'input_part4.csv')
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')
        df_input = pd.read_csv(StringIO(csv_string))

        csv_obj = s3.get_object(Bucket= 'team2bdia', Key= 'cik_lookup.csv')
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')
        df_lookup = pd.read_csv(StringIO(csv_string))
        data = response.css("#paging > ul.list-inline > li:last-child a::text")
        for i,j in df_lookup.iterrows():
            for a,b in df_input.iterrows():
                if df_input["CIK"][0] == b["CIK"]:
                    x = (j["Ticker"])
                    url = "https://seekingalpha.com/symbol/%s/earnings/transcripts" % (x)
                    yield scrapy.Request(url=url, callback=self.parse)
#         last_page = data.extract()
#         last_page = int(last_page[0])
#         for x in range(0, last_page+1):
#             # DEBUGGING: CHECK ONLY FIRST ELEMENT
#             if debug_mode == True and x > 0:
#                 break
#             url = "https://seekingalpha.com/symbol/%s/earnings/transcripts" % (x)
            

    # SAVE CONTENTS TO AN HTML FILE 
    def save_contents(self, response):
        data = response.css("div#content-rail article #a-body")
        #data = response.css("p")
        data = data.extract()
        new_data = re.sub('<[^<]+?>', '', data)
        url = urlparse(response.url)
        url = url.path
        filename = "part4_scrape.txt"
        with open(filename, 'a') as f:
            f.write(new_data[0])
        #upload_to_aws(filename, 'team2bdia', 'part4_scrape.txt')
        

    def parse(self, response):
        print("Parsing results for: " + response.url)
        links = response.css("a[sasource='qp_analysis']")
        links.extract()
        for index, link in enumerate(links):
            url = link.xpath('@href').extract()
            print(url)
            # DEBUGGING MODE: Parse only first link
            if debug_mode == False and index > 0:
                break
            url = link.xpath('@href').extract()
            data = urlparse(response.url)
            data = data.scheme + "://" + data.netloc + url[0]  # .scheme, .path, .params, .query
            user_agent = random.choice(user_agent_list)
            print("======------======")
            print("Getting Page:")
            print("URL: " + data)
            print("USER AGENT: " + user_agent)
            print("======------======")
            request = scrapy.Request(data,callback=self.save_contents,headers={'User-Agent': user_agent})
            yield request
            
    def upload_to_aws(local_file, bucket, s3_file):
        import boto3
        from botocore.exceptions import NoCredentialsError
        ACCESS_KEY = ''
        SECRET_KEY = ''
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY)
        try:
            s3.upload_file(local_file, bucket, s3_file)
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',
})
c.crawl(QuotesSpider)
c.start()