import requests
import json


# this method is used to find 5 the most repositories by key words
def search_popular_repos(keywords):
    keywords.replace(" ", "+")
    # creating url of request with given key words
    url = 'https://api.github.com/search/repositories?q=' + keywords + '&sort=stars&order=desc'
    r = requests.get(url)
    # if response is ok
    if r.ok:
        data = json.loads(r.text)
        # check if there are more or equal to 5 items in the response
        if len(data['items']) >= 5:
            for i in range(5):
                print(json.dumps(data['items'][i]['html_url']))
        else:
            # if number of items in the response less then 5, print all of them
            for i in range(len(data['items'])):
                print(json.dumps(data['items'][i]['html_url']))


search_popular_repos('java language')
