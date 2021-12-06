# Gistblog Action

The Gistblog [GitHub Action](https://github.com/features/actions) is [part of an opinionated setup](https://github.com/seajoshc/gistblog) that lets you use GitHub Gists as a blogging engine. I strongly urge you to [read this first](https://github.com/seajoshc/gistblog#readme). You can also [checkout this blogpost](https://gist.github.com/seajoshc/9a3ee57dd7f380b5d6ce2a17805013c8) for more info about Gistblog.

## Inputs

This action expects three things in order: a [GitHub Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with "gist" scope, either the "create" or "update" command, and a space delimited list of blog post (markdown) files to process. Create a [secret within the repo you're using](https://docs.github.com/en/actions/security-guides/encrypted-secrets) named GISTS_TOKEN and store the value of the aforementioned personal access token. The secret can be securely accessed as shown in the below examples.

## gists-token

- description: A valid GitHub Personal Access Token with "gist" scope.
- required: true

## operation

- description: The operation to perform either "create" or "update".
- required: true

## blog-files

- description: A space delimited list of files to process.
- required: true

## Outputs

None.

## Example usage

[As per the opinionated setup guide](https://github.com/seajoshc/gistblog#readme), the best way to consume this action is by including it in a workflow that will find the appropriate files to manage as blog posts and feed them into this action for handling the Gists. The full Gistblog workflow is:

```yaml
name: Gistblog
on:
  push:
    branches:
      - main
jobs:
  gistblog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: dorny/paths-filter@v2
        id: blog
        with:
          list-files: shell
          filters: |
            create_blog:
            - added: 'blog/*.md'
            update_blog:
            - modified: 'blog/*.md'
      - if: steps.blog.outputs.create_blog == 'true'
        uses: seajoshc/gistblog-action@v1
        with:
          gists-token: ${{ secrets.GISTS_TOKEN }}
          operation: create
          blog-files: "${{ steps.blog.outputs.create_blog_files }}"
      - if: steps.blog.outputs.update_blog == 'true'
        uses: seajoshc/gistblog-action@v1
        with:
          gists-token: ${{ secrets.GISTS_TOKEN }}
          operation: update
          blog-files: "${{ steps.blog.outputs.update_blog_files }}"
```

But the most basic usage examples would be:

```yaml
uses: seajoshc/gistblog-action@v1
with:
  gists-token: ${{ secrets.GISTS_TOKEN }}
  operation: create
  blog-files: "blog/filename.md"
```

```yaml
uses: seajoshc/gistblog-action@v1
with:
  gists-token: ${{ secrets.GISTS_TOKEN }}
  operation: update
  blog-files: "blog/filename.md blog/otherfile.md"
```
