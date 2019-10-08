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
        print(bibtex+'\n')


#http://dl.acm.org/exportformats.cfm?id=544220&expformat=bibtex
def acm_bibtex(parent_id,id):
    s = requests.Session()
    r = s.get('http://dl.acm.org/downformats.cfm?id='+id+'&parent_id='+parent_id+'&expformat=bibtex')
    print(r.text)
    bibtex = re.sub(r' url = {.*},\n','',r.text)
    bibtex = re.sub(r' keywords={(.*)},','',bibtex)
    bibtex = re.sub(r' title = {(.*)}',r' title = {{\1}}',bibtex)
    print(bibtex+'\n')




def ieee_search(word):
    s = requests.Session()
    r = s.post('https://ieeexplore.ieee.org/rest/search', data =  '{"newsearch":true,"queryText":"%s","highlight":true,"returnFacets":["ALL"],"returnType":"SEARCH"}' % (word),
            headers = {
                "Accept":"application/json, text/plain, */*",
                "Content-Type":"application/json",
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
                "Origin": "https://ieeexplore.ieee.org"
            })

    print(r.text)
    results = json.loads(r.text)

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
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36 OPR/39.0.2256.48'}
    s = requests.Session()
    r =  s.get("http://dl.acm.org/exportformats_search.cfm?query="+ word+"&filtered=&within=owners%2Eowner%3DGUIDE&dte=&bfr=&srt=%5Fscore&expformat=bibtex", stream = True,headers=headers)
    r.raise_for_status()

    bibtex = r.text

    bibtex = re.sub(r' url = {.*},[\r\n]+','',bibtex)
    bibtex = re.sub(r' keywords = {(.*)},[\r\n]+','',bibtex)
    bibtex = re.sub(r' title = {(.*)}',r' title = {{\1}}',bibtex)
    print(bibtex)
    #print repr(bibtex)


if __name__ == "__main__":
    word = sys.argv[1]
    #print word
    #ieee_search(word)
    acm_search(word)



