from classes import *
from util import *
from operationalize import *
from verify_hard import *
from sort import *
import pandas as pd
import os
import random
import ast
import json
from tqdm import *
from itertools import permutations, combinations, product
from collections import Counter
import time


def operationalize(course, stud_file, req_file, pref_dir):
    """Translates the desires of the students and the educator to requirements and initializes the course"""
    # initialize students
    initialize_students(course, stud_file)

    # set the requirements and preferences for the course
    determine_reqs_and_prefs(req_file, course)

    # set the individual preferences of the students 
    set_preferences(pref_dir, course.unassigned_students)

    

def generate(course):
    """Initalizes all groups and generates all possible configurations"""

    # initialize the group instances given the specified amount of groups and students and give each group a number (starting from 1)
    for number in range(course.amt_groups):
         course.add_group(Group(course.group_size, number))

    print('Groups have been initialized succesfully')

    # retrieve the group and student instances
    group_list = course.groups
    students = course.unassigned_students
    # generate all possible student combinations given the group size
    
    student_combos = permutations(students, course.group_size)#course.group_size) 
    
    # generate all possible group configurations given the amount of groups
    group_combos = permutations(student_combos, course.amt_groups)
    print('All possible group configurations are succesfully generated')

    # group_combos = filter(duplicate_check, group_combos)
    
    print('it worked?')
    return group_combos


def find_acceptable_configurations(course, possible_configurations, max_iter):
    """Finds all configurations that meet the hard requirements within the maximum amount of iterations"""
    accepted_configurations = []
    iteration = 0
    
    for configuration in possible_configurations:
       
        if iteration > max_iter:
            return accepted_configurations

        iteration +=1

        truth_value = propose(course,configuration)
        if truth_value == True:
            accepted_configurations.append(configuration)

    return accepted_configurations


def propose(course, configuration):
    """Proposes a single configuration to check"""
    configuration = list(configuration)
    
    # check for duplicate students in the proposed configuration and return False when found
    if duplicate_check(configuration) == False:
        return False

    # verify the hard requirements for this configuration and return the truth value
    truth_value = verify_hard(course, configuration)

    return truth_value


def verify_hard(course, configuration):
    'Verify whether the hard requirements are met for the given configuration'
    
    satisfied=0
    for iteration in range(len(course.groups)):
        # pick a random pair of students from group configuration
        group = random.choice(configuration)
        # remove that group the list so it can not be picked in next iteration
        configuration.remove(group)
        # converse tuple to list
        group = list(group)

        # go through the hard requirement checklist

        # check minimal preferences satisfied
        evaluation = check_minimal_preferences(group)

        if evaluation == False:
            return False

        # check maximal amount of students in previous group in current group
        evaluation = check_max_previous(group)

        if evaluation == False:
            return False

        # check whether the average grade of the group is at least 7 for all course requirements
        evaluation = check_average_per_req(course, group)

        if evaluation == False:
            return False

        # check comfortable role
        evaluation = check_comf(course, group)

        if evaluation == False:
            return False

        # check uncomfortable role
        evaluation = check_uncomf(course, group)
        if evaluation == False:
            return False

    
        satisfied += 1

    # if all groups in this configuration are satisfied, return
    if satisfied == len(course.groups):
        return True

def sort(course, accepted_configurations):
    """sorts the accepted configuration based on the soft requirements, selects the optimal configurations
     and assigns the students to their respective groups"""

     # variables to keep track of the current best values for the soft requirements
    current_min_previous = course.group_size-1 * len(course.unassigned_students)
    current_max_preferences = 0

    # go through the accepted configurations
    for configuration in accepted_configurations:
        new_min_previous = determine_amt_previous(configuration)
        new_max_preferences = determine_preferences_satisified(configuration)
       
       # if both soft requirements score better for the selected configuration than for the current best configuration, 
       # the selected configuration becomes the new best configuration
        if new_min_previous <= current_min_previous & new_max_preferences >= current_max_preferences :
            best_configuration = configuration
            current_min_previous = new_min_previous
            current_max_preferences = new_max_preferences
    
    # set best variables for evaluation
    course.min_previous = current_min_previous
    course.max_preferences = current_max_preferences

    best_configuration = list(best_configuration)
    # assign the students to the actual groups held by the course
    number = 0
    for group in course.groups:  
            group.students = best_configuration[number]
            number+=1
            group.hard_reqs_satisfied = 5
            
    return course



