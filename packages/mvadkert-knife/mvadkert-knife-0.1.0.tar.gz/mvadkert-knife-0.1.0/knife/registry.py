import json
import re
import requests

from dataclasses import dataclass, field
from typing import Any, Dict, List
from urllib.parse import urljoin

import typer


app = typer.Typer()


def info(msg: str):
    typer.secho(f"[+] {msg}", fg=typer.colors.GREEN)


def error(msg: str):
    typer.secho(f"[E] {msg}", fg=typer.colors.RED)
    raise typer.Exit(code=1)


@dataclass
class Tag:
    name: str


@dataclass
class Repository:
    name: str
    tags: List[Tag]


@dataclass
class Registry:
    name: str
    repositories: List[Repository]


def delete_resource(
    registry: str,
    endpoint: str,
    err: str = None
):
    url = urljoin(registry, endpoint)

    try:
        response = requests.delete(url)
        response.raise_for_status()

    except requests.exceptions.RequestException as exc:
        err = err or f"Failed to delete '{url}'"
        error(f"{err}: {str(exc)}")


def head_resource(
    registry: str,
    endpoint: str,
    headers = None,
    key = None,
    err: str = None
) -> Any:

    headers = headers or {}
    url = urljoin(registry, endpoint)

    try:
        response = requests.head(url, headers=headers)
        response.raise_for_status()

    except requests.exceptions.RequestException as exc:
        err = err or f"Failed to get head '{url}'"
        error(f"{err}: {str(exc)}")

    return response.headers[key] if key else response.headers


def get_resource(
    registry: str,
    endpoint: str,
    headers = None,
    key: str = None,
    err: str = None
) -> Any:

    headers = headers or {}
    url = urljoin(registry, endpoint)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

    except requests.exceptions.RequestException as exc:
        err = err or f"Failed to get '{url}'"
        error(f"{err}: {str(exc)}")

    try:
        return response.json()[key] if key else response.json()
    except KeyError:
        error(f"Key '{key}' not found in response")


@app.command()
def remove_tags(
    ctx: typer.Context,
    tag_regex: str = typer.Option(..., '--tag', help="Tag to remove specified as regular expression")
):
    registry = ctx.obj

    for repo in registry.repositories:
        for tag in repo.tags:
            if not re.search(tag_regex, tag.name):
                continue

            info(f"Removing '{registry.name}/{repo.name}:{tag.name}")
            digest = head_resource(
                registry.name, f"/v2/{repo.name}/manifests/{tag.name}",
                headers={
                    "Accept": "application/vnd.docker.distribution.manifest.v2+json"
                },
                key="Docker-Content-Digest",
                err=f"Could not get details of tag '{tag.name}'"
            )

            try:
                delete_resource(
                    registry.name, f"v2/{repo.name}/manifests/{digest}",
                    err="Failed to delete image '{registry.name}/{repo.name}:{tag.name}'"
                )
            except typer.Exit:
                continue


@app.callback()
def registry(
    ctx: typer.Context,
    registry: str = typer.Argument(..., help="Container registry host"),
    repository: List[str] = typer.Option([], help="Use given repositories")
):
    info(f"Using registry '{registry}'")

    # check registry access
    get_resource(registry, "v2", err="Could not connect to given registry")

    # get repositories or use those specified on command line
    repository_names = repository or get_resource(registry, "v2/_catalog", key="repositories", err="Could not list repositories")

    repositories = []
    for repo_name in repository_names:

        try:
            tag_names = get_resource(
                registry, f"v2/{repo_name}/tags/list",
                key="tags",
                err=f"Could not list tags for repository {repo_name}"
            )
        except typer.Exit as error:
            continue

        info(f"Found repository '{repo_name}' with {len(tag_names)} tags")

        tags = []
        for tag_name in tag_names:
            tags.append(Tag(tag_name))

        repositories.append(Repository(repo_name, tags))

    ctx.obj = Registry(registry, repositories)


if __name__ == "__main__":
    app()
