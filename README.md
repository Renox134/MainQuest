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
### Disclaimer
Before you go through any of this trouble, let me tell you one thing up front:
I am working on creating a docker image that would hopefully make readying and doing everything here obsolete. So if things go according to plan, going through the trouble described below will hopefully never be necessary for anyone other than me again.

---


The project is intended to be build with **buildozer**, which is only available for unix systems (at least to my knowledge). Hence, you'll either need a unix system or use WSL or a VM or something like that before you can even install it. Once your system is ready, just type:

```bash
pip install buildozer
```
Usually, buildozer would now have to be initialized. However, I already provided a **buildozer.spec** file in the root directory of the project. I edited it to the best of my knowledge to function with this project. The edits include the inclusion of ".json" as a file ending for files to take and more importantly, the exclusion of pycairo from the build because (to my knowledge) python-for-android currently doesn't support it.

Now, on my own Ubuntu machine, I also had to install **setuptools**, because I didn't have **dstutils** installed. If your system has this, you can skip this step. If you'don't know what I am talking about, just install it anyway, it sholdn't hurt (hopefully)...
```bash
pip install setuptools
```
Then, I ran the common build stack used by buildozer. You'll likely already have a few things listed here (looking at you, git), but I for one just did it like this anyway,
```bash
sudo apt install -y \
    build-essential \
    autoconf \
    automake \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo6 \
    cmake \
    git \
    unzip
```
Next, you'll need **cython**, so if you don't already have it, install :D
```bash
pip3 install Cython==0.29.33
```
With that out of the way, we now also need a java compiler.
For that, the most striaght way is to install a jdk.
```bash
sudo apt install openjdk-17-jdk
```
Now, we shold have everything we need and can finally run the build command :D
```bash
buildozer android debug
```
This will likely take some time, so you can go get yourself some tea ☕.
However, during the first build, you'll likely have to agree to a few **license agreements** every now and then, so watch out for that. Otehrwise, this can be a very lengthy process, so on a slower system you might as well go get some dinner.

Should you encounter any build issues, which sadly isn't that unlikely, please don't bother me with it. It's not that I'd be unwilling to help, but rather because I'd be **unable** to help. I'm just some random guy who thought developing a mobile app would be a fun hobby...
I have absolutely no idea what I'm doing. You're better of asking Google or Claude, trust me.