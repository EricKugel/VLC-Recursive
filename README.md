# VLC Recursive

When you open a folder in VLC and try to shuffle all contents recursively, VLC picks one subfolder and plays all files from that, then repeats. This isn't ideal. This is a script to create a playlist file including ALL files in a directory, recursively.

This is built with a python package to make it easy to get the command installed.

### Installation

```
pip install .
```

### Usage

```
vlcr [PATH]
```

Ignore any AudioMetadataWarning warnings.

## Update

I recently found out that VLC does this if you choose Tools -> Preferences -> All -> Playlist -> Subdirectory behavior -> Expand.
