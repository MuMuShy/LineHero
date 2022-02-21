import urllib.request


url = "https://bybitline.herokuapp.com/"
conn = urllib.request.urlopen(url)
for key, value in conn.getheaders():
    print(key, value)