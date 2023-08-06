# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nlhappy',
 'nlhappy.callbacks',
 'nlhappy.configs',
 'nlhappy.datamodules',
 'nlhappy.layers',
 'nlhappy.layers.attention',
 'nlhappy.layers.classifier',
 'nlhappy.layers.embedding',
 'nlhappy.metrics',
 'nlhappy.models',
 'nlhappy.models.event_extraction',
 'nlhappy.models.language_modeling',
 'nlhappy.models.span_classification',
 'nlhappy.models.text_classification',
 'nlhappy.models.text_multi_classification',
 'nlhappy.models.text_pair_classification',
 'nlhappy.models.text_pair_regression',
 'nlhappy.models.token_classification',
 'nlhappy.models.triple_extraction',
 'nlhappy.spacy_components',
 'nlhappy.tricks',
 'nlhappy.utils']

package_data = \
{'': ['*'],
 'nlhappy.configs': ['callbacks/*',
                     'datamodule/*',
                     'experiment/*',
                     'hparams_search/*',
                     'logger/*',
                     'mode/*',
                     'model/*',
                     'trainer/*']}

install_requires = \
['catalogue>=2.0.7,<3.0.0',
 'datasets>=2.0.0,<3.0.0',
 'hydra-colorlog>=1.1.0,<2.0.0',
 'hydra-core>=1.1.1,<2.0.0',
 'onnx>=1.11.0,<2.0.0',
 'onnxruntime>=1.10.0,<2.0.0',
 'oss2>=2.15.0,<3.0.0',
 'pytorch-lightning>=1.5.10,<2.0.0',
 'rich>=12.0.0,<13.0.0',
 'spacy>=3.2.3,<4.0.0',
 'transformers>=4.17.0,<5.0.0',
 'wandb>=0.12.11,<0.13.0']

entry_points = \
{'console_scripts': ['nlhappy = nlhappy.run:train'],
 'spacy_factories': ['span_classifier = nlhappy.spacy_components:make_spancat']}

setup_kwargs = {
    'name': 'nlhappy',
    'version': '0.1.52',
    'description': '致力于SOTA的中文自然语言处理库',
    'long_description': None,
    'author': 'wangmengdi',
    'author_email': '790990241@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
