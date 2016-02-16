import requests
from bs4 import BeautifulSoup


def page_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html5lib")
    words = words_count(soup)
    print "The number of words on your webpage is %d." % words
    forms = forms_count(soup)
    print "Your webpage has %d forms and a total of %d input fields (including hidden ones)." % (len(forms),sum(forms))
    print "Oh, so you want more detail?  The number of input fields for each form is as follows:"
    print forms
    print "There are %d links overall and %d of them are external links." % links_count(soup)
    links = links_count(soup)
    return (words, forms, links)


def words_count(soup):
    n = 0
    for s in soup.strings:
        if s.parent.name not in ['script','style','head','title']:
            n = n + len(s.split())
    return n

def forms_count(soup):
    forms = []
    for form in soup.findAll('form'):
        forms.append(len([i for i in form.findAll('input')]))
    return forms

def links_count(soup):
    links = 0
    external_links = 0
    for link in soup.findAll('a'):
        if link.has_attr('href'):
            links = links + 1
            if link['href'].find("http") == 0:
                external_links = external_links + 1
    return (links, external_links)



if __name__ == "__main__":
    parsepage("http://www.google.com")