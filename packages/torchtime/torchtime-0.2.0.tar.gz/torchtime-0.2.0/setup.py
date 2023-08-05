# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['torchtime']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0',
 'sklearn>=0.0,<0.1',
 'sktime>=0.10.1,<0.11.0',
 'torch>=1.11.0,<2.0.0']

setup_kwargs = {
    'name': 'torchtime',
    'version': '0.2.0',
    'description': 'Time series data sets for PyTorch',
    'long_description': '# Time series data sets for PyTorch\n\n[![PyPi](https://img.shields.io/pypi/v/torchtime)](https://pypi.org/project/torchtime)\n[![Build status](https://img.shields.io/github/workflow/status/philipdarke/torchtime/build.svg)](https://github.com/philipdarke/torchtime/actions/workflows/build.yml)\n![Coverage](https://philipdarke.com/torchtime/assets/coverage-badge.svg)\n[![License](https://img.shields.io/github/license/philipdarke/torchtime.svg)](https://github.com/philipdarke/torchtime/blob/main/LICENSE)\n[![DOI](https://zenodo.org/badge/475093888.svg)](https://zenodo.org/badge/latestdoi/475093888)\n\nReady-to-go PyTorch data sets for supervised time series prediction problems. `torchtime` currently supports:\n\n* All data sets in the UEA/UCR classification repository [[link]](https://www.timeseriesclassification.com/)\n\n* PhysioNet Challenge 2019 (sepsis prediction) [[link]](https://physionet.org/content/challenge-2019/1.0.0/)\n\n## Installation\n\n```bash\n$ pip install torchtime\n```\n\n## Example usage\n\n`torchtime.data` contains a class for each data set above. Each class has a consistent API.\n\nThe `torchtime.data.UEA` class returns the UEA/UCR data set specified by the `dataset` argument (see list of data sets [here](https://www.timeseriesclassification.com/dataset.php)). For example, to load training data for the [ArrowHead](https://www.timeseriesclassification.com/description.php?Dataset=ArrowHead) data set with a 70/30% training/validation split and create a [DataLoader](https://pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader):\n\n```python\nfrom torch.utils.data import DataLoader\nfrom torchtime.data import UEA\n\narrowhead = UEA(\n    dataset="ArrowHead",\n    split="train",\n    train_prop=0.7,\n    seed=123\n)\ndataloader = DataLoader(arrowhead, batch_size=32)\n```\n\nBatches are dictionaries of tensors `X`, `y` and `length`.\n\n`X` are the time series data. The package follows the *batch first* convention therefore `X` has shape (*n*, *s*, *c*) where *n* is batch size, *s* is (maximum) trajectory length and *c* is the number of channels. By default, a time stamp is appended to the time series data as the first channel.\n\n`y` are one-hot encoded labels of shape (*n*, *l*) where *l* is the number of classes and `length` are the length of each trajectory (before padding if series are of irregular length) i.e. a tensor of shape (*n*).\n\nArrowHead is a univariate time series therefore `X` has two channels, the time stamp followed by the time series (*c* = 2). Each series has 251 observations (*s* = 251) and there are three classes (*l* = 3).\n\n```python\nnext_batch = next(iter(dataloader))\n\nnext_batch["X"].shape  # (32, 251, 2)\nnext_batch["y"].shape  # (32, 3)\nnext_batch["length"].shape  # (32)\n```\n\n## Additional options\n\n* The `split` argument determines whether training, validation or test data are returned. The size of the splits are controlled with the `train_prop` and `val_prop` arguments.\n\n* Missing data can be imputed by setting `impute` to *mean* (replace with training data channel means) or *forward* (replace with previous observation). Alternatively a custom imputation function can be used.\n\n* A time stamp, missing data mask and the time since previous observation can be appended to the time series data with the boolean arguments ``time``, ``mask`` and ``delta`` respectively.\n\n* For reproducibility, an optional random `seed` can be specified.\n\nMost UEA/UCR data sets are regularly sampled and fully observed. Missing data can be simulated using the `missing` argument to drop data at random from UEA/UCR data sets. See the [tutorials](https://philipdarke.com/torchtime/tutorials/index.html) and [API](https://philipdarke.com/torchtime/api/index.html) for more information.\n\n## Acknowledgements\n\n`torchtime` uses some of the data processing ideas in Kidger et al, 2020 [[1]](https://arxiv.org/abs/2005.08926) and Che et al, 2018 [[2]](https://doi.org/10.1038/s41598-018-24271-9).\n\nThis work is supported by the Engineering and Physical Sciences Research Council, Centre for Doctoral Training in Cloud Computing for Big Data, Newcastle University (grant number EP/L015358/1).\n\n## References\n\n1. Kidger, P, Morrill, J, Foster, J, *et al*. Neural Controlled Differential Equations for Irregular Time Series. *arXiv* 2005.08926 (2020). [[arXiv]](https://arxiv.org/abs/2005.08926)\n\n1. Che, Z, Purushotham, S, Cho, K, *et al*. Recurrent Neural Networks for Multivariate Time Series with Missing Values. *Sci Rep* 8, 6085 (2018). [[doi]](https://doi.org/10.1038/s41598-018-24271-9)\n\n1. Reyna, M, Josef, C, Jeter, R, *et al*. Early Prediction of Sepsis From Clinical Data: The PhysioNet/Computing in Cardiology Challenge. *Critical Care Medicine* 48 2: 210-217 (2019). [[doi]](https://doi.org/10.1097/CCM.0000000000004145)\n\n1. Reyna, M, Josef, C, Jeter, R, *et al*. Early Prediction of Sepsis from Clinical Data: The PhysioNet/Computing in Cardiology Challenge 2019 (version 1.0.0). *PhysioNet* (2019). [[doi]](https://doi.org/10.13026/v64v-d857)\n\n1. Goldberger, A, Amaral, L, Glass, L, *et al*. PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. *Circulation* 101 (23), pp. e215–e220 (2000). [[doi]](https://doi.org/10.1161/01.cir.101.23.e215)\n\n1. Löning, M, Bagnall, A, Ganesh, S, *et al*. sktime: A Unified Interface for Machine Learning with Time Series. *Workshop on Systems for ML at NeurIPS 2019* (2019). [[doi]](https://doi.org/10.5281/zenodo.3970852)\n\n1. Löning, M, Bagnall, A, Middlehurst, M, *et al*. alan-turing-institute/sktime: v0.10.1 (v0.10.1). *Zenodo* (2022). [[doi]](https://doi.org/10.5281/zenodo.6191159)\n\n## License\n\nReleased under the MIT license.\n',
    'author': 'Philip Darke',
    'author_email': 'hello@philipdarke.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://philipdarke.com/torchtime',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
