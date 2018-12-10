import csv
import pandas as pd

def deduce_skill(grade):
    if grade < 1 or grade > 10:
        print ('Grade out of range')
        return

    if grade >= 1 and grade <= 3:
        level = 'poor'
    elif grade > 3 and grade <= 5.4:
        level = 'insufficient'
    elif grade >= 5.5 and grade <=7:
        level = 'sufficient'
    else:
        level = 'proficient'

def read_csv(f, delim=','):
	'''opens a csv reader object'''
	# return csv.reader(open(f, 'r'), delimiter=delim)
	return pd.read_csv(f, sep=';', encoding = "ISO-8859-1", engine='python', error_bad_lines=False, index_col=False) #index_col='pseudopatnummer'
	# return pd.read_csv(open(f, 'r'), sep=delim,encoding='latin-1')

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


def check_preferences(group, student):
    '''evaluation of the satisfaction of preferences for a particular student'''
    counter = 0 


    # determine the amount of preferences that are satisfied for this student
    for preference in student.preferences:
        print(preference.name)
        if preference.name == 'pref_role':
            if preference.value == determine_best(student.grades):
                preference.satisfied = True
                counter+=1

        if preference.name == 'anti_role':
            if preference.value == determine_worst(student.grades):
                # print('2')
                preference.satisfied = True
                counter+=1

        if preference.name == 'work_with':
            if preference.value in [student.name for student in group.students]:
                # print('3')
                preference.satisfied = True
                counter+=1

        if preference.name == 'not_work_with':
            if preference.value not in [student.name for student in group.students]:
                # print('4')
                preference.satisfied = True
                counter+=1
    
    return counter

def determine_best(grades):
    '''detmerine the requirement for which the student has the highest grade'''
    highest = 0
    for key, value in grades.items():
        if value > highest:
            highest = value
            best = key

    return best


def determine_worst(grades):
    '''determine the requirement for which the student has the lowest grade'''
    lowest = 10
    
    for key, value in grades.items():
        if value < lowest:
            lowest = value
            worst = key

    return worst


def switch_student(course, group, student):
    '''randomly picks a new student from a random group as long as that group has not yet been satisfied and switches
        it with the given student'''

    # determine which students we want to switch
    old_student = student  
    new_student = []

    for x_group in course.groups:
        # if x_group.satisfied == False:
            for stud in x_group.students:
                if old_student.name != stud.name:
                    new_student.append(stud)
      
    new_student = random.choice(new_student)


    # select the groups of the students that we want to switch
    group_new_student = [group for group in course.groups if new_student.group_number == group.group_number][0]
    group_old_student = group
    

    # remove respective students from their old groups
    group_old_student.remove_from_group(old_student)
    group_new_student.remove_from_group(new_student)

    # both group satisfactions need to be reset
    group_new_student.satisfied=False

    # add students to their new groups
    group_old_student.add_to_group(new_student)
    group_new_student.add_to_group(old_student)

    # change group numbers for both students
    new_student.group_number = group_old_student.group_number
    old_student.group_number = group_new_student.group_number
    return


def evaluate_prefs(course):
    ''' evaluate the performance of the group configuration based on the soft requirements'''
    eval_list = []
    for student in course.assigned_students:
        plist = []
        for preference in student.preferences:
            plist.append(preference.satisfied)

        eval_list.append(plist)


    total_satisfied = 0
    total_n_satisfied = 0

    for plist in eval_list:
        satisfaction_count = 0
        for preference in plist:
            if preference == False:
                total_n_satisfied += 1
            else:
                total_satisfied += 1

    satisfaction_rate = (float(total_satisfied) / (float(total_satisfied) + float(total_n_satisfied))) * 100
    average_satisfaction = float(total_satisfied) / float(len(course.assigned_students))

    print('The total amount of preferences that were satisfied is {}'.format(total_satisfied))
    print('The total amount of preferences that were not satisfied is {}'.format(total_n_satisfied))
    print('The satisfaction rate is {}'.format(satisfaction_rate))
    print('The average amount of satisfied preferences per student is {}'.format(average_satisfaction))


