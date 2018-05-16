# Architecture
* pb description method to replace copypasta
* reduce globals to permit module-ification

# Functionality
* invoke as pbimg/pbscrub for -I/-Z default
* detect nonprintable characters and only display "<binary data>" or hexdump
* implement some zap-gremlins features
  * https://forums.tumult.com/t/zap-gremlins-cutting-and-pasting-code-from-a-book-about-hype/10673
* check against Apple PB code practices to ensure cross-version MacOS compat
  * https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/PasteboardGuide106/Articles/pbConcepts.html
* pbcopy/pbpaste command-line compatibility
* image pbcopy/pbpaste

# Other
* tests

