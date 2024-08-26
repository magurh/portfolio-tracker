[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://choosealicense.com/licenses/mit/)

# Portfolio Tracker

### Status

Stock Analytics:

- [x] Current portfolio dashboard: valuation and breakdown
    - [x] Defined all neccesary functions
    - ⏳ GUI integration
- [ ] Realized and unrealized gains from historic positions
- [ ] Portfolio performance over time and benchmark comparison
- [ ] Dividends and Commissions
- [ ] Tax calculation on capital gains

To be added:
- [ ] Index funds
- [ ] Crypto assets
- [ ] Forex and cash positions


### Setup

1. Clone the repository:

```
git clone https://github.com/magurh/ML-encryption.git
cd ML-encryption
```

2. Poetry is used for dependency management. Whenever new dependencies are added, run:

```
poetry install
```

To use Jupyter Lab, set the kernel to the fast-updates-monitoring environment created by poetry:

```
poetry run python -m ipykernel install --user --name=fast-updates-analysis
```

One can open Jupyter lab using `poetry run jupyter lab`. For simply activating the virtual environment, run: `poetry shell`.
To add new dependencies, use: `poetry add <dependency>`.

