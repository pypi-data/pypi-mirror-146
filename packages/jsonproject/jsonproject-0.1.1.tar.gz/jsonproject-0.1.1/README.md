# Jsonproject
Easily manage your projects
## What is jsonproject?
jsonproject is a simple, easy to use, and powerful project configuration manager. It is a JSON based configuration project manager that allows you to manage your projects in a simple and easy way. Its just like npm's `package.json` file.

## Installation
To install jsonproject, just run the following command:

```
pip install jsonproject
```

## Usage

### Initialize
To initialize a new project, run `jsonproject init`. This will walk you through the process of creating a new project.

jsonproject will ask you for the following information:
- Project name
- Project description
- Project author
- Project license
- Project version
- Project homepage
- Project email
- Project actions

It will then create a new project directory and a new `project.json` file.
```json
{
    "name": "Example",
    "description": "This is an example project",
    "version": "0.1",
    "author": "John Doe",
    "license": "GNU-3",
    "url": "www.example.com",
    "email": "example@example.com",
    "languages": [
        "python",
        "javascript",
        "c++"
    ],
    "actions": {
        "build": "example build",
        "test": "example test",
        "install": "example install",
        "uninstall": "example uninstall"
    }
}
```
### Search
To search for a project, run `jsonproject search`. This will search for a project in the current directory and all subdirectories.
```
projects in C:\Projects\
name:Example version:0.1 location:.\example
```
### Info
To get information about a project, run `jsonproject info`. This will print out the information about the project.
```
name:Example
version:0.1
description:This is an example project
author:John Doe
license:GNU-3
url:www.example.com
email:example@example.com
languages:
        python
        javascript
        c++
actions:
        build:example build
        test:example test
        install:example install
        uninstall:example uninstall
```