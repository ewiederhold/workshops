## ++++++++++++++++++++++++++++++++++
## Fall 2018
## Workshops at the Library
## Stop Copying & Pasting & Start Webscraping with Python
## Mollie Webb, Data Service, University Libraries
## molliewebb@wustl.edu
## Notes:
## Comments are denoted with '##'
## Code to be run is denoted with '####'
## Use Alt+3 to comment
## Use Alt+4 to uncomment
## ++++++++++++++++++++++++++++++++++

## Preparation Steps
## Use the command line to install the BeautifulSoup and Requests site packages
## Note: May need to change directory "cd" to the directory with "pip.exe"
## On the machines in Olin, this path is "C:\Python27\ArcGIS10.5\Scripts"
## Commands:
## pip install beautifulsoup4
## pip install requests

## 1)Import the necessary libraries, fetch the html from the website and preview the tags

## CODE BLOCK 1a

import requests
from bs4 import BeautifulSoup
import csv

## TO DO - Update this path to reflect local machine and desired output file name
#output_file = r"C:\path\to\my\file"

base_link = "http://www.gunviolencearchive.org"
html = requests.get(base_link + "/mass-shooting")
html_text = html.text
soup = BeautifulSoup(html_text,"html.parser")
####print soup.prettify

## 2)Examine the tags, isolate the ones that contain the desired information

## CODE BLOCK 2a

####for tr in soup.find_all('tr'):
####    print tr

## The first "tr" tag is the header information, the subsequent "tr" tags have "td" tags nested in them
## The "td" tags contain the incident-level information, so now retrieve the "td" tags
## that are nested in the "tr" tags

## CODE BLOCK 2b

####for tr in soup.find_all('tr'):
####    for td in tr.find_all('td'):
####        print td

## 3) Each "tr" element contains multiple "td" tags, determine which "td" tags contain which pieces
## of information

## CODE BLOCK 3a

####for tr in soup.find_all('tr'):
####    date = tr.find_all('td')[0]
####    print "Date = " + date

## ERROR - The above code will throw an error because the first "tr" tag (the heading) does not contain
## any "td" tags, so there is no "td" tag with the index of zero
## So before calling any "td" tags, we need to make sure that there are some "td" tags swithin the "tr" tag

## CODE BLOCK 3b

####for tr in soup.find_all('tr'):
####    if (len(tr.find_all('td')) > 0):
####           date = tr.find_all('td')[0]
####           print "Date = " + str(date)

## We have found the date, let's see what the rest of the "td" tags contain, uncomment and run Code Block 2b
## to refresh our memories

## CODE BLOCK 3c

####for tr in soup.find_all('tr'):
####    td_list = tr.find_all('td')
####    if (len(td_list) > 0):
####        date = td_list[0]
####        print "Date = " + str(date)
####        state = td_list[1]
####        print "State = " + str(state)
####        city = td_list[2]
####        print "City/County = " + str(city)
####        address = td_list[3]
####        print "Address = " + str(address)
####        num_killed = td_list[4]
####        print "NumKilled = " + str(num_killed)
####        num_injured = td_list[5]
####        print "NumInjured = " + str(num_injured)

## Those results look great, but they still have the html syntax "<>" brackets, let's strip those off of the results
## To do this, we can use the text property of "Tag" element.

## CODE BLOCK 3d
        
####for tr in soup.find_all('tr'):
####    td_list = tr.find_all('td')
####    if (len(td_list) > 0):
####        date = td_list[0].text
####        print "Date = " + date
####        state = td_list[1].text
####        print "State = " + state
####        city = td_list[2].text
####        print "City/County = " + city
####        address = td_list[3].text
####        print "Address = " + address
####        num_killed = td_list[4].text
####        print "NumKilled = " + num_killed
####        num_injured = td_list[5].text
####        print "NumInjured = " + num_injured

## 4) Now let's write the data to a csv so it can be analyzed or brought in to another application
## To do this, we are going to write a line to the csv with each iteration through the "tr" tags

## CODE BLOCK 4a

