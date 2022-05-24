#!/bin/bash -e

components_num=${#components[@]}
python3 -m pip install -r ../requirements.txt
./build.sh

gnome-terminal -- python3 -m style
gnome-terminal -- python3 -m body
gnome-terminal -- python3 -m format
gnome-terminal -- python3 -m animal
gnome-terminal -- python3 -m core
