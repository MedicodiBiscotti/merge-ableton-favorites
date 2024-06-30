# Merge Ableton Favourites

Ableton Live has a feature where you can add sounds and other things to user-defined collections. These are what I refer to as "favourites".

This is a tool designed to merge different favourites files.

## Motivation

I had inadvertently created multiple versions of my favourites from moving the `Ableton Folder Info` folder
and then adding more favourites in Ableton. So now I essentially have multiple backups of earlier versions that I want to merge together.
Doing that will give me an updated favourites section with all the sounds I hadn't added the second time around.

## Background knowledge

Files use [XMP](https://en.wikipedia.org/wiki/Extensible_Metadata_Platform) format, a standard for metadata developed by Adobe, often serialized to [RDF/XML](https://en.wikipedia.org/wiki/RDF/XML). The XMP files are stored in the `Ableton Folder Info` folder.

You have one file per "pack" of Ableton sounds, e.g. Core Library, Drum Booth, etc. The file names almost seem like random characters,
but the same pack will get the same file name across different versions of the favourites.
This leads to naming conflicts when trying to merge them into the same folder again.

## Libraries

I would've liked to have used [python-xmp-toolkit](https://pypi.org/project/python-xmp-toolkit/) to read the XMP files, as it specifically deals with XMP.
However, I could not get it installed on Windows, and the library might be overkill anyway, as part of the point seems to dig the XMP out of image files, and we just have RDF/XML.

To that point, we have two options:

1. Use a library that can parse RDF/XML, like [rdflib](https://pypi.org/project/rdflib/).
2. Use a library that can parse XML, like [xml.etree.ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html).

RDFLib deserializes RDF/XML into a graph, which is useful for querying and manipulating the data. It might prove useful for merging and de-duping the data.

You should also easily be able to just navigate the XML tree and selectively merge things in.

I'm interested in doing both to see which is easier to work with and which is more efficient. If I manage to implement both, I can benchmark them.
