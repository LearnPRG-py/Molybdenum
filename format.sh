#!/bin/bash
shopt -s globstar
black -l 80 *.py
black -l 80 testing/*.py
