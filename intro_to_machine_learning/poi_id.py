#!/usr/bin/python

import sys
import pickle
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

# These are all of the features that will be helpful in
# feature selection below
features_list = [
            'poi',
            'bonus',
            'deferral_payments',
            'deferred_income',
            'director_fees',
            'exercised_stock_options',
            'expenses',
            'from_messages',
            'from_poi_to_this_person',
            'from_this_person_to_poi',
            'long_term_incentive',
            'loan_advances',
            'other',
            'restricted_stock',
            'restricted_stock_deferred',
            'salary',
            'shared_receipt_with_poi',
            'to_messages',
            'total_payments',
            'total_stock_value'
                ]


# Load the dictionary containing the dataset
with open('final_project_dataset.pkl', 'r') as data_file:
    data_dict = pickle.load(data_file)


# Uncomment for example of employee and their standard features
# from pprint import pprint
# pprint (data_dict['KOPPER MICHAEL J'])

# Find the number of POIs and NaNs in our data
pois = []
nans = []
for k,v in data_dict.iteritems():
    if data_dict[k]['poi'] == True:
        pois.append(k)
    for i in features_list:
        if data_dict[k][i] == 'NaN':
            nans.append(v)

print '      ///////////////////////////////////////////////////////'
print '     // Total number of employees:',len(data_dict.keys()),'//'.rjust(21,' ')
print '    // Total number of POIs:',len(pois),'//'.rjust(27,' ')
print '   // Total number of features for each employee:',len(data_dict['KOPPER MICHAEL J']),'//'.rjust(5,' ')
print '  // Total number of NaNs in the dictionary',len(nans),'//'.rjust(8,' ')
print ' ///////////////////////////////////////////////////////','\n'



# Uncomment to check for outliers
# data_copy = featureFormat(data_dict, ['salary','bonus'])
# import matplotlib.pyplot
# salaries = []
# for point in data_copy:
#     salary = point[0]
#     bonus = point[1]
#     salaries.append(point[0])
#     matplotlib.pyplot.scatter(salary, bonus)
#
# matplotlib.pyplot.xlabel('Salary')
# matplotlib.pyplot.ylabel('Bonus')
# matplotlib.pyplot.title('Comparison of Salary to Bonus of Enron Employes')
# matplotlib.pyplot.show()

# Find the outlier on the scatter plot and set it to a variable to find
# max_salary =  max(salaries)
# for k,v in data_dict.iteritems():
#     if data_dict[k]['salary'] == max_salary:
#         print k,'is an outlier.'

# Create new features
# features_list.append('from_poi_to_person_ratio')
# features_list.append('from_person_to_poi_ratio')
#
# for k in data_dict:
#     data_dict[k]['from_poi_to_person_ratio'] = 0
#     data_dict[k]['from_person_to_poi_ratio'] = 0
#     if (data_dict[k]['from_messages'] != 'NaN' and
# 		data_dict[k]['from_messages'] != 0 and
# 		data_dict[k]['from_poi_to_this_person'] != 'NaN' and
# 		data_dict[k]['from_poi_to_this_person'] != 0) :
#             data_dict[k]['from_poi_to_person_ratio'] = data_dict[k]['from_poi_to_this_person'] / \
#                                                        float(data_dict[k]['from_messages'])
#     elif (data_dict[k]['to_messages'] != 'NaN' and
#           data_dict[k]['to_messages'] != 0 and
#           data_dict[k]['from_this_person_to_poi'] != 'NaN' and
#           data_dict[k]['from_this_person_to_poi'] != 0):
#             data_dict[k]['from_person_to_poi_ratio'] = data_dict[k]['from_this_person_to_poi'] / \
#                                                        float(data_dict[k]['to_messages'])
#     else:
#         data_dict[k]['from_poi_to_person_ratio'] = 0
#         data_dict[k]['from_person_to_poi_ratio'] = 0


# Remove NaNs by setting to 0.0
data = featureFormat(data_dict, features_list, remove_NaN=True, sort_keys = True)
labels, features = targetFeatureSplit(data)

for k,v in data_dict.iteritems():
    for i in features_list:
        if data_dict[k][i] == 'NaN':
            data_dict[k][i] = 0.0

# Removing outlier
data_dict.pop('TOTAL',0)

# This entry is not part of the list of employees
data_dict.pop('THE TRAVEL AGENCY IN THE PARK',0)

# Uncomment to make sure new features work
# from pprint import pprint
# pprint(data_dict['HICKERSON GARY J'])
# pprint(data_dict['FREVERT MARK A'])


# Create copy of dataset
my_dataset = data_dict

# Setup cross validation
from sklearn.cross_validation import StratifiedShuffleSplit
sss = StratifiedShuffleSplit(labels,100, random_state = 32)

# Import modules for classification
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import precision_score, recall_score

# Import feature selection modules
from sklearn.feature_selection import SelectKBest
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.grid_search import GridSearchCV

# Import pipeline module
from sklearn.pipeline import Pipeline

# Declare pipeline line-by-line for easy commenting out
pipe = Pipeline(steps = [
    ('MinMaxScaler', MinMaxScaler()),
    ('SKB', SelectKBest()),
    #('PCA', PCA()),
    ('NaiveBayes', GaussianNB()),
    #('DTC',DecisionTreeClassifier()),
    #('SVC', SVC())
    ])

# Define grid search params line-by-line for easy commenting out
params = {
        'SKB__k': [5],
        #'PCA__n_components': [1,2,3],
        # 'DTC__criterion': ('gini','entropy'),
        # 'DTC__splitter':('best','random'),
        # 'DTC__min_samples_split': [2,3,4],
        # 'DTC__max_depth': [20,25,30],
        # 'DTC__max_leaf_nodes': [8,15,25],
        #'SVC__kernel':['rbf','linear'],
        #'SVC__C':[1,50,250,1000,2000],
         }

# Prepare the grid search
gs = GridSearchCV(pipe,param_grid=params,scoring='f1',cv=sss)

# Train data
gs.fit(features, labels)

# Scores
scores = gs.grid_scores_
print scores,'\n'

# Print the SelectKBest results
skb_features =  gs.best_estimator_.named_steps['SKB'].get_support(indices=True)
selected_features = []
for i in skb_features:
    selected_features.append(features_list[i+1])
print 'SelectKBest results:',selected_features,'\n'

# Print results
clf = gs.best_estimator_
print 'The best parameters:',gs.best_params_,'\n'

# Uncomment to test against tester.py
# Set time to current time
from time import time
t0 = time()
from tester import test_classifier
test_classifier(clf,my_dataset,features_list)
print 'Training time:', round(time()-t0,3),'s'

# Dump classifier, dataset, and features_list
dump_classifier_and_data(clf, my_dataset, features_list)



















