import urllib.request
hashid_data = urllib.request.urlopen("https://raw.githubusercontent.com/ninja542/autograde-testing/master/mth314/hashids.py").read()
with open("hashids.py", "wb+") as f:
  f.write(hashid_data)