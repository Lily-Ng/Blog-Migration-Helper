'''
Runs BlogMigrationHelper for an entire batch of article listing pages, for window machines only.
'''
import os
import sys

# Run Blog MigrationHelper for article listing
def executeMigration(listingAddr, siteName):
    os.system("python BlogMigrationHelper.py "+listingAddr+" "+siteName+"Migration")

# Read the list of article listing pages from "migrationSource.txt" in the current directory
def readInputFile():
    with open("migrationSource.txt") as inputFile:
        for articleListing in inputFile:
            if articleListing == "":
                continue
            articleListing = (articleListing.strip().replace("https://", "")).rstrip("/")
            siteName = articleListing.split(".")[0]
            executeMigration(articleListing, siteName)
            
def main():
    if os.name != "nt":
        sys.exit()
    readInputFile()

if __name__ == "__main__":
    main()
