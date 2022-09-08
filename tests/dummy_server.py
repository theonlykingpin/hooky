import base64

from aiohttp import web
from aiohttp.abc import Request
from aiohttp.web_response import Response, json_response


async def repo_details(request: Request) -> Response:
    github_base_url = request.app['dynamic']['github_base_url']
    org = request.match_info['org']
    repo = request.match_info['repo']
    return json_response({'url': f'{github_base_url}/repos/{org}/{repo}', 'full_name': f'{org}/{repo}'})


async def pull_details(request: Request) -> Response:
    github_base_url = request.app['dynamic']['github_base_url']
    org = request.match_info['org']
    repo = request.match_info['repo']
    pull_number = request.match_info['pull_number']
    return json_response(
        {
            'url': f'{github_base_url}/repos/{org}/{repo}/pulls/{pull_number}',
            'issue_url': f'{github_base_url}/repos/{org}/{repo}/issues/{pull_number}',
            'base': {
                'label': 'foobar:main',
                'ref': 'main',
                'sha': 'abc1234',
                'repo': {'url': f'{github_base_url}/repos/{org}/{repo}', 'full_name': f'{org}/{repo}'},
            },
        }
    )


async def pull_files(_request: Request) -> Response:
    return json_response(
        [
            {
                'deletions': 0,
                'additions': 1,
                'changes': 2,
                'filename': 'changes/123-foobar.md',
                'sha': 'abc',
                'status': 'added',
            }
        ]
    )


async def pull_commits(request: Request) -> Response:
    github_base_url = request.app['dynamic']['github_base_url']
    org = request.match_info['org']
    repo = request.match_info['repo']
    return json_response(
        [{'sha': 'abc', 'url': f'{github_base_url}/repos/{org}/{repo}/commits/abc', 'commit': {'message': 'foobar'}}]
    )


async def update_status(_request: Request) -> Response:
    return json_response({})


async def comment_details(request: Request) -> Response:
    github_base_url = request.app['dynamic']['github_base_url']
    org = request.match_info['org']
    repo = request.match_info['repo']
    comment_id = request.match_info['comment_id']
    return json_response({'url': f'{github_base_url}/repos/{org}/{repo}/comments/{comment_id}'})


async def comment_reaction(_request: Request) -> Response:
    return json_response({})


async def get_labels(_request: Request) -> Response:
    return json_response({})


async def add_labels(_request: Request) -> Response:
    return json_response({})


async def add_assignee(_request: Request) -> Response:
    return json_response({'assignees': []})


async def remove_assignee(_request: Request) -> Response:
    return json_response({'assignees': []})


pyproject_toml = b"""
[tool.hooky]
reviewers = ['user1', 'user2']
"""


async def py_project_content(_request: Request) -> Response:
    return json_response({'content': base64.b64encode(pyproject_toml).decode(), 'encoding': 'base64', 'type': 'file'})


async def repo_apps_installed(request: Request) -> Response:
    assert request.headers['Accept'] == 'application/vnd.github+json'
    return json_response({'id': '654321'})


async def installation_access_token(request: Request) -> Response:
    assert request.headers['Accept'] == 'application/vnd.github+json'
    return json_response({'token': 'foobar'})


async def catch_all(request: Request) -> Response:
    print(f'{request.method}: {request.path} 404')
    return Response(body=f'{request.method} {request.path} 404', status=404)


routes = [
    web.get('/repos/{org}/{repo}', repo_details),
    web.get('/repos/{org}/{repo}/pulls/{pull_number}', pull_details),
    web.get('/repos/{org}/{repo}/pulls/{pull_number}/files', pull_files),
    web.get('/repos/{org}/{repo}/pulls/{pull_number}/commits', pull_commits),
    web.post('/repos/{org}/{repo}/statuses/{commit}', update_status),
    web.get('/repos/{org}/{repo}/issues/comments/{comment_id}', comment_details),
    web.post('/repos/{org}/{repo}/comments/{comment_id}/reactions', comment_reaction),
    web.get('/repos/{org}/{repo}/issues/{issue_id}/labels', get_labels),
    web.post('/repos/{org}/{repo}/issues/{issue_id}/labels', add_labels),
    web.post('/repos/{org}/{repo}/issues/{issue_id}/assignees', add_assignee),
    web.delete('/repos/{org}/{repo}/issues/{issue_id}/assignees', remove_assignee),
    web.get('/repos/{org}/{repo}/contents/pyproject.toml', py_project_content),
    web.get('/repos/{org}/{repo}/installation', repo_apps_installed),
    web.post('/app/installations/{installation}/access_tokens', installation_access_token),
    web.route('*', '/{path:.*}', catch_all),
]
