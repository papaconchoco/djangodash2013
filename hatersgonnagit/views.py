import json
from text.blob import TextBlob

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

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
    commits = repo.commits().get()
    committers = {}
    for commit in commits:
        try:
            committer = commit['committer']['login']
            meta = commit['committer']
        except TypeError:
            # Sometimes 'author' and 'committer' fields are null
            committer = commit['commit']['committer']['name']
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
    return HttpResponse(json.dumps({}),
                        content_type="application/json")


@login_required
def issues_view(request, repo_user, repo_name):
    sa = request.user.social_auth.get()
    gh = GitHub(sa.tokens)
    repo = gh.repo(repo_user, repo_name)
    return HttpResponse(json.dumps({}),
                        content_type="application/json")
