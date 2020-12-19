## Data
* [NYT10](https://raw.githubusercontent.com/thunlp/NRE/master/data.zip)
* [en_core_web_lg](https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-2.3.0/en_core_web_lg-2.3.0.tar.gz)
* [en_core_web_sm](https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.0.0/en_core_web_sm-2.0.0.tar.gz)

## Usage
1. Download and unzip the `NYT10` data and put it in the current folder.
2. Delete `test.txt` and random sample 20% items from `train.txt` as the new `test.txt`.
3. Download `en_core_web_lg` or `en_core_web_sm` of spaCy and put it in the current folder.
4. Put corpus into the `data` folder.
5. Put the target relation set into the `data` folder.
6. Run `wikidataautolabelling.py`.
```shell
python3 wikidataautolabelling.py
```
7. Run `preprocess.py`.
8. Run the following concands.
```shell
python3 run.py --encoder='cnn' --selector='one'
python3 run.py --encoder='cnn' --selector='att'
python3 run.py --encoder='cnn' --selector='avg'
python3 run.py --encoder='pcnn' --selector='one'
python3 run.py --encoder='pcnn' --selector='att'
python3 run.py --encoder='pcnn' --selector='avg'
```
9. Run `draw.py` to visualize the results.
```shell
python3 draw.py
```