####with open(output_file,'wb') as file_out:
####    fieldnames = ['Date','State','City','Address','NumKilled','NumInjured']
####    writer = csv.DictWriter(file_out,fieldnames = fieldnames)
####    writer.writeheader()
####
####    for tr in soup.find_all('tr'):
####        td_list = tr.find_all('td')
####        if (len(td_list) > 0):
####            date = td_list[0].text
####            state = td_list[1].text
####            city = td_list[2].text
####            address = td_list[3].text
####            num_killed = td_list[4].text
####            num_injured = td_list[5].text
####            writer.writerow({'Date':date,
####                             'State':state,
####                             'City':city,
####                             'Address':address,
####                             'NumKilled':num_killed,
####                             'NumInjured':num_injured})

## 5) The above code will retrieve all of the basic data for each record, but will we have not addressed the links
## Let's look at the structure of the "td" tags again - uncomment and run Code Block 2b
## The 7th element is the section with the links, and they are presented as a list with "lines"
## The tag for each element is "li"

## CODE BLOCK 5a

####for tr in soup.find_all('tr'):
####    td_list = tr.find_all('td')
####    if (len(td_list) > 0):
####        print td_list[6]

## The "li" elements are embedded in a "ul" tag, so first we isolate the "ul" tags, then isolate the "li" tags.

## CODE BLOCK 5b

####for tr in soup.find_all('tr'):
####    td_list = tr.find_all('td')
####    if (len(td_list) > 0):
####        for ul in td_list[6]:
####            li = ul.findAll('li')
####            for l in li:
####                print l

## The first "li" element is the link associated with "View Incident," the second "li" element is the tag associated with "View Source"
## What we are really interested in is the URLs associated with these elements.  They are designated with the "href" tag.
## We will isolate those in the next code block

## CODE BLOCK 5c

####for tr in soup.find_all('tr'):
####    td_list = tr.find_all('td')
####    if (len(td_list) > 0):
####        for ul in td_list[6]:
####            li = ul.findAll('li')
####            incident_url = li[0].find_all('a',href=True,text="View Incident")[0]['href']
####            print "Incident: " + str(incident_url)
####            source_url = li[1].find_all('a',href=True,text="View Source")[0]['href']
####            print "Source: " + str(source_url)

## 6) Now that we have isolated the links, we can add these back in to the full dataset and write everything to a csv
## The following code block is similar to Code Block 4a, but includes entries for the links

## CODE BLOCK 6a

####with open(output_file,'wb') as file_out:
####    fieldnames = ['Date','State','City','Address','NumKilled','NumInjured',"IncidentInfo","Source"]
####    writer = csv.DictWriter(file_out,fieldnames = fieldnames)
####    writer.writeheader()
####
####    for tr in soup.find_all('tr'):
####        td_list = tr.find_all('td')
####        if (len(td_list) > 0):
####            date = td_list[0].text
####            state = td_list[1].text
####            city = td_list[2].text
####            address = td_list[3].text
####            num_killed = td_list[4].text
####            num_injured = td_list[5].text
####            incident_url = str(td_list[6].find_all('ul')[0].findAll('li')[0].find_all('a',href=True,text="View Incident")[0]['href'])
####            source_url =  str(td_list[6].find_all('ul')[0].findAll('li')[1].find_all('a',href=True,text="View Source")[0]['href'])
####            writer.writerow({'Date':date,
####                             'State':state,
####                             'City':city,
####                             'Address':address,
####                             'NumKilled':num_killed,
####                             'NumInjured':num_injured,
####                             'IncidentInfo':base_link + incident_url,
####                             'Source':source_url})

## 7) Up to this point, we have scraped the text from the table on the webpage as well as the links that were
## embedded within each row.  Next we are going to use information extracted from the table to scrape information
## from an additional page - the incident details page for each record. Our goal is to isolate the exact location
## of the indcident by extracting the latitude and longitude from the details page.

## First, let's take a look at what one of the incident details pages

## CODE BLOCK 7a

