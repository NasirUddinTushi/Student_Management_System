import json

# Class 1: Person
class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):
        print(f"Name: {self.name}\nAge: {self.age}\nAddress: {self.address}")

# Class 2: Student (Inherits from Person)
class Student(Person):
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}  # {subject: grade}
        self.courses = []  # List of enrolled courses

    def add_grade(self, subject, grade):
        self.grades[subject] = grade

    def enroll_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def display_student_info(self):
        self.display_person_info()
        print(f"ID: {self.student_id}\nEnrolled Courses: {', '.join(self.courses) if self.courses else 'None'}")
        print(f"Grades: {self.grades if self.grades else 'No grades assigned'}")

# Class 3: Course
class Course:
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []  # List of enrolled students

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)

    def display_course_info(self):
        print(f"Course Name: {self.course_name}\nCode: {self.course_code}\nInstructor: {self.instructor}")
        print(f"Enrolled Students: {', '.join(self.students) if self.students else 'No students enrolled'}")

# Database for storing students and courses
students = {}
courses = {}

# Save Data to File
def save_data(filename="data.json"):
    try:
        data = {
            "students": {sid: vars(student) for sid, student in students.items()},
            "courses": {cid: vars(course) for cid, course in courses.items()}
        }
        with open(filename, "w") as f:
            json.dump(data, f,indent=4)
        print("All student and course data saved successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")

# Load Data from File
def load_data(filename="data.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        for sid, sdata in data["students"].items():
            student = Student(sdata["name"], sdata["age"], sdata["address"], sdata["student_id"])
            student.courses = sdata["courses"]
            student.grades = sdata["grades"]
            students[sid] = student
        for cid, cdata in data["courses"].items():
            course = Course(cdata["course_name"], cdata["course_code"], cdata["instructor"])
            course.students = cdata["students"]
            courses[cid] = course
        print("Data loaded successfully.")
    except FileNotFoundError:
        print("No saved data found.")
    except Exception as e:
        print(f"Error loading data: {e}")

# Menu-Driven CLI
def main():
    while True:
        print("\n==== Student Management System ====")
        print("1. Add New Student")
        print("2. Add New Course")
        print("3. Enroll Student in Course")
        print("4. Add Grade for Student")
        print("5. Display Student Details")
        print("6. Display Course Details")
        print("7. Save Data to File")
        print("8. Load Data from File")
        print("0. Exit")

        option = input("Select Option: ")

        if option == "1":
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            address = input("Enter Address: ")
            student_id = input("Enter Student ID: ")
            if student_id in students:
                print("Student ID already exists.")
            else:
                students[student_id] = Student(name, age, address, student_id)
                print(f"Student {name} (ID: {student_id}) added successfully.")

        elif option == "2":
            course_name = input("Enter Course Name: ")
            course_code = input("Enter Course Code: ")
            instructor = input("Enter Instructor Name: ")
            if course_code in courses:
                print("Course code already exists.")
            else:
                courses[course_code] = Course(course_name, course_code, instructor)
                print(f"Course {course_name} (Code: {course_code}) created with instructor {instructor}.")

        elif option == "3":
            student_id = input("Enter Student ID: ")
            course_code = input("Enter Course Code: ")
            if student_id in students and course_code in courses:
                students[student_id].enroll_course(course_code)
                courses[course_code].add_student(student_id)
                print(f"Student {students[student_id].name} (ID: {student_id}) enrolled in {courses[course_code].course_name} (Code: {course_code}).")
            else:
                print("Invalid student ID or course code.")

        elif option == "4":
            student_id = input("Enter Student ID: ")
            course_code = input("Enter Course Code: ")
            if student_id in students and course_code in students[student_id].courses:
                grade = input("Enter Grade: ")
                students[student_id].add_grade(course_code, grade)
                print(f"Grade {grade} added for {students[student_id].name} in {course_code}.")
            else:
                print("Student is not enrolled in the specified course.")

        elif option == "5":
            student_id = input("Enter Student ID: ")
            if student_id in students:
                print("Student Information: ")
                students[student_id].display_student_info()
            else:
                print("Student not found.")

        elif option == "6":
            course_code = input("Enter Course Code: ")
            if course_code in courses:
                print("Course Information: ")
                courses[course_code].display_course_info()
            else:
                print("Course not found.")

        elif option == "7":
            save_data()

        elif option == "8":
            load_data()

        elif option == "0":
            print("Exiting Student Management System. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
