# Contributing to Fabricius

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. See the [Table of Contents](#table-of-contents) for different ways to help and details about how this project handles them. Please make sure to read the relevant section before making your contribution. It will make it a lot easier for us maintainers and smooth out the experience for all involved. The community looks forward to your contributions. 🎉

> And if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
>
> - Star the project
> - Tweet about it
> - Refer this project in your project's README
> - Mention the project at local meetups and tell your friends/colleagues

<!-- omit in toc -->
## Table of Contents

- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Your First Code Contribution](#your-first-code-contribution)
- [Improving The Documentation](#improving-the-documentation)
- [Styleguides](#styleguides)
- [Commit Messages](#commit-messages)

## I Have a Question

> If you want to ask a question, we assume that you have read the available [Documentation](https://fabricius.readthedocs.io).

Before you ask a question, it is best to search for existing [Issues](https://github.com/Predeactor/Fabricius/issues) that might help you. In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Join the [Discord Server](https://discord.gg/aPVupKAxxP)
- Open an [Issue](https://github.com/Predeactor/Fabricius/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions (Python, OS, etc.), depending on what seems relevant.

We will then take care of the issue as soon as possible.

## I Want To Contribute

> ### Legal Notice
>
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project license.

### Reporting Bugs

#### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible.

- Make sure that you are using the latest version.
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions (Make sure that you have read the [documentation](https://fabricius.readthedocs.io). If you are looking for support, you might want to check [this section](#i-have-a-question)).
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker](https://github.com/Predeactor/Fabricius/issues?q=label%3Abug).
- Also make sure to search the internet (including Stack Overflow) to see if users outside of the GitHub community have discussed the issue.
- Collect information about the bug:
- Stack trace (Traceback)
- OS, Platform and Version (Windows, Linux, macOS, x86, ARM)
- Version of the interpreter, compiler, SDK, runtime environment, package manager, depending on what seems relevant.
- Possibly your input and the output
- Can you reliably reproduce the issue? And can you also reproduce it with older versions?

#### How Do I Submit a Good Bug Report?

> You must never report security related issues, vulnerabilities or bugs including sensitive information to the issue tracker, or elsewhere in public. Instead sensitive bugs must be sent by email to [pro.julien.mauroy@gmail.com](mailto:pro.julien.mauroy@gmail.com). You may add a PGP key to allow the messages to be sent encrypted as well.

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [Issue](https://github.com/Predeactor/Fabricius/issues/new). (Since we can't be sure at this point whether it is a bug or not, we ask you not to talk about a bug yet and not to label the issue.)
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the *reproduction steps* that someone else can follow to recreate the issue on their own. This usually includes your code. For good bug reports you should isolate the problem and create a reduced test case.
- Provide the information you collected in the previous section.

Once it's filed:

- The project team will label the issue accordingly.
- A team member will try to reproduce the issue with your provided steps. If there are no reproduction steps or no obvious way to reproduce the issue, the team will ask you for those steps and mark the issue as `needs-repro`. Bugs with the `needs-repro` tag will not be addressed until they are reproduced.
- If the team is able to reproduce the issue, it will be marked `needs-fix`, as well as possibly other tags (such as `critical`), and the issue will be left to be [implemented by someone](#your-first-code-contribution).

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for Fabricius, **including completely new features and minor improvements to existing functionality**. Following these guidelines will help maintainers and the community to understand your suggestion and find related suggestions.

#### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Read the [documentation](https://fabricius.readthedocs.io) carefully and find out if the functionality is already covered, maybe by an individual configuration.
- Perform a [search](https://github.com/Predeactor/Fabricius/issues) to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.
- Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to convince the project's developers of the merits of this feature. Keep in mind that we want features that will be useful to the majority of our users and not just a small subset. If you're just targeting a minority of users, consider writing an add-on/plugin library.

#### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://github.com/Predeactor/Fabricius/issues).

- Use a **clear and descriptive title** for the issue to identify the suggestion.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why. At this point you can also tell which alternatives do not work for you.
- You may want to **include screenshots and animated GIFs** which help you demonstrate the steps or point out the part which the suggestion is related to. You can use [this tool](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and [this tool](https://github.com/colinkeenan/silentcast) or [this tool](https://github.com/GNOME/byzanz) on Linux. <!-- this should only be included if the project has a GUI -->
- **Explain why this enhancement would be useful** to most Fabricius users. You may also want to point out the other projects that solved it better and which could serve as inspiration.

<!-- You might want to create an issue template for enhancement suggestions that can be used as a guide and that defines the structure of the information to be included. If you do so, reference it here in the description. -->

### Your First Code Contribution
<!-- TODO
include Setup of env, IDE and typical getting started instructions?

-->

We use [Poetry](https://python-poetry.org/) to manage our environment of development, it is extremely recommended you use this tool yourself when editing Fabricius source code. This guide will explain you how to configure, edit, push and request changes into Fabricius.

#### Install Poetry

To install Poetry, please follow the guide provided by the Poetry's documentation: <https://python-poetry.org/docs/#installation>

#### Fork & Clone Fabricius repository

PS: Do not forget to [install Git](https://docs.github.com/en/get-started/quickstart/set-up-git) ;)

To fork the Fabricius's repository, you can follow the GitHub's documentation: <https://docs.github.com/en/get-started/quickstart/fork-a-repo>

This will create a repository of Fabricius with the exact same code in your account.

After forking the repository, you can clone your repository locally, again, you can follow the GitHub's documentation: <https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository>

#### Create a virtual environment & install dependencies

After installing Poetry, open a terminal into the cloned, you can run this command to install a virtual environment and install dependencies into it: `poetry install`
After Poetry is done installing your virtual environment, you can jump into it by using `poetry shell` or run commands into it using `poetry run <Your command here (Without brackets)>`

You now have to setup your IDE to make use of the create virtual environment. This guide does not cover this part as everyone may use a different IDE, we recommend you to read your IDE's documentation.

- [Visual Studio Code Documentation](https://code.visualstudio.com/docs)
- [JetBrain's PyCharm](https://www.jetbrains.com/help/pycharm/quick-start-guide.html)

After then, you're ready to edit Fabricius safely!

#### Commit your changes

You have made your changes into Fabricius, that's awesome! Thank for your time and contribution, and it is now time to publish them to the world!

Before you commit your changes, it would be preferable that you setup one of our tool, `pre-commit`, this tool will make sure you respect the project's rules so you can respect our consistency (As for example, we use Conventional Commit, and `pre-commit` check if your commit respect it). To install it, you need to run these 2 commands into your virtual environment:

```shell
pre-commit install
# If you wish to respect Conventional Commit
pre-commit install -t commit-msg
```

You're all set! Now, when you commit your changes, `pre-commit` will run automatically. If you wish to run it manually, you just have to run the `pre-commit` command.

If `pre-commit` fails, it has probably automatically added fixed files you can add to your changes.

After committing your changes, you can push them to your repository, you're then able to create a pull request at Fabricius's repository, check out (Once again :)) the GitHub's documentation for how to do so: <https://docs.github.com/en/get-started/quickstart/contributing-to-projects#making-a-pull-request>

## Styleguides

Fabricius respect the Black formatting and isort.

When you are committing changes, we'd like you to run `black` and `isort` to respect project's style.

### Commit Messages

Fabricius respect the Conventional Commit 1.0.0.

You can learn more about Conventional Commit here: <https://www.conventionalcommits.org/en/v1.0.0/>
You are free to use the Conventional Commit convention as long as you're not pushing directly to the repository of Fabricius.

## Attribution

This guide was partially made by [contributing-gen](https://github.com/bttger/contributing-gen). Licensed under MIT license.
