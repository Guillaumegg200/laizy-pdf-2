from sklearn.model_selection import train_test_split

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import classification_report

import pandas as pd 
import pickle


# Read the dataset
df_label_dataset = pd.read_csv('./labelize/label_dataset.csv')
print(df_label_dataset)

# Format the dataset
X,y = df_label_dataset.text.values.astype('U'), df_label_dataset.label

# Create a batch to train and another to test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state = 42 , stratify=y)

# Create the model to make predictions
model = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', LogisticRegression(n_jobs=1, C=1e5)),
               ])
# Fit the model
model.fit(X_train, y_train)

# Predict on the batch test
y_pred = model.predict(X_test)
#print('accuracy %s' % accuracy_score(y_pred, y_test))
print(classification_report(y_test, y_pred,target_names=None))

#save the model to disk

# filename = 'label_model.sav'
# pickle.dump(model, open(filename, 'wb'))