# -*- coding: utf-8 -*-

# Jieba and BeatuifulSoup 4 should be installed before running the script.
import sys
import urllib2
import random
import jieba
import jieba.analyse
from bs4 import BeautifulSoup

# The script only reads input Chinese term list in UTF-8 to avoid encoding issues.
reload(sys)
sys.setdefaultencoding('utf-8')

# User agnets are used for preventing being banned by search engine.
user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
        (KHTML, like Gecko) Element Browser 5.0',
        'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
        'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
        Version/6.0 Mobile/10A5355d Safari/8536.25',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']


# Search a term against Google. Change the base URL below to use other search engines.
def search(query):
    query = urllib2.quote(query)
    # url = 'http://www.baidu.com/s?wd=%s' % query # To search from Baidu
    url = 'https://www.google.com/search?hl=zh-cn&q=%s' % query
    request = urllib2.Request(url)
    index = random.randint(0, 9)
    user_agent = user_agents[index]
    request.add_header('User-agent', user_agent)
    
    html = ''
    while not html:
        try:
            print("Connecting...")
            response = urllib2.urlopen(request)
            print("Result retrieved...")
        except httplib.BadStatusLine:
            response = ''
        if response:
            html = response.read()
    return html
    
# Read a file of list of terms and their classifications, one term per line. Each line consistes of "Classification \t Term"
infile = open("drugList.txt")
lines = infile.readlines()
infile.close()

allWordList = ['drug-name', 'drug-type']    # To store all the possible features
drugDictList = []    # To store feature words of each drug in a list

jieba.set_dictionary('dict.txt.big')	# Read a better dictionary for text segmentation

i = 1
for line in lines:
    print "\nSearching for Entity:\t%s" % i
    i += 1
    fieldList = line.split("\t")
    queryStr = fieldList[1].strip()
    drugType = fieldList[0].strip()

    html = search('%s' % queryStr)
    soup = BeautifulSoup(html)    # Build a html object easy to parse
    
    drugDict = {'drug-name': queryStr, 'drug-type': drugType}    # Every drug has these two features
    # for content in soup.find_all("div", "c-abstract"): # Parse Baidu page
    for content in soup.find_all("span", "st"):    # Digest for each search result from google
        seg_list = jieba.cut(content.get_text().strip(),cut_all=True)    # Full cut for more features
        #seg_list = jieba.cut_for_search(content.get_text().strip())	# Srarch Engine Mode if want to use
        seg_list = map(lambda item: item.strip(), seg_list)
        seg_list = filter(lambda item: item, seg_list)
        
        for seg in seg_list:    # Put all features found for a particular drug
            if seg not in drugDict.keys():
                drugDict[seg] = 1
            else:
                drugDict[seg] += 1
            
            if seg not in allWordList:    # Put all features found for the drug into all feature list
                allWordList.append(seg)

    drugDictList.append(drugDict) 

# Now output the matrix
outfile = open("drugFeature.txt", "w")

for word in allWordList:
    outfile.write("%s\t" % word)
outfile.write("\n")

for drugDict in drugDictList:
    for word in allWordList:
        if word not in drugDict.keys():
            outfile.write("0\t")
        else:
            outfile.write("%s\t" % drugDict[word])
    outfile.write("\n")