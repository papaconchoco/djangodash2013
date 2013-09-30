import json
from text.blob import TextBlob

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from libsaas.http import HTTPError
from libsaas.services.github import GitHub


def home_view(request):
    return render(request, 'hatersgonnagit/home.html', {})


@login_required
def repo_view(request, repo_user, repo_name):
    sa = request.user.social_auth.get()
    gh = GitHub(sa.tokens)
    repo = gh.repo(repo_user, repo_name).get()
    return render(request, 'hatersgonnagit/repo.html', {
        'repo': repo,
    })


@login_required
def commits_view(request, repo_user, repo_name):
    sa = request.user.social_auth.get()
    gh = GitHub(sa.tokens)
    repo = gh.repo(repo_user, repo_name)
    committers = {}
    try:
        commits = repo.commits().get(per_page=100)
    except HTTPError:
        return HttpResponse(json.dumps(committers),
                            content_type="application/json")
    for commit in commits:
        committer = commit['commit']['committer']['name']
        try:
            committer = commit['author']['login']
            meta = commit['author']
        except TypeError:
            # Sometimes 'author' and 'committer' fields are null
            meta = None
        if committer not in committers:
            committers[committer] = {
                'pos': 0,
                'neg': 0,
                'meta': meta,
            }
        message = commit['commit']['message']
        # We use pattern because NLTK NaiveBayesAnalyzer is too slow
        blob = TextBlob(message)
        polarity, subjectivity = blob.sentiment
        if polarity >= 0.1:
            committers[committer]['pos'] += 1
        else:
            committers[committer]['neg'] += 1
    return HttpResponse(json.dumps(committers),
                        content_type="application/json")


@login_required
def comments_view(request, repo_user, repo_name):
    sa = request.user.social_auth.get()
    gh = GitHub(sa.tokens)
    repo = gh.repo(repo_user, repo_name)
    users = {}
    try:
        comments = repo.commits().comments().get(per_page=100)
    except HTTPError:
        return HttpResponse(json.dumps(users),
                            content_type="application/json")
    for comment in comments:
        user = comment['user']['login']
        meta = comment['user']
        if user not in users:
            users[user] = {
                'pos': 0,
                'neg': 0,
                'meta': meta,
            }
        text = comment['body']
        blob = TextBlob(text)
        polarity, subjectivity = blob.sentiment
        if polarity >= 0.1:
            users[user]['pos'] += 1
        else:
            users[user]['neg'] += 1
    return HttpResponse(json.dumps(users),
                        content_type="application/json")


@login_required
def issues_view(request, repo_user, repo_name):
    sa = request.user.social_auth.get()
    gh = GitHub(sa.tokens)
    repo = gh.repo(repo_user, repo_name)
    users = {}
    try:
        issues = repo.issues().get()
    except HTTPError:
        return HttpResponse(json.dumps(users),
                            content_type="application/json")
    for issue in issues:
        user = issue['user']['login']
        meta = issue['user']
        if user not in users:
            users[user] = {
                'pos': 0,
                'neg': 0,
                'meta': meta,
            }
        for element in ['title', 'body']:
            text = issue[element]
            blob = TextBlob(text)
            polarity, subjectivity = blob.sentiment
            if polarity >= 0.1:
                users[user]['pos'] += 1
            else:
                users[user]['neg'] += 1
        if issue['comments'] > 0:
            issue_number = issue['number']
            comments = repo.issue(issue_number).comments().get(per_page=100)
            for comment in comments:
                user = comment['user']['login']
                meta = comment['user']
                if user not in users:
                    users[user] = {
                        'pos': 0,
                        'neg': 0,
                        'meta': meta,
                    }
                text = comment['body']
                blob = TextBlob(text)
                polarity, subjectivity = blob.sentiment
                if polarity >= 0.1:
                    users[user]['pos'] += 1
                else:
                    users[user]['neg'] += 1
    return HttpResponse(json.dumps(users),
                        content_type="application/json")
