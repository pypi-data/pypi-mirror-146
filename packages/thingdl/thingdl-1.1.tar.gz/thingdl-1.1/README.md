# thingdl

Thingiverse is a wonderful place for makers to share their works with the world. 

However, when makers upload their parts, often they are uploaded in many different pieces, each of which requires a separate download.

thingdl is a command line tool that is aimed to simplify that. With a single command, you can download all files related to a given thing 

## Installation

`pip3 install thingdl`

Next, find the thing you wish to download. ~~Click on the "download all files" link, and copy the url
(it will end in /files)~~ Now the base url and the `/files` url are compatible! 

From a terminal or command prompt:

```
thingdl -u <yourthingurl/files> -d <your destination directory>

```

in a few moments, it will download all the files from that thing into your specified directory.