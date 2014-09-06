from github3 import login

class GithubTask(object):
    out = []
    gh = login(username=None, password=None, token='3cbad1dfffbf983a2577a0c7d094254fea041fb0')
    repo = gh.repository('NerdNu', 'NerdBugs')
    for issue in repo.list_issues():
        t = {'title': issue.title,
             'url': issue.html_url,
             'author': issue.user.login,
             'num_comments': issue.comments,
             'tags': [l.name for l in issue.labels]}
        out.append(t)
    write_json('github.json', out)
    print "... done"
