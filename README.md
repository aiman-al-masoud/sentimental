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

### For example:

```
Enter: path
/home/user/foobar/data/Books_10000.json
Enter: filetype
json
Enter: text_field_name
reviewText
Enter: score_field_name
rating 
Enter: score_field_type
num # numerical score, as opposed to str (string score).
Enter: good_score
4   # max score on a scale of 0-4
```



### Once the model is generated you should see something like this:

```
done loading file...
using 536 reviews. Half of which positive.
done vectorizing texts...
training model... (may take a while)
all done
```

Now you can save your model, or use your model to "predict" the sentiment of a piece of text.









