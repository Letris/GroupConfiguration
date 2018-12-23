from util import *

def check_minimal_preferences(group):
    '''evaluation of the satisfaction of preferences for a particular student'''

    for student in group:
        counter = 0 


        # determine the amount of preferences that are satisfied for this student
        for preference in student.preferences:
            if preference.name == 'pref_role':
                if determine_best(group, student, preference.value) == True:
                    preference.satisfied = True
                    counter+=1

            if preference.name == 'anti_role':
                if determine_worst(group, student, preference.value) == True:
                    preference.satisfied = True
                    counter+=1

            if preference.name == 'work_with':
                if preference.value in [student.name for student in group]:
                    preference.satisfied = True
                    counter+=1

            if preference.name == 'not_work_with':
                if preference.value not in [student.name for student in group]:
                    preference.satisfied = True
                    counter+=1
        
        if counter < 1:
            return False

    return True


def check_max_previous(group):
    """evaluation function for amt of students in the group that the students has worked with in the previous course requirement"""

    # for each student in given group
    for student in group:

        # count the amt of students in the group that the student has worked with in the previous course
        prev_names_counter = 0 
        for stud in group:
            if stud.name in student.prev_names:
                prev_names_counter+=1

        if prev_names_counter > 1:
            return False

    return

def check_average_per_req(course, group):
    """evaluation function for checking if the average group grade for each requirement
         is at least the minimal required average"""

    # for each course requirement
    for req in course.requirements:
        total_grade = 0

        # count the grades of all students for that requirement
        for student in group:
            grade = student.grades[req.name]
            total_grade += grade

        # check if group average is at least as high as minimal requirement
        if (total_grade / course.group_size) >= 6:
            continue
        else:
            return False

    return True


def check_comf(course, group):
    """check if any of the students in the group are in a comfortable role twice in a row"""
    # make a dictionary containing the best students for each requirement
    for req in course.requirements:
            highest = 0
            top_students = {}

            for student in group:
                if student.grades[req.name] > highest:
                    highest = student.grades[req.name]
                    top_students[req.name] = student
                else: 
                    continue

    # check for every student if they have the highest grade of the group for requirements in which they are comfortable
    for student in group:
        comfortable_requirements = []
        for key, value in student.grades.items():
            if value > 7:
                comfortable_requirements.append(key)

        for req in comfortable_requirements:
            if req in [key for key, value in top_students.items()]:
               if top_students[req] == student.name and student.prev_comf == True:
                  return False
            
    return True

def check_uncomf(course, group):
    """check if any of the students in the group are in an uncomfortable role twice in a row"""

     # make a dictionary containing the worst students for each requirement
    for req in course.requirements:
            lowest = 10
            bottom_students = {}

            for student in group:
                if student.grades[req.name] < lowest:
                    lowest= student.grades[req.name]
                    bottom_students[req.name] = student
                else: 
                    continue

    # check for every student if they have the lowest grade of the group for requirements in which they are uncomfortable
    for student in group:
        uncomfortable_requirements = []
        for key, value in student.grades.items():
            if value < 7:
                uncomfortable_requirements.append(key)

        for req in uncomfortable_requirements:
            if req in [key for key, value in bottom_students.items()]:
                if bottom_students[req] == student.name and student.prev_comf == False:
                    return False

    return True   