import pdfminer
from pdfminer.high_level import extract_text
import requests
from config import NAVER_API_ID,NAVER_API_SECRET,RAPID_API


from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

pdfname= '23_4_06_480-490(21-522).pdf'

def convert_pdf_to_txt(pdfname):
    #pdf리소스 매니저 객체 생성
    rsrcmgr = PDFResourceManager()
    #문자열 데이터를 파일처럼 처리하는 stringio -> pdf 파일 내용이 여기 담김
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(pdfname, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
 
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    #text에 결과가 담김
    text = retstr.getvalue()
 
    fp.close()
    device.close()
    retstr.close()
    return text
 

def summarize_and_translate(article, min_length=100, max_length=300):
    

    url = "https://tldrthis.p.rapidapi.com/v1/model/abstractive/summarize-text/"

    payload = {
    "text":article,
    "min_length": 100,
    "max_length": 300
    }
    headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": RAPID_API,
    "X-RapidAPI-Host": "tldrthis.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    summary = response.json()['summary'].strip()
    
    url = "https://openapi.naver.com/v1/papago/n2mt"

    payload = {
        "source": "en",
        "target": "ko",
        "text": summary,
    }

    headers = {
        "content-type": "application/json",
        "X-Naver-Client-Id": NAVER_API_ID,
        "X-Naver-Client-Secret": NAVER_API_SECRET
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    return response.json()['message']['result']['translatedText']

article = convert_pdf_to_txt(pdfname)
a = summarize_and_translate(article, 100, 200)
