# 🌸 lanime 🌸
An aesthetic anime client for your terminal

## Current Features

1. Stream anime 
2. Find out about your favourite or new anime 

## Installation

### 1. Clone the repo

```sh
git clone https://github.com/Arihasaheadache/lanime.git
```

### 2. move to the directory

```sh
cd lanime
```

### 3. run install.py

```sh
python install.py
```
this should handle the dependencies for you and give you a go ahead message if everything went right

## MPV
MPV is a video streaming client that is required to run the streaming section. You can choose to opt out of downloading MPV as it is not part of install.py, but only do so if you do not want to stream anime and only look up information.

1. For Linux:

Debian/Ubuntu:
```sh
sudo apt install mpv
```
Arch/Manjaro:
```sh
sudo pacman -S mpv
```
Fedora:
```sh
sudo dnf install mpv
```
2. For MacOS:

```sh
brew install mpv
```
3. For Windows:

   You have to install [MPV](https://mpv.io/installation/) and add the .exe to PATH

## Usage

### Run lanime.py

```sh
python lanime.py
```
### 1. Anime TUI

![TUI](https://github.com/Arihasaheadache/lanime/blob/main/img/startpage.png)

Upon running, the terminal will show the above as the starting TUI

### 2. Anime Information

![DB](https://github.com/Arihasaheadache/lanime/blob/main/img/information.png)

On running option 2 from TUI, you can get information about your favourite anime

### 3. Anime Streaming

![Streaming](https://github.com/Arihasaheadache/lanime/blob/main/img/s1.png)

Upon running option 1, you can start watching your favourite anime by selecting the title you'd like...

![Streaming](https://github.com/Arihasaheadache/lanime/blob/main/img/s2.png)

..picking the episode you'd like to watch...

![Streaming](https://github.com/Arihasaheadache/lanime/blob/main/img/s3.png)

And let lanime handle the rest!
