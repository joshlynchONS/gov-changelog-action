# gov-changelog-action
Github workflow that automatically generates a change-log, using git commits, when a new release is created.

## The Workflow
Copy and paste the following code into your .github\workflows folder. (example of this in this repository)

```shell
name: Generate changelog
on:
  release:
    types: [created, edited]
  workflow_dispatch:

jobs:
  generate-changelog:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0
    - uses: joshlynchONS/gov-changelog-action@main
      with:
        ACCESS_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        PATH: 'CHANGELOG.md'
        UNRELEASED_COMMITS: 'true'
        UPDATE_CHANGELOG: 'true'
```

## Conventional Commit

For this code to work effectively, it is important to follow the commit practice of conventional commits (conventional commit link). This is
effectively adding a prefix to your commit that informs someone of what your commit has done. The prefixes follow the keep a change-log practice
(keep a changelog link) and are listed below:

* add:
    - Description: "Adding a new feature"
    - Heading in changelog: "Added"
    - Shown in changelog: true

* change:
    - Description: "Changes to an existing feature"
    - Heading in changelog: "Changed"
    - Shown in changelog: true

* depreciated:
    - Description: "Updating depreciated code"
    - Heading in changelog: "Depreciated"
    - Shown in changelog: true

* remove:
    - Description: "Removing an existing feature"
    - Heading in changelog: "Removed"
    - Shown in changelog: true

* fix:
    - Description: "Fixing an existing bug"
    - Heading in changelog: "Fixed"
    - Shown in changelog: true

* security:
    - Description: "Improving/removing security concerns"
    - Heading in changelog: "Security"
    - Shown in changelog: true

* docs:
    - Description: "Updating documentation"
    - Heading in changelog: "Added"
    - Shown in changelog: true

* chore:
    - Description: "Any changes that do not effect user experience (e.g. style or refactoring)"
    - Heading in changelog: "Chore"
    - Shown in changelog: false

* "No Prefix":
    - Description: "Any changes that are not labelled correctly"
    - Heading in changelog: "Other"
    - Shown in changelog: true
