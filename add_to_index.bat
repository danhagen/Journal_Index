@echo off
 ipython IndexInput.py
 pdflatex main.tex 
 git add . 
 git commit --quiet -m "Adding to Index!" 
 git push --quiet origin master
