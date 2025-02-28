import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import matplotlib.pyplot as plt 

DATABASE_NAME = "students_marks.db"

LOGIN = {
    "Register": ("Id", "Password", "Confirm_Password", "Key"),
    "delete_login_id": ("Id", "Password"),
    "login": ("Id", "Password"),
}

MENU = {

"Student":{
    "Add Student": ("Std_Name", "Std_Roll", "Class_Id"),
    "Delete Student": ("Std_Id",),
    "Student Details": ("Std_Id",),
    "Add Student Marks": ("Std_Id", "Sub_Id", "Marks"),
    "Update Student Marks": ("Std_Id", "Sub_Id", "Marks"),
    "Show All Students": None,
    "Delete Student Marks": ("Std_Id", "Sub_Id"),
    "Student Subject Marks": ("Std_Id", "Sub_Id"),
    },

"Subject":{
    "Show All Subjects": None,
    "Subject Details": ("Sub_Id",),
    "Add New Subject": ("Sub_Name", "Max_Marks", "Class_Id"),
    "Delete Subject": ("Sub_Id",),
    },

"Class":{
    "Show All Classes": None,
    "Class Details": ("Class_Id",),
    "Class Student List": ("Class_Id",),
    "Class Subject List": ("Class_Id",),
    },

"Semester":{
    "Semester List": None,
    "Semester Subjects": ("Semester_Number",),
    },

"Course":{
    "Courses List": None,
    "Course Subjects": ("Course_Name",),
    },

"Branch":{
    "Branch List": None,
    "Branch Subjects": ("Branch_Name",),
    },

"Report":{
    "Student Report": ("Std_Id",),
    "Class Report": ("Class_Id",),
    "College Toppers Report": ("Number_Of_Top_Students",),
    "Overall Report": None,
    },

"Others":{
    "Logout": None,
    "Update Password": ("Old_Password", "New_Password"),
    "About": None,
    "Exit": None,
    },

}

THEMES = {

    "Theme1":{"dark": "DeepSkyBlue4", "light": "LightCyan2", "Supporting1": "sky blue", "Supporting2": "ivory2", "BgImg": "./static/blue2.png"},

    "Theme2":{"dark": "green4", "light": "DarkSeaGreen1", "Supporting1": "light goldenrod yellow", "Supporting2": "DarkOliveGreen1", "BgImg": "./static/green5.png"},

    "Theme3":{"dark": "brown4", "light": "peach puff", "Supporting1": "light salmon", "Supporting2": "ivory2", "BgImg": "./static/crimson4.png"},

    "Theme4":{"dark": "purple4", "light": "plum2", "Supporting1": "mediumPurple1", "Supporting2": "ivory2", "BgImg": "./static/purple.png"},

    "Theme5":{"dark": "DeepPink4", "light": "pink", "Supporting1": "rosy brown", "Supporting2": "ivory2", "BgImg": "./static/pink3.png"},

    "Theme6":{"dark": "LightSalmon4", "light": "bisque", "Supporting1": "gold", "Supporting2": "ivory2", "BgImg": "./static/gold3.png"},

}

GRAPHS = {
    "Subject wise Average Marks": 1,
    "Class wise Average Marks": 2,
    "Semester wise Average Marks": 3,
    "Branch wise Average Marks": 4,
    "Course wise Average Marks": 5,
    "College Toppers Average Marks": 6,
}

