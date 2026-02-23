#!/usr/bin/env python3
import os
import re
import sys
import subprocess

try:
    import requests
except ImportError:
    print('The "requests" package is required. Install it with "pip install requests".')
    sys.exit(1)

MARKER_START = '<!-- START_LATEST_PROJECTS -->'
MARKER_END = '<!-- END_LATEST_PROJECTS -->'
README_PATH = 'README.md'


def get_owner():
    repo = os.environ.get('GITHUB_REPOSITORY')
    if repo and '/' in repo:
        return repo.split('/')[0]
    return os.environ.get('REPO_OWNER') or 'AtaCanYmc'


def fetch_repos(owner, per_page=5, token=None):
    url = f'https://api.github.com/users/{owner}/repos'
    params = {'per_page': per_page, 'sort': 'updated', 'type': 'owner'}
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'token {token}'
    r = requests.get(url, params=params, headers=headers, timeout=30)
    r.raise_for_status()
    items = r.json()
    # filter archived and forks
    items = [it for it in items if not it.get('fork') and not it.get('archived')]
    return items[:per_page]


def format_markdown_list(repos):
    lines = []
    for repo in repos:
        name = repo.get('name')
        url = repo.get('html_url')
        desc = repo.get('description') or ''
        desc = ' '.join(desc.splitlines()).strip()
        if desc:
            lines.append(f'- [{name}]({url}) — {desc}')
        else:
            lines.append(f'- [{name}]({url})')
    return '\n'.join(lines)


def update_readme(content_block):
    with open(README_PATH, 'r', encoding='utf-8') as f:
        readme = f.read()

    pattern = re.compile(r'(' + re.escape(MARKER_START) + r')(.*?)(' + re.escape(MARKER_END) + r')', re.S)
    if not pattern.search(readme):
        print('Markers not found in README — make sure START/END markers exist')
        sys.exit(2)

    replacement = MARKER_START + '\n' + content_block + '\n' + MARKER_END
    new_readme = pattern.sub(replacement, readme)

    if new_readme == readme:
        print('No changes to README necessary.')
        return False

    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(new_readme)
    print('README updated.')
    return True


def git_commit_push():
    subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], check=True)
    subprocess.run(['git', 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com'], check=True)
    subprocess.run(['git', 'add', README_PATH], check=True)
    # commit may fail if no changes — handle that
    res = subprocess.run(['git', 'commit', '-m', 'chore: update latest projects in README'], check=False)
    if res.returncode != 0:
        print('Nothing to commit.')
        return
    subprocess.run(['git', 'push'], check=True)
    print('Changes pushed.')


def main():
    owner = get_owner()
    per_page = int(os.environ.get('NUM_PROJECTS', '5'))
    token = os.environ.get('GITHUB_TOKEN')

    print(f'Fetching latest repos for owner: {owner}')
    repos = fetch_repos(owner, per_page=per_page, token=token)
    if not repos:
        print('No repositories found (after filtering).')
        sys.exit(0)

    md = format_markdown_list(repos)

    changed = update_readme(md)
    if changed:
        git_commit_push()


if __name__ == '__main__':
    main()

