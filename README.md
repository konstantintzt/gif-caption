# Broksy's GIF Captioner

Have you ever wanted to easily caption a GIF without having to send it to an external website, or even have an Internet connection? Well, here you go!

## Features
The GIF Captioner is very straightforward: you open a file, choose a font size and write your caption. That's it! 
The generated captioned GIF file will be stored at in the same directory as the source GIF, under the name `captioned_<RANDOM_STRING>.gif`.

## Usage
There are two ways to use this software:

### Install the executable (Windows only)
The executable is available in the "releases" tab. It was generated using [pyinstaller](https://github.com/pyinstaller/pyinstaller). With this method, all you need to do is download the executable and you're good to go! You'll be able to run it anytime you want.

### Run the Python file
If you're not on Windows or you simply prefer running the Captioner manually (loading times are usually a bit quicker), it's totally fine. You will only need to run `pip install -r requirements.txt` to download all necessary libraries first, then you'll be able to run the Captioner anytime you want by running the `gif_caption.py` file, like you usually do for other Python files.