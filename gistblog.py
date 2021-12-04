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
if args.operation != "create" or "update":
    print("Invalid Operation: only 'create' or 'update' are allowed.")
    exit(1)

# Setup PyGithub
g = Github(args.token)
github_user = g.get_user()

# Start processing all the blog posts
for post in args.blog.split(" "):
    print("Processing {}".format(post))
    post_title = ""
    post_description = ""
    post_file_name = post.split("/")[1]

    # Parse Title and Description out of blog post
    with open(post, encoding="utf-8") as file:
        for line in file:
            if "Title:" in line:
                post_title = line.split("Title:")[1]
            if "Description:" in line:
                post_description = line.split("Description:")[1]
            if post_title and post_description:
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

        # Print out new row for blog table of contents
        print("| Title | Published  | Id |")
        print("| [{}]({}) | {} | {} |".format(
            post_title.replace("\n", ""),
            new_gist.html_url,
            new_gist.created_at.strftime("%Y-%m-%d"),
            post))

    # Update a blog post
    if args.operation == "update":
        all_gists = github_user.get_gists()
        gist_id = ""

        # Find the id of the gist we need to update by looking
        # at all gists and matching on filename of the blog post
        for gist in all_gists:
            if post_file_name in gist.files:
                gist_id = gist.id
                break

        # Update the gist with the new content
        gist_to_update = g.get_gist(gist_id)
        gist_to_update.edit(description=post_description, files={
            post_file_name: InputFileContent(Path(post).read_text(encoding="utf-8"))})

        print(" Updated blog post with Gist ID {}".format(gist_id))
