# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytorch_ie',
 'pytorch_ie.core',
 'pytorch_ie.data',
 'pytorch_ie.data.datamodules',
 'pytorch_ie.data.datasets',
 'pytorch_ie.data.datasets.hf_datasets',
 'pytorch_ie.models',
 'pytorch_ie.models.genre',
 'pytorch_ie.models.modules',
 'pytorch_ie.taskmodules',
 'pytorch_ie.utils']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=1.17.0,<2.0.0',
 'huggingface-hub>=0.2.1,<0.3.0',
 'pytorch-lightning>=1.5.7,<2.0.0',
 'setuptools==59.5.0',
 'torchmetrics>=0.6.2,<0.7.0',
 'transformers>=4.15.0,<5.0.0']

setup_kwargs = {
    'name': 'pytorch-ie',
    'version': '0.3.2',
    'description': 'State-of-the-art Information Extraction in PyTorch',
    'long_description': 'PyTorch-IE: State-of-the-art Information Extraction in PyTorch\n==============================================================\n\n.. badges-begin\n\n| |Status| |Python Version| |License| |Read the Docs|\n| |Tests| |Codecov| |pre-commit| |Black| |Contributor Covenant|\n\n.. |Status| image:: https://badgen.net/badge/status/alpha/d8624d\n   :target: https://badgen.net/badge/status/alpha/d8624d\n   :alt: Project Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/pytorch-ie\n   :target: https://github.com/christophalt/pytorch-ie\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/github/license/christophalt/pytorch-ie\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/pytorch-ie/latest.svg?label=Read%20the%20Docs\n   :target: https://pytorch-ie.readthedocs.io/\n   :alt: Read the documentation at https://pytorch-ie.readthedocs.io/\n.. |Tests| image:: https://github.com/christophalt/pytorch-ie/workflows/Tests/badge.svg\n   :target: https://github.com/christophalt/pytorch-ie/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/christophalt/pytorch-ie/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/christophalt/pytorch-ie\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n.. |Contributor Covenant| image:: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg\n   :target: https://github.com/christophalt/pytorch-ie/blob/main/CODE_OF_CONDUCT.rst\n   :alt: Contributor Covenant\n\n.. badges-end\n\n-----\n\n🚀️ Quickstart\n---------------\n\n.. code:: console\n\n    $ pip install pytorch-ie\n\n\n⚡️ Examples\n------------\n\nSpan-classification-based Named Entity Recognition\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n.. code:: python\n\n    from pytorch_ie.taskmodules import TransformerSpanClassificationTaskModule\n    from pytorch_ie.models import TransformerSpanClassificationModel\n    from pytorch_ie import Pipeline, Document\n\n    model_name_or_path = "pie/example-ner-spanclf-conll03"\n    ner_taskmodule = TransformerSpanClassificationTaskModule.from_pretrained(model_name_or_path)\n    ner_model = TransformerSpanClassificationModel.from_pretrained(model_name_or_path)\n\n    ner_pipeline = Pipeline(model=ner_model, taskmodule=ner_taskmodule, device=-1)\n\n    document = Document("“Making a super tasty alt-chicken wing is only half of it,” said Po Bronson, general partner at SOSV and managing director of IndieBio.")\n\n    ner_pipeline(document, predict_field="entities")\n\n    for entity in document.predictions.spans["entities"]:\n        entity_text = document.text[entity.start : entity.end]\n        label = entity.label\n        print(f"{entity_text} -> {label}")\n\n    # Result:\n    # IndieBio -> ORG\n    # Po Bronson -> PER\n    # SOSV -> ORG\n\nText-classification-based Relation Extraction\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n.. code:: python\n\n    from pytorch_ie.taskmodules import TransformerRETextClassificationTaskModule\n    from pytorch_ie.models import TransformerTextClassificationModel\n    from pytorch_ie import Pipeline\n    from pytorch_ie.data import Document, LabeledSpan\n\n    model_name_or_path = "pie/example-re-textclf-tacred"\n    re_taskmodule = TransformerRETextClassificationTaskModule.from_pretrained(model_name_or_path)\n    re_model = TransformerTextClassificationModel.from_pretrained(model_name_or_path)\n\n    re_pipeline = Pipeline(model=re_model, taskmodule=re_taskmodule, device=-1)\n\n    document = Document("“Making a super tasty alt-chicken wing is only half of it,” said Po Bronson, general partner at SOSV and managing director of IndieBio.")\n\n    for start, end, label in [(65, 75, "PER"), (96, 100, "ORG"), (126, 134, "ORG")]:\n        document.add_annotation("entities", LabeledSpan(start, end, label))\n\n    re_pipeline(document, predict_field="relations")\n\n    for relation in document.predictions.binary_relations["relations"]:\n        head, tail = relation.head, relation.tail\n        head_text = document.text[head.start : head.end]\n        tail_text = document.text[tail.start : tail.end]\n        label = relation.label\n        print(f"({head_text} -> {tail_text}) -> {label}")\n\n    # Result:\n    # (Po Bronson -> SOSV) -> per:employee_of\n    # (Po Bronson -> IndieBio) -> per:employee_of\n    # (SOSV -> Po Bronson) -> org:top_members/employees\n    # (IndieBio -> Po Bronson) -> org:top_members/employees\n\n..\n  github-only\n\n✨📚✨ `Read the full documentation`__\n\n__ https://pytorch-ie.readthedocs.io/\n\nDevelopment Setup\n-----------------\n\n🏅 Acknowledgements\n---------------------\n\n- This package is based on the `sourcery-ai/python-best-practices-cookiecutter`_ and `cjolowicz/cookiecutter-hypermodern-python`_ project templates.\n\n.. _sourcery-ai/python-best-practices-cookiecutter: https://github.com/sourcery-ai/python-best-practices-cookiecutter\n.. _cjolowicz/cookiecutter-hypermodern-python: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n\n\n📃 Citation\n-------------\n\nIf you want to cite the framework feel free to use this:\n\n.. code:: bibtex\n\n    @misc{alt2022pytorchie,\n    author={Christoph Alt, Arne Binder},\n    title = {PyTorch-IE: State-of-the-art Information Extraction in PyTorch},\n    year = {2022},\n    publisher = {GitHub},\n    journal = {GitHub repository},\n    howpublished = {\\url{https://github.com/ChristophAlt/pytorch-ie}}\n    }\n',
    'author': 'Christoph Alt',
    'author_email': 'christoph.alt@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/christophalt/pytorch-ie',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
