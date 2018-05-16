# pbtool
manipulate the MacOS pasteboard from the CLI beyond pbcopy/pbpaste

## Modes
* Info: display useful information about the data contained in the five default pasteboards
* Zap: scrub non-printing characters from pasteboard text
  * This feature was initially needed to allow pasting of terminal output into HipChat, which silently fails to send messages containing some control characters.
* Image: remove non-image datatypes from the pasteboard
  * This feature was initially needed to allow copying of images from Chrome and pasting them into web applications that prioritized text over image data, resulting in just the image URL Chrome "helpfully" placed alongside the image to be pasted.

## Useful Shell Aliases
* `alias pbscrub=pbtool -Z`
* `alias pbimg=pbtool -i`
* `alias pbinfo=pbtool -I`