class Student():
    """ 
        Attribute: std_id, std_name, std_roll_number, class_id
        Methods: new_student(), delete_student(), get_student_details(), get_student_subjects_marks(), get_student_percentage(), get_student_grade()
    """ 

    @classmethod
    def new_student(cls, Std_Name, Std_Roll, Class_Id):
        Class_Id = Class_Id.upper()
        Std_Name = Std_Name.lower()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute("SELECT * from Students where std_roll_number = :roll and class_id = :cid ",{"roll": Std_Roll, "cid": Class_Id})
        records =c.fetchall()

        if records:
            return False, f":Student with Roll Number = {Std_Roll}, already Exist!"
        
        c.execute("select * from Class where class_id = :cid ",{"cid": Class_Id})
        records =c.fetchall()

        if not records:
            return False, f":No Class with Id = {Class_Id} Exist!"
        
        c.execute("SELECT COUNT(*) FROM STUDENTS")
        numbers = c.fetchall()

        numbers = numbers[0][0]
        Std_Id = f"ST{numbers + 1 :04}"
        
        c.execute("INSERT INTO Students (std_id, std_name, std_roll_number, class_id) Values(:id, :sname, :roll, :class_id)",{"id":Std_Id, "sname": Std_Name, "roll": Std_Roll, "class_id": Class_Id})
        
        
        conn.commit()
        conn.close()

        return True, f":Student with Id = {Std_Id} Added! to Class {Class_Id}"
    
    @classmethod
    def get_all_students_list(cls):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT std_id, std_name, std_roll_number, class_id FROM Students")
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False

        return [{"student_id": record[0], "student_name": record[1], "std_roll_number": record[2], "class_id": record[3]} for record in records]

    @classmethod
    def delete_student(cls, Std_Id):
        Std_Id = Std_Id.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute("SELECT std_id from Students where std_id = :id ",{"id": Std_Id})
        records =c.fetchall()

        if not records:
            return False, f":No Student with Id = {Std_Id} Exist"  
        
        c.execute("DELETE FROM Students WHERE std_id = :sid",{"sid":Std_Id})
        c.execute("DELETE FROM Marks WHERE std_id = :sid",{"sid":Std_Id})
        
        conn.commit()
        conn.close()

        return True, f":Student with Id = {Std_Id} Deleted!"

    @classmethod
    def get_student_details(self, Std_Id):
        Std_Id = Std_Id.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute("SELECT * from Students where std_id = :id ",{"id": Std_Id})
        records =c.fetchall()

        if not records:
            return False, f":No Details with Id = {Std_Id} found"
        
        record = records[0]

        conn.commit()
        conn.close()

        return[{"std_id": record[0], "std_name": record[1], "std_roll_number": record[2], "class_id": record[3]}], f":Details of Id = {Std_Id} found!"

    @classmethod
    def get_student_subjects_marks(cls, Std_Id):
        Std_Id = Std_Id.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        
        c.execute("SELECT * from Students where std_id = :id ",{"id": Std_Id})
        records =c.fetchall()

        if not records:
            return False 
        
        c.execute("select subject_id, subject_name, marks_obtained, max_marks from Marks NATURAL JOIN Subject WHERE Marks.std_id = :std_id",{"std_id": Std_Id})
        records= c.fetchall()

        conn.commit()
        conn.close()

        return [{"subject_id": record[0], "subject_name": record[1], "marks_obtained": record[2], "max_marks":record[3]} for record in records]

    @classmethod
    def get_student_percentage(cls, Std_Id):
        records = Student.get_student_subjects_marks(Std_Id)
        if records:
            total_marks = 0
            total_obtained_marks = 0
            for record in records:
                total_marks += record["max_marks"]
                total_obtained_marks += record["marks_obtained"]
            return float(f"{total_obtained_marks/ total_marks * 100 :.2f}")
        return False      

    @classmethod
    def get_student_grade(cls, Std_Id):
        percentage = Student.get_student_percentage(Std_Id)
        if percentage:
            if percentage > 85:
                return "A"
            elif percentage > 70:
                return "B"
            elif percentage > 55:
                return "C"
            elif percentage > 40:
                return "D"
            elif percentage > 35:
                return "E"
            return "F"
        return False

