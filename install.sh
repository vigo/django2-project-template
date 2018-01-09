#!/usr/bin/env bash
#
# Created by Uğur Özyılmazel on 2018-01-09.
# bash <(curl -fsSL https://raw.githubusercontent.com/vigo/django2-project-template/master/install.sh)

set -e
set -o pipefail

AVAILABLE_OPTIONS=("Django 2.0.1" "Cancel and quit")

echo "Django Project Template Installer"
PS3="Select option:"
select i in "${AVAILABLE_OPTIONS[@]}"
do
    case $i in
        "Django 2.0.1")
            PACKAGE="django-2.0.1"
            break
            ;;
        "Cancel and quit")
            echo "Canceled..."
            exit 1
            ;;
    esac
done

echo "What is your project name?"
read PROJECT_NAME

if [[ ! $PROJECT_NAME ]]; then
    echo "Canceled..."
    exit 1
fi

PACKAGE_URL="https://github.com/vigo/django2-project-template/archive/${PACKAGE}.zip"

curl -L "${PACKAGE_URL}" > template.zip &&
unzip template.zip &&
mv "django2-project-template-${PACKAGE}" "${PROJECT_NAME}" &&
rm template.zip &&
cd "${PROJECT_NAME}" &&
cp config/settings/development.example.py config/settings/development.py &&
echo
echo
echo "Installation completed..."
echo "Now, create your virtual environment and run:"
echo "cd ${PROJECT_NAME}/"
echo "pip install -r requirements/development.pip"
