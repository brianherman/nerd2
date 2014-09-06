import json
from nerdnu.compile import write_json
from nerdnu.compile import reddit
from flask import Markup

def compile():
    r = reddit.Reddit(user_agent='nerd.nu homepage')
    submissions = r.get_subreddit('mcpublic').get_hot(limit=50)
    out = {'creative': [], 'survival': [], 'pve': [], 'chaos': [], 'unknown': []}
    for x in submissions:
        c = x.link_flair_css_class
        out[c if c in out else 'unknown'].append({
            'votes': x.score,
            'title': Markup(x.title).unescape(),
            'author': x.author.name,
            'permalink': x.permalink,
            'num_comments': x.num_comments,
            'url': x.url})
    
    #print out
    write_json('subreddit.json', out)
    
    print "... done"
