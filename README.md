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

2. Create and Activate Virtual Environment

On Windows:
```
python -m venv venv
venv\Scripts\activate
```

On MacOS/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Set path (for absolute imports)

On Windows:
```
set PYTHONPATH=.
```

On MacOS/Linux:
```
export PYTHONPATH=.
```

5. Run app:

```
python app/gui.py
```

