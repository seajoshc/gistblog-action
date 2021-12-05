# Blog your little &lt;3 out using GitHub Gists.

This action is part of an opinionated setup that lets you use GitHub Gists as a blogging engine. You'll need to follow the setup below carefully in order for this to be used properly.

# Setup

Create a new [GitHub Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with the `gist` scope.

Create a repo.

Create a [secret for the repo](https://docs.github.com/en/actions/security-guides/encrypted-secrets) named GISTS_TOKEN.

Create a `blog/` directory in your repo. Blog files should be `markdown` (.md) files.

Add `.github/workflows/gistblog.yaml` with the following contents:

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
        uses: seajoshc/gistblog@v1
        with:
          gists-token: ${{ secrets.GISTS_TOKEN }}
          operation: create
          blog-files: "${{ steps.blog.outputs.create_blog_files }}"
      - if: steps.blog.outputs.update_blog == 'true'
        uses: seajoshc/gistblog@v1
        with:
          gists-token: ${{ secrets.GISTS_TOKEN }}
          operation: update
          blog-files: "${{ steps.blog.outputs.update_blog_files }}"
```

Add or updated your markdown files in the `blog/` directory and your workflow will now automatically turn them into, or update, Gists.

Check build output to get a markdown table that contains info about new blog posts so you can add them to someplace like your [personal README](https://github.com/seajoshc)
