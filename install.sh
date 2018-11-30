#!/usr/bin/env bash
#
# Created by Uğur Özyılmazel on 2018-01-09.
# bash <(curl -fsSL https://raw.githubusercontent.com/vigo/django2-project-template/master/install.sh)

set -e
set -o pipefail

color_0=$(tput setaf 0)
color_1=$(tput setaf 1) # red
color_2=$(tput setaf 2) # green
color_3=$(tput setaf 3) # orange
color_4=$(tput setaf 4) # blue
color_5=$(tput setaf 5) # pink
color_6=$(tput setaf 6) # cyan
color_7=$(tput setaf 7) # white
color_8=$(tput setaf 8) # gray
color_r=$(tput sgr0)    # reset

AVAILABLE_OPTIONS=(
    "Django 2.0.5"
    "Django 2.1.3"
    "Cancel and quit"
)

echo "Django Project Template Installer"
PS3="Select option:"
select i in "${AVAILABLE_OPTIONS[@]}"
do
    case $i in
        "Django 2.0.5")
            PACKAGE="django-2.0.5"
            break
            ;;
        "Django 2.1.3")
            PACKAGE="django-2.1.3"
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
rm -f LICENSE.txt
rm -f README.md
rm -f README.md
rm -f install.sh
cp config/settings/development.example.py config/settings/development.py &&
cp config/settings/test.example.py config/settings/test.py &&
echo
echo
printf "${color_2}Installation completed...${color_r}\n\n"
echo -e "\tNow, create your virtual environment and run:"
echo
echo -e "\tcd ${PROJECT_NAME}/"
echo -e "\tpip install -r requirements/development.pip"
echo
echo
