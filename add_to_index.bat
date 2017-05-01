@echo off
 ipython IndexInput.py
 pdflatex main.tex >nul 2>nul
 git add . 
 git commit --quiet -m "Adding to Index!" 
 git push --quiet origin master