class Subject():
    """
        Attributes: subject_id, subject_name, max_marks, class_id
        Methods: get_subject_details(), new_subject(), get_all_subject_list(), delete_subject()
    """
    @classmethod
    def get_subject_details(cls, Sub_Id):
        Sub_Id = Sub_Id.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        
        c.execute("SELECT * from Subject where Subject_id = :id ",{"id": Sub_Id})
        records =c.fetchall()

        if not records:
            return False, f":No subject with Subject Id = {Sub_Id} Exist!"  
        
        record = records[0]

        conn.commit()
        conn.close()

        return [{"subject_id": record[0], "subject_name": record[1], "max_marks": record[2], "class_id": record[3]}], ":Details found!"
    
    @classmethod
    def new_subject(cls, Sub_Name, Max_Marks, Class_Id):
        Class_Id = Class_Id.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute("SELECT * from Class where class_id = :cid ",{"cid": Class_Id})
        records =c.fetchall()

        if records == []:
            return False, f":No class with Class Id = {Class_Id} Exist!"
        
        c.execute("SELECT * from Subject where subject_name = :sname and class_id = :cid ",{"sname": Sub_Name, "cid": Class_Id})
        records =c.fetchall()

        if records:
            return False, f"Subject Already exist in class = {Class_Id}" 
        
        c.execute("SELECT COUNT(*) FROM SUBJECT")
        numbers = c.fetchall()

        numbers = numbers[0][0]
        Sub_Id = f"SUB{numbers + 1:02}"

        c.execute("INSERT INTO Subject (subject_id, subject_name, max_marks, class_id) Values(:id, :name, :marks, :class_id)",{"id":Sub_Id, "name": Sub_Name, "marks": Max_Marks, "class_id": Class_Id})

        conn.commit()
        conn.close()

        return True, f":Subject {Sub_Name} added to class {Class_Id}!"

    @classmethod
    def get_all_subject_list(cls):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT subject_id, subject_name, max_marks FROM Subject")
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False

        return [{"semester_id": record[0], "semester_name": record[1], "max_marks": record[2]} for record in records]

    @classmethod
    def delete_subject(cls, Sub_Id):
        Sub_Id = Sub_Id.upper()
        
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        
        c.execute("SELECT * from Subject where Subject_id = :id ",{"id": Sub_Id})
        records =c.fetchall()

        if not records:
            return False, f":No subject with Subject Id = {Sub_Id} Exist!"
        
        c.execute("DELETE FROM Subject WHERE subject_id = :id",{"id":Sub_Id})
        c.execute("DELETE FROM Marks WHERE subject_id = :id",{"id":Sub_Id})
        
        conn.commit()
        conn.close()

        return True, f":Subject = {Sub_Id} deleted!"

    @classmethod
    def subject_wise_average_marks(cls):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT Subject.subject_id, Subject.subject_name, AVG(Marks.marks_obtained), AVG(Subject.max_marks) FROM Marks JOIN Subject WHERE Subject.subject_id = Marks.subject_id GROUP BY Marks.subject_id ORDER BY AVG(Marks.marks_obtained) DESC")
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False

        return [{"subject_id": record[0], "subject_name": record[1], "average_marks": record[2], "max_marks":record[3]} for record in records]

