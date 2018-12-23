
def evaluate_performance(course):
    """ evaluates the hard requirements and soft requirements and shows the selected group configuration"""
    evaluate_hard_reqs(course)
    evaluate_soft_reqs(course)
    student_assignment_output(course)


def student_assignment_output(course):
    """shows the selected group configuration"""
    for group in course.groups:

        for student in group.students:
            preferences = []
            preference_count = 0

            for preference in student.preferences:
                if preference.satisfied == True:
                   preference_count += 1

                preferences.append(",".join([preference.name, 'Satisfied:%s' % preference.satisfied]))

            print([student.name, 'Group:%s' % group.group_number, preferences, 'Satisfied:%.2f%%' % ((preference_count / 4) * 100)])
    print('...................................................................')


def evaluate_soft_reqs(course):
    ''' evaluate the performance of the group configuration based on the soft requirements'''

    eval_list = []
    # go through the list of students and a list for each student containing the satisfactions of their preferences
    for group in course.groups:
        for student in group.students:
            plist = []
            for preference in student.preferences:
                plist.append(preference.satisfied)

            eval_list.append(plist)

    total_satisfied = 0
    total_n_satisfied = 0

    # determine the total amount of preferences that are satisfied and not satisfied
    for plist in eval_list:
        satisfaction_count = 0
        for preference in plist:
            if preference == False:
                total_n_satisfied += 1
            else:
                total_satisfied += 1

    # determine the satisfaction rate (percentage of preferences satisfied)
    satisfaction_rate = (float(total_satisfied) / (float(total_satisfied) + float(total_n_satisfied))) * 100
    # determine the average amount of preferences satisfied per student
    average_satisfaction = float(total_satisfied) / float(len(course.unassigned_students))
   

    print('The total amount of preferences that were satisfied is {}'.format(total_satisfied))
    print('The total amount of preferences that were not satisfied is {}'.format(total_n_satisfied))
    print('The satisfaction rate is {}%'.format(satisfaction_rate))
    print('The average amount of satisfied preferences per student is {}'.format(average_satisfaction))
    print('...................................................................')
    print('The best result for minimal amount of students from previous group in current group has a count of {}'.format(course.min_previous))
    print('...................................................................')


def evaluate_hard_reqs(course):
    """evaluates the hard requirements"""
    
    total_n_satisfied = 0
    total_reqs_to_satisfy = 5 * len(course.groups)

    for group in course.groups:
        total_n_satisfied += group.hard_reqs_satisfied
    
    total_n_not_satisfied = total_reqs_to_satisfy - total_n_satisfied
    satisfaction_rate = (float(total_n_satisfied)/ (float(total_n_satisfied) + float(total_n_not_satisfied))) * 100
    print('...................................................................')
    print('The total amount of hard requirements that was satisfied is {}'.format(total_n_satisfied))
    print('The total amount of hard requirements that were not satisfied is {}'.format(total_n_not_satisfied))
    print('The satisfaction rate is {}%'.format(satisfaction_rate))
    print('...................................................................')
