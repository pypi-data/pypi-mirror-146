# How it's made

## How the how it's made package is made
This package recursively generates a title for the show "How It's Made" for n iterations, and can also read the title aloud.

  ![cropped-700bd0ce-3f1c-4cd3-a2f2-2931567a425a-HowItsMade_S26_Episode16-740x416](https://user-images.githubusercontent.com/62618224/163507083-e4f994f4-08d3-45a8-ba81-1437ef04e772.jpg)

## Installation

How it's made has one requirement, pyttsx3, and can be installed using:

```bash
pip install how-its-made
```
## Usage

```python
import how_its_made as him

# This will print "How It's Made"
how = him.how_its_made()
print(how.title)

# This will print "How How How A Chair's Made Is Made Is Made"
how = him.how_its_made(3, "a chair")
print(how.title)

# This will read aloud "How How How A Chair's Made Is Made Is Made"
how.text_to_speech()

```