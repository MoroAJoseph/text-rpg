# Text RPG

## Table of Contents

1. [About](#about)
2. [Setup](#setup)
    - [Installation](#installation)
    - [Running the Project](#running-the-project)
        - [Production](#production)
        - [Development](#development)
3. [Project Structure](#project-structure)
    - [Directory](#directory)
    - [Directory Overview](#directory-overview)
    - [Environment Files](#environment-files)
    - [Entry Point](#entry-point)
4. [Contribution](#contrubution)
    - [Git CLI](#git-cli)
    - [Design Principles](#design-principles)

## About

Text RPG is a terminal-based role-playing game implemented in Python. The
project focuses on modular game systems, maintainable code structure, and
collaborative development.

The goal of the project is to build a flexible engine for text-based gameplay
including combat, inventory management, character progression, and story
interaction.

This repository is intended for developers interested in contributing to the
game's architecture and gameplay systems.

---

## Setup

This section explains how to prepare your environment and run the project
locally.

### Installation

**System Requirements**

Supported environments:

- Linux
- macOS
- Windows

Required tools:

- `Git CLI`
- `Python 3.x`

**Python Requirements**

Recommended setup using a virtual environment.

- Clone the project:

```bash
git clone https://github.com/MoroAJoseph/text-rpg.git
cd text-rpg
```

- Create a virtual environment:

```bash
# Linux / macOS
python3 -m venv .venv

# Windows (Powershell)
python -m venv .venv
```

- Activate the virtual environment:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows (Powershell)
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

### Production

Run the project normally.

```bash
python -m main
```

### Development

Development mode should be used when contributing or testing new features.

Typical workflow:

```bash
git switch -c feature/your-feature
python -m main
```

---

## Project Structure

### Directory

Components:

```bash
│   Vertical continuation of a branch
├── Intermediate branch (more items follow)
└── Final branch (last item in a directory)
```

Structure:

```bash
text-rpg/
│
├── .vscode/                # (u) VS Code workspace settings
│
├── config/                 # Configuration files for the application
│
├── data/                   # (u) Generated game data
│   ├── saves/              # Player save files
│   └── cache/              # Temporary runtime data
│
├── logs/                   # (u) Runtime logs
│
├── scripts/                # Utility and automation scripts
│   ├── dev/                # Development helper scripts
│   └── setup/              # Build / setup scripts
│
├── src/                    # Application source code
│   ├── models/             # Data models
│   ├── runtime/            # Game runtime
│   ├── ui/                 # UI modules
│   ├── utils/              # Utility helpers
│   └── __init__.py
│
├── tests/                  # Automated tests
│
├── .env                    # (u) Local environment variables
├── .env.example            # Example environment configuration
├── .env.development        # (u) Development environment configuration
│
├── .gitignore              # Git ignore rules
├── main.py                 # Application entry point
├── todos.py                # (d) Development task tracker
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

> **Tags**
>
> - (u) - Untracked - Refer to files/directories not being tracked by git
> - (d) - Development - Refer to files/directories meant for development
>   purposes

### Directory Overview

**`/src`**

Contains all primary application code. Game systems, engine components, and
utilities live here.

**`/scripts`**

Helper scripts used for development tasks, automation, or project maintenance.

Examples:

- setup scripts
- environmental helpers
- build scripts

**`/config`**

Centralized configuration files for the application.

**`/data`** Generated runtime data such as saves and temporary files. This
directory should remain **untracked by Git**.

**`/logs`**

Application runtime logs.

**`/tests`**

Automated tests validating project functionality.

**`/vscode`**

Editor workspace settings. Typically ignored in version control.

### Environment Files

| File             | Purpose                                     |
| ---------------- | ------------------------------------------- |
| .env             | Local environment variables (not committed) |
| .env.example     | Template used by developers                 |
| .env.development | Development-specific configuration          |

### Entry Point

Starts the application and initializes the core systems.

```bash
main.py
```

## Contrubution

This section explains how to contribute to the project, including workflow rules
and development practices.

Contributors should follow the Git workflow and design principles described
below.

### Git CLI

Common commands used when contributing.

**Cloning the repository**

```bash
git clone https://github.com/MoroAJoseph/text-rpg.git
```

**Create a new branch**

```bash
git switch -c feature/branch-name
```

**Switch branches**

```bash
git switch branch-name
```

**Check current status**

```bash
git status
```

**Stage files**

```bash
git add .
```

**Commit changes**

```bash
git commit -m "Short title" -m "Brief description of change"
```

**Push a branch**

```bash
git push -u origin branch-name
```

**Update from branch**

```bash
git switch branch-name
git pull
```

### Design Principles

Guidelines for project development.

**Creating Git branches**

Create a new branch when:

- Adding a feature
- Fixing a bug
- Refactoring existing code
- Making strucural changes

Avoid committing directly to `main`.

**Git branch naming**

Use consistent prefixes.

Example:

```bash
feature/player-combat
feature/inventory-system
fix/save-bug
refactor/game-loop
docs/readme-update
```

Common prefixes:

- `feature/`
- `fix/`
- `refactor/`
- `docs/`
- `test/`
