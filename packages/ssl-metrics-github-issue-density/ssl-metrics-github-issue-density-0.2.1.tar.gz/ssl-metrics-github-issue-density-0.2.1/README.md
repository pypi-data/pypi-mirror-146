# Software Systems Laboratory Metrics GitHub Issue Density

> A `python` tool to calculate the issue density of a GitHub repository

![[https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue](https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue)](https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue)

![[https://img.shields.io/badge/DOI-Example-red](https://img.shields.io/badge/DOI-Example-red)](https://img.shields.io/badge/DOI-Example-red)

[![Release Project](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issue-density/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issue-density/actions/workflows/release.yml)
![[https://img.shields.io/badge/license-BSD--3-yellow](https://img.shields.io/badge/license-BSD--3-yellow)](https://img.shields.io/badge/license-BSD--3-yellow)

## Table of Contents

- [Software Systems Laboratory Metrics GitHub Issue Density](#software-systems-laboratory-metrics-github-issue-density)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Developer Tooling](#developer-tooling)
    - [Operating System](#operating-system)
  - [How To Use](#how-to-use)
    - [Installation](#installation)
    - [Command Line Arguements](#command-line-arguements)

## About

The Software Systems Laboratory (SSL) GitHub Issue Density Project is a `python` tool to calculate the issue density of a GitHub repository. It is reliant upon the output of the [GitHub Issue](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issues) and [Git Commits](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-git-commits-loc) tools.

This project is licensed under the BSD-3-Clause. See the [LICENSE](LICENSE) for more information.

## Developer Tooling

To maximize the utility of this project and the greater SSL Metrics project, the following software packages are **required**:

### Operating System

All tools developed for the greater SSL Metrics project **must target** Mac OS and Linux. SSL Metrics software is not supported or recommended to run on Windows *but can be modified to do so at your own risk*.

It is recomendded to develop on Mac OS or Linux. However, if you are on a Windows machine, you can use WSL to develop as well.

## How To Use

### Installation

You can install the tool via `pip` with either of the two following one-liners:

- `pip install --upgrade pip ssl-metrics-meta`
- `pip install --upgrade pip ssl-metrics-github-issue-density`

### Command Line Arguements

`ssl-metrics-github-issue-density-compute -h`

```shell
options:
  -h, --help            show this help message and exit
  -c COMMITS, --commits COMMITS
                        Commits JSON file
  -i ISSUES, --issues ISSUES
                        Issues JSON file
  -o OUTPUT, --output OUTPUT
                        output JSON file
```

`ssl-metrics-github-issue-density-graph -h`

```shell
options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        The input data file that will be read to create the graphs
  -o OUTPUT, --output OUTPUT
                        The filename to output the bus factor graph to
  -m MAXIMUM_DEGREE_POLYNOMIAL, --maximum-degree-polynomial MAXIMUM_DEGREE_POLYNOMIAL
                        Estimated maximum degree of polynomial
  -r REPOSITORY_NAME, --repository-name REPOSITORY_NAME
                        Name of the repository that is being analyzed
  --x-window-min X_WINDOW_MIN
                        The smallest x value that will be plotted
  --x-window-max X_WINDOW_MAX
                        The largest x value that will be plotted
```
