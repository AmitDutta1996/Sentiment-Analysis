from bs4 import BeautifulSoup as soup
from textblob import TextBlob
from requests import get
from contextlib import closing


def analyzer(url):
    scrap_url = url
    with closing(get(scrap_url, stream=True)) as resp:
        page_html = resp.content
    page_soup = soup(page_html, 'html.parser')
    containers = page_soup.find_all('div', {'class': 'text_content'})
    i = 0;
    for container in containers:
        i += 1
        print(str(i) + ' .')
        if len(container.text.split('|')) > 1:
            x = container.text.split('|')[1].strip()
        else:
            x = container.text.split('|')[0].strip()
        print(x + '\n')
        blob = TextBlob(x)
        print(blob.sentiment)
        grader(blob)
        print('\n\n')

def grader(blob):
    pol_grade = 'NA'
    sub_grade = 'NA'
    pol=blob.polarity
    sub=blob.subjectivity
    if pol>0:
        if pol < 0.2:
            pol_grade = 'Slightly Positive'
        if (pol >= 0.2) and (pol < 0.6):
            pol_grade = 'Moderately Positive'
        if (pol >= 0.6) and (pol < 1):
            pol_grade = 'Highly Positive'
        if pol == 1:
            pol_grade = 'Extremely Positive'

    elif pol == 0:
        pol_grade = 'Neutral'

    else:
        if pol > -0.2:
            pol_grade = 'Slightly Negative'
        if (pol > -0.6) and (pol <= -0.2):
            pol_grade = 'Moderately Negative'
        if (pol > -1) and (pol <= -0.6):
            pol_grade = 'Highly Negative'
        if pol == -1:
            pol_grade = 'Extremely Negative'
    print('\nStatement Sentiment:'+pol_grade)
    if 0 <= sub < 0.3:
        sub_grade = 'Low Subjectivity'
    elif 0.3 <= sub < 0.7:
        sub_grade = 'Moderate Subjectivity'
    elif 0.7 <= sub < 1:
        sub_grade = 'High Subjectivity'
    else:
        sub_grade = 'Extreme Subjectivity'
    print('\nSubjectivity:' + sub_grade)


url = input('Enter url:')
analyzer(url)