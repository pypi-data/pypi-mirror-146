# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sdd_segmentation']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.0,<2.0.0']

setup_kwargs = {
    'name': 'sdd-segmentation',
    'version': '0.1.0a0',
    'description': "The python implementation of algorithm proposed by Z. Wang, 'A New Approach for Segmentation and Quantification of Cells or Nanoparticles,' in IEEE Transactions on Industrial Informatics, vol. 12, no. 3, pp. 962-971, June 2016, DOI: 10.1109/TII.2016.",
    'long_description': '# Slope Difference Distribution Segmentation\n\nThe python implementation of algorithm proposed by Z. Wang, "A New Approach for Segmentation and Quantification of Cells or Nanoparticles," in IEEE Transactions on Industrial Informatics, vol. 12, no. 3, pp. 962-971, June 2016, DOI: 10.1109/TII.2016.\n\n## Description\nLet people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.\n\n## Badges\n\nTODO: Add bagdes https://shields.io/\n\n## Visuals\nDepending on what you are making, it can be a good idea to include screenshots or even a video (you\'ll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.\n\n## Installation\n\nYou can install ``sdd-segmentation`` directly from PyPi via ``pip``:\n\n```bash\n    pip install sdd-segmentation\n```\n\n## Usage\nUse examples liberally, and show the expected output if you can. It\'s helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.\n\n## License\n\nThis software is licensed under the BSD 3-Clause License.\n\nIf you use this software in your scientific research, please cite our paper:\n\n```bibtex\n\n```\n\nAND original [work](https://doi.org/10.1109/TII.2016.2542043):\n```bibtex\n@ARTICLE{Wang2016,\n    author={Wang, ZhenZhou},\n    journal={IEEE Transactions on Industrial Informatics}, \n    title={A New Approach for Segmentation and Quantification of Cells or Nanoparticles}, \n    year={2016},\n    volume={12},\n    number={3},\n    pages={962-971},\n    doi={10.1109/TII.2016.2542043}\n}\n```\n\n## Project status\nIf you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.\n',
    'author': 'Aleksandr Sinitca',
    'author_email': 'siniza.s.94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/digiratory/sdd-segmentation',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
