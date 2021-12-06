#!/usr/bin/env python3
"""
Blog your little heart out using GitHub Gists.
"""

import argparse
from pathlib import Path

from github import Github, InputFileContent

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("token", help="GitHub Personal Access Token with only 'Gists' scope. More info at https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token.")
parser.add_argument("operation", help="create or update")
parser.add_argument(
    "blog", help="Space delimited list of all files to upload to Gists.")
args = parser.parse_args()
print("Blog posts to process\n {}\n  {}".format(args.operation, args.blog))

# Validate arguments
if args.operation not in "create, update":
    print("Invalid Operation: only 'create' or 'update' are allowed.")
    exit(1)

# Setup PyGithub
g = Github(args.token)
github_user = g.get_user()

###
# Start processing all the blog posts
###
for post in args.blog.split(" "):
    print("Processing {}".format(post))
    post_file_name = "gistblog_" + post.split("/")[1]
    post_description = post_file_name  # default to file name

    # Parse description out of blog post if there
    with open(post, encoding="utf-8") as file:
        for line in file:
            if "post_description:" in line:
                post_description = line.split("post_description:")[1]
                break

    # Create new blog posts
    if args.operation == "create":
        # Create a dict with the file name and content
        d = {}
        d[post_file_name] = InputFileContent(
            Path(post).read_text(encoding="utf-8"))

        # Create a new gist
        new_gist = github_user.create_gist(True, d, post_description)
        print(" Created new blog post with Gist ID: {}".format((new_gist.id)))

    # Update a blog post
    if args.operation == "update":
        all_gists = github_user.get_gists()
        gist_to_update = None

        # Find the id of the gist we need to update by looking
        # at all gists and matching on filename of the blog post
        for gist in all_gists:
            if post_file_name in gist.files:
                gist_to_update = gist
                break

        gist_to_update.edit(description=post_description, files={
            post_file_name: InputFileContent(Path(post).read_text(encoding="utf-8"))})

        print(" Updated blog post with Gist ID {}".format(gist_to_update.id))

###
# Managing the Table of Contents (ToC)
###
all_gists = github_user.get_gists()
toc_gist = None
gistblogs = []

# Look through all the user's gists so we can:
# 1. Find the ToC gist, if it exists
# 2. Find any gist that is a gistblog post
for gist in all_gists:
    if "gistblog-table-of-contents.md" in gist.files:
        toc_gist = gist
        continue
    if any(key.startswith("gistblog_") for key in gist.files):
        gistblogs.append(gist)

# Build the Table of Contents markdown file
table = "| Post | Published |"  # Header row
table += "\n| ---- | --------- |"
for post in gistblogs:
    table += ("\n| [{}]({}) | {} |".format(
        post.description.replace("\n", ""),
        post.html_url,  # TODO this should be the long form URL with the GH username,
        post.created_at.strftime("%Y-%m-%d")
    ))

toc = {}
toc['gistblog-table-of-contents.md'] = InputFileContent(table)

# Update ToC if we found one, otherwise create it
if toc_gist:
    toc_gist.edit(description="Blog Table of Contents", files=toc)
else:
    github_user.create_gist(public=True, files=toc,
                            description="Blog Table of Contents")
