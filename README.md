# Emotional valence detection using biphone analysis

A project developed by students at New Bulgarian University for detecting emotional valence in text via phonemic analysis.

The software uses the technique described in [V. Slavova - Emotional Valence Coded in the Phonemic Content - Statistical Evidence Based on Corpus Analysis](https://www.researchgate.net/publication/342146201_Emotional_Valence_Coded_in_the_Phonemic_Content_-_Statistical_Evidence_Based_on_Corpus_Analysis).


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

