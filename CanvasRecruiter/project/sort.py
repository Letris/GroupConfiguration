
def determine_amt_previous(configuration):
    """determines the amount of students that have worked with each other in the previous course"""
    
    prev_names_counter = 0
    for group in list(configuration):
        for student in list(group):
            prev_names_counter = 0 
            for stud in group:
                if stud.name in student.prev_names:
                    prev_names_counter += 1

    return prev_names_counter

def determine_preferences_satisified(configuration):
    """determines the total amount of preferences satisfied"""

    preferences_satisfied = 0
    for group in list(configuration):
        for student in list(group):
            for preference in student.preferences:
                if preference.satisfied == True:
                    preferences_satisfied += 1

    return preferences_satisfied