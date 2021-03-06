from libsaas.services.github import GitHub

from django.conf import settings


def project_name(request):
    return {
        "PROJECT_NAME": settings.PROJECT_NAME,
    }


def github(request):
    try:
        sa = request.user.social_auth.get()
        gh = GitHub(sa.tokens)
        repos = gh.repos().get(type='all')
        user = gh.user().get()
    except:
        user = {}
        repos = []
    sorted_repos = sorted(repos, key=lambda repo: -repo['watchers'])
    return {
        "gh_user": user,
        "gh_repos": sorted_repos,
    }
