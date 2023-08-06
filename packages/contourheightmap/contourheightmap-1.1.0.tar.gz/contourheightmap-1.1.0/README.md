# Contour Heightmap

A fast python library and command line tool for generating contour maps from heightmaps and images.

Given an image file (preferably RGB PNG), it will output a PNG with topographic contour lines 
and an SVG file of the contour lines.

If viewing this document on the gitlab page, you should see some example images below:

![Heightmap with contour lines](examples/heightmap_500x800.png "Contoured")
![Heightmap with contour lines](examples/heightmap_500x800_contour.png "Contoured")



![Heightmap with contour lines](examples/snowdon.png "Contoured")
![Heightmap with contour lines](examples/snowdon_contour.png "Contoured")


Questions? Contributions? Bug reports? Open an issue on the [gitlab page for the project](https://gitlab.com/dodgyville/contourheightmap).
We are very interested in hearing your use cases for `contourheightmap` to help drive the roadmap.

### Roadmap
* More control on the output image
* More control on the output svg

### Contributors
* Luke Miller

## Installing
```
pip install contourheightmap
```
or
```
py -m pip install contourheightmap
```

## Source

```
git clone https://gitlab.com/dodgyville/contourheightmap
```

# Quick Start

## How do I...

### contour an image from the shell command line?

`./contourheightmap path/to/heightmap.png`

Result will be in output.png and output.svg

### contour an image from within python?

```python
from contourheightmap import ContourHeightmap

c = ContourHeightmap()
c.contour("path/to/heightmap.png")
```

Result will be in output.png and output.svg


### provide an output filename within python?
```python
from contourheightmap import ContourHeightmap

c = ContourHeightmap()
c.contour("path/to/heightmap.png", "path/to/output.png")
```

Output will also be in path/to/output.svg


# Changelog

* 1.1.0
    - begin switch from setup.py to `pyproject` and `poetry`
    - added cli tool to make library available from command line