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
- NvidiaTX2

You are more than welcome, and in fact, are encouraged to try to contribute to more than 1 project. The more you help with different projects,
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

### Creating a Feature Branch

If you need to create a feature branch then always remember to branch off from your base project branch. For example, if I need to create a feature branch under the User Interface project then I will branch off from the User Interface branch.

```
├───master
  ├───UserInterface
    ├───feature/UserInterface-Layout-19
```

## Git Layout

Our layout for the git structure looks like so:
```
├───master
   ├───UserInterface
   ├───MobileApp
   ├───ProcessManager
   ├───Autonomy
   ├───ComputerVision
   ├───Mobility
   ├───Science
   ├───NvidiaTX2
   ├───docs
```

## Project Layout 

Our current project layout looks like so from a top level view:
```
├───docs
├───hoembase
├───rover
├───schematics
```

- **docs** will hold all of our documentation files
- **homebase** will hold any code that will be run on the homebase e.g. User Interface
- **rover** will hold any code that will run on the rover e.g. Control Systems
- **schematics** will hold any schematic diagrams that are helpful for the Eletrical team to use for wiring up our rover

## Git GUI

If you are not a fan of using Git in your CLI, you can always use a GUI to interact with Git.
Here are a number of good Git GUIs that are free:

- https://www.gitkraken.com/
- https://www.sourcetreeapp.com/
- https://www.syntevo.com/smartgit/


## GitHub Labels

We have a number of labels that can be applied to any GitHub Issues created and thought it would be helpful to
go over them. You can view our labels here: https://github.com/CSUFTitanRover/TitanRover2018/labels

Priority tags - define how urgent it is an issue needs to be completed
  - There should only be 1 priority tag per issue
Status tags - define what the status is for an issue
  - There should only be 1 status tag per issue
Default tags - these tags help describe what the issue is or wants
  - There can be any number of tags per issue

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










