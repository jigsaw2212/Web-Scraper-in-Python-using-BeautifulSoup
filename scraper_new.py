import requests  #requests module is used to fetch the HTML code from a webpage
import bs4 #beautiful soup is a module used to parse HTML code using its various functions
import re  #re is a module used to implement various functionalities of regualar expressions

#imported the modules I will require in the project

#http://pyvideo.org/category/50/pycon-us-2014 -Is the webpage i'm parsing in this script

root_url = 'http://pyvideo.org'
page_url = root_url + '/category/50/pycon-us-2014'

links=[]
links_clean=[]
urls=[]

#print 'debug'
   
r = requests.get(page_url)
#The HTML of the website formed by the url is retrieved by the get function and stored in r


#Then we use the python library BeautifulSoup to parse the HTML code, by creating a soup of the contents of the retrieved HTML codes of the webpage
soup = bs4.BeautifulSoup(r.content)

#print soup
#print soup.find_all("a") #Used to retrieve all the HTML lines of code having the <a> tag


#An empty file created for the purpose of storing data; data.txt stores information about our source website. The title, URL, the description, date of creation and the no of videos on the page is stored.
fp=open('data.txt','w+')


fp.write(soup.select('div h1')[0].get_text() + '\n')
#Stores title of webpage. h1 acts like the child tag for <div>. Since the title is stored in the first h1 tag we encounter, we parse the title by selecting ('div h1')[0]. 

#select function is used to retrieve the required HTML tag. It returns the whole HTML line complete with the tags

#get_text() is a function we use on the parsed HTML line to retrieve the actual textual info which is written by the programmer (which is displayed on the web page) 


fp.write(soup.select('div a[href^=https]')[0].get_text() + '\n\n')
#Stores the URL. The URL we needed to store was located within the first anchor tag <a> with href we in the HTML code. We check for the hypertext reference in the anchor tags and use 'select' the first one with a hypertext reference that begins with https, making it clear that it is our required webpage URL. 

#'href^=https' is a Regular expression which is used to denoted an href statement beginning with the keyword https followed by any other characters


#Stores the Description in the form of a paragraph
#NOTE: Here I have used a for loop because the overall description of the webpage was distributed among 3 <p></p> tags, under the <div>tag, hence I have to access it using ('div p')[0], ('div p')[1] and ('div p')[2] one by one and write into my file
for i in range(3):
    fp.write(soup.select('div p')[i].get_text())

fp.write('\n\n')
    
    
fp.write(str(soup.select('div dd')[2].get_text()).strip('\n').strip(' ') + '\n')    
#Writes Date of creation of the page into the file. 
#Next, I retrive the date of creation of the webpage as displayed on the page using ('div dd')[2], as it is the 3rd <dd> tag whose text contains this date.

#I have used the strip('\n') and strip(' ') functions on the date, so that I can remove the formatting from the date and store it in the file in a concise manner. Other wise it was found to be disturbing the alignment in the file



#Write the no of videos to the file
#fp.write( '%-10s' %(str(soup.select('div dd')[3].get_text())))
fp.write (str(soup.select('div dd')[3].get_text() ).strip('\n').strip(' ') + '\n')
#The no of videos on the webpage was found to be contained in the 4th <dd> child tag under div, hence the ('div dd')[3] part of the code has been used

 
fp.close()  #closes the file

#Parsing the first 10 video links on our webpage that we will branch to:-
    
#links is an empty list define above.
#Here we search for the HTML statments in the code for all the anchor tags and from all the anchor tags recieved, we filter out those anchor tags <a> which contain a hypertext reference href. They are something like <a href = "https://...whatever...".
#These filtered anchor tags are stored in the list links[]    
for link in soup.find_all("a"):
    links.append(link.get("href"))
 
 
#We iterate over all the saved tags in links[] (len(links) gives us the number of elements the list links[] contains, which is nothing else but the no of href links.        
for i in range(len(links)):
    links[i]=str(links[i])
    
#print links


#Now for all the links in the links[] list, we find out those which denote a video embedded on the site, the links which are the urls for our videos.

#We check this by again employing the usage of regurlar expressions and we filer out the links in the list links[] which have '/video' keyword in them. These are the URLs we are looking for, as they will redirect us to the page on which the associated video exists    
for link in links:
    if re.match("^/video", link):    
        links_clean.append(link) 