class Marks():
    """
        Attributes: student_id, subject_id, marks_obtained, class_id
        Methods: get_student_subject_marks(), update_student_subject_marks(), add_student_subject_marks(), delete_student_subject_marks()    
    """
    @classmethod
    def get_student_subject_marks(cls, Std_Id, Sub_Id):
        Sub_Id = Sub_Id.upper()
        Std_Id = Std_Id.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute("SELECT std_id from Students where std_id = :id ",{"id": Std_Id})
        records =c.fetchall()

        if not records:
            return False, f":No Student with Id = {Std_Id} Exist"
        
        c.execute("SELECT * from Subject where subject_id = :id ",{"id": Sub_Id})
        records =c.fetchall()

        if not records:
            return False, f":No Subject with Id = {Sub_Id} Exist"
       
        c.execute("SELECT marks_obtained, Subject.subject_name, max_marks from Marks NATURAL JOIN Subject where Marks.Subject_id = :sub_id and std_id = :std_id",{"sub_id": Sub_Id, "std_id": Std_Id})
        records =c.fetchall()

        if not records:
            return False, f":Marks of student with Id = {Std_Id} for subject = {Sub_Id} doesn't exist!"

        record = records[0]

        conn.commit()
        conn.close()

        return [{"marks_obtained": record[0], "subject_name": record[1], "max_marks": record[2]}], f":Marks of student with Id = {Std_Id} for subject = {Sub_Id} found!"
    
    @classmethod
    def update_student_subject_marks(cls, Std_Id, Sub_Id, Marks):
        Sub_Id = Sub_Id.upper()
        Std_Id = Std_Id.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT std_id from Students where std_id = :id ",{"id": Std_Id})
        records =c.fetchall()

        if not records:
            return False, f":No Student with Id = {Std_Id} Exist"
        
        c.execute("SELECT * from Subject where subject_id = :id ",{"id": Sub_Id})
        records =c.fetchall()

        if not records:
            return False, f":No Subject with Id = {Sub_Id} Exist"

        c.execute("SELECT * from Marks where Marks.Subject_id = :sub_id and std_id = :std_id",{"sub_id": Sub_Id, "std_id": Std_Id})
        records =c.fetchall()

        d, message = Subject.get_subject_details(Sub_Id)
        max_marks = d[0]["max_marks"]

        if not records: 
            return False, f":subject(Id = {Sub_Id}) marks need to be added first from 'ADD SUBJECT' Option before updating!"
        
        if Marks > max_marks:
            return False, f":Marks can't be greater than {max_marks}"
        
        c.execute("SELECT DISTINCT class_id FROM STUDENTS WHERE std_id = :std_id",{"std_id": Std_Id})
        records =c.fetchall()
        Class_Id = records[0][0]
        
        c.execute("UPDATE Marks SET marks_obtained = :marks_obtained WHERE Subject_id = :sub_id and std_id = :std_id and class_id = :class_id", {"sub_id": Sub_Id, "std_id": Std_Id, "class_id": Class_Id, "marks_obtained": Marks})

        conn.commit()
        conn.close()
        return True, f":Marks of Student with Id = {Std_Id} updated for the subject = {Sub_Id}"
    
    @classmethod
    def add_student_subject_marks(cls, Std_Id, Sub_Id, Marks):

        Sub_Id = Sub_Id.upper()
        Std_Id = Std_Id.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute("SELECT std_id from Students where std_id = :id ",{"id": Std_Id})
        records =c.fetchall()

        if not records:
            return False, f":No Student with Id = {Std_Id} Exist"
        
        c.execute("SELECT * from Subject where subject_id = :id ",{"id": Sub_Id})
        records =c.fetchall()

        if not records:
            return False, f":No Subject with Id = {Sub_Id} Exist"
       
        c.execute("SELECT * from Marks where Marks.Subject_id = :sub_id and std_id = :std_id",{"sub_id": Sub_Id, "std_id": Std_Id})
        records =c.fetchall()

        d, message = Subject.get_subject_details(Sub_Id)
        max_marks = d[0]["max_marks"]

        if records: 
            return False, f":Subject(Id = {Sub_Id}) marks already exist for Student with Id = {Std_Id}, only Updation/ Deletion options are available!"
        
        if Marks > max_marks:
            return False, f":Marks can't be greater than {max_marks}"
        
        c.execute("SELECT DISTINCT class_id FROM STUDENTS WHERE std_id = :std_id",{"std_id": Std_Id})
        records =c.fetchall()
        Class_Id = records[0][0]

        c.execute("INSERT INTO Marks (std_id, subject_id, marks_obtained, class_id) Values(:id, :sub_id, :marks, :class_id)",{"id":Std_Id, "sub_id": Sub_Id, "marks": Marks, "class_id": Class_Id})

        conn.commit()
        conn.close()
        return True, f":Marks for Student with Id = {Std_Id} added for the subject id = {Sub_Id}"
    
    @classmethod
    def delete_student_subject_marks(cls, Std_Id, Sub_Id):

        Sub_Id = Sub_Id.upper()
        Std_Id = Std_Id.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute("SELECT std_id from Students where std_id = :id ",{"id": Std_Id})
        records =c.fetchall()

        if not records:
            return False, f":No Student with Id = {Std_Id} Exist"
        
        c.execute("SELECT * from Subject where subject_id = :id ",{"id": Sub_Id})
        records =c.fetchall()

        if not records:
            return False, f":No Subject with Id = {Sub_Id} Exist"
        
        c.execute("SELECT * from Marks where Marks.Subject_id = :sub_id and std_id = :std_id",{"sub_id": Sub_Id, "std_id": Std_Id})
        records =c.fetchall()

        if not records:
            return False, f":Marks of Student with Id = {Std_Id} for subject with Id = {Sub_Id} don't exist!"
        
        c.execute("SELECT DISTINCT class_id FROM STUDENTS WHERE std_id = :std_id",{"std_id": Std_Id})
        records =c.fetchall()
        Class_Id = records[0][0]

        c.execute("DELETE FROM Marks WHERE Subject_id = :sub_id and std_id = :std_id and class_id = :class_id",{"sub_id": Sub_Id, "std_id": Std_Id, "class_id": Class_Id})

        conn.commit()
        conn.close()
        return True, f":Marks of Student with Id = {Std_Id} for subject with Id = {Sub_Id} deleted!"
        
