Pirates Online Retribution Source Code
======================================
This repository is the source code for Pirates Online Retribution.

### Info

* Only push game code to this repository.
* *Never* force a git push.
* 


````
git clone https://github.com/pearson1919/Pirates-Online-Retribution.git por
cd por
mkdir resources
git https://github.com/pearson1919/Resources.git resources
````

### Production

**LIVE**: In production, we will be using git tags for deployment on the master branch. When we are ready to deploy a prod build, we will merge qa into master and then create a git tag. 

**QA**: Deployment is based on git commit hashes using the qa branch.
