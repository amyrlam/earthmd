# from pyquery import PyQuery as pq
# from lxml import etree
# import urllib
# d = pq(url='http://www.earthclinic.com/Remedies/acvinegar.html')



from pyquery import PyQuery as pq
 
with open('example.html') as f:
    doc = pq(f.read())