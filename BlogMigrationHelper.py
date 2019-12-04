<<<<<<< HEAD
'''
BlogMigrationHelper.py is a command line helper script for pulling necessary blog data from webpages.
Accepts a .txt file containing old article links, one link on each line.
Outputs a .xls file containing the data of interest, (almost) ready for migration.

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
import urllib.request
import xlwt 
from xlwt import Workbook

'''
Config
'''
error = 0
inputFileName = "in"
outputFileName = "out"
siteAddress = ""
scrapeFromLink = False

# class holding data of interest
class BlogObj:
    
    # data of interest
    oldLink = ""
    newLink = ""
    metaTitle = ""
    metaDescription = ""
    pageContent = ""
    
    def __init__(self, oldLink):
        global error
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
            
            # Get Meta Tags
            self.updateMetaTitle()
            self.updateMetaDescription()

            # get blog content
            self.pullContent()
        except:
            error += 1
        
    def __str__(self):
        return self.oldLink

    # Pull meta title data
    def updateMetaTitle(self):
        self.metaTitle = self.soup.find("meta",property="og:title")["content"]

    # Pull meta description data
    def updateMetaDescription(self):
        self.metaDescription = self.soup.find("meta",property="og:description")["content"]

    def pullContent(self):
        page = self.soup.findAll(class_="col-md-8 col-md-offset-2")
        
        # Get rid of h1 headers
        h1Index = str(page).find("</h1>")
        page = str(page)[h1Index+5:]

        # Get rid of responsive containers
        page = page.replace(" class=\"img-responsive center-block\"","")

        self.pageContent = page

# Read the list of old blog article links from a .txt file named inFileName
def readInputFile(blogObjects):
    global inputFileName
    with open(inputFileName+".txt") as inputFile:
        for link in inputFile:
            link = link.strip()
            if link != "":
                blogObjects.append(BlogObj(link))

# Outputs scraped data to .xls file
def writeResult(blogObjects):
    global outputFileName
    col_width = 256 * 100 # 100 characters long
    
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')

    # Set column width
    for i in range(5):
        sheet1.col(i).width = col_width

    # write table heading
    sheet1.write(0, 0, "Redirect From URL") 
    sheet1.write(0, 1, "Redirect To URL") 
    sheet1.write(0, 2, "Title") 
    sheet1.write(0, 3, "Description")
    sheet1.write(0, 4, "Blog Content")

    for rowNum in range(len(blogObjects)):
        sheet1.write(rowNum+1, 0, blogObjects[rowNum].oldLink)
        sheet1.write(rowNum+1, 1, blogObjects[rowNum].newLink)
        sheet1.write(rowNum+1, 2, blogObjects[rowNum].metaTitle)
        sheet1.write(rowNum+1, 3, blogObjects[rowNum].metaDescription)
        sheet1.write(rowNum+1, 4, blogObjects[rowNum].pageContent)

    wb.save(outputFileName + ".xls")

def printHelp():
    print("""
example:\npython BlogMigrationHelper.py input futurebranches.wbresearch.com FutureBranchesMigration\n
will take in input.txt and output FutureBranchesMigration.xls
""")

def main():
    global inputFileName
    global outputFileName
    global siteAddress
    global error
    
    #Parse command line arguments
    if len(sys.argv) > 4:
        print("Too many arguments given.\n")
        sys.exit()
    if len(sys.argv)== 2:
        if sys.argv[1] == "-help":
            printHelp()
        sys.exit()
    if len(sys.argv) <= 2:
        print("""\nERROR: Too few arguments. \n\nFormat:\npython BlogMigrationHelper.py inputFileName HomePageAddress outputFile\n
Type \"python BlogMigrationHelper.py -help\" for an example.""")
        sys.exit()
    if len(sys.argv) == 4:
        outputFileName = sys.argv[3]
        
    inputFileName = sys.argv[1]
    siteAddress = sys.argv[2].rstrip("/").replace("https://","")

    # Check if file exists
    if not os.path.isfile(inputFileName+".txt"):
        print("ERROR: File {} does not exist.".format(inputFileName+".txt"))
        sys.exit()

    # read the input file and put them into a list of BlogObjs
    blogObjects = []
    readInputFile(blogObjects)

    # Output Result
    writeResult(blogObjects)

    print("*Task done. Program terminated with", str(error), "errors.*")

if __name__ == "__main__":
    main()
=======
'''
Version 2.0.0
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
        page = self.soup.findAll(class_="col-md-8 col-md-offset-2")
        
        # Get rid of h1 headers
        h1Index = str(page).find("</h1>")
        page = str(page)[h1Index+5:]

        # Get rid of responsive containers
        page = page.replace(" class=\"img-responsive center-block\"","")

        self.pageContent = page

# Scan for a list of old blog article links from the provided link
def scanArticleListing(blogObjects):
    try:
        listingHtml = urllib.request.urlopen(articleListingLink).read()
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
    for i in range(5):
        sheet1.col(i).width = col_width

    # write table heading
    sheet1.write(0, 0, "Redirect From URL") 
    sheet1.write(0, 1, "Redirect To URL") 
    sheet1.write(0, 2, "Title") 
    sheet1.write(0, 3, "Description")
    sheet1.write(0, 4, "Blog Content")

    for rowNum in range(len(blogObjects)):
        sheet1.write(rowNum+1, 0, blogObjects[rowNum].oldLink)
        sheet1.write(rowNum+1, 1, blogObjects[rowNum].newLink)
        sheet1.write(rowNum+1, 2, blogObjects[rowNum].metaTitle)
        sheet1.write(rowNum+1, 3, blogObjects[rowNum].metaDescription)
        sheet1.write(rowNum+1, 4, blogObjects[rowNum].pageContent)

    wb.save(outputFileName + ".xls")

def printHelp():
    print("""
Format:
python BlogMigrationHelper.py articleListingLink outputFileName

example:\npython BlogMigrationHelper.py https://programmaticusa.wbresearch.com/programmatic-pioneers-blog FutureBranchesMigration

will scan the Programmatic Pioneers article listing page and output FutureBranchesMigration.xls which contains the retrieved data.
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
            articleListingLink = sys.argv[1]
            if len(sys.argv) > 2:
                outputFileName = sys.argv[2]
            tmpsiteAddress = ((articleListingLink.replace("https://", "")).rstrip("/")).split("/")
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
    
    # output result
    writeResult(blogObjects)

    print("*Task done. Program terminated with", str(error), "errors.*")

    # print troubleshooting info
    if error > 0:
        print("Error found in the following links:")
        for err in errorList:
            print(err)

if __name__ == "__main__":
    main()
>>>>>>> version2.0.0
