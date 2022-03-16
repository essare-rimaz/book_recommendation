import pandas as pd
import numpy as np

# from sklearn import preprocessing
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.pipeline import Pipeline
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import SGDClassifier


class PipelineClassifier:
    """
    This is the flow of my classifier, along with some notes of my decision making process or ideas.
    For the purposes of practising coding I have
    turned the classification case study into a class - it could've been done with a simple script too.

    ***

    Some websites I have used to kickstart my memory are listed below. In the end scikit-learn documentation was my primary source
    of information.
    - <https://developers.google.com/machine-learning/guides/text-classification/step-2-5>
    - <https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html>
    - <https://www.analyticsvidhya.com/blog/2021/06/part-5-step-by-step-guide-to-master-nlp-text-vectorization-approaches/>
    - <https://www.educative.io/edpresso/countvectorizer-in-python>
    - <https://towardsdatascience.com/basics-of-countvectorizer-e26677900f9c>
    """
    def __init__(self, data):
        """
        Original dataset was not readable in excel so `utf-8` encoding should do the trick.
        Making sure it will take top row as header as well.
        """
        self.data = dd.read_csv(data, encoding="latin-1", header=0, delimiter="\t")
        print(self.data.head())


    def start_dask(self):
        spark = SparkSession \
            .builder \
            .appName("Python Spark SQL basic example") \
            .config("spark.some.config.option", "some-value") \
            .getOrCreate()
        df = spark.read.csv("data\\BX-Books.csv")
        df.show()

    def change_col_names(self, names):
        """
        For the sake of simplicity I rename the columns.
        """
        old_columns = self.data.columns
        self.data.columns = names
        print(f"Changed the header from {old_columns} to: {self.data.columns}\n")

    def show_dimensions(self):
        """
        I did take a look at the dataset in the excel form, but just as a reminder, I want to know
        what I am dealing with.
        """
        print(f"The dimensions of the dataset are: {self.data.shape}\n")

    def describe_data(self):
        """
        The good news is that there is not any imputation to be done, all values are there.
        I was expecting every observation to be unique, but some repeat themselves tens of times. This
        is worth investigating.
        """
        print(f"The basic description of the dataframe and cols is:\n {self.data.describe()}")

    def search_in_text(self, string):
        """
        I used this function to take a look at how many times the value of the `dataset.text` is
        `"Galerie"` and how many it is a date. It seems that my assumption that the `dataset.text` col
        will be more informative than `dataset.title` is not necessarily true. This makes me wonder whether it would be
        a good idea to merge the two columns together.
        """
        print(f"\nExploring some observations based on text using '{string}'")
        print(self.data[self.data['text'].str.count(f'{string}') > 0])

    def show_unique_values(self, colname):
        """
        I was curious how many sports there are - Rugby is there too! yay!
        """
        print(f"\nThe unique values for the category col are:\n {self.data.get(colname).unique()}")

    def dependent_var_to_numeric(self):
        """
        This is not necessary but I wanted to give it a shot and encode the category into numeric format.
        """
        self.data["label"] = self.le.fit_transform(self.data["category"])
        print(f"This is the head of new col called 'label':\n{self.data['label'].head()}")

    def split_dataset(self, size=0.33, seed=42):
        """
        Using seed for reproducibility of result, keeping an open door for a potential
        validation data split.
        """
        X, y = self.data["text"], self.data["label"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=size, random_state=seed)
        return X_train, X_test, y_train, y_test

    def classify_by_NB(self, X_train, X_test, y_train, y_test):
        """
        `count_vectorizer` has some nice functionalities such as it should remove all interpunction
        and any word that has `len(word)<=2`. Then it turns it into tokens. `tfidf_transformer`
        implements relevance schema normalisation. Other than that NB is quick, and has decent accuracy.
        """
        text_clf = Pipeline([
            ('vect', self.count_vectorizer),
            ('tfidf', self.tfidf_transformer),
            ('clf', self.multinomial_nb),
        ])
        text_clf.fit(X_train, y_train)
        predicted = text_clf.predict(X_test)
        print(f"MultinomialNB has a success rate of: {np.mean(predicted == y_test)}")

    def classify_by_kn(self, X_train, X_test, y_train, y_test):
        """
        Takes a long time to process - but is quite good.
        """
        text_clf = Pipeline([
            ('vect', self.count_vectorizer),
            ('tfidf', self.tfidf_transformer),
            ('clf', self.kn),
        ])
        text_clf.fit(X_train, y_train)
        predicted = text_clf.predict(X_test)
        print(f"KN has a success rate of: {np.mean(predicted == y_test)}")

    def classify_by_sgd(self, X_train, X_test, y_train, y_test):
        """
        Fastest classifier with the highest accuracy. Perhaps I could finetune the hyperparameters
        """
        text_clf = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', self.sgd),
        ])
        text_clf.fit(X_train, y_train)
        predicted = text_clf.predict(X_test)
        print(f"SGD has a success rate of: {np.mean(predicted == y_test)}")








