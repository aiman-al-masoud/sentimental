# sentimental
A simple sentiment-analysis tool based on the sklearn library.

## Dependencies:
* Scikitlearn
* Pandas


## Starting the Program:

### In your shell:

```
python3 sentimental.py
```
### Output:

```
Enter command-name or 'help':
```

## Training:

### To create a new model object and train it with fresh data, type in:

```
t
```
### You'll be prompted to enter:

* path: the path to the csv or json that contains your training data.
* filetype: csv or json
* text_field_name: the name of the column/field in the csv/json that contains the natlang text.
* score_field_name: ... that contains the text's score (how positive-negative the feeling it expresses is).
* score_field_type: the type of score_field_name. It's either "num" (eg: 0 to 5) or "str" (POSITIVE, NEGATIVE)
* good_score: this is the (+ve) maximum score in case of a numerical score_field_type (NB: assuming 0 is the least score). If score_field_type is a string, it's the string literal that indicates a positive score in the data file (eg: "POSITIVE").





