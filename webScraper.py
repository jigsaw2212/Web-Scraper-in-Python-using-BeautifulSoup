import requests
import bs4
import re
#imported the modules I will require in the project

#http://en.wikipedia.org/wiki/Member_states_of_the_United_Nations - The wikipedia page I'm scraping

root_url = 'http://en.wikipedia.org'
page_url = root_url + '/wiki/Member_states_of_the_United_Nations' 

r = requests.get(page_url) #returns the HTML of the page, can be done through urlopen as well
#The HTML of the website formed by the url is retrieved by the get function and stored in r


#Then we use the python library BeautifulSoup to parse the HTML code, by creating a soup of the contents of the retrieved HTML codes of the webpage
soup = bs4.BeautifulSoup(r.content)

#print soup
#for link in soup.find_all("a"):
#    print link.get("href")


fp=open('data_wiki.txt','w+')
#An empty file created for the purpose of storing data from our source page; data_wiki.txt stores general information from the chosen Wiki page, i.e the member countries in the UN. Along with that, it lists the countries about which we will be scraping more info from the respective links


fp.write( soup.select('div p')[0].get_text() + '\n')
#Writing general info about the UN and the member nations on to the file
fp.write( soup.select('div p')[4].get_text() + '\n\n')
#select function is used to retrieve the required HTML tag. It returns the whole HTML line complete with the tags

#The returned HTML code is the code made up by the first <p> tag (because of [0]), and the fifth <p> tag (as specified using [5]) under the> <div> tag.
#Using get_text, we retrieve the textual information contained between the text, the actual text that shows up on the website

country=[] #List variable used to iterate over the country names
countries=[]    #List of all the 10 chosen countries 
admission_date=[]   #Date of admission of the country into the UN

fp.write('%-15s  %-15s\n\n' %('Country', 'Admission_date'))
#Headers for the file

for i in range(11,21):
 
    country= (str( soup.select('tr a[href^=/wiki]')[i].get_text() ) ) 
    #Again,select function is used to retrieve the required HTML tag. It returns the whole HTML line wherever it finds an anchor tag beginning with /wiki, like <a href="/wiki...whatever">, under the base tag tr.
    #This piece of code makes the tag 'country' point to the parsed country which is assigned to it

    countries.append((str( soup.select('tr a[href^=/wiki]')[i].get_text() ) )) #Adding country name to the list
    
    admission_date = ( str(soup.select('tr span[style^="white"]')[i-3].get_text() ))
    #Similarly, this piece of code parses the date of admission of the country and assigns it to admission date. 
    #The HTML code of the admission date carries the tag <span style=/wiki...something..>, which is the information I have exploited to extract the required date.
    
    
    fp.write('%-15s  %-15s\n' %(country, admission_date))
    #This data about a country and its date of admission is then written into the file with the appropriate formatting.
    
fp.write('\n\n')

fp.write( str(soup.select('ul li[id^="footer"]')[0].get_text() ).strip(' ') + '\n\n')
#Along with that, the last date of modification of the webpage is extracted from the footer. It is contained as a text inside the li tag, which itself lies inside the ul tag in the HTML of the page.
#It is converted into a string and stripped of all formatting before it is added to the file using fp.write(). 

fp.write( 'Now let us find some basic information about these countries from their Wikipedia page, using a Python script') 

fp.close() #Closed the file for the source page data

#Empty list for storing the page urls of the countries, who's wikipedia page I have to parse next
urls = []



   #print (link.get("href"))
'''   
for link in soup.select('tr')[2]:
   print link.find('a').attrs['href']   
'''
  
i=1 #intitalised a counter variable which counts from 1 to 10

for link in soup.select('tr a[href^=/wiki]'):
    #for link in soup.find_all('a'):
    if(i>11 and i<=21):  #A chunk of 10 urls belonging to 10 different countries is extracted somehwere from the middle of the list of countries displayed on the source web page.
    
        urls.append(str(link.get('href')) ) #Add the page url to the list
    i=i+1   #Increment counter
   
   #soup.select('div#sidebar a[href^=http://www.youtube.com]')[0].get_text()
 
#mw-content-text > table.sortable.wikitable.jquery-tablesorter


#Another empty file for writing the information extracted from the page of every country we traverse.
fp = open('data_from_links.txt','w+')  #The file has been opened in write mode using w+

fp.write('%-12s  %-12s %-20s %-15s %-25s %-15s %-25s\n\n' %(' ',  'Capital' ,'Official Language', 'Telephone Code', 'President', 'Demonym ', 'Page Last Modified')) 
#Headers for the information to be stored about each country


