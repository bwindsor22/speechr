Program to detect hate speech on Reddit with the aim of tracking and reporting it. This repository contains reference files with strong language.

![site](https://raw.githubusercontent.com/bwindsor22/speechr/master/speechr/ref/29634694_10156194179469417_1582013879_o.png)

## Getting Started

1. Clone repository from github 
```
	git clone https://github.com/bwindsor22/speechr.git
```
2. Gather api key from secret bitbucket repo <br>
```
	git clone https://bwindsor22@bitbucket.org/bwindsor22/speechr-secret.git
```
3. Copy praw.ini file to speechr directory from secret repo and move the aws key to the admin folder.<br>
```
	cp speechr-secret/praw.ini speechr/speechr/
	cp speechr-secret/keypairname.pem speechr/admin/
```
4. Install all python packages <br>
```
	pip install -r .\admin\requirements.txt
```
5. Make the package by running run_setup.sh <br>
	Windows: setup.py develop <br>
