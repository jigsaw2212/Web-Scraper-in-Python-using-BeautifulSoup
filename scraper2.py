import requests
import bs4
import re


root_url = 'http://pyvideo.org'
index_url = root_url + '/category/50/pycon-us-2014'
links=[]
links_clean=[]
video_page_urls=[]
def get_video_page_urls():
    #print 'debug'
   
    r = requests.get(index_url)
    print r
    soup = bs4.BeautifulSoup(r.content)
    #print soup
    #print soup.find_all("a")
    
    for link in soup.find_all("a"):
        links.append(link.get("href"))
        
    for i in range(len(links)):
        links[i]=str(links[i])
    
    #print links
    
    for string in links:
        if re.match("^/video", string):    
            links_clean.append(string) 
    #print links_clean
    
    for i in range(len(links_clean)):
        if i<20:
            if i%2==0 :
                video_page_urls.append(links_clean[i])
                
    return video_page_urls
    '''       
    return [a.attrs.get('href') for a in soup.select('div.video-summary-data a[href^=/video]')]
    '''
        
video_page_url = (get_video_page_urls())



video_data = {}
    
for i in range(len(video_page_url)):    
    response = requests.get(root_url + video_page_url[i])
    soup = bs4.BeautifulSoup(response.text)


    print soup.select('div#videobox h3')[0]
    '''
    video_data['speaker'] = [a.get_text() for a in soup.select('div#sidebar a[href^=/speaker]')]
    video_data['youtube_url'] = soup.select('div#sidebar a[href^=http://www.youtube.com]')[0].get_text()
    #video_data['Record data']


    print video_data
    '''
    
    
    
    
    
