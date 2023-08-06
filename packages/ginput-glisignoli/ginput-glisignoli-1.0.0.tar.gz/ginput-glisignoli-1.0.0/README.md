# GInput

This is just a simple (and dirty) python script that will take input from a string, piped stdin or clipboard and send it to a virtual keyboard using libevdev

## Installation
```
python setup.py install
```

## Usage
```
usage: ginput [-h] [-s STRING] [-c]

Type a string to virtual input device

options:
  -h, --help            show this help message and exit
  -s STRING, --string STRING
                        The string to send to the virtual input device
  -c, --clipboard       Use contents of the clipboard
```

## Examples
Type contents of clipboard:
`ginput -c`

Type contents of string:
`ginput -s "foo"`

Type contents of piped input (stdin):
`echo "foo" | ginput`
