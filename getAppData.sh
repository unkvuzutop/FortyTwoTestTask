#!/usr/bin/env bash

_now=$(date +"%m_%d_%Y %H:%M:%S")
_file="datalist_$_now.dat"
./manage.py datalist hello 2> "$_file"
