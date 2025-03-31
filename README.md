# 🌸 lanime 🌸
A terminal anime client that can show information and stream anime directly from your client

## Current Features

1. Stream anime from your terminal
2. Find out about your favourite or new anime from your terminal

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
this should handle the dependencies (and the dependencies' dependencies) for you and give you a go ahead message if everything went right

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

![TUI](https://github.com/Arihasaheadache/lanime/blob/main/img/tui.png)

### 2. Anime Information

![DB](https://github.com/Arihasaheadache/lanime/blob/main/img/DBDB.png)

### 3. Anime Streaming

![Streaming](https://github.com/Arihasaheadache/lanime/blob/main/img/stream.png)
