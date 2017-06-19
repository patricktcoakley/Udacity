"""
Patrick Coakley - 2-15-2017
Udacity Project 2
Only the visualizations are enabled by default, 
and any print statements require boolean set to 'True'
This was done in order to keep the output limited 
to the visualizations on first-run
"""
#Importing all of the necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

"""
Setting the session width to be wider than default in order
to see all of the data in the console
"""

TERMINAL_WIDTH = 320
pd.set_option('display.width', TERMINAL_WIDTH)

#Importing all of the data from the CSV using Pandas
titanicData = pd.read_csv('titanic-data.csv',
                          dtype={'Age': float,'Survived': bool})
"""
Removing most columns as they are not relevant to figuring out
correlation to survival and age/gender
"""
titanicData = titanicData.drop(
    ['PassengerId','Name','SibSp','Parch','Ticket','Embarked','Cabin'],axis=1)

#Set to true to test if the data was imported and formatted correctly
if False:
    print(titanicData[:20])
"""
Creating a simple count plot to compare the surviving men and women using 
Seaborn
"""
sns.countplot(x="Sex", hue="Survived", data=titanicData)
sns.set(style="darkgrid")
plt.title('Comparison of Total Survivors by Gender')
plt.ylabel('Total Survivors')
plt.xlabel('Gender')
plt.show()

#Calculating the average fare versus the survived and dead
sns.barplot(x="Survived", y="Fare", hue="Survived",data=titanicData)
sns.set(style="darkgrid")
plt.title('Comparison of Total Survivors by Fare')
plt.ylabel('Average Fare')
plt.xlabel('Survived')
plt.show()

#Showing how class effected survivability
sns.pointplot(x="Pclass", y="Survived", dodge=True,data=titanicData)
plt.title('Comparison of Total Survivors by Fare')
plt.xlabel('Passenger Class')
plt.ylabel('Average of Survivability')
plt.show()

#Creating a violin plot that compares first class survivors to others by age/sex
plt.ylim(0,100)
sns.violinplot(x="Sex", y="Age", data=titanicData[(titanicData['Survived']==1)
                                                  & (titanicData['Pclass']==1)],
               palette="OrRd", hue="Pclass",alpha=.1,inner=None)
sns.violinplot(x="Sex", y="Age", data=titanicData[(titanicData['Survived']==1)
                                                  & (titanicData['Pclass']!=1)]
               , palette="BuPu",hue="Pclass",alpha=.9,inner=None)
plt.title('Comparison of Total Survivors by Sex, Sex, and Class')
plt.show()

#Set to true to check to see older passengers that survived against the dead
if False:
    print(titanicData[(titanicData['Survived']==1)
                      & (titanicData['Age'] >= 60)])
    print(titanicData[(titanicData['Survived']==0)
                      & (titanicData['Age'] >= 60)])

"""
Set to true to check the total count of survivors in first class against other
classes by sex against non-survivors
"""
if False:

    """
    Printing the survivors total count with age greater than zero against total
    This allows us to see the discrepancy between Unknown ages and "true" ages
    """
    print("Total survivors with numeric ages: " +
          str(len(titanicData[(titanicData['Survived']==1)
                                & (titanicData['Age'] > 0)])))
    print("Total survivors (including unknown ages): " +
          str(len(titanicData[(titanicData['Survived']==1)])) + "\n")

    #Total number of non-survivors with "true ages"
    print("Total non-survivors with numeric ages: " +
          str(len(titanicData[(titanicData['Survived'] == 0)
                                & (titanicData['Age'] > 0)])))
    print("Total non-survivors (including unknown ages): " +
          str(len(titanicData[(titanicData['Survived'] == 0)])) + "\n")

    #Print out the total of survivors and non-survivors broken down by sex
    print("Total number of female survivors: "
          + str(len(titanicData[(titanicData['Survived']==1)
                                & (titanicData['Age'] > 0)
                                & (titanicData['Sex'] == 'female')])))
    print("Total number of male survivors: "
          + str(len(titanicData[(titanicData['Survived']==1)
                                & (titanicData['Age'] > 0)
                                & (titanicData['Sex'] == 'male')])) + "\n")
    print("Total number of female non-survivors: "
          + str(len(titanicData[(titanicData['Survived']!=1)
                                & (titanicData['Age'] > 0)
                                & (titanicData['Sex'] == 'female')])))
    print("Total number of male non-survivors: "
          + str(len(titanicData[(titanicData['Survived']!=1)
                                & (titanicData['Age'] > 0)
                                & (titanicData['Sex'] == 'male')])) + "\n")

    #Print the average age of a survivor by sex
    print("The average age of a female survivor: "
          + str(titanicData.Age[(titanicData['Survived'] == 1)
                                & (titanicData['Age'] > 0)
                                & (titanicData['Sex'] == 'female')].mean()))
    print("The average age of a male survivor: "
          + str(titanicData.Age[(titanicData['Survived'] == 1)
                                & (titanicData['Age'] > 0)
                                & (titanicData['Sex'] == 'male')].mean()) 
                                + "\n")

    #Print the average age of a non-survivor by sex
    print("The average age of a female non-survivor: "
          + str(titanicData.Age[(titanicData['Survived'] == 0)
                                & (titanicData['Age'] > 0)
                                & (titanicData['Sex'] == 'female')].mean()))
    print("The average age of a male non-survivor: "
          + str(titanicData.Age[(titanicData['Survived'] == 0)
                                & (titanicData['Age'] > 0)
                                & (titanicData['Sex'] == 'male')].mean()) 
                                + "\n")

    #Print the average age of a survivor by sex in first class
    print("The average age of a female survivor in first class: "
          + str(titanicData.Age[(titanicData['Survived'] == 1)
                                & (titanicData['Age'] > 0)
                                & (titanicData['Sex'] == 'female')
                                & (titanicData['Pclass'] == 1)].mean()))
    print("The average age of a male survivor in first class: "
          + str(titanicData.Age[(titanicData['Survived'] == 1)
                                & (titanicData['Age'] > 0)
                                & (titanicData['Sex'] == 'male')
                                & (titanicData['Pclass'] == 1)].mean()) 
                                + "\n")

    #Print the average age of a survivor by sex in non-first class
    print("The average age of a female survivor in non-first class: "
          + str(titanicData.Age[(titanicData['Survived'] == 1)
                                & (titanicData['Age'] > 0)
                                & (titanicData['Sex'] == 'female')
                                & (titanicData['Pclass'] != 1)].mean()))
    print("The average age of a male survivor in non-first class: "
          + str(titanicData.Age[(titanicData['Survived'] == 1)
                                & (titanicData['Age'] > 0) 
                                & (titanicData['Sex'] == 'male')
                                & (titanicData['Pclass'] != 1)].mean()))
