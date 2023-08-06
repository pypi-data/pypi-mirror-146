# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['contourheightmap']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0',
 'importlib>=1.0.4,<2.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['contourheightmap = contourheightmap.cli:app']}

setup_kwargs = {
    'name': 'contourheightmap',
    'version': '1.1.1',
    'description': 'A fast python library and command line tool for generating topographic contour maps from heightmaps and images.',
    'long_description': '# Contour Heightmap\n\nA fast python library and command line tool for generating contour maps from heightmaps and images.\n\nGiven an image file (preferably RGB PNG), it will output a PNG with topographic contour lines \nand an SVG file of the contour lines.\n\nIf viewing this document on the gitlab page, you should see some example images below:\n\n![Heightmap with contour lines](examples/heightmap_500x800.png "Contoured")\n![Heightmap with contour lines](examples/heightmap_500x800_contour.png "Contoured")\n\n\n\n![Heightmap with contour lines](examples/snowdon.png "Contoured")\n![Heightmap with contour lines](examples/snowdon_contour.png "Contoured")\n\n\nQuestions? Contributions? Bug reports? Open an issue on the [gitlab page for the project](https://gitlab.com/dodgyville/contourheightmap).\nWe are very interested in hearing your use cases for `contourheightmap` to help drive the roadmap.\n\n### Roadmap\n* More control on the output image\n* More control on the output svg\n\n### Contributors\n* Luke Miller\n\n## Installing\n```\npip install contourheightmap\n```\nor\n```\npy -m pip install contourheightmap\n```\n\n## Source\n\n```\ngit clone https://gitlab.com/dodgyville/contourheightmap\n```\n\n# Quick Start\n\n## How do I...\n\n### Contour an image from the shell command line?\n\n`contourheightmap path/to/heightmap.png`\n\nResult will be in output.png and output.svg\n\n\n### Provide an output file from the shell command line?\n\n`contourheightmap path/to/heightmap.png my-output.png`\n\nResult will be in my-output.png and my-output.svg\n\n\n### Contour an image from within python?\n\n```python\nfrom contourheightmap import ContourHeightmap\n\nc = ContourHeightmap()\nc.contour("path/to/heightmap.png")\n```\n\nResult will be in output.png and output.svg\n\n\n### Provide an output filename within python?\n```python\nfrom contourheightmap import ContourHeightmap\n\nc = ContourHeightmap()\nc.contour("path/to/heightmap.png", "path/to/output.png")\n```\n\nOutput will also be in path/to/output.svg\n\n\n# Changelog\n\n* 1.1.0\n    - begin switch from setup.py to `pyproject` and `poetry`\n    - added cli tool to make library available from command line',
    'author': 'Luke Miller',
    'author_email': 'dodgyville@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/dodgyville/contourheightmap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
