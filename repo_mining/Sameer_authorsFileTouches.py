import json
import requests
import csv

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if not jsonCommits or len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                
                #
               
                filesjson = shaDetails.get('files',[])
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if findSourceFile(filename):
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                        print(filename)
                    

            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

# Source code files
# languages used from repo
sourceFiles = {".java", ".kt", ".cpp", ".h", ".c"}

def findSourceFile(filename):
    for ext in sourceFiles:
        if filename.endswith(ext):
            return True
    return False

# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = [""]

repo = "scottyab/rootbeer"
# :3
