@echo off
 git pull --quiet origin master
 ipython IndexInput.py
 pdflatex CompleteIndex.tex >nul 2>nul
 git add .
 git commit --quiet -m "Adding to Index!"
 git push --quiet origin master
