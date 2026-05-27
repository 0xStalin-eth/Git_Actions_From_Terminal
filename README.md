# GitHub Issue Manager

Python scripts to bulk open and close GitHub issues by issue number.

## Requirements

- Python 3
- A GitHub [classic personal access token](https://github.com/settings/tokens) with the `repo` scope (or `public_repo` for public repos)

## Setup

**1. Install dependencies:**
```bash
pip install -r requirements.txt
```

**2. Configure environment:**

You can set the variables in any of these ways:

- **`.env` file** (recommended for per-project config):
```bash
cp .env.example .env
```
Edit `.env`:
```
GITHUB_TOKEN=ghp_your_classic_token_here
GITHUB_REPO=https://github.com/owner/repo
```

- **Shell profile** (sets them globally for all projects): add the following to your `~/.zshrc`, `~/.bashrc`, or `~/.zshenv`:
```bash
export GITHUB_TOKEN=ghp_your_classic_token_here
export GITHUB_REPO=https://github.com/owner/repo
```
Then reload it:
```bash
source ~/.zshrc    # or ~/.bashrc or ~/.zshenv
```

**3. Prepare your issue number files:**
```bash
cp open_numbers.example.txt open_numbers.txt
cp close_numbers.example.txt close_numbers.txt
```

Edit each file with the issue numbers you want to act on, one per line:
```
1
2
3
```

## Usage

**Reopen issues:**
```bash
python open_issues.py open_numbers.txt
```

**Close issues:**
```bash
python close_issues.py close_numbers.txt
```

**Override the repo inline (no .env needed):**
```bash
python open_issues.py open_numbers.txt https://github.com/owner/repo
python close_issues.py close_numbers.txt https://github.com/owner/repo
```
