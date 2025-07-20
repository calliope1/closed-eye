# The Order of the Closed Eye

In 2015 I made a video game at the Scripture Union summer camp Transformers. It uses Pygame and Easygame, the latter of which is a Python library by Dickon Reed and Adam Rowell designed to make 2D graphics intensive games programming as easy as possible. My own (slight) modification of Easygame 6.0 is included in this repo (with permission) until the authors create an official channel for citation.

The current version is the "remastered" edition in which I have made a few improvements to the code. However, [commit 8f5fc29](https://github.com/calliope1/closed-eye/commit/8f5fc29340a480f5965a1bb9777787c04d825cf5) is the original release with only a single debugging `print` statement removed.

## How to run
* Make sure Pygame is installed.
* Either add Easygame to PYTHONPATH or put it in the same directory as TheOrderOfTheClosedEye.py. **Important:** This game uses a slight modification of Easygame 6.0, be sure to use the version from this repo.
* Run TheOrderOfTheClosedEye.py with python.

The floor texture `Sprites/Floor/FloorTexture.bmp` is based on the Minecraft cobblestone texture (pre 1.14). My (hopefully final) update to this game will involve changing this to my own texture (`Sprites/Floor/FloorTexture21.bmp` is a current very early alpha version of this).

Honestly, the game is as good as I remember. I'm quite proud of 16-year-old me making this in a week. I have the code for two other games that I made, but they don't function at the moment and I don't recall how far they got in development. If I can debug them then I'll release them as well.

## Changes in Version 4.0
* Sprites are round
* Better collision detection
* MUCH better lighting
* Enemies detect you faster the longer the game goes
* Removed a lot of junk from the code that either did nothing or did something inefficiently
