import os

from src.readme_generator import generate_readme


def test_generates_readme():
    title = ""
    description = ""
    repo_name = ""
    github_handle = ""
    before = os.listdir()
    assert "GENERATED.md" not in before
    generate_readme(title, description, repo_name, github_handle)
    after = os.listdir()
    assert "GENERATED.md" in after
    os.remove("GENERATED.md")
