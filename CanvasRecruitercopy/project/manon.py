# checkt voor elke requirement of het een requirement voor het vak is & returned het skill percentage per vak
def skills(self, student):
        percentages = []
        percentages.append(students.id[student])
        percentages.append(students.name[student])
        for requirement in self.requirements:
            if requirement == "programming":
                programming = calculation(students.programming_courses, students.likes_programming, students.programming_grade)
                percentages.append(programming[student])
            elif requirement == "presenting":
                presenting = calculation(students.presenting_courses, students.likes_presenting, students.presenting_grade)
                percentages.append(presenting[student])
            elif requirement == "writing":
                writing = calculation(students.writing_courses, students.likes_writing, students.writing_grade)
                percentages.append(writing[student])
        return percentages


course = Course("Knowledge egineering", (["programming", "presenting"]), 5) #vak heeft in dit geval 2 requirements


# berekent het skill percentage
def calculation(courses,likes,grades, students):
    percentages = []
    for student in range(len(students)):
        percentage = (courses[student] + likes[student] + grades[student]) / 30
        percentages.append(round(percentage, 2))
    return percentages


# returned voor elke student het 'skill' percentage, voor de requirements van het vak
def skills_per_student():
    skills = []
    for student in range(len(students)):
        skills.append(course.skills(student))
    return skills


print(skills_per_student())

