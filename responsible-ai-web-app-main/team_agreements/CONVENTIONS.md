# Conventions Agreement

`V1.1 - 19/04/2023`

<br>

## Table of Contents

- [Conventions Agreement](#conventions-agreement)
  - [Table of Contents](#table-of-contents)
  - [1. Code Conventions](#1-code-conventions)
    - [1.1 General Code Conventions](#11-general-code-conventions)
    - [1.2 Python Code Conventions](#12-python-code-conventions)
    - [1.3 Jupyter Notebook Conventions](#13-jupyter-notebook-conventions)
  - [2. Scrum Conventions](#2-scrum-conventions)
    - [2.1 Scrum Roles](#21-scrum-roles)
    - [2.2 Scrum Events](#22-scrum-events)
    - [2.3 Scrum Artifacts](#23-scrum-artifacts)
  - [3. Git](#3-git)
    - [3.1 Commit Messages](#31-commit-messages)
    - [3.2 Branch Naming](#32-branch-naming)
    - [3.3 Pull Request Guidelines](#33-pull-request-guidelines)
  - [4. Compliance](#4-compliance)


## 1. Code Conventions

This section outlines the conventions used for all code produced related to the project.

### 1.1 General Code Conventions

The Parties agree to adhere to the following general code conventions for the Code:

- Use descriptive variable names that accurately describe the purpose of the variable.

- Use consistent indentation using tabs.

- Use comments to explain code blocks and highlight any significant changes.

- Use whitespace to improve the readability of the Code.

### 1.2 Python Code Conventions

The Parties agree to adhere to the following specific code conventions for writing Python code:

- Follow [PEP 8](https://peps.python.org/pep-0008/) guidelines for Python code.

- Use lowercase with underscores for variable and function names.

- Use uppercase with underscores for constant names.

- Use single quotes for string literals unless the string contains a single quote.

- Use docstring's to document all classes, functions, and modules.

### 1.3 Jupyter Notebook Conventions

The Parties agree to adhere to the following specific conventions for writing Jupyter Notebooks:

- Use Markdown cells to explain the purpose of the notebook and any major changes.

- Use Markdown headers to structure the notebook.

- Use Markdown text to explain code blocks and highlight any significant changes.

- Use whitespace to improve the readability of the notebook.

> See the [Markdown Guide](https://www.markdownguide.org/basic-syntax/) for more information on Markdown

## 2. Scrum Conventions

This section outlines the conventions for implementing Scrum.

### 2.1 Scrum Roles

The Parties agree to the following Scrum roles:

- **Product Owner**: The Product Owner is responsible for maximizing the value of the product and managing the Product Backlog.

- **Scrum Master**: The Scrum Master is responsible for ensuring that Scrum is understood and enacted, and for facilitating the Scrum Team's progress.

- **Development Team**: The Development Team is responsible for delivering a potentially releasable Increment of the product at the end of each Sprint.

### 2.2 Scrum Events

The Parties agree to the following Scrum events:

- **Sprint**: The Parties agree to have a Sprint length of 2 weeks.

- **Sprint Planning**: At the beginning of each Sprint, the Product Owner and Development Team will collaborate to create a Sprint Goal and select items from the Product Backlog that they can complete during the Sprint.

- **Daily Scrum**: The Development Team will hold a Daily Scrum meeting to inspect progress toward the Sprint Goal and adapt the Sprint Backlog as necessary.

- **Sprint Review**: At the end of each Sprint, the Development Team will demonstrate the work done during the Sprint to the Product Owner and other stakeholders, and gather feedback to help refine the Product Backlog.

- **Sprint Retrospective**: After the Sprint Review, the Development Team will hold a Sprint Retrospective to inspect and adapt their processes and identify areas for improvement.

### 2.3 Scrum Artifacts

The Parties agree to the following Scrum artifacts:

- **Product Backlog**: The Product Owner is responsible for maintaining the Product Backlog, which is an ordered list of items that describe the work to be done on the product.

- **Sprint Backlog**: The Development Team is responsible for creating and maintaining the Sprint Backlog, which is a list of items selected from the Product Backlog that the Development Team plans to complete during the Sprint.

- **Increment**: At the end of each Sprint, the Development Team will deliver a potentially releasable Increment of the product, which is a usable and valuable piece of the product that meets the Definition of Done.

> See the [Scrum Guide](https://scrumguides.org/scrum-guide.html) for more information on Scrum

## 3. Git

This section outlines the conventions for working with git.

### 3.1 Commit Messages

The Parties agree to the following commit-message conventions:

- Keep it concise: Aim for short, descriptive messages that summarize the changes made in the commit.
- Use the imperative mood: Write commit messages in the imperative mood (e.g., "Add feature X" instead of "Added feature X").
- Separate subject and body: If necessary, use the subject line to summarize the changes and add a more detailed explanation in the body of the message.
- Reference issues: If the commit is related to an issue or ticket, include a reference to it in the commit message. For example, "Fix issue #123" or "Implement feature X (closes #456)".
- Use present tense: Write commit messages in the present tense, as if describing the changes as they are happening.

### 3.2 Branch Naming

The Parties agree to the following branch naming conventions:

- Use descriptive names: Aim for branch names that clearly indicate what the branch is for. For example, "feature/add-user-authentication" or "bugfix/fix-login-issue".
- Use lowercase letters: Branch names should be written in lowercase letters, as this is the convention in Git.
- Use hyphens: Use hyphens to separate words in branch names (e.g., "feature/new-ui" instead of "feature_new_ui").
- Include the issue number: If the branch is related to an issue or ticket, include the issue number in the branch name (e.g., "feature/123-add-user-authentication").

### 3.3 Pull Request Guidelines

The Parties agree to the following pull-request conventions:

- Keep it small: Aim for small, focused pull requests that address a single issue or feature. This makes it easier for reviewers to understand and test the changes.
- Include a description: Provide a detailed description of the changes made in the pull request, including any relevant context or background information.
- Include tests: If applicable, include tests that cover the changes made in the pull request.
- Request reviews: Request reviews from relevant team members or stakeholders before merging the pull request.
- Resolve conflicts: If there are conflicts with the main code-base, resolve them before merging the pull request.
- Include issue number: If the pull request is related to an issue or ticket, include the issue number in the pull request description or title.

> See the [Git Reference](https://git-scm.com/docs) for more information on Git

## 4. Compliance

All parties agree to comply with the code conventions set forth in this Agreement. If a Party fails to comply with the code conventions, the other Party may notify them in writing and request that they make the necessary corrections.
