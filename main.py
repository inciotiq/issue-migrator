import time
import requests
import csv

# export your issues from gitlab as csv
ISSUES_CSV_FILENAME = 'iotiq-coworking-coworkingapi_issues_2023-01-20.csv'
# paste your repo url
REPO_URL = 'https://api.github.com/repos/{organization}/{repo}/issues'
# create a fine grain token with issue permissions
GITHUB_TOKEN = '<github token>'


def parse_issues():
    filename = ISSUES_CSV_FILENAME

    with open(filename) as f:
        reader = csv.DictReader(f)
        list_of_dict = list(reader)

    # print(list_of_dict)
    return list_of_dict


def issue_desc(issue):
    return issue.get('Description') \
        + '\nCreated by: ' + issue.get('Author Username') \
        + '\nCreated at: ' + issue.get('Created At (UTC)') \
        + '\nGitlab link: ' + issue.get('URL')


def send_issue(issue):
    data = {
        'title': issue.get('Title'),
        'body': issue_desc(issue)
    }

    headers = {'Authorization': ('Bearer %s' % GITHUB_TOKEN),
               'Accept': 'application/vnd.github+json',
               'X-GitHub-Api-Version': '2022-11-28',
               'Content-Type': 'application/json'}
    response = requests.post(REPO_URL, json=data, headers=headers)
    # print(response)
    return response


issues = parse_issues()

for issue in issues:
    res = send_issue(issue)
    print(issue.get('Title'), res)

    if res.status_code != 201:
        print('could not send, will try again after a minute')
        print(issue)
        time.sleep(60)
        send_issue(issue)