#print links_clean
#These video links are stored in the list links_clean[]
    
for i in range(len(links_clean)):
    if i<20:
        if i%2==0 :
            urls.append(links_clean[i])
#The above part of the code selects the first 10 video links from the list links_clean[] and stores them in another list urls[]. That's a lot of lists.
 
#I am running the loop till 20 because all my video links were repeated int the HTML of the webpage, because the video thumbnails and the video title are both hyperlinks that direct us to the video 




#Now open another file to save the data at every link
fp = open('link_data.txt','w+')



#Dictionary to store the data
videoInfo = {}
#I am also storing the data in the dictionary, to display it at regular intervals on my terminal window in addition to writing it on a file    
    


#Lists which will contain the data for every video (as the names suggests). Data from them would be written on the file eventually
#Working with lists is helping me format my data in a concise and resusable format.    
titles=[]
speakers=[]
YouTube_links=[]
Dates=[]    

    
#Now I iterate through my generated list of urls of videos and branch to those webpages    
for i in range(len(urls)):  #for loop begins

    r = requests.get(root_url + urls[i])
    
    soup = bs4.BeautifulSoup(r.text)
    #Just like I did before, now I will parse the HTML code of each of the video pages one by one, by cooking a separate soup for each of them, to retrieve their HTML separately
    

    #Retrieving each video's title and storing it in the list titles[].
    #I'm converting the title from unicode to string so that I can strip that string of any formatting before writing to the file
    titles = str(soup.select('div#videobox h3')[0].get_text()).strip('\n').strip(' ')
    
    
    #NOTE: Here we select our base tags as videobox by writing div#videobox and sidebar by writing div#sidebar, access their child tags, and then get_text them to retrieve the info we need.
    
    
    #Retrieving each talk's speaker and storing it in the list speakers[].
    #Formatting is removed as before writing to the file
    speakers = str(soup.select('div#sidebar dd')[1].get_text()).replace('\n','').replace(' ','').strip(' ')
    
    
    #Retrieving each video's YouTube URL and storing it in the list YouTube_links[].
    YouTube_links = str(soup.select('div#sidebar a[href^=http://www.youtube.com]')[0].get_text())
   
   
    #Retrieving each video's date and storing it in the list Dates[].
    #The date has also been converted from unicode to a string and stripped of line breaks and spaces for consistency just like before to maintain consistency of formatting in the file
    Dates = str(soup.select('div#sidebar dd')[4].get_text()).strip('\n')
    
    
    #THE DATA WRITING STEP
    fp.write('%-70s  %-30s  %-80s %-20s\n' %(titles , speakers , YouTube_links , Dates))    
    #All data is written to the file while taking care to left align every data element for consitency and ease of removal of a value from the file. 
    #The write attributes %-70s , %-30s etc tell us the maximum space(length) the attributes in the respective columns can take. '-' sign signifies the left alignment of data .
    #Data can be truncated or lost if this parameter is not specified with care.
    #Here I have hard coded this data, keeping in mind the maximum values each attribute can take, otherwise we can also run a for loop and calculate the maxlength an attribute can take for each field.
    
    
#NOTE: I can write a lot of other attributes like Language, speaker website etc to the files but I hope 4 field are enough to give the reader an idea of web scraping using this script    
    
    
    #The same data is added to the dictionary videoInfo, so that the user running this script can display the data on the termical screen as well
    videoInfo['title'] = (str(soup.select('div#videobox h3')[0].get_text().strip('\n') ))
    
    
    videoInfo['Speaker'] = ( str(soup.select('div#sidebar dd')[1].get_text()).replace('\n','').replace(' ','') )
    
    
    videoInfo['Youtube URL'] = ( str(soup.select('div#sidebar a[href^=http://www.youtube.com]')[0].get_text()) )
    
    
    videoInfo['Modification date'] = (str(soup.select('div#sidebar dd')[4].get_text()).strip('\n').strip(' ') )
    
    
    

    print "."*i
    print '\n'
    
    print videoInfo #print the dictionary elements for every video
    #end of for loop; for display on the terminal
    
fp.close() #closing the file object
    
    
    
    
    