class Semester():
    """
        Attribute: semester_id, semester_name
        Methods: get_all_semester_list(), get_sem_subjects()
    """

    @classmethod
    def get_all_semester_list(cls):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT semester_id, semester_name FROM Semester")
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False

        return [{"semester_id": record[0], "semester_name": record[1]} for record in records]

    @classmethod
    def get_sem_subjects(cls, Semester_Number):

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT * FROM Semester WHERE semester_name = :sem_name",{"sem_name": f"{Semester_Number}"})
        records =c.fetchall()

        if records == []:
            return False, f":Semester {Semester_Number} don't Exist!"

        c.execute("SELECT subject_id, subject_name FROM Subject WHERE class_id in (SELECT class_id FROM Class WHERE semester_id = (SELECT semester_id FROM Semester WHERE semester_name = :sem_name))",{"sem_name": Semester_Number})
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False, f":No Subject in semester {Semester_Number}"
        
        return [{"subject_id": record[0], "subject_name": record[1]} for record in records], f":Details of subject for semester {Semester_Number} found!"

    @classmethod
    def semester_wise_average_marks(cls):
        
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT Semester.semester_id, Semester.semester_name, AVG(Marks.marks_obtained), AVG(Subject.max_marks) FROM Marks JOIN Subject JOIN Class JOIN Semester WHERE Subject.subject_id = Marks.subject_id and Class.class_id = Marks.class_id and Semester.semester_id = Class.semester_id GROUP BY Semester.semester_id, Semester.semester_name ORDER BY AVG(Marks.marks_obtained) DESC")
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False

        return [{"semester_id": record[0], "semester_name": record[1], "average_marks": record[2], "max_marks":record[3]} for record in records]

class Course():
    """
        Attribute: course_id, course_name
        Methods: get_all_course_list(), get_course_subjects()
    """

    @classmethod
    def get_all_course_list(cls):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT course_id, course_name FROM Course")
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False

        return [{"course_id": record[0], "course_name": record[1]} for record in records]

    @classmethod
    def get_course_subjects(cls, Course_Name):
        Course_Name = Course_Name.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT * FROM Course WHERE course_name = :course_name",{"course_name": Course_Name})
        records =c.fetchall()

        if records == []:
            return False, f":No {Course_Name} Course Exist!"

        c.execute("SELECT subject_id, subject_name FROM Subject WHERE class_id in (SELECT class_id FROM Class WHERE course_id = (SELECT course_id FROM Course WHERE course_name = :course_name))",{"course_name": Course_Name})
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False, f":No subject in {Course_Name} Course!"
        
        return [{"subject_id": record[0], "subject_name": record[1]} for record in records], f":Details of subject of {Course_Name} course found!"
    
    @classmethod
    def course_wise_average_marks(cls):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT Course.course_id, Course.course_name, AVG(Marks.marks_obtained), AVG(Subject.max_marks) FROM Marks JOIN Subject JOIN Class JOIN Course WHERE Subject.subject_id = Marks.subject_id and Class.class_id = Marks.class_id and Course.course_id = Class.course_id GROUP BY Course.course_id, Course.course_name ORDER BY AVG(Marks.marks_obtained) DESC")
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False

        return [{"course_id": record[0], "course_name": record[1], "average_marks": record[2], "max_marks":record[3]} for record in records]