#Empty lists, to which the associated attributes of each country will be assigned
language = []
capital = []
telephone = []
presidents = []
demonym = []
modified = []

for i in range(len(urls)):  #for loop begins; We iterate over all the page urls in our list urls[]

    r = requests.get(root_url + urls[i])
    soup = bs4.BeautifulSoup(r.text)
    #Just like I did before, now I will parse the HTML code of each of the countries pages one by one, by cooking a separate soup for each of them, to retrieve their HTML code
    
    
    #Retrieving the Official LANGUAGE of each country 
    if i==5:
        language = (str(soup.select('div#bodyContent tr td')[10].get_text() ))
    else:
        language = ( str( soup.select('div#bodyContent tr a[href$=language]')[0].get_text() ))
        
     #Needed to access a separate set of tags for one particular country. That is how the HTML of the webpage was written,
     #For all other countries, I was able to extract info from the <tr..> tag where href ends with the word language
     
     #NOTE: The $ symbol here denotes a regular expression, wherein we are matching our required info with the characters at the end of something. So ony those href tags in the code which end at 'language' are selected
        
        
    #Code used to retrieve the capital of each country    
    if (i==4 or i==7 or i==8 or i==9):
        capital = ( str( soup.select('div#bodyContent tr[class^=mergedtoprow] td a[href^=/wiki]')[5].get_text() ) )    
    else:
        capital = ( str( soup.select('div#bodyContent tr[class^=mergedtoprow] td a[href^=/wiki]')[4].get_text() ) )
    
    # The HTML of the pages is such that all the capital names are not contained in the same tag.
    #Therefore, I had to retrieve the capital names from different tags for different countries
    
    #NOTE: The data recieved in unicode format is first converted into a string, and then stripped of any formatting so that it can successfully written to the file
    
    #Retrieving the telephone code of the country
    if (i==2 or i==5 ):
        telephone = ( str( soup.select('div#bodyContent tr td a[href^=/wiki/Area]')[0].get_text() ))
    elif(i==6 or i==9):
        telephone = ( str( soup.select('div#bodyContent tr td a[href^=/wiki/%2B]')[0].get_text() ))
    elif(i==8):
        telephone = (' ')
    else:
        telephone = ( str( soup.select('div#bodyContent tr td a[href^=/wiki/Telephone]')[0].get_text() ))
     #Had to retrieve the capital names from different tags for different countries due to inconsistencies in the page HTML codes
        

    
    #Retrieving the names of the incumbent presidents for each country
    if i==9:
        presidents = ( str( soup.select('div#bodyContent tr[class^=mergedbottomrow] td a[href^=/wiki/]')[2].get_text() ) )
    else:
        presidents = ( str( soup.select('div#bodyContent tr[class^=mergedrow] td a[href^=/wiki/]')[1].get_text()  ) )     
    
    
    #Retrieving the demonym with which the people of each country are referred to, and then assigned to the list demonym.
    #It again lies at different places for different countries.
    if (i==0 or i==1 or i==3 or i==7):
        demonym = ( str( soup.select('div#bodyContent tr td a[class^=mw-redirect]')[1].get_text() ))
    elif (i==2 or i==5 or i==8):
        demonym = ( str( soup.select('div#bodyContent tr td a[class^=mw-redirect]')[3].get_text()   ) )
    elif (i==4):
        demonym = ( str( soup.select('div#bodyContent tr td a[class^=mw-redirect]')[2].get_text() ) )
    elif (i==6):
        demonym = ( str( soup.select('div#bodyContent tr td a[href^=/wiki/Belarusian]')[1].get_text() ) )
    else:
        demonym = (str( soup.select('div#bodyContent tr td ul li')[16].get_text() ))
       
    
    #The list modified is assigned the date and time of the latest modification of the wikipedia page of the respective countries
    modified = ( str(soup.select('ul li[id^="footer"]')[0].get_text() ).strip(" This page was last modified on") )
     
    #THE DATA WRITING STEP
    fp.write('%-12s  %-12s %-20s %-15s %-25s %-15s %-25s\n' %(countries[i],  capital, language, telephone, presidents, demonym, modified))    
  
#All data generated is written to the file while taking care to left align every data element for consitency and ease of removal of a value from the file. '-' sign signifies the left alignment  
    #The write attributes %-12s , %-12s, %-15s,  etc tell us the maximum space(length) the attributes in the respective columns can take
    #Here I have hard coded this data, keeping in mind the maximum values each attribute can take, otherwise we can also run a for loop and calculate the maxlength an attribute can take for each field.
     
    print '.'*i
    
fp.close() #closing the file 



