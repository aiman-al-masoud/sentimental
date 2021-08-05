# sentimental
A simple sentiment-analysis tool based on the sklearn library.

This project was inspired by this great video:

https://www.youtube.com/watch?v=M9Itm95JzL0


## Dependencies:
* Scikitlearn
* Pandas

### Getting 'em with pip:

```
pip install scikit-learn
pip install pandas
```



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

Sidenote: the program will use an equal number of positive and negative reviews to train the model. For example, if your file contains 300 positive reviews and only 50 negative reviews, the model will be trained with a total of 100 reviews (50 positive and 50 negtaive).

Now you can save your model, or use your model to "predict" the sentiment of a piece of text.

## Predicting Sentiment:

### Once you have a model, Try typing in:

```
p
```
## You will be prompted to enter some text.

### For instance:

```
Enter command-name or 'help':
p
Enter: text
this book is as horrible as Spam and eggs.  
['NEGATIVE']
```

## Saving a model as a pickle-file (a binary/serialized object):

Generating a model every time from raw data can become very inefficient.

### You can store a model (after having trained it) using the command:

```
s
```

### You will be prompted to enter a pathname.


## Loading a model from a pickle-file:

### Use the command:

```
l
```
You will be prompted to enter the pathname of a valid binary-file. One is already provided as an example in this repo, it contains an already-trained model. As a sidenote, the csv it was trained on contained ~ 20000 rows, and it took my compute at least half a minute to generate the model.











