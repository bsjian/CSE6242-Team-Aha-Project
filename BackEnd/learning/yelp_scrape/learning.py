# In[1]: importing libs
from six.moves import urllib
from bs4 import BeautifulSoup
import json

# In[2]: this is an example url
url = "https://www.yelp.com/search?find_desc=Restaurants&find_loc=30309"

# In[3]: setup the request header
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

# In[4]: Let's get the request
request = urllib.request.Request(url,headers={'User-Agent': user_agent})
html = urllib.request.urlopen(request).read()
soup = BeautifulSoup(html, 'html.parser')

# In[5]: First lets get the HTML of the table called site Table where all the infos are displayed
main_table = soup.find_all("div",attrs={'class':\
    "lemon--div__373c0__6Tkil searchResult__373c0__1yggB border-color--default__373c0__2oFDT"})
print(main_table)

# In[6]: select a tags with the name
name_a_tags = main_table.find_all('a', attrs={'class':\
    "lemon--a__373c0__1_OnJ link__373c0__29943 link-color--blue-dark__373c0__1mhJo link-size--inherit__373c0__2JXk5"})
print(name_a_tags)
