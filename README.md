# MainQuest
A todo list and calendar project, providing modern todo list features with an interface typical for video games, RPGs in particular. 

# How to Build?
As far as I know, it is best to build this on a unix system (e.g., Ubuntu). At least that's how I did it and how it works for me.
To build the project, you'll first need to install a tool called **buildozer**.

```bash
pip install buildozer
```
Then, buildozer has to be initialized.
```bash
buildozer init
```
Now, there shold be a **buildozer.spec** file in the root directory of the project. In this file, the properties of the app we're building can be edited, such as name, version etc. The one thing that **has** to be edited is the root directory, as it isn't just **"."** (as buildozer assumes by defaullt) but rather **"./src"**.
Also, you'll have to add **"json"** to the list of file endings that should be used, as the config and the journal use the json format.

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
However, during the build, you'll likely have to agree to a few **license agreements** every now and then, so watch out for that.

Should you encounter any build issues, not because I'd be unwilling to help, but rather because I'd be **unable** to help. I have absolutely no idea what I'm doing. You're better of asking Google, trust me.