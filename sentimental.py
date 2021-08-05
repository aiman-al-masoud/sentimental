#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 07:56:38 2021

@author: aiman


This is a sentiment-prediction tool based on the scikitlearn libary, 
that can be used to programmatically deduce the sentiment behind 
a piece of text (POSITIVE OR NEGATIVE).


"""


import sys
import inspect
import json
import random as rand
import pickle
#from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from collections import defaultdict
import pandas as pd



#model 
model = None
#vectorizer
vectorizer = None


class FileType:
    
    """
    Supported machine readable formats for training data input.
    """
    
    JSON = "json"
    CSV = "csv"
    


class ScoreFieldType:
    
    """
    In the data file, the type of data in the score field/column.
    """
    
    NUMERICAL = "num"
    STRING = "str"



class Sentiment:
    
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    
    
    def get_from_number(number, maximum):
                
        """
        Converts a number to a POSITIVE of a NEGATIVE sentiment.
        Assumes 0=negative, maximum=positive.
        """
        
        if int(number) >= int(maximum)/2:
            return Sentiment.POSITIVE
        
        return Sentiment.NEGATIVE
        
            
    def get_from_string(string, positive):
        
        
        """
        Converts a string to a POSITIVE of a NEGATIVE sentiment.
        """
        
        if string == positive:
            return Sentiment.POSITIVE
        
        return Sentiment.NEGATIVE
    


class Review:
    
    """
    A review has a text and a sentiment (POSITIVE or NEGATIVE)
    """
    
    def __init__(self, text, sentiment):
        self.text = text
        self.sentiment = sentiment
    
    def __str__(self):
        return "Review'["+self.text+self.sentiment+"]"
    



def load_json(jsonpath):
    
    """
    Loads a json file as a list of dictionaries.
    """
    
    file = open(jsonpath)
    
    list_of_dictionaries = []
    
    #each line is a json object
    for line in file:
        list_of_dictionaries.append(json.loads(line))
    
    return list_of_dictionaries
    

def load_data(filetype, path, text_field_name, score_field_name, score_field_type, good_score):
    
    """
    Load data from a machine readable file.
    """
    
    score_function = Sentiment.get_from_number if score_field_type == ScoreFieldType.NUMERICAL else Sentiment.get_from_string

    #list of reviews used for training 
    reviews = []
    
    #for jsons:
    if(filetype==FileType.JSON):
        list_of_dictionaries = load_json(path)
        
        #convert the list of dictionaries into a list of reviews
        for dictionary in list_of_dictionaries:

           text = dictionary[text_field_name]
           score = dictionary[score_field_name]
           sentiment = score_function(score, good_score)
           review = Review(text, sentiment)
           reviews.append(review)
           
    #for csvs       
    elif(filetype==FileType.CSV):
        
        df = pd.read_csv(path, encoding='iso-8859-1')
        
        texts = list(df[text_field_name])
        scores = list(df[score_field_name])
        
        
        for i in range(len(texts)):
            review = Review(texts[i], score_function(scores[i], good_score))
            reviews.append(review)
        
        
    return reviews
    





def get_evened_out(reviews):
        
    
        """
        Get equal number of positive and negative reviews and shuffle them.
        (Chooses number of reviews of each type based on the minimum)
        """
        
        
        #filter out the positive reviews
        positives = list(filter(lambda x :  True if x.sentiment==Sentiment.POSITIVE else False, reviews))
        #filter out the negative reviews
        negatives = list(filter(lambda x :  True if x.sentiment==Sentiment.NEGATIVE else False, reviews))
        number_each = min(len(positives), len(negatives))               
        result = positives[0:number_each-1]+negatives[0:number_each-1]
        rand.shuffle(result)
        
        return result
        



def train(path, filetype, text_field_name, score_field_name, score_field_type, good_score):
    
    """
    Creates and trains the model with input data.
    """
    
    global model, vectorizer
    
    #list of reviews used for training 
    reviews = load_data(filetype, path, text_field_name, score_field_name, score_field_type, good_score)
    
    #notify user about status    
    print("done loading file...")
    
    
    #get an equal number of positive and negative reviews and shuffle them
    reviews = get_evened_out(reviews)
    
    
    print("using", len(reviews), "reviews. Half of which positive.")
    
    #get a list of texts
    train_texts_vector = [x.text for x in reviews] 
    #get a list of sentiments
    train_y_vector = [x.sentiment for x in reviews] 
    
    #create a vectorizer that takes stop words into account
    vectorizer = TfidfVectorizer()
    
    #convert the array of texts into an array of vectors (bags of words)
    train_x_vector = vectorizer.fit_transform(train_texts_vector)
        
    #notify user about status    
    print("done vectorizing texts...")
    print("training model... (may take a while)")
    
    #create and train the model
    model = svm.SVC(kernel="linear")
    model.fit(train_x_vector, train_y_vector)
    
    #notify user about status    
    print("all done")
    
    
    

def predict(text):
    """
    Predicts y given x
    """
    
    test_x_vector = []
    
    test_x_vector.append(text)
    
    x = vectorizer.transform(test_x_vector)
    
    predicted_y = model.predict(x)
    
    print(predicted_y)
    


def save(destpath):
    """
    Pickles the model and vectorizer to specified directory
    """
    
    objects = {"model" : model, "vectorizer" : vectorizer} 
    
    #open file for writing binary data
    file = open(destpath, "wb")
    
    #store the serialized model in that file
    pickle.dump(objects, file)
    


def load(sourcepath):
    """
    Loads back a pickled model and vectorizer
    """
    
    global model, vectorizer

    
    #open file in "read binary" mode
    file = open(sourcepath, "rb")
    
    #load the model from the pickled file
    objects = pickle.load(file)
        
    model = objects["model"]
    vectorizer = objects["vectorizer"]
    



def get_user_input(*args):
    
    """
    Triggers a series of prompts, collects user responses, and returns 
    them as a list.
    """
    
    argv = []
    
    for parameter in args:
        user_arg = input("Enter: "+ str(parameter)+"\n")
        argv.append(user_arg)
    
    return argv
    


def my_help():
    
    """
    Displays some help information:
    """
    print("t: train a new model\np: predict y given x\ns: save model as a binary file for later use\nl:load previously saved model from binary file\nexit: quit the program")
    

def my_exit():
    """
    Terminates the program.
    """
    sys.exit()
    

def main():
    
    """
    The main loop.
    """
    
    #dictionary that returns a callable (function).
    #by default returns the "my_help" function
    switch_case  = defaultdict(lambda : my_help)
    switch_case["t"] = train
    switch_case["p"] = predict
    switch_case["s"] = save
    switch_case["l"] = load
    switch_case["help"] = my_help    
    switch_case["exit"] = my_exit
    
    
    while True:
        mode = input("Enter command-name or 'help':\n")
        function = switch_case[mode]
        parameters = list(inspect.getfullargspec(function))[0]
        args = get_user_input(*parameters)
        function(*args)
    
    
    
#prevent execution of main if just imported as a module
if __name__ == "__main__":
    main()



