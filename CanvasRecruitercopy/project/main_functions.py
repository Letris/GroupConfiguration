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


    # if soft reqs already met: return. Else: start going through other options
    for group in course.groups:
        truth_value = check_soft(group)
        if truth_value == False:
            course = verify_soft(course)

    return course


def verify_soft(course):
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

            truth_value = check_soft(group)

            if truth_value == False:
                continue

            else:
                satisfied += 1

               
        # if all groups in this configuration are satisfied, return
        if satisfied == len(course.assigned_students):
            return course


def check_soft(group):
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

            return False
                
                # else, up the amount of satisfied groups for this configuration
        
    return True


def verify_hard(course):
    for group in course.groups:
        truth_value = check_hard(course, group)
        if truth_value == True:
            return

    group_list = course.groups
    students = course.assigned_students

    # check if current configuration already adheres to hard reqs
    

    # generate all possible student combinations
    student_combos = permutations(students, course.group_size) 
    
    # generate all possible group configurations
    group_combos = permutations(student_combos, course.amt_groups)
    
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

            truth_value = check_hard(course, group)

            if truth_value == False:
                continue

            else:
                satisfied += 1

        # if all groups in this configuration are satisfied, return
        if satisfied == len(course.assigned_students):
            return course


def check_hard(course, group):
    x = check_average_per_req(course, group)

    if x == False:
        print('xxxxxx')
        return False

    y = check_comf(course, group)

    if y == False:
        print('yyyyyy')
        return False

    z = check_uncomf(course, group)

    if z == False:
        print('zzzzzz')
        return False


def check_average_per_req(course, group):
    for req in course.requirements:
        total_grade = 0

        for student in group.students:

            grade = student.grades[req.name]
            total_grade += grade

        if (total_grade / group.group_size) >= 7:
            continue
        else:
            return False

    return True


def check_comf(course, group):
    # make a dictionary containing the best students for each requirement
    for req in course.requirements:
            highest = 0
            top_students = {}

            for student in group.students:
                if student.grades[req.name] > highest:
                    highest = student.grades[req.name]
                    top_students[req.name] = student
                else: 
                    continue

    # check for every student if they have the highest grade of the group for requirements in which they are comfortable
    for student in group.students:
        comfortable_requirements = []
        for key, value in student.grades.items():
            if value > 7:
                comfortable_requirements.append(key)

        for req in comfortable_requirements:
            if top_students[req] == student.name and student.prev_comf == True:
                return False

    return True


def check_uncomf(course, group):
     # make a dictionary containing the worst students for each requirement
    for req in course.requirements:
            lowest = 10
            bottom_students = {}

            for student in group.students:
                if student.grades[req.name] < lowest:
                    lowest= student.grades[req.name]
                    bottom_students[req.name] = student
                else: 
                    continue

    # check for every student if they have the lowest grade of the group for requirements in which they are uncomfortable
    for student in group.students:
        uncomfortable_requirements = []
        for key, value in student.grades.items():
            if value < 7:
                uncomfortable_requirements.append(key)

        for req in uncomfortable_requirements:
            if bottom_students[req] == student.name and student.prev_comf == False:
                return False

    return True    
