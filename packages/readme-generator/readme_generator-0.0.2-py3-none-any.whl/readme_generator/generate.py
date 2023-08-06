from .template import template


def generate_readme(
    title: str,
    description: str,
    repo_name: str,
    github_handle: str,
):
    readme = template.format(
        title,
        description,
        github_handle,
        repo_name,
        github_handle,
        repo_name,
        github_handle,
        repo_name,
        github_handle,
        repo_name,
        github_handle,
        repo_name,
        github_handle,
        repo_name,
        github_handle,
        repo_name,
    )
    with open("./GENERATED.md", "w+") as f:
        f.write(readme)
