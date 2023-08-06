# How it's made

## How the how it's made package is made
This package recursively generates a title for the show "How It's Made" for n iterations. It can be run from a terminal, in which case it will also read the title allowed.

  ![cropped-700bd0ce-3f1c-4cd3-a2f2-2931567a425a-HowItsMade_S26_Episode16-740x416](https://user-images.githubusercontent.com/62618224/163507083-e4f994f4-08d3-45a8-ba81-1437ef04e772.jpg)

## Requirements

How it's made requires two packages, gTTS and pyttsx3, which can be installed using:

```bash
pip3 install gTTS pyttsx3
```
## Example
The command below will print, and then read aloud "How It's Made."
```bash
python3 how_its_made.py 1
```
The module can also be called within code, where the depth and the "it" can be customised.

```python
how = how_its_made(3, "a chair")

# This will print "How How How A Chair's Made Is Made Is Made"
print(how.title)

# This will then create a 'how_its_made.mp3' file using Google's Text to Speech package
how.text_to_speech(delete_sound_file=True)
```