## Sample indicent id
####incident_id = str(763313)
####
####incident_html = requests.get(base_link + "/incident/" + incident_id)
####incident_text = incident_html.text
####soup = BeautifulSoup(incident_text,"html.parser")
####print soup.prettify

## The incident details are within the 'span' elements, so let's take a look at those:
## Keep CODE BLOCK 7a uncommented except for 'print soup.prettify'

## CODE BLOCK 7b

####for span in soup.find_all('span'):
####    print span

## On this page, the "Geolocation" information is in the 7th element.  Let's check another incident details page
## to see if this is consistent across the incident pages.
## Comment out CODE BLOCK 7a now

## CODE BLOCK 7c

## Sample indicent id
####incident_id = str(757955)
####
####incident_html = requests.get(base_link + "/incident/" + incident_id)
####incident_text = incident_html.text
####incident_soup = BeautifulSoup(incident_text,"html.parser")
####
####for span in incident_soup.find_all('span'):
####    print span

## On this page, the "Geolocation" information may be in a different element. This means that we cannot rely on
## using the index to find the 'span' element that contains the geolocation.  We will need to search specifically
## for the geolocation element
## Keep CODE BLOCK 7c uncommented

## CODE BLOCK 7d

####for span in incident_soup.find_all('span'):
####    if "Geolocation" in str(span):
####        print "Found Geolocation:"
####        print span

## Now that we know we can isolate the Geolocation this way, we will split and slice the text to extract
## the latitude and longitude values
## Comment out CODE BLOCK 7d
## Keep CODE BLOCK 7c uncommented

## CODE BLOCK 7e

####for span in incident_soup.find_all('span'):
####    if "Geolocation" in str(span):
####        loc = span.text
####        split = loc.split(", ")
####        lat = split[0].replace("Geolocation: ","")
####        long = split[1]
####        print "lat = " + lat
####        print "long = " + long

## 8) Now let's pull it all together!  Scrape the main table page, scrape the associated incident details pages
## and write everything out to a csv
## Comment out CODE BLOCK 7c now

## CODE BLOCK 8a

## This block combines CODE BLOCK 6a and CODE BLOCK 7e

####with open(output_file,'wb') as file_out:
####    fieldnames = ['Date','State','City','Address','NumKilled','NumInjured',"IncidentInfo","Source","Lat","Long"]
####    writer = csv.DictWriter(file_out,fieldnames = fieldnames)
####    writer.writeheader()
####
####    for tr in soup.find_all('tr'):
####        td_list = tr.find_all('td')
####        if (len(td_list) > 0):
####            date = td_list[0].text
####            state = td_list[1].text
####            city = td_list[2].text
####            address = td_list[3].text
####            num_killed = td_list[4].text
####            num_injured = td_list[5].text
####            incident_url = str(td_list[6].find_all('ul')[0].findAll('li')[0].find_all('a',href=True,text="View Incident")[0]['href'])
####            source_url =  str(td_list[6].find_all('ul')[0].findAll('li')[1].find_all('a',href=True,text="View Source")[0]['href'])
####
####            # Split the incident_url to get the incident_id
####            incident_id = incident_url.split("/")[2]
####            incident_html = requests.get(base_link + "/incident/" + incident_id)
####            incident_text = incident_html.text
####            incident_soup = BeautifulSoup(incident_text,"html.parser")
####
####            for span in incident_soup.find_all('span'):
####                if "Geolocation" in str(span):
####                    loc = span.text
####                    split = loc.split(", ")
####                    lat = split[0].replace("Geolocation: ","")
####                    long = split[1]
####                
####            writer.writerow({'Date':date,
####                             'State':state,
####                             'City':city,
####                             'Address':address,
####                             'NumKilled':num_killed,
####                             'NumInjured':num_injured,
####                             'IncidentInfo':base_link + incident_url,
####                             'Source':source_url,
####                             'Lat': lat,
####                             'Long': long})

## With this basic scrape script, additional code can be written to loop through each webpage,
## perform the scrape operation and write to csv.
                             
