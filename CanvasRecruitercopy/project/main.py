from classes import Instance
from main_functions import specify, determine_reqs_and_prefs, set_preferences, initialize_students, propose, evaluate_prefs

#--------------------------------------------------------------- Parameters

# specify the file containing the student data
stud_file = '/Users/Tristan/Downloads/Uni/KnowledgeEngineering/CanvasRecruiter/csv/students.csv'

# specify the requirements file
req_file = '/Users/Tristan/Downloads/Uni/KnowledgeEngineering/CanvasRecruiter/csv/requirements.csv'

# specifify the preferences directory
pref_dir = '/Users/Tristan/Downloads/Uni/KnowledgeEngineering/CanvasRecruitercopy/csv/preferences/'

#--------------------------------------------------------------- Main

# initialize an instance of the course
course = Instance('KE', 123, 'Annette', 5, 2)

# initialize students
initialize_students(course, stud_file)

# create the groups
specify(course, course.amt_groups, course.group_size)

# set the requirements and preferences for the course
determine_reqs_and_prefs(req_file, course)

# set the individual preferences of the students 
set_preferences(pref_dir, course.unassigned_students)

# propose the first initialization based on soft requirements
propose(course)

# evaluate the performance of the first initialization
evaluate_prefs(course)