class Class():
    """
        Attributes: class_id, course_id, semester_id, branch_id
        Methods: get_all_classes_list(), calculate_class_subject_wise_average(), get_class_details(), get_student_list()
    """

    @classmethod
    def get_all_classes_list(cls):
 
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT class_id FROM Class;")
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False

        return [{"class_id": record[0]} for record in records]

    @classmethod
    def calculate_class_subject_wise_average(cls, Class_Id):
        Class_Id = Class_Id.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT Subject.subject_id, Subject.subject_name, AVG(Marks.marks_obtained), AVG(Subject.max_marks) FROM Marks JOIN Subject WHERE Subject.subject_id = Marks.subject_id and Marks.class_id = :class_id GROUP BY Subject.subject_id, Subject.subject_name ORDER BY AVG(Marks.marks_obtained) DESC",{"class_id": Class_Id})
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False

        return [{"subject_id": record[0], "subject_name": record[1], "average": record[2], "max_marks":record[3]} for record in records]

    @classmethod
    def get_class_student_wise_average(cls, Class_Id):
        Class_Id = Class_Id.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT Students.std_id, Students.std_name, AVG(Marks.marks_obtained), AVG(Subject.max_marks) FROM Marks JOIN Subject JOIN Students WHERE Subject.subject_id = Marks.subject_id and Students.std_id = Marks.std_id and Marks.class_id = :class_id GROUP BY Students.std_id, Students.std_name ORDER BY AVG(Marks.marks_obtained) DESC" ,{"class_id": Class_Id})
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False

        return [{"std_id": record[0], "std_name": record[1], "average_marks": record[2], "max_marks":record[3]} for record in records]

    @classmethod
    def average_marks(cls, Class_Id):
        Class_Id = Class_Id.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute('SELECT * FROM Class WHERE class_id = :class_id',{"class_id": Class_Id})
        records =c.fetchall()
        
        if records == []:
            return False

        c.execute("SELECT AVG(marks_obtained) FROM Marks WHERE class_id = :class_id" ,{"class_id": Class_Id})
        records =c.fetchall()
        conn.commit()
        conn.close()

        if records[0][0] == None:
            return 0

        return records[0][0]

    @classmethod
    def get_class_details(cls, Class_Id):
        Class_Id = Class_Id.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute("SELECT * from Class where class_id = :cid ",{"cid": Class_Id})
        records =c.fetchall()

        if not records:
            return False, f":No class with Class Id = {Class_Id} Exist!"
       
        c.execute("SELECT Course.course_name, Semester.semester_name, Branch.branch_name FROM Class JOIN Course JOIN Semester JOIN Branch WHERE Class.course_id = Course.course_id and Class.semester_id = Semester.semester_id and Class.branch_id = Branch.branch_id and Class.class_id = :class_id",{"class_id": Class_Id})
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False, f":No details of class with Class Id = {Class_Id} found!"
        
        return [{"course_name": records[0][0], "semester_name": records[0][1], "branch_name": records[0][2]}], f":Details of class with class Id = {Class_Id} found!"

    @classmethod
    def get_student_list(cls, Class_Id):
        Class_Id = Class_Id.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute("SELECT * from Class where class_id = :cid ",{"cid": Class_Id})
        records =c.fetchall()

        if not records:
            return False, f":No class with Class Id = {Class_Id} Exist!"
       
        c.execute("SELECT std_id, std_name FROM Students WHERE class_id = :class_id",{"class_id": Class_Id})
        records =c.fetchall()

        if records == []:
            return False, f":No student in class with Class Id = {Class_Id}"

        conn.commit()
        conn.close()
        return [{"std_id": record[0], "std_name": record[1]} for record in records], f":List of class Students with class Id = {Class_Id} found!"

    @classmethod    
    def class_wise_average_marks(cls):

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT Marks.class_id, AVG(Marks.marks_obtained), AVG(Subject.max_marks) FROM Marks JOIN Subject WHERE Subject.subject_id = Marks.subject_id GROUP BY Marks.class_id ORDER BY AVG(Marks.marks_obtained) DESC")
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False

        return [{"class_id": record[0], "average_marks": record[1], "max_marks":record[2]} for record in records]

    @classmethod
    def get_class_subjects(cls, Class_Id):
        Class_Id = Class_Id.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute("SELECT * from Class where class_id = :cid ",{"cid": Class_Id})
        records =c.fetchall()

        if not records:
            return False, f":No class with Class Id = {Class_Id} Exist!"
       
        c.execute("SELECT Subject.subject_id, Subject.subject_name FROM Subject WHERE class_id = :class_id",{"class_id": Class_Id})
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False, f":No Subject in class with Class Id = {Class_Id}"

        return [{"subject_id": record[0], "subject_name": record[1]} for record in records], f":List of Class Subjects with class Id = {Class_Id} found!"

