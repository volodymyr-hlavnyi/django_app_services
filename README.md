# Django application for control Services

---
![Main workflow](https://github.com/volodymyr-hlavnyi/django_app_services/actions/workflows/main-workflow.yml/badge.svg)

## 🏠 Homework 

### (Base project)

Homework related actions.

### ▶️ Run

Make all actions needed for run homework from zero. Including configuration.

```shell
make d-homework-i-run
```

### 🚮 Purge

Make all actions needed for run homework from zero.

```shell
make d-homework-i-purge
```

---

## 🛠️ Dev

### Initialize dev

Install dependencies and register pre-commit.

```shell
make init-dev
```

### ⚙️ Configure

Configure homework.

```shell
make init-configs
```

---

## 🐳 Docker

Use services in dockers.

### ▶️ Run

Just run

```shell
make d-run
```

### ⏹️Stop

Stop services

```shell
make d-stop
```

### 🚮 Purge

Purge all data related with services

```shell
make d-purge
```

## Cmd for initial setup from base project

```shell
#!/usr/bin/env sh

NEW_REPOSITORY_NAME="django_base__hlavnyi_volodymyr__step_1"
BASE_REPOSITORY_NAME="django_base__hlavnyi_volodymyr"
OWNER_NAME="hillel-i-python-pro-i-2023-06-23"

cd /home/vladimir/develop/python/Hillel
git clone "https://github.com/${OWNER_NAME}/${BASE_REPOSITORY_NAME}.git" "${NEW_REPOSITORY_NAME}" && \
cd "${NEW_REPOSITORY_NAME}" && \
git remote set-url origin "https://github.com/${OWNER_NAME}/${NEW_REPOSITORY_NAME}.git" && \
echo "Clone Done!"

echo "Create venv..."
cd /home/vladimir/develop/python/Hillel/"${NEW_REPOSITORY_NAME}"
python3.11 -m venv venv
source venv/bin/activate
make init-dev
cd /home/vladimir/develop/python/Hillel/"${NEW_REPOSITORY_NAME}"
```