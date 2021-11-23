#!/usr/bin/env python
# coding: utf-8
from time import sleep
import requests
import json




author_ids = [
    (1745524,    'Tim'),
    (2230578,    'Leilani'),
    (143711421,  'Alex'),
]


endpoint = 'https://api.semanticscholar.org/graph/v1/author/{:d}?fields=papers.authors,papers.year,papers.venue,papers.title,papers.url'


papers = {}
# using dict to de-duplicate

for author_id, name in author_ids:
    print(f'Getting papers by {name}')
    response = requests.get(endpoint.format(author_id))
    response = response.json()
    print(f'Got {len(response["papers"]):,d} papers.')
    
    for paper in response['papers']:
        papers[ paper['paperId'] ] = paper
    
    sleep(2)

print(f'Finished. Got {len(papers):,d} papers total.')


def format_authors(authors):
    author_strs = []
    for author in authors:
        if (author['authorId'] is not None) and (int(author['authorId']) in author_ids):
            author_strs.append('**'+author['name']+'**')
        else:
            author_strs.append(author['name'])
            
    return ', '.join(author_strs)


def format_long_authors(authors):
    if len(authors) > 6:
        author_str = format_authors(authors[:6])
        return author_str + ', *et al.*'
    else:
        return format_authors(authors)


def format_paper(paper):
    
    title_str = '**[{title}]({url})**'.format(**paper)
    
    venue_str = '*{venue}*'.format(**paper) if len(paper['venue'])>0 else ''
    year_str  = '{year}'.format(**paper) if paper['year'] is not None else ''
    
    authors = format_long_authors(paper['authors'])
    
    return f'{title_str}\n\n{authors}\n\n{venue_str} {year_str}\n\n   ' # <--- these spaces are important as they indicate a paragraph break

 
def get_year(paper):
    try: return int( paper['year'] )
    except:
        return 1900


with open('../publications.md', 'w') as f:
    for paper in sorted(papers.values(), key=get_year, reverse=True):
        f.write( format_paper(paper) )
        f.write(4*'\n')
        
print(f'Finished writing {len(papers):,d} papers to markdown.')