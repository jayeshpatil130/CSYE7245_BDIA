# -*- coding: utf-8 -*-

def upload_to_aws(local_file, bucket, s3_file):
    import boto3
    from botocore.exceptions import NoCredentialsError
    ACCESS_KEY = 'your access key here'
    SECRET_KEY = 'secret key'
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
def Scrape():
    from bs4 import BeautifulSoup as BS
    import requests
    import re
    import json
    import nltk
    nltk.download('all')
    import boto3
    from botocore.exceptions import NoCredentialsError
    import pandas as pd
    import io
    ACCESS_KEY = ''
    SECRET_KEY = ''
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    obj = s3.get_object(Bucket= 'team2bdia', Key= 'input.csv')
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    #df = pd.read_csv(r'C:\Users\Sharvari Karnik\Desktop\Courses\Spring 2020\BDIA\Assignment2\input.csv')
    link_list = df['Link'].tolist()
    cookie = 'machine_cookie=9062154383403; _gcl_au=1.1.924130171.1582252008; _ga=GA1.2.1384740589.1582252008; _gid=GA1.2.249310695.1582252008; _pxvid=9ccd129b-5451-11ea-8898-0242ac12000c; ga_clientid=1384740589.1582252008; __qca=P0-1246656394-1582252007547; _fbp=fb.1.1582252008277.574065899; __adroll_fpc=251061c4aa0b4fd9d3c5ea7f89ea18d2-1582252008347; __pnahc=0; __tbc=%7Bjzx%7DlCp-P5kTOqotpgFeypItnPkAkhPKLTSq3_bwgv0wceUL0n8kchskkYMGU-o--ONCScGMG-JRrQt-S6FtZiPB7DzEFzAJI3ZiG1o6dNyXVAOEkZ_2_PShGiyrDnMfatfMUVgFAp6l8Mpn6PJS7yCpyA; __pat=-18000000; h_px=1; __gads=ID=dcf1307782c8aa7d:T=1582324512:S=ALNI_MbJpAUy-Q-LbcY4vJbkNYiIhO6O0A; __aaxsc=2; _igt=0d7d8a0e-295a-4aed-8ede-ae356283253a; user_id=51308290; user_nick=; user_devices=; u_voc=; marketplace_author_slugs=; user_cookie_key=0; has_paid_subscription=false; user_perm=; sapu=101; user_remember_token=edd61bc13f86ff518cbc045d1e52d98084d39c5d; url_source_before_register=https%3A%2F%2Fseekingalpha.com%2Farticle%2F4326424-anglogold-ashantis-au-ceo-kelvin-dushnisky-on-q4-2019-results-earnings-call-transcript; _gat_UA-142576245-4=1; _dc_gtm_UA-142576245-1=1; _pxff_tm=1; _pxff_wa=1; gk_user_access=1**1582417614; gk_user_access_sign=92f9ed29e45eea251819d5f3af828af6fac6af1e; _ig=c660f960-ee32-4c76-873d-5e5d0c17401b; __pvi=%7B%22id%22%3A%22v-2020-02-22-19-26-40-010-2ikV3vBhW0gpvbRo-cdb33e367f67c6e8080cae89c514452e%22%2C%22domain%22%3A%22.seekingalpha.com%22%2C%22time%22%3A1582417613607%7D; __adblocker=false; xbc=%7Bjzx%7Dh0iw7KKTbT6jbZkUCrkkW0-zDOwbGdXoRJTpVBdWJ6f8Bii4Gjd6ytM3WnwVcZrLf2uDBULSM1I9AmPWVo6wlxA2GoMSF5Cq4WokXLHgAvmnfvx4e0WnIbGDKPbV-dfUer2-17mC71H-Eab-BdwULhY3tZRFetdJWwPhkQr-DnU6GKTXVpvVJghKbFYZP1nA5CvWLyiQHn1ccMVQUADCyGklZJekhtNw3ZilovgtGSR1Zyr9e7MvmxD7gVl_9QH4l1AQnBtaIsV86Pb8joawYOpqhR_TrWwCgmay4NZmVBfbYX8hqRbIAHBD2HkFWRQwsYsdPKVgZs6waN0pV392Pr67SaKWeOW_Lfffr7fjZXO3pqhqKh1MIw4FVmECLowbZfuFuE1XvlbZiZKyXr9JLbJPGSDNFjkm41VTCFxL2cMBgVkrPLABdKQtSzvggTVBkl0YSGKhIURFGddA3Ii4zUl0psc3x6O7rU5U0dMALbwfBm5rzX5WxWAAoZbMm5P_g66CVckGJEOHLvKq9Hde9j6nWtjNxWMln-LZNHL-pxR0ViXdFw4L6bDWnctCXoPXlF5BfQeIJ0MXPJ_1Ue9ew9Tw86_st8Z8KhoUjTkpbDM3baQEgOGddKUhXk8DdheSMbcQy316flME7YL2lxPoiW0biYybnXmr4UKLxCRPcxPxZozRYQ420hS9O4mUxeNhvMJz2RNHsGfhGt_vTVJlzQ; __ar_v4=ULCHBRH4ZZGFXDWGQTC6RG%3A20200222%3A44%7CRFXAEISDJFDZDINVACZG6X%3A20200222%3A177%7CHWYEUMZG3RCB3IJESAMRSO%3A20200222%3A177%7CF6X65CJ4K5E43AFRH5CGQD%3A20200222%3A131%7CDZPINTYKVVC37LE5MJWGEE%3A20200223%3A1%7C2EEQPRZIBZB7VIPPEX2IGK%3A20200223%3A1; _px2=eyJ1IjoiMzBkNzU0MjAtNTVkMy0xMWVhLTlmNTktMjdmOTZhMDJiN2VkIiwidiI6IjljY2QxMjliLTU0NTEtMTFlYS04ODk4LTAyNDJhYzEyMDAwYyIsInQiOjE1ODI0MTgxMjAwNDgsImgiOiI2MzAzOTAwMTc5MzAyMWJjM2MyMWM4NGYxYjYxOGQ5YzQ0NWM2NjcxOGE3NDQzYTYzM2RkZTcwYTY0ZjUwZDUzIn0=; _px=xSET+4bMfbwf+Wbd47dPmBctqM4aGmN6A1XoaeOaCUIPZFvtNtzCf/TFNJFWORDGVR+mc5+Q6uhW6AFnMig/1Q==:1000:UeMsJWyu1UMOgsI6sr+VqUH6XCzI+d2fUkwd7JnpdXMA+ax6gg9Gr2DG0Ot2DaK3D/3HTrlesymw2Hd0QoAkY/efhDkPy0/JepBBUM295ot6QVdYSzrv3fAhk4nGQg9wwvP6jMOdz35fBeGmWhsyd77d//cg2BMmj567aqqtRI7PMVcshX63fnLNtmJMfPrwsvGWs6L18/yFcuCM4s9osI2xKBt6JSFfghXYheVlSocWAmnwanIiN2h6/wCzXT30PMpiL8M6tP+NGum71LYQxA==; _pxde=5c727d115b6cb0e54b79d36455fe050f8f7882ed5c83a5e331ace42c8aaa6385:eyJ0aW1lc3RhbXAiOjE1ODI0MTc2NDQxNjksImZfa2IiOjB9; mnet_session_depth=4%7C1582417599647'
    for item in link_list:
        url = item
        agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                "cookie" : cookie}
        page = requests.get(url, headers=agent)
        soup = BS(page.content, 'lxml')
           #print(soup.prettify())
        first_list = []
        remove_from_list = []
        #clear_list = []
        for test1 in soup.find_all('p'):
            op = test1.text
            #print(op)
            #print(".....")
            first_list.append(op)
        for item in first_list:
            if item != 'Operator':
                remove_from_list.append(item)
            else:
                break
        remove_from_list.append('Operator')
        #for item in remove_from_list:
            #clear_list.append(item[:item.find(" – ")])
        final_list = [i for i in first_list if i not in remove_from_list]
        my_json_string = json.dumps(final_list)
        my_json_string.replace('[Operator Instructions]','')
        my_json_string2 = re.sub('[^a-zA-Z.]', ' ', my_json_string)
        sent_text = nltk.sent_tokenize(my_json_string2)
