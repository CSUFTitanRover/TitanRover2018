# Contributing

Thank you for taking interest in helping contribute to the Titan Rover project.
This guide hopes to serve as a clear way for you to get onboard what we are doing
and the way we do things.

## Getting Started

If you have never used Git before then that's okay. We got you covered right
here: 
  - https://learngitbranching.js.org/
  - https://try.github.io/levels/1/challenges/1

Make sure you understand the basic commands of Git
like: `pull`, `push`, `commit`, and `checkout`

If you do not have a GitHub account, then you will need to create one 
in order to push your development progress to our GitHub repository.

Create a GitHub account: https://github.com/join

## Projects

We currently have the following projects baking in the oven:

- UserInterface
- MobileApp
- ProcessManager
- Autonomy
- ComputerVision
- Mobility
- Science

You are more than welcome, and in fact, are encouraged to try to contribute to more than 1 project. The more you help with differnt projects,
the more you come to learn about the entire rover system. 

We have a _projects page*_ where you can read more about our system: https://github.com/CSUFTitanRover/TitanRover2018/projects

_\* There are additional side projects listed that are not listed above._

We encourage our team members to track issues/progress of your team by going to the project tracking view. Which is done by clicking on the project link in the [projects page listing](https://github.com/CSUFTitanRover/TitanRover2018/projects).

e.g. https://github.com/CSUFTitanRover/TitanRover2018/projects/1

## GitFlow

GitFlow is a naming convention for a certain type of branching model.
Here at _Titan Rover Industries<sup>tm</sup>_ we are using the [Feature Branch Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow).

Our use cases for **feature branches** are mainly to be implementing one single aspect of a project. Once done implementing a feature, then you would submit a Pull Request to merge the branch back into your base project branch and have it reviewed by your team lead.

### Feature Naming Scheme

If you need to create a feature branch, it's suggested to follow this naming scheme.

`feature/<ProjectName>-<FeatureName>-<IssueID>`

1. Project Name (Pascal Case) - refers to the base project the feature is for.
2. Feature Name (Camel Case) - refers to the name of the feature(s) you are implementing.
3. Issue ID(s) - refers to the ID of an issue that is created in the [GitHub Issues](https://github.com/CSUFTitanRover/TitanRover2018/issues) page. 
  - If you are tackling a Feature that refers to multiple issues then simply append
  the issue numbers, separated by a dash.

Simple Example: `feature/UserInterface-rethinkDB-24`

Multiple Issues Example: `feature/UserInterface-components-14-17-23`

## Typical Workflow

A typical day in development land looks like so:

1. `git pull` for new updates if there are any.
2. Do your development
3. Commit your work and push to GitHub.

A typical day implementing a feature:

1. `git pull` for new updates if there are any.
2. Do your development and complete the feature.
3. Commit your work and push to GitHub.
4. Create a Pull-Request to merge your feature into your base project.
5. Add your team lead as a Reviewer.










