# Building readable artifacts

Using the batch script in the `builder` folder EPUB, Mobipocket (mobi) and PDF files could be generated from the
current text files. Preinstalled Python 3 Calibre, and Libre Office are required.
Python 3 should be added to the PATH.
Open Office is currently unsupported as its default install location has been changed but is has not been tracked by
the uniconv library.
Command to generate release:

`builder\release.cmd releasename`

Expected outputs:

```
.
+-- target
    +-- releasename.epub
    +-- releasename.mobi
    +-- releasename.pdf
```

If no Calibre and Libre Office would be present, EPUB could still be generated thanks to its pure python
implementation.
