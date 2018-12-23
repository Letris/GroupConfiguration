from classes import *
from util import *
import pandas as pd
import os
import random
import ast
import json

def initialize_students(course, file):
    ''' Read student data from file and add student objects to the course'''

    rows = read_csv(file)

    # create student objects and add them to the course
    for index, row in rows.iterrows():
        grades = eval(row.grades)
        course.add_student(Student(row.id, row.stud_name, row.courses, row.prev_comf, row.prev_names, grades, row.self_eval))

    print('Initialized students')

    return course

def determine_reqs_and_prefs(file, course):
    ''' reads requirements from csv file and creates objects from them'''
    rows = read_csv(file)

    requirement_list = []

    # create requirement and preference objects for each requirement and possible preference set by the teacher and add them to the course
    for index, row in rows.iterrows():
        requirement = Requirement()
        requirement.set_name(row.requirement)

        requirement_list.append(requirement)
        course.set_preferences(row.preference)

    course.set_requirements(requirement_list)


    print('Requirements set')
    return course

def set_preferences(directory, students):
    ''' reads preferences for each student and adds them to object'''

    for filename in os.listdir(directory):

        # extract the name of the student
        student_name = os.path.splitext(os.path.split(filename)[1])[0]

        csv_file = open(os.path.join(directory, filename))

        rows = read_csv(csv_file)

        preference_list = []

        # create preference objects for each of the preferences specified by the students
        for index, row in rows.iterrows():
            preference = Preference()
            preference.set_attributes(row.pref_name, row.type, row.value)
            preference_list.append(preference)

        for student in students:

            if student.name == student_name:
                student.preferences = preference_list


    print('Preferences set')
