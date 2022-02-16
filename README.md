# Emotional valence detection using biphone analysis

## Install

Recommended version of Python is 3.9.

```bash
# create a virtual environment and activate it
python -m venv env
source env/bin/activate

# install all dependencies
pip install -r requirements.txt

# install additional library modules that are required
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt')"
```

