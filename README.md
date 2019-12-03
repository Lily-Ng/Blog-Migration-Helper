# Blog Migration Helper
A web scraper project that pulls meta data &amp; content, formatting them according to blog migration specifications of WBR.
Blog Migration Helper is a command line tool programmed in Python.

Raw source code is in "BlogMigrationHelper.py"

# Modules & Dependencies
- Tested on Python version 3.7.3
- BeautifulSoup4 version 4.8.1
- xlwt version 1.3.0

# How to Install (Method 1, for Windows Only)
1. Download or clone this repository
This method will use the build BlogMigrationHelper.exe in the dist folder
2. Open the terminal/command line in the directory where BlogMigrationHelper.exe is in.
3. Type "BlogMigrationHelper.exe nameofinputfile siteaddress nameofoutputfile" and press enter.
For example, I want to migrate eTail West articles. I have a list of article links to migrate in "oldArticles.txt" and want the output to be called "newArticles.xls", I would type...
```
BlogMigrationHelper.exe oldArticles etailwest.wbresearch.com newArticles
```
*Please make sure that oldArticles.txt is in the same directory as where BlogMigrationHelper.exe is*
4. The program will tell you if there are any errors

# How to Install (Method 2, Run with Python 3.7.3)
1. Download or clone this repository
2. Download Python 3.7.3 here:
https://www.python.org/downloads/
3. Install module dependencies with pip
```
pip install –upgrade pip
```
to get the latest version of pip
```
pip install bs4
```
to get BeautifulSoup4, and
```
pip install xlwt
```
to get xlwt
4. Open the terminal/command line in the directory where "BlogMigrationHelper.py" is in.
5. Type "python BlogMigrationHelper.py nameofinputfile siteaddress nameofoutputfile" and press enter.
For example, I want to migrate eTail West articles. I have a list of article links to migrate in "oldArticles.txt" and want the output to be called "newArticles.xls", I would type...
```
python BlogMigrationHelper.py oldArticles etailwest.wbresearch.com newArticles
```
*Please make sure that oldArticles.txt is in the same directory as where BlogMigrationHelper.py is*

# What the program is doing
Blog Migration Helper scrapes the websites and obtain their meta title, meta description, and page content. The URL and content are formatted according to specifications, and they will be nicely laid out on a spreadsheet – **no need to manually keep going back and forth between pages.**
- Generates new internal blog link
brand-strategy-aligning-with-ecommerce-marketplaces-research-ty-u
becomes
blog/brand-strategy-aligning-with-ecommerce-marketplaces-research
**ready to be copied and pasted into the system to set up permanent redirects(!)**
- Removes unnecessary top h1 heading at the top (the new blog feature separates it from the content body)
- Removes bootstrap containers (the blog feature already puts content inside a fully responsive container, so old ones are obsolete)
- Removes old responsive image containers (same reason as above. The new blog feature has its own formatting for that.)
