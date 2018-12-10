import pandas as pd

class Course:
    def __init__(self, name, ID):
        self.name = name
        self.ID = ID
    

class Instance(Course):
    def __init__(self,  name, ID, educator, amt_groups, group_size):
        super().__init__(name, ID)

        self.educator = educator
        self.requirements = []
        self.amt_groups = amt_groups
        self.group_size = group_size
        self.unassigned_students = []
        self.assigned_students = []
        self.groups = []
        self.preferences = []

    def set_requirements(self, requirements):
        self.requirements = requirements

    def set_preferences(self, preference):
        self.preferences.append(preference)

    def add_student(self, student):
        self.unassigned_students.append(student)

    def assign_student(self, student):
        self.assigned_students.append(student)

    def remove_student(self, student, student_list):
        student_list.remove(student)

    def add_group(self, group):
        self.groups.append(group)


class Student:
    def __init__(self, ID, name, courses, prev_comf, prev_names, grades, self_eval):
        self.ID = ID
        self.name = name
        self.courses = courses
        self.preferences = []
        self.assigned = False
        self.prev_comf = prev_comf
        self.prev_names = prev_names
        self.grades = grades
        self.self_eval = self_eval
        

    def add_preference(self, preference):
        self.preferences.append(preference)

    def assign(self):
        self.assigned = True

  

class Educator:
    def __init__(self, name, courses):
        self.name = name
        self.teaches = courses


class Requirement:
    def __init__(self, req_type=None, name=None):
        self.name = name
        self.req_type = req_type 

    def set_name(self, name):
        self.name = name

class Preference:
    def __init__(self, pref_type=None, name=None):
        self.pref_type = pref_type
        self.name = name
        self.satisfied = False

    def set_attributes(self, name, pref_type, value):
        self.pref_type = pref_type
        self.name = name
        self.value = value


class Group:
    def __init__(self, group_size, group_number):
        self.group_number = group_number
        self.group_size = group_size
        self.students = []
        #self.min_grade_range = range(5.5, 6)
        #self.med_grade_range = range(6.1, 7.5)
        #self.optim_grade_range = range(7.5, 10)
        self.satisfied = False

    def add_to_group(self, student):
        self.students.append(student)
    
    def remove_from_group(self, student):
        self.students.remove(student)
