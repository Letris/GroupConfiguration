from classes import Requirement, Preference, Group, Student
from util import *
import pandas as pd
import os
import random
import ast
import json
from tqdm import *
from itertools import permutations 
from collections import Counter

def initialize_students(course, file):
    ''' Read student data from file and add student objects to the course'''

    rows = read_csv(file)

    for index, row in rows.iterrows():
        grades = eval(row.grades)
        # grades = json.loads('"' + row.grades + '"')
        print(type(grades))
        course.add_student(Student(row.id, row.stud_name, row.courses, row.prev_comf, row.prev_names, grades, row.self_eval))

    print('Initialized students')


def determine_reqs_and_prefs(file, course):
    ''' reads requirements from csv file and creates objects from them'''
    rows = read_csv(file)

    requirement_list = []

    for index, row in rows.iterrows():
        requirement = Requirement()
        requirement.set_name(row.requirement)
        #ToDo: add more attributes?

        requirement_list.append(requirement)
        course.set_preferences(row.preference)

    course.set_requirements(requirement_list)


    print('Requirements set')


def set_preferences(directory, students):
    ''' reads preferences for each student and adds them to object'''

    for filename in os.listdir(directory):

        # extract the name of the student
        student_name = os.path.splitext(os.path.split(filename)[1])[0]

        csv_file = open(os.path.join(directory, filename))

        rows = read_csv(csv_file)

        preference_list = []

        for index, row in rows.iterrows():
            preference = Preference()
            preference.set_attributes(row.pref_name, row.type, row.value)
            preference_list.append(preference)

        for student in students:

            if student.name == student_name:
                student.preferences = preference_list


    print('Preferences set')


def specify(course, amt_groups, group_size):
    for number in range(amt_groups):
        course.add_group(Group(group_size, number))

    print('Groups made')


def propose(course):
    '''assigns students to groups randomly and then switches students untill soft requirements are satisfied'''

    # assign students to groups randomly
    for group in course.groups:
        while len(group.students) <= group.group_size - 1:
            student = random.choice(course.unassigned_students)
            # add student to group
            group.add_to_group(student)
            # assign group number to student
            student.group_number = group.group_number
            # remove student from list of unassigned students
            course.remove_student(student, course.unassigned_students)
            # add student to list of assigned students
            course.assign_student(student)

    check_soft_requirements(course)


def check_soft_requirements(course):
    'Exhaustively search for a group configuration that satisfies the soft requirements'

    group_list = course.groups
    students = course.assigned_students

    
    # generate all possible student combinations
    student_combos = permutations(students, course.group_size) 
    
    # generate all possible group configurations
    group_combos = permutations(student_combos, course.amt_groups)

    # ToDo: eliminate all group configuations with duplicates to reduce the amount of possible configs

    # go through all group configurations and determine whether soft requirements are satisfied
    for combination in tqdm(group_combos):
        list_com = list(combination)
        
        duplicate_list = []

        # check if duplicates students are in the group configuration. If so, continue to next combination

        for students in list_com:
            students = list(students)
            duplicate_list.append(students[0].name)
            duplicate_list.append(students[1].name)

        counter = Counter(duplicate_list)

        if value_check(counter) == False:
            continue
        
        satisfied=0

        for group in group_list:
            # pick a random pair of students from group configuration
            pair = random.choice(list_com)
            # remove that group the list so it can not be picked in next iteration
            list_com.remove(pair)
          
            group.students = list(pair)

            for student in group.students:
                # count the amount of preferences satisfied
                preference_counter = check_preferences(group, student)

                # count the amt of students in the group that the students has worked with in the previous course
                prev_names_counter = 0 
                for stud in group.students:
                    if stud.name in student.prev_names:
                        prev_names_counter+=1

                # if either of the counts is too high, continue to check next group configuration
                if preference_counter < 2 or prev_names_counter > 1:
                    for preference in student.preferences:
                            preference.satisfied = False

                    continue
                
                # else, up the amount of satisfied groups for this configuration
                else:
                    satisfied+=1
               
        # if all groups in this configuration are satisfied, return
        if satisfied == len(course.assigned_students):
            return





      