class Branch():
    """
        Attributes: branch_id, branch_name
        Methods: get_all_branch_list(), get_branch_subjects()
    """

    @classmethod
    def get_all_branch_list(cls):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT branch_id, branch_name FROM Branch")
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False

        return [{"branch_id": record[0], "branch_name": record[1]} for record in records]

    @classmethod
    def get_branch_subjects(cls, Branch_Name):
        Branch_Name = Branch_Name.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT * FROM Branch WHERE branch_name = :branch_name",{"branch_name": Branch_Name})
        records =c.fetchall()

        if records == []:
            return False, f":No {Branch_Name} Branch Exist!"

        c.execute("SELECT subject_id, subject_name FROM Subject WHERE class_id in (SELECT class_id FROM Class WHERE branch_id = (SELECT branch_id FROM Branch WHERE branch_name = :branch_name))",{"branch_name": Branch_Name})
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False, f":No Subjects in {Branch_Name} Branch"
        
        return [{"subject_id": record[0], "subject_name": record[1]} for record in records], f":Details of Subjects of {Branch_Name} Branch found!"

    @classmethod
    def branch_wise_average_marks(cls):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT Branch.branch_id, Branch.branch_name, AVG(Marks.marks_obtained), AVG(Subject.max_marks) FROM Marks JOIN Subject JOIN Class JOIN Branch WHERE Subject.subject_id = Marks.subject_id and Class.class_id = Marks.class_id and Branch.branch_id = Class.branch_id GROUP BY Branch.branch_id, Branch.branch_name ORDER BY AVG(Marks.marks_obtained) DESC")
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False

        return [{"branch_id": record[0], "branch_name": record[1], "average_marks": record[2], "max_marks":record[3]} for record in records]
        
class Login():
    """
        Attributes: login_authority, key_auth
        Methods: create_login_id(), delete_login_id(), update_login_pwd(), login()
    """
    KEY_AUTH = "@7224Cs8$"

    @classmethod
    def create_login_id(cls, Id, Password, Confirm_Password, Key):

        if Password != Confirm_Password:
            return False, f":Password and Confirm Password do not match!"
    
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute("SELECT login_id from Login")
        records =c.fetchall()
        l = [record[0] for record in records]

        if Id in l:
            return False, f":Login Id = {Id} already Exist!"
        
        if Key == cls.KEY_AUTH:
            cls.AUTHORITY = "ADMIN"
        else:
            # cls.AUTHORITY = "STUDENT"
            return False, f":Incorrect Key!"

        hashed = str(generate_password_hash(Password))
        
        c.execute("INSERT INTO Login (login_id, login_pwd, login_authority) values(:user, :hashed, :authority)",{"user": Id, "hashed": hashed, "authority": cls.AUTHORITY})
        
        conn.commit()
        conn.close()

        return True, f":Login Id = {Id} Created!"

    @classmethod
    def delete_login_id(cls, Id, Password):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute("SELECT login_id, login_pwd from Login where login_id = :id ",{"id": Id})
        records =c.fetchall()

        if not records:
            return False, f":No Login Id with Id = {Id} Exist"    
        
        if not check_password_hash(records[0][1], Password):
            return False, f":Incorrect Password"
        
        c.execute("DELETE from Login where login_id = :id ",{"id": Id})

        conn.commit()
        conn.close()

        return True, f":Login Id = {Id} Deleted!"
    
    @classmethod
    def update_login_pwd(cls, Id, Old_Password, New_Password):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute("SELECT login_id, login_pwd from Login where login_id = :id ",{"id": Id})
        records =c.fetchall()

        if not records:
            return False, f":No Login Id with Id = {Id} Exist"   
        
        if not check_password_hash(records[0][1], Old_Password):
            return False, f":Incorrect Old Password"
        
        new_hashed = str(generate_password_hash(New_Password))
        
        c.execute("UPDATE Login SET login_pwd = :pwd where login_id = :id ",{"pwd": new_hashed, "id": Id})

        conn.commit()
        conn.close()

        return True, f":Password of Login Id = {Id} Updated!"
    
    @classmethod 
    def login(cls, Id, Password):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute("SELECT login_id, login_pwd from Login where login_id = :id ",{"id": Id})
        records =c.fetchall()

        if not records:
            return False, f"No Login Id with Id = {Id} Exist"    
        
        if not check_password_hash(records[0][1], Password):
            return False, f"Incorrect Password"
        
        conn.commit()
        conn.close()

        return True, f"Login Successful!"

