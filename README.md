# MainQuest
Main Quest is supposed to be a combination of todo list, calendar and progress tracking app.
Q: Why is it called Main Quest
A: Because I love Video Games and thought it sounds decent.
 I say "is supposed to" be because, as of writing this, the only thing it actually is is a somewhat ambition loaded, part time supported coding project by some random guy who thought "Developing an app can't be that hard, can it". Oh, how wrong I was...
But anyway, here we are.

## Current state
As of writing this, the backend is already provides most required functionalities. Tasks can be given time and date (which is important for the calendar) and progress tracking should theoretically also work. I dind't spend forever thinking about everything and seasoned developers will likely spot numerous things I messed up, but for the most part I think the **backend is doing fine** (at least by my standards). What I am more concerned about is the frontend of the app.

What the project is **lacking most** is some real **frontend** and **design love**. Basically every component of this app is still unpolished and could really use some attention, be it widgets, context menus or all the stuff that I don't even have an idea how to implement such as color scheme choosers.

## Installation
As always, start by cloning the repository (provided that you have git already up and running).
```bash
git clone https://github.com/Renox134/MainQuest.git
```

Then, as the project has quite a few requirements, I **highly** suggest that you create a virtual environment before installing the dependencies.
```bash
python -m venv venv
```
(The venv then also has to be activated)
```bash
.\venv\Scripts\activate  # for windows
source venv/bin/activate # for linux
```
Now, simply install the project requirements by typing
```bash
pip install -r requirements.txt
```
Note: Most requirements are currently bound to a specific version. That was mostly done to avoid potential version clashes and incompatibility wars. Still, it is likely that some more recent versions of certain packages could work all the same. So if you feel like it, you can try update stuff and see what happens. Just know that for me personally, it was a tedious journey to figure out versions for everything that work together properly.

## Usage
For developing, the core command is
```bash
python ./src/main.py
```
This is what starts the app.

## How to Build?
The easiest way to build this project is probably by using the docker environment provided in the repo.
This saves you the trouble of going through everything by yourself. Also the project is intended to be build with **buildozer**, which is only available for unix systems anyway (at least to my knowledge). If, for some reason, you want to build it on your own linux system/vm, you can more or less see all necessary steps by looking into the dockerfile and simply redoing all necessary steps on your own system.

To build any project with buildozer, you need generally need a **buildozer.spec** file. In the case of this project, I already provided one, which lies in the  root directory of the project. I edited it to the best of my knowledge to function with this project. The edits include the inclusion of ".json" as a file ending for files to take and more importantly, the exclusion of pycairo from the build because (to my knowledge) python-for-android currently doesn't support it.

### Building with docker
When using docker, hopefully all you have to do is to run:
```bash
sudo docker build -t kivymd-builder .
```
to build the image. Then, run the actual build with
```bash
sudo 
```

This will take some time, so you can go get yourself some tea ☕, or even dinner on a slower device.
However, during the first build, you'll likely have to agree to a few **license agreements** every now and then, so watch out for that. Otehrwise, this can be a very lengthy process, so on a slower system you might as well go get some dinner.

Regarding any questions on the building pipeline, it is sadly very likely that I won't be able to help, because I don't really know build process myself. So you're likely better off asking Google.
