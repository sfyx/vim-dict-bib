import requests
import json
import re
import sys

def ieee_bibtex(id):
    s = requests.Session()
    payload = {'recordIds': id, 'citations-format': 'citation-only', 'download-format':'download-bibtex', 'x':'74','y':'7'}
    r = s.post("http://ieeexplore.ieee.org/xpl/downloadCitations", data=payload, allow_redirects=False)

    if r.status_code in (301, 302, 303, 307):
        r = s.post(r.headers['location'], data=payload, allow_redirects=False)
        bibtex = re.sub(r'<br>\s*','',r.text)
        bibtex = re.sub(r'\ntitle={(.*)}',r'\ntitle={{\1}}',bibtex)
        bibtex = re.sub(r'\nkeywords={(.*)},','',bibtex)
        print bibtex, '\n'


#http://dl.acm.org/exportformats.cfm?id=544220&expformat=bibtex
def acm_bibtex(parent_id,id):
    s = requests.Session()
    r = s.get('http://dl.acm.org/downformats.cfm?id='+id+'&parent_id='+parent_id+'&expformat=bibtex')
    print r.text
    bibtex = re.sub(r' url = {.*},\n','',r.text)
    bibtex = re.sub(r' keywords={(.*)},','',bibtex)
    bibtex = re.sub(r' title = {(.*)}',r' title = {{\1}}',bibtex)
    print bibtex, '\n'



#<a href="/xpl/articleDetails.jsp?tp=&amp;arnumber=7037801&amp;queryText%3Dcloud">

def ieee_search(word):
    s = requests.Session()
    r = s.post('http://ieeexplore.ieee.org/rest/search?reload=true', data=json.dumps({"queryText": word, "refinements": [], "searchWithin": [], "newsearch": "true"}),
            headers = {"Content-Type":"application/json", "Accept":"application/json, text/plain, */*","Content-Type":"application/json;charset=UTF-8","User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"})


    results = json.loads( r.text)

    count = 0
    if "records" in results:
        for articleNumber in results["records"]:
            ieee_bibtex(articleNumber["articleNumber"])
            count = count + 1
            if count > 2:
                break


    #ieee_bibtex(results["records"][1]["articleNumber"])
    #ieee_bibtex(results["records"][2]["articleNumber"])
    #ieee_bibtex(arnumber)

def acm_search(word):
    s = requests.Session()
    count = 0
    r =  s.get("http://dl.acm.org/exportformats_search.cfm?query="+ word+"&filtered=&within=owners%2Eowner%3DGUIDE&dte=&bfr=&srt=%5Fscore&expformat=bibtex", stream = True)
    r.raise_for_status()

    your_maximum = 2048
    size = 0
    count = 0
    bibtex = ''
    for chunk in r.iter_content(1024):
        size += len(chunk)
        bibtex = bibtex + chunk
        count = count + chunk.count("\n@")
        if count >=3:
            break
        if size > your_maximum:
            break

    bibtex = re.sub(r' url = {.*},[\r\n]+','',bibtex)
    bibtex = re.sub(r' keywords = {(.*)},[\r\n]+','',bibtex)
    bibtex = re.sub(r' title = {(.*)}',r' title = {{\1}}',bibtex)
    print bibtex
    #print repr(bibtex)


if __name__ == "__main__":
    word = sys.argv[1]
    #print word
    ieee_search(word)
    acm_search(word)