#print(my_json_string)
#         with open('scrape.txt', 'a') as outfile:
#             json.dump(sent_text, outfile)
#         upload_to_aws('scrape.txt', 'team2bdia', 'scrape_edgar_final.txt')
    return sent_text

def IBMSentimentAnalysis():
    import json
    from ibm_watson import NaturalLanguageUnderstandingV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ibm_watson.natural_language_understanding_v1 import Features, SyntaxOptions,SyntaxOptionsTokens,SentimentOptions
    import boto3
    from botocore.exceptions import NoCredentialsError
    import pandas as pd
    import io
    import re
    import csv
    authenticator = IAMAuthenticator('')
    ACCESS_KEY = ''
    SECRET_KEY = ''
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    obj = s3.get_object(Bucket= 'team2bdia', Key= 'scrape_edgar_final.txt')
    body = obj['Body'].read().decode('utf-8')
    body1 = re.sub('[^a-zA-Z.]', ' ', body)
    body_list = list(body1.split("."))
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2019-07-12',
        authenticator=authenticator
    )
    f = csv.writer(open("text.csv", "a+"))
    f.writerow(["text","score","label"])
    for item in sent_text:
        try:
            response = natural_language_understanding.analyze(
            text = item,
            features=Features(sentiment=SentimentOptions(targets=[item])),
            language = "en").get_result()
            x = json.dumps(response)
            x_load = json.loads(x)
            f.writerow([x_load["sentiment"]["targets"][0]["text"],
                        x_load["sentiment"]["targets"][0]["score"],
                        x_load["sentiment"]["targets"][0]["label"]])
        except:
            pass
    upload_to_aws('text.csv', 'team2bdia', 'text_final.csv')
    return x_load

sent_text = Scrape()
#IBMSentimentAnalysis()