Pirates Online Retribution Source Code
======================================
This repository is the source code for Pirates Online Retribution.

## Build Instructions
Instrutions on how to set up a development environment for POR (run server/clients locally)

#### 1) Install Git and learn the basics

#### 2) Clone this and the 2 resource repos
```bash
git clone https://github.com/pearson1919/Pirates-Online-Retribution.git por
cd por
git clone https://github.com/pearson1919/Resources.git resources
cd resources
git clone https://github.com/pearson1919/SecureResources.git phase_1
```

#### 3) Install Panda3D
**From this link specifically**: https://piratesonline.us/files/Panda3D-1.10.0.exe

#### 4) Install MongoDB
* **From here**: https://www.mongodb.com/download-center?jmp=nav
* Run this to make the appropriate folder structure for it:
```bash
mkdir C:/data
mkdir C:/data/db
```
or just make them manually.

#### 5) Install requests
Do `where python` and *make sure* that it shows `C:\Panda3D-1.10.0\python\python.exe` as the first entry.
If it's not:
**Fix your PATH** by adding this *at the front* of your PATH variable.
```
C:\Panda3D-1.10.0\python;C:\Panda3D-1.10.0\python\Scripts;C:\Panda3D-1.10.0\bin
```
Finally, do `python -m pip install requests` in a terminal.
If you find out you don't have pip, install that too (for Python 2 of course).

#### 6) Test the server/client
Go in `win32` if you're on Windows and double click `start-all.bat`.


### Rules

* Only push game code to this repository.
* *Never* force a git push.

### Production

**LIVE**: In production, we will be using git tags for deployment on the master branch. When we are ready to deploy a prod build, we will merge qa into master and then create a git tag. 

**QA**: Deployment is based on git commit hashes using the qa branch.
Note: Currently unused, just push to master.



---

**These are a list of crashlogs submitted to us by players on the public server. If a crash has been fixed/resolved, insert a (RESOLVED) following the description for the crash and the link to it. We'd like to keep all of these crashes on record, so do not remove any of them.**


1.) Very bumpy crash, not responding, then not working, then closed program, it responds and plays for 3 seconds, then closes.
https://cdn.discordapp.com/attachments/226498380338167808/228280686304428033/160921_171726.log

2.) Memory Leak - https://images-ext-2.discordapp.net/eyJ1cmwiOiJodHRwOi8vaW1hZ2UucHJudHNjci5jb20vaW1hZ2UvYjdmZTI5NWQ3M2ViNDAxYjhlZTQ5MzA3ODY2NGU4NGQucG5nIn0.vgNLpjOXaAcxXFhQEWoCZ4zGebI

3.) was fighting an alligator on tortuga, alligator wasnt taking damage then lost connection to server - https://cdn.discordapp.com/attachments/227515252252737536/228283977763389441/unknown.png

4.) I through a grenade at a alligator and it crashed - https://cdn.discordapp.com/attachments/225307184487989248/228286681143443456/160921_183452.log

5.) I just crashed on Tortuga while shooting an alligator - https://cdn.discordapp.com/attachments/228287346183766018/228291381385363458/nativelog.txt

6.) been getting this whenever I initiate a fight - http://pastebin.com/6nrTvs8q

7.) When using a particular weapon - http://pastebin.com/de6meaTG

8.) trying to put a weapon in one of the weapon slots - http://pastebin.com/fPTCxBUe

9.) This is happening frequently while fishing - http://prntscr.com/ckwduw

10.) I was in the graveyard, fighting the undead. - https://cdn.discordapp.com/attachments/228424497882071041/228425345064370176/160922_035255.log