class Report():
    """
        Methods: generate_student_report(), generate_class_report(), generate_overall_report(), generate_graphs()
    """
    @classmethod
    def generate_student_report(cls, Std_Id):
        Std_Id = Std_Id.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute("SELECT std_id from Students where std_id = :id ",{"id": Std_Id})
        records =c.fetchall()

        conn.commit()
        conn.close()

        if not records:
            return False, False, f":No Student with Id = {Std_Id} Exist"

        details, message = Student.get_student_details(Std_Id)
        details[0]["Percentage"] = Student.get_student_percentage(Std_Id)
        details[0]["Grade"] = Student.get_student_grade(Std_Id)

        return Student.get_student_subjects_marks(Std_Id), details[0], f":Report of Student with Id = {Std_Id} Generated!"

    @classmethod
    def generate_class_report(cls, Class_Id):
        Class_Id = Class_Id.upper()

        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        c.execute("SELECT * from Class where class_id = :id ",{"id": Class_Id})
        records =c.fetchall()

        conn.commit()
        conn.close()

        if not records:
            return False, False, f":No Class with Id = {Class_Id} Exist"

        details, message = Class.get_class_details(Class_Id)

        # Class.calculate_class_subject_wise_average(Class_Id)
        # Class.get_class_student_wise_average(Class_Id)

        details[0]["Class_Average_Marks"] = Class.average_marks(Class_Id)

        return Class.get_student_list(Class_Id)[0], (details[0], Class_Id), f":Report of Class with Class Id = {Class_Id} Generated!"
        
    @classmethod
    def get_college_toppers_students(cls, Number_Of_Top_Students= 5):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
       
        c.execute("SELECT Students.std_id, Students.std_name, AVG(Marks.marks_obtained), AVG(Subject.max_marks) FROM Marks JOIN Subject JOIN Students WHERE Subject.subject_id = Marks.subject_id and Students.std_id = Marks.std_id GROUP BY Students.std_id, Students.std_name ORDER BY AVG(Marks.marks_obtained) DESC LIMIT :n",{"n": Number_Of_Top_Students})
        records =c.fetchall()

        conn.commit()
        conn.close()

        if records == []:
            return False, ":No student found!"

        return [{"std_id": record[0], "std_name": record[1], "average_marks": record[2], "max_marks":record[3]} for record in records], ":Details found!"

    @classmethod
    def generate_overall_report(cls):
        Subject.subject_wise_average_marks()
        Class.class_wise_average_marks()
        Semester.semester_wise_average_marks()
        Branch.branch_wise_average_marks()
        Course.course_wise_average_marks()

    @classmethod
    def generate_graph(cls, Type = 1, Number_Of_Students= 0, Std_id = ""):
        match(Type):
            case 1:
                list_name = Subject.subject_wise_average_marks()
                labels_identifier = "subject_name"
                values_identifier =  "average_marks"
                title = "Subject wise Average Marks"
            case 2:
                list_name = Class.class_wise_average_marks()
                labels_identifier = "class_id"
                values_identifier =  "average_marks"
                title = "Class wise Average Marks"
            case 3:
                list_name = Semester.semester_wise_average_marks()
                labels_identifier = "semester_id"
                values_identifier = "average_marks"
                title = "Semester wise Average Marks"
            case 4:
                list_name = Branch.branch_wise_average_marks()
                labels_identifier = "branch_name"
                values_identifier = "average_marks"
                title = "Branch wise Average Marks"
            case 5:
                list_name = Course.course_wise_average_marks()
                labels_identifier = "course_name"
                values_identifier = "average_marks"
                title = "Course wise Average Marks"
            case 6:
                list_name, message = Report.get_college_toppers_students()
                labels_identifier = "std_name"
                values_identifier = "average_marks"
                title = "College Toppers Average Marks"
            case 7:
                list_name = Student.get_student_subjects_marks(Std_Id= Std_id)
                labels_identifier = "subject_name"
                values_identifier = "marks_obtained"
                title = "Student Subjects Marks"
            case _:
                list_name = Class.class_wise_average_marks()
                labels_identifier = "class_id"
                values_identifier = "average_marks"
                title = "Class wise Average Marks"

        records = list_name
        labels, values = [],[]

        if len(records) > Number_Of_Students and Number_Of_Students:
            records= records[0:Number_Of_Students]

        for record in records:
            labels.append(record[labels_identifier])
            values.append(record[values_identifier])

        return (labels, values, title)
    
if __name__=="__main__":
    pass