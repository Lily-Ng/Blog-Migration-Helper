'''
Version 4.0.0
BlogMigrationHelper.py is a command line helper script for pulling necessary blog data from webpages.
obtains all old article links, scrapes each for meta tags and page content, then format them according to specifications for the new blog feature.
Outputs a collective .xls file containing all data of interest, (almost) ready for migration.

Modules & Dependencies:
- Tested on Python version 3.7.3
- BeautifulSoup4 version 4.8.1
- xlwt version 1.3.0

Before running,install the packages:
pip install –upgrade pip
pip install bs4
pip install xlwt

'''
from bs4 import BeautifulSoup
import os
import sys
import urllib
import urllib.request
import xlwt 
from xlwt import Workbook

'''
Config
'''
error = 0
errorList = []
outputFileName = "out"
siteAddress = ""
articleListingLink = ""

# class holding data of interest
class BlogObj:
    
    # data of interest
    articleTitle = ""
    oldLink = ""
    newLink = ""
    metaTitle = ""
    metaDescription = ""
    pageContent = ""
    
    def __init__(self, oldLink):
        global error, errorList
        oldLink = oldLink.replace("https://","")
        if oldLink.find(".")!= -1:
            parsedLink = oldLink.split("/")
            oldLink = parsedLink[-1]
        oldLink = oldLink.strip("/")
        self.oldLink = oldLink
        self.newLink = ("blog/" + oldLink).replace("-ty-u","")

        # Retrive web info
        try:
            html = urllib.request.urlopen("https://" + siteAddress + "/" + self.oldLink).read()
            self.soup = BeautifulSoup(html,"lxml")
            
            # get Meta Tags
            self.updateMetaTitle()
            self.updateMetaDescription()

            # get blog content
            self.pullContent()
            
        except:
            # log errors
            error += 1
            errorList.append("https://" + siteAddress + "/" + self.oldLink)
            
    def __str__(self):
        return self.oldLink

    # Pull meta title data
    def updateMetaTitle(self):
        self.metaTitle = self.soup.find("meta",property="og:title")["content"]

    # Pull meta description data
    def updateMetaDescription(self):
        self.metaDescription = self.soup.find("meta",property="og:description")["content"]

    def pullContent(self):
        global error, errorList
        h2flag = False
        inColContainer = False
        
        page = self.soup.find(class_="subpagecontent")

        # Get article title
        titleTag = self.soup.find(class_="subpagecontent").find_all('h1')
        if len(titleTag) == 0:
            titleTag = self.soup.find(class_="subpagecontent").find_all('h2')
            h2flag = True
        for title in titleTag:
            if len(title.text.strip()) != 0:
                self.articleTitle += title.text.strip() + " "
            if h2flag == True:
                break
        self.articleTitle = self.articleTitle.strip()

        # test for col-md-8 col-md-offset-2 container
        container = self.soup.find(class_="subpagecontent").find(class_="container")
        
        if container != None and container.text.strip() != "":
            page = container
            
        # test for container class
        container = self.soup.find(class_="subpagecontent").find(class_="container").find(class_="col-md-8 col-md-offset-2")
            
        if container != None:
            page = container
            inColContainer = True

        # Take out title tags
        for title in titleTag:
            title.decompose()
            if h2flag == True:
                break
        
        page = str(page).replace("&amp;", "&")

        """
        # EDITED: EXCLUDED IN VERSION 4.0.0
        # Get rid of responsive containers
        page = str(page).replace(" class=\"img-responsive center-block\"","")
        """

        # Remove by-line
        page = str(page).replace("<p style=\"font-size:80%;\">Brought to you by <a href=\"http://www.wbrinsights.com/\" target=\"_blank\">WBR Insights</a></p>","")

        # Preprocess
        containerStart = page.find("container")
        if containerStart != -1:
            containerStart = page.find(">", containerStart)
            containerEnd = page.rfind("</div>")
            page = page[containerStart+1:containerEnd].strip()
        if inColContainer == True:
            containerStart = page.find("col-md-8 col-md-offset-2")
            containerStart = page.find(">", containerStart)
            containerEnd = page.rfind("</div>")
            page = page[containerStart+1:containerEnd].strip()

        self.pageContent = page

        # If content is too long to be written, display an error instead of writing.
        if len(self.pageContent) > 32767:
            self.pageContent = "ERROR: CONTENT TOO LONG TO WRITE TO FILE"
            error += 1
            errorList.append(self.oldLink)

