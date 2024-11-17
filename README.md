[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://choosealicense.com/licenses/mit/)

# Portfolio Tracker

### Status

Stock Analytics: (Currently only testing in jupyter notebooks)

- [x] Current portfolio dashboard: valuation and breakdown
- [X] Realized and unrealized gains from historic positions (FIFO method)
- [ ] Portfolio performance over time and benchmark comparison
- [ ] Dividends and Commissions
- [ ] Tax calculation on capital gains

To be added at a later stage:
- [ ] Compatibility with Google sheets
- [x] Index funds
    - TODO: Possibly create separate tracker for owned index funds from individual stocks
- [ ] Crypto assets
- [ ] Forex and cash positions

Bugs to be fixed:
- [ ] Fetching exchange rates


### Setup

1. Clone the repository:

```bash
git clone https://github.com/magurh/ML-encryption.git
cd ML-encryption
```

2. `uv` is used for dependency management. Whenever new dependencies are added, run:

```bash
uv sync --all-extras
```

To use Jupyter Lab, set the kernel to the fast-updates-monitoring environment created by poetry:

```bash
uv run python -m ipykernel install --user --name=fast-updates-analysis
```

One can open Jupyter lab using `poetryuv run jupyter lab`. To add new dependencies, use: `uv add <dependency>`.


3. Add your data in the `data` folder and follow formatting instructions [TBD]. Make sure that all tickers are available through `yfinance` package -- for instance, VUSA needs to be replaced by VUSA.AS.