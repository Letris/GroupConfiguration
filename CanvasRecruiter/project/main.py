from classes import Instance
from inference_functions import *
from util import *
from evaluation import *

#--------------------------------------------------------------- Parameters

# specify the file containing the student data
stud_file = '/Users/Tristan/Downloads/Uni/KnowledgeEngineering/GroupConfiguration/CanvasRecruiter/csv/scenario1/students.csv'

# specify the requirements file
req_file = '/Users/Tristan/Downloads/Uni/KnowledgeEngineering/GroupConfiguration/CanvasRecruiter/csv/scenario2/requirements.csv'

# specify the preferences directory
pref_dir = '/Users/Tristan/Downloads/Uni/KnowledgeEngineering/GroupConfiguration/CanvasRecruiter/csv/scenario2/preferences/'

# specify the amount of groups
amt_groups = 3

# specify the amount of students per groups
amt_students = 3

# specify the amount of iterations for the search (advised betweeen 20000000 and 100000000)
max_iterations = 50000000000000000

#--------------------------------------------------------------- Main

# initialize an instance of the course
course = Instance('KE', 123, 'Annette', amt_groups, amt_students)

# operationalize the desires of the teachers and students to soft and hard requirements
operationalize(course, stud_file, req_file, pref_dir)

# generate all possible group configurations
possible_combinations = generate(course)

# find all the accepted configurations within a given limit of iterations
accepted_configurations = find_acceptable_configurations(course, possible_combinations, max_iterations)

# sort the accepted configurations based on the soft requirements
course = sort(course, accepted_configurations)

# evaluate the performance of the system and show output to educator
evaluate_performance(course)

print('configuration success')