# Scan for a list of old blog article links from the provided link
def scanArticleListing(blogObjects):
    try:
        listingHtml = urllib.request.urlopen("https://"+articleListingLink).read()
    except urllib.error.HTTPError:
        print("Unable to connect to",articleListingLink)
        sys.exit()
    soup = BeautifulSoup(listingHtml,"lxml")
    articleTable = soup.findAll("td")
    
    for article in articleTable:
        article = str(article)
        startInd = article.find("\"")
        endInd = article.find("\"", startInd+1)
        link = article[startInd+1:endInd].replace("https://","").split("/")[-1]
        if link != "":
            blogObjects.append(BlogObj(link))

# Outputs scraped data to .xls file
def writeResult(blogObjects):
    global outputFileName
    col_width = 256 * 100 # 100 characters long
    
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')

    # Set column width
    for i in range(6):
        sheet1.col(i).width = col_width

    # write table heading
    sheet1.write(0, 0, "Article Title")
    sheet1.write(0, 1, "Redirect From URL") 
    sheet1.write(0, 2, "Redirect To URL") 
    sheet1.write(0, 3, "Meta Title") 
    sheet1.write(0, 4, "Meta Description")
    sheet1.write(0, 5, "Blog Content")

    for rowNum in range(len(blogObjects)):
        sheet1.write(rowNum+1, 0, blogObjects[rowNum].articleTitle)
        sheet1.write(rowNum+1, 1, blogObjects[rowNum].oldLink)
        sheet1.write(rowNum+1, 2, blogObjects[rowNum].newLink)
        sheet1.write(rowNum+1, 3, blogObjects[rowNum].metaTitle)
        sheet1.write(rowNum+1, 4, blogObjects[rowNum].metaDescription)
        sheet1.write(rowNum+1, 5, blogObjects[rowNum].pageContent)

    wb.save(outputFileName + ".xls")

def printHelp():
    print("""
Format:
python BlogMigrationHelper.py articleListingLink outputFileName

example:\npython BlogMigrationHelper.py https://programmaticusa.wbresearch.com/programmatic-pioneers-blog programmaticusaMigration

will scan the Programmatic Pioneers article listing page and output programmaticusaMigration.xls which contains the retrieved data.
""")

def main():
    global articleListingLink,outputFileName,siteAddress,error,errorList

    # parse command line arguments
    if len(sys.argv) > 3:
        print("Too many arguments given. Please refer to documentation or use the -help option\n")
        sys.exit()
    if len(sys.argv) > 1:
        if sys.argv[1] == "-help":
            printHelp()
            sys.exit()
        else:
            articleListingLink = sys.argv[1].strip()
            if len(sys.argv) > 2:
                outputFileName = sys.argv[2]
            articleListingLink = articleListingLink.replace("https://", "")
            tmpsiteAddress = articleListingLink.rstrip("/").split("/")
            if len(tmpsiteAddress) == 1:
                print(articleListingLink,"is not an article listing page.")
                sys.exit()
            elif tmpsiteAddress[1] == 0:
                print(articleListingLink,"is not an article listing page.")
                sys.exit()
            else:
                siteAddress = tmpsiteAddress[0]

    # scan site and put them into a list of BlogObjs
    blogObjects = []
    scanArticleListing(blogObjects)
    
    # output results
    writeResult(blogObjects)

    print("*Task done. Program terminated with", str(error), "errors.*")

    # print troubleshooting info
    if error > 0:
        print("Error found in the following links:")
        for err in errorList:
            print(err)

if __name__ == "__main__":
    main()
