import csv
import pandas as pd
from collections import Counter

def duplicate_check(configuration):
    """returns whether the given configuration contains any duplicate student objects"""

    duplicate_list = []

    # create a counter for the student names in the configuration

    for group in configuration:
        students = list(group)
        duplicate_list.append(students[0].name)
        duplicate_list.append(students[1].name)

    counter = Counter(duplicate_list)

    # check if duplicates are in the current configuration
    if value_check(counter) == False:
        return False

def read_csv(f, delim=','):
	'''opens a csv reader object'''

	return pd.read_csv(f, sep=';', encoding = "ISO-8859-1", engine='python', error_bad_lines=False, index_col=False) #index_col='pseudopatnummer'


def value_check(counter):
    '''function that returns whether duplicate elements were found'''
    for value in counter.values():
        if value > 1:
            return False

    return True


def all_satisfied(groups):
    '''check of all groups are satisfied'''
    for group in groups:
        if group.satisfied == False:
            return False

    return True 


def determine_best(group, student, pref_value):
    '''detmerine the requirement for which the student has the highest grade'''

    # create a dictionary that for each students in the goup holds the grade for their preferred skill
    best_dict = {}
    for stud in group:
        highest = 0
        for key, value in stud.grades.items():
            if value > highest:
                highest = value
                best = key

        if best == pref_value:
            best_dict[stud.name] = {best : highest}

    # determine whether the given student has the highest grade in the group for their preferred skill 
    highest = 0
    for stud, grade_dict in best_dict.items():
        for role, grade in grade_dict.items():
            if grade > highest:
                highest = grade
                best = stud

    if best == student.name:          
        return True
    else: 
        return False


def determine_worst(group, student, pref_value):
    '''determine the requirement for which the student has the lowest grade'''

    # create a dictionary that for each students in the goup holds the grade for their unpreferred skill
    worst_dict = {}
    for stud in group:
        lowest = 10
        for key, value in stud.grades.items():
            if value < lowest:
                lowest = value
                worst = key

        if worst == pref_value:
            worst_dict[stud.name] = {worst : lowest}

     # determine whether the given student has the lowest grade in the group for their unpreferred skill
    lowest = 0
    for stud, grade_dict in worst_dict.items():
        for role, grade in grade_dict.items():
            if grade < lowest:
                lowest = grade
                worst = stud

    if worst == student.name:          
        return True
    else: 
        return False


