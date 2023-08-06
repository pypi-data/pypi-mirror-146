# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pinferencia',
 'pinferencia.apis',
 'pinferencia.apis.default',
 'pinferencia.apis.default.v1',
 'pinferencia.apis.default.v1.routers',
 'pinferencia.apis.kserve',
 'pinferencia.apis.kserve.v1',
 'pinferencia.apis.kserve.v1.routers',
 'pinferencia.apis.kserve.v2',
 'pinferencia.apis.kserve.v2.routers']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.75.1,<0.76.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['numpy>=1.19.5,<2.0.0'],
 ':python_version >= "3.7" and python_version < "3.8"': ['numpy>=1.20.3,<2.0.0'],
 ':python_version >= "3.8" and python_version < "4.0"': ['numpy>=1.22.3,<2.0.0'],
 'uvicorn': ['uvicorn[standard]>=0.16.0,<0.17.0']}

setup_kwargs = {
    'name': 'pinferencia',
    'version': '0.1.0rc1',
    'description': 'Aims to be the Simplest Machine Learning Model Inference Server',
    'long_description': '<h1 align="center">\n    Pinferencia\n</h1>\n\n<p align="center">\n    <em>Simple, but Powerful.</em>\n</p>\n\n<p align="center">\n    <a href="https://lgtm.com/projects/g/underneathall/pinferencia/context:python">\n        <img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/underneathall/pinferencia.svg?logo=lgtm&logoWidth=18"/>\n    </a>\n    <a href="https://codecov.io/gh/underneathall/pinferencia">\n        <img src="https://codecov.io/gh/underneathall/pinferencia/branch/main/graph/badge.svg?token=M7J77E4IWC"/>\n    </a>\n    <a href="https://opensource.org/licenses/Apache-2.0">\n        <img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg"/>\n    </a>\n    <a href="https://pypi.org/project/pinferencia/">\n        <img alt="PyPI" src="https://img.shields.io/pypi/v/pinferencia?color=green">\n    </a>\n    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pinferencia">\n</p>\n\n![Pinferencia](/docs/asserts/images/serve-model.jpg)\n\n---\n\n<p align="center">\n<a href="https://pinferencia.underneathall.app" target="_blank">\n    English Doc\n</a> |\n<a href="https://pinferencia.underneathall.app/re" target="_blank">\n    Seriously, Doc\n</a> |\n<a href="https://pinferencia.underneathall.app/zh" target="_blank">\n    中文文档\n</a> |\n<a href="https://pinferencia.underneathall.app/rc" target="_blank">\n    正襟危坐版文档\n</a>\n</p>\n\n<p align="center">\n    <em>Help wanted. Translation, rap lyrics, all wanted. Feel free to create an issue.</em>\n</p>\n\n---\n\n**Pinferencia** tries to be the simplest AI model inference server ever!\n\nServing a model with REST API has never been so easy.\n\nIf you want to\n\n- find a simple but robust way to serve your model\n- write minimal codes while maintain controls over you service\n- avoid any heavy-weight solutions\n- easily to integrate with your CICD\n- make your model and service portable and runnable across machines\n\nYou\'re at the right place.\n\n## Features\n\n**Pinferencia** features include:\n\n- **Fast to code, fast to go alive**. Minimal codes needed, minimal transformation needed. Just based on what you have.\n- **100% Test Coverage**: Both statement and branch coverages, no kidding.\n- **Easy to use, easy to understand**.\n- **Automatic API documentation page**. All API explained in details with online try-out feature.\n- **Serve any model**, even a single function can be served.\n\n## Install\n\n```bash\npip install "pinferencia[uvicorn]"\n```\n\n## Quick Start\n\n**Serve Any Model**\n\n```python title="app.py"\nfrom pinferencia import Server\n\n\nclass MyModel:\n    def predict(self, data):\n        return sum(data)\n\n\nmodel = MyModel()\n\nservice = Server()\nservice.register(\n    model_name="mymodel",\n    model=model,\n    entrypoint="predict",\n)\n```\nJust run:\n```\nuvicorn app:service --reload\n```\n\nHooray, your service is alive. Go to http://127.0.0.1/ and have fun.\n\n**Any Deep Learning Models?** Just as easy. Simple train or load your model, and register it with the service. Go alive immediately.\n\n**Pytorch**\n\n```python title="app.py"\nimport torch\n\nfrom pinferencia import Server\n\n\n# train your models\nmodel = "..."\n\n# or load your models (1)\n# from state_dict\nmodel = TheModelClass(*args, **kwargs)\nmodel.load_state_dict(torch.load(PATH))\n\n# entire model\nmodel = torch.load(PATH)\n\n# torchscript\nmodel = torch.jit.load(\'model_scripted.pt\')\n\nmodel.eval()\n\nservice = Server()\nservice.register(\n    model_name="mymodel",\n    model=model,\n)\n```\n\n**Tensorflow**\n\n```python title="app.py"\nimport tensorflow as tf\n\nfrom pinferencia import Server\n\n\n# train your models\nmodel = "..."\n\n# or load your models (1)\n# saved_model\nmodel = tf.keras.models.load_model(\'saved_model/model\')\n\n# HDF5\nmodel = tf.keras.models.load_model(\'model.h5\')\n\n# from weights\nmodel = create_model()\nmodel.load_weights(\'./checkpoints/my_checkpoint\')\nloss, acc = model.evaluate(test_images, test_labels, verbose=2)\n\nservice = Server()\nservice.register(\n    model_name="mymodel",\n    model=model,\n    entrypoint="predict",\n)\n```\n\nAny model of any framework will just work the same way. Now run `uvicorn app:service --reload` and enjoy!\n\n\n## Contributing\n\nIf you\'d like to contribute, details are [here](./CONTRIBUTING.md)',
    'author': 'Jiuhe Wang',
    'author_email': 'wjiuhe@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pinferencia.underneathall.app',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
