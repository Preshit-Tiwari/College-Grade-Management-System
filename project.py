import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import matplotlib.pyplot as plt
from tkinter import filedialog, messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from helper import *
import tkinter as tk
import random


type_of_window = "-fullscreen"

class College_Grade_Management:

    # Choosing Random Theme constants from theme pack
    main_theme = "Theme" + "1"#str(random.randint(1,len(THEMES)))

    main_color_theme_dark = THEMES[main_theme]["dark"]
    main_color_theme_light = THEMES[main_theme]["light"]
    supporting_light_color = THEMES[main_theme]["Supporting1"]
    supporting_light_color2 = THEMES[main_theme]["Supporting2"]
    main_bg_img = THEMES[main_theme]["BgImg"]
    
    # Static constants
    main_title= "College Data Manager"
    normal_font = ("Arial", 14)
    main_heading_font = ("Arial", 25)
    sub_headings_font = ("Arial", 14, "bold")

    
    # Status bar colors
    dark_red_color = "red4"
    status_red_color = "hot pink"
    status_green_color = "pale green" 


    def __init__(self, root, Id = None):

        # setting up the root
        self.root = root
        self.root.attributes(type_of_window, True)
        self.root.title(self.main_title)

        # Login In of session
        self.ID = Id

        # screen size switching options
        self.fullscreen = True
        self.root.bind("<F11>", lambda event: self.toggle_fullscreen())
        self.root.bind("<Escape>", lambda event: self.exit_fullscreen())

        """ Part for main heading area """

        self.main_viewing_heading_sub_frame = self.generate_heading(self.root, self.main_title, font= self.main_heading_font)     


        """ Creating main frame """  

        self.main_frame = tk.LabelFrame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=1, pady=4)


        """ Partition the main frame"""

        self.main_viewing_frame = tk.Canvas(self.main_frame, bg= self.main_color_theme_light, bd=1, relief="solid")
        self.main_viewing_frame.pack(fill="both", expand=1, side= tk.LEFT, anchor='w')

        self.main_details_frame = tk.LabelFrame(self.main_frame, bg= self.supporting_light_color2, bd=1, relief="solid")
        self.main_details_frame.pack(fill="both", expand=1, side= tk.TOP, anchor='e')

        self.main_graph_frame = tk.LabelFrame(self.main_frame, bg= self.supporting_light_color2, bd=1, relief="solid")
        self.main_graph_frame.pack(fill="both", expand=1, side= tk.BOTTOM , anchor='e', pady=4)

        
        """ part for scrollbar code for viewing canvas"""

        self.main_viewing_canvas = tk.Canvas(self.main_viewing_frame, bd=1, relief= "solid", bg= self.supporting_light_color2)
        self.main_viewing_canvas.pack(side="left", fill="both", expand=True)

        # vertical scrollbar
        self.y_scrollbar_canvas = tk.Scrollbar(self.main_viewing_canvas, orient="vertical", command=self.main_viewing_canvas.yview)
        self.y_scrollbar_canvas.pack(side="left", fill="y")

        self.main_viewing_canvas.configure(yscrollcommand=self.y_scrollbar_canvas.set)
        self.main_viewing_canvas.bind('<Configure>', lambda e: self.main_viewing_canvas.configure(scrollregion=self.main_viewing_canvas.bbox("all")))

        # horizontal scrollbar
        self.x_scrollbar_canvas = tk.Scrollbar(self.main_viewing_canvas, orient="horizontal", command=self.main_viewing_canvas.xview)
        self.x_scrollbar_canvas.pack(side="bottom", fill="x", anchor="s")

        self.main_viewing_canvas.configure(xscrollcommand=self.x_scrollbar_canvas.set)
        self.main_viewing_canvas.bind('<Configure>', lambda e: self.main_viewing_canvas.configure(scrollregion=self.main_viewing_canvas.bbox("all")))


        """ Part for main viewing area """

        self.bg = tk.PhotoImage(file = self.main_bg_img)
        self.main_viewing_canvas.create_image( 0, 0, image = self.bg, anchor = "center") 

        # Status part        
        self.clear_status_frame()

        # Entry part
        self.entry_frame_parent = tk.LabelFrame(self.main_viewing_canvas, bg= self.main_color_theme_light, bd=1, relief="solid")
        self.entry_frame_parent.pack(anchor="center", padx= 10, pady= 150)
        

        """ Menu Part """
        
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.Student = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="Student", menu=self.Student)
        self.Student.add_command(label="Add Student", command=lambda: self.set_up_entry_window("Add Student", MENU["Student"]["Add Student"]))
        self.Student.add_command(label="Delete Student", command=lambda: self.set_up_entry_window("Delete Student", MENU["Student"]["Delete Student"]))
        self.Student.add_command(label="Student Details", command=lambda: self.set_up_entry_window("Student Details", MENU["Student"]["Student Details"]))
        self.Student.add_separator()
        self.Student.add_command(label="Add Student Marks", command=lambda: self.set_up_entry_window("Add Student Marks", MENU["Student"]["Add Student Marks"]))
        self.Student.add_command(label="Update Student Marks", command=lambda: self.set_up_entry_window("Update Student Marks", MENU["Student"]["Update Student Marks"]))
        self.Student.add_command(label="Delete Student Marks", command=lambda: self.set_up_entry_window("Delete Student Marks", MENU["Student"]["Delete Student Marks"]))
        self.Student.add_command(label="Show All Students", command=lambda: self.print_details(Student.get_all_students_list()))
        self.Student.add_command(label="Student Subject Marks", command=lambda: self.set_up_entry_window("Student Subject Marks", MENU["Student"]["Student Subject Marks"]))
        
        
        self.Subject = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="Subject", menu=self.Subject)
        self.Subject.add_command(label="Subject Details", command=lambda: self.set_up_entry_window("Subject Details", MENU["Subject"]["Subject Details"]))
        self.Subject.add_separator()
        self.Subject.add_command(label="Add New Subject", command=lambda: self.set_up_entry_window("Add New Subject", MENU["Subject"]["Add New Subject"]))
        self.Subject.add_command(label="Delete Subject", command=lambda: self.set_up_entry_window("Delete Subject", MENU["Subject"]["Delete Subject"]))
        self.Subject.add_command(label="Show All Subjects", command=lambda: self.print_details(Subject.get_all_subject_list()))
        

        self.Class = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="Class", menu=self.Class)
        self.Class.add_command(label="Class Details", command=lambda: self.set_up_entry_window("Class Details", MENU["Class"]["Class Details"]))
        self.Class.add_separator()
        self.Class.add_command(label="Class Student List", command=lambda: self.set_up_entry_window("Class Student List", MENU["Class"]["Class Student List"]))
        self.Class.add_command(label="Class Subject List", command=lambda: self.set_up_entry_window("Class Subject List", MENU["Class"]["Class Subject List"]))
        self.Class.add_command(label="Show All Classes", command=lambda: self.print_details(Class.get_all_classes_list()))


        self.Semester = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="Semester", menu=self.Semester)
        self.Semester.add_command(label="Semesters List", command=lambda: self.print_details(Semester.get_all_semester_list()))
        self.Semester.add_command(label="Semester Subjects", command=lambda: self.set_up_entry_window("Semester Subjects", MENU["Semester"]["Semester Subjects"]))


        self.Course = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="Courses", menu=self.Course)
        self.Course.add_command(label="Courses List", command=lambda: self.print_details(Course.get_all_course_list()))
        self.Course.add_command(label="Course Subjects", command=lambda: self.set_up_entry_window("Course Subjects", MENU["Course"]["Course Subjects"]))


        self.Branch = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="Branch", menu=self.Branch)
        self.Branch.add_command(label="Branch List", command=lambda: self.print_details(Branch.get_all_branch_list()))
        self.Branch.add_command(label="Branch Subjects", command=lambda: self.set_up_entry_window("Branch Subjects", MENU["Branch"]["Branch Subjects"]))


        self.Report = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="Reports", menu=self.Report)
        self.Report.add_command(label="Student Report", command=lambda: self.set_up_entry_window("Student Report", MENU["Report"]["Student Report"]))
        self.Report.add_command(label="Class Report", command=lambda: self.set_up_entry_window("Class Report", MENU["Report"]["Class Report"]))
        self.Report.add_command(label="College Toppers Report", command=lambda: self.set_up_entry_window("College Toppers Report", MENU["Report"]["College Toppers Report"]))
        self.Report.add_separator()
        self.Report.add_command(label="Overall Report", command= lambda: self.set_up_extra_details_window("Overall Report", "..."))


        self.Login_options = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="Others", menu=self.Login_options)
        self.Login_options.add_command(label="Logout", command=lambda: self.logout_to_login_window())
        self.Login_options.add_command(label="Update Password", command=lambda: self.set_up_entry_window("Update Password", MENU["Others"]["Update Password"]))
        self.Report.add_separator()
        self.Login_options.add_command(label="About", command=self.show_about)
        self.Login_options.add_command(label="Exit", command=self.exit_app)


    def logout_to_login_window(self):
        # clearing up the root
        for widget in self.root.winfo_children():
            widget.destroy()

        # setting up the login page components
        Login_Grade_Management(self.root)
        

    def toggle_fullscreen(self):
        """Toggles fullscreen on and off"""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.root.attributes("-fullscreen", True)
        else:
            self.root.attributes("-zoomed", True)


    def exit_fullscreen(self):
        """Exists fullscreen"""
        self.fullscreen = False
        self.root.attributes("-fullscreen", self.fullscreen)


    def generate_heading(self, parent, text, font):
        """ Generates heading form a provided text and font for a provided container with pack placing"""

        self.temp = tk.LabelFrame(parent, bg= self.main_color_theme_dark, bd=0.5, relief="solid")
        self.temp.pack(fill="both", side="top", anchor='w')

        tk.Label(self.temp, text= f" {text} ", font=font, fg="white", bg=self.main_color_theme_dark).pack(anchor="center")
        return self.temp


    def show_graph(self, type=0, limit=5, Std_Id = ""):
        """ Shows graph of a given type in the screen """

        for widget in self.main_graph_frame.winfo_children():
            widget.destroy()

        self.labels, self.values, self.title = Report.generate_graph(type,limit, Std_id= Std_Id)

        if self.labels:
            self.generate_heading(self.main_graph_frame, f"Graph: {self.title}", font= self.sub_headings_font)

            tk.Label(self.main_graph_frame, text="\n"*1, bg= self.supporting_light_color2).pack()

            
            fig, ax = plt.subplots()
            bars = ax.barh(self.labels, self.values)
            ax.bar_label(bars)
            self.canvas = FigureCanvasTkAgg(fig, master=self.main_graph_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.main_graph_frame, pack_toolbar = False)
            self.toolbar.update()
            self.toolbar.pack()


    def status_update(self, message="Enter the given values 😊", bck= status_green_color):
        """ Updates/generates the given message with given background color on the screen """

        try:
            for widget in self.status_frame.winfo_children():
                widget.destroy()

        except AttributeError:
            self.status_frame = tk.LabelFrame(self.main_viewing_canvas, border=0.5, relief="solid")
            self.status_frame.pack(padx=10, pady=10, fill="both")

        self.status_text = tk.Label(self.status_frame, text = message, bg= bck, font= self.sub_headings_font, wraplength= 1000)
        self.status_text.pack(anchor="center", padx=5, pady=5)
        self.status_frame.configure(bg= bck)

        return self.status_text


    def clear_status_frame(self):
        self.status_update("",self.main_color_theme_light).pack_forget()


    def clear_entry_frame(self):
        for widget in self.entry_frame_parent.winfo_children():
            widget.destroy()


    def set_up_entry_window(self, function_used, data_fields):
        """ Updates/generates the given entry window with required fields and button on screen """

        if data_fields:
            self.clear_entry_frame()          

            self.entry_updation_window = self.generate_heading(self.entry_frame_parent, "Entry Window", font= self.sub_headings_font)

            self.entry_frame = tk.LabelFrame(self.entry_frame_parent, bg= self.main_color_theme_light, bd=1, relief="solid")
            self.entry_frame.pack(fill="both", expand=1, padx= 3, pady= 3)

            message = f"Enter the values in the Entry window to {function_used}"
            self.status_update(message, self.status_green_color)

            # for passing the entry widget to the entry_functionality
            self.parameters = []
            for iter, data_label in enumerate(data_fields):
                temp_dict = {}
                temp_dict["label"] = data_label

                tk.Label(self.entry_frame, text= data_label, font= self.sub_headings_font, bg= self.main_color_theme_light).grid(row=iter, column=0, padx=15, pady=15)

                temp_dict["entry_widget"] = tk.Entry(self.entry_frame, font= self.normal_font)
                temp_dict["entry_widget"].grid(row=iter, column=1, padx=15, pady=15)

                self.parameters.append(temp_dict)

            # submitting button for the entry form 
            tk.Button(self.entry_frame, text = "Ok", bg=self.main_color_theme_dark, fg="white", font= self.sub_headings_font, width= 10, command= lambda: self.entry_submission(function_used, self.parameters)).grid(padx=15, pady=15)


    def set_up_extra_details_window(self, function_used, data_fields=None):
        """ Updates/generates the given entry window with required fields and button on screen """

        if data_fields:
            try:
                self.main_extra_details_canvas.destroy()
            except AttributeError:
                pass

            self.main_extra_details_canvas = tk.Canvas(self.main_viewing_canvas, bd=1, relief= "solid", bg=self.supporting_light_color2)
            self.main_extra_details_canvas.pack(anchor="center", expand= 1)

            self.extra_details_frame = tk.Frame(self.main_extra_details_canvas, bg= self.main_color_theme_light, bd=1, relief="solid")
            self.extra_details_frame.pack(side= "right", fill="both", expand= 1)

            self.generate_heading(self.extra_details_frame, "Extra Details Window", font= self.sub_headings_font)

            tk.Button(self.extra_details_frame, text = "X", bg=self.dark_red_color, fg="white", font= self.normal_font, command= lambda: self.main_extra_details_canvas.destroy()).pack(side="top", anchor="e", fill="x", ipady=0)

            self.xyz = tk.Canvas(self.extra_details_frame, bg= self.main_color_theme_light, bd=1, relief="solid")
            self.xyz.pack(fill="both", side="bottom", padx= 3, pady= 3, expand = 1)

            self.scrollbar_y_details = tk.Scrollbar(self.extra_details_frame, orient="vertical", command=self.xyz.yview)
            self.scrollbar_y_details.pack(side="right", fill="y")

            self.xyz.configure(yscrollcommand=self.scrollbar_y_details.set)

            self.content_frame = tk.Frame(self.xyz, bg= self.main_color_theme_light, bd=1, relief="solid")
            self.xyz.create_window((0, 0), window=self.content_frame, anchor="nw")

            self.content_frame.bind("<Configure>", lambda e: self.xyz.configure(scrollregion=self.xyz.bbox("all")))

            if function_used == "Student Report":

                # printing details on the extra window
                for iter, data_label in enumerate(data_fields):

                    tk.Label(self.content_frame, text= f"{data_label}:", font= self.sub_headings_font, bg= self.main_color_theme_light).grid(row=iter, column=0, padx=15, pady=15)

                    tk.Label(self.content_frame, text= data_fields[data_label], font= self.normal_font, bg= self.main_color_theme_light).grid(row=iter, column=1, padx=15, pady=15)

            elif function_used == "Overall Report":

                message = f"Click Given buttons in the Extra Details window to get particulars for {function_used}"
                self.status_update(message, self.status_green_color)

                # buttons for extra graph and details for extra window 
                tk.Button(self.content_frame, text= "Subject wise Average Marks", font= self.sub_headings_font, bg= self.main_color_theme_dark, fg="white", command= lambda: self.print_details(Subject.subject_wise_average_marks()) and self.show_graph(GRAPHS["Subject wise Average Marks"])).grid(row=0, column=0, padx=7, pady=7)

                tk.Button(self.content_frame, text= "Class wise Average Marks", font= self.sub_headings_font, bg= self.main_color_theme_dark, fg="white", command= lambda: self.print_details(Class.class_wise_average_marks()) and self.show_graph(GRAPHS["Class wise Average Marks"])).grid(row=1, column=0, padx=7, pady=7)
                    
                tk.Button(self.content_frame, text= "Semester wise Average Marks", font= self.sub_headings_font, bg= self.main_color_theme_dark, fg="white", command= lambda: self.print_details(Semester.semester_wise_average_marks()) and self.show_graph(GRAPHS["Semester wise Average Marks"])).grid(row=2, column=0, padx=7, pady=7)
                    
                tk.Button(self.content_frame, text= "Branch wise Average Marks", font= self.sub_headings_font, bg= self.main_color_theme_dark, fg="white", command= lambda: self.print_details(Branch.branch_wise_average_marks()) and self.show_graph(GRAPHS["Branch wise Average Marks"])).grid(row=3, column=0, padx=7, pady=7)
                    
                tk.Button(self.content_frame, text= "Course wise Average Marks", font= self.sub_headings_font, bg= self.main_color_theme_dark, fg="white", command= lambda: self.print_details(Course.course_wise_average_marks()) and self.show_graph(GRAPHS["Course wise Average Marks"])).grid(row=4, column=0, padx=7, pady=7)
                    
                tk.Button(self.content_frame, text= "College Toppers Average Marks", font= self.sub_headings_font, bg= self.main_color_theme_dark, fg="white", command= lambda: self.print_details(Report.get_college_toppers_students()[0]) and self.show_graph(GRAPHS["College Toppers Average Marks"])).grid(row=5, column=0, padx=7, pady=7)

            elif function_used == "Class Report":

                message = f"Click Given buttons in the Extra Details window to get particulars for {function_used}"
                self.status_update(message, self.status_green_color)

                Class_Id = data_fields[1]
                data_fields = data_fields[0]

                # printing details on the extra window
                for iter, data_label in enumerate(data_fields):

                    tk.Label(self.content_frame, text= f"{data_label}:", font= self.sub_headings_font, bg= self.main_color_theme_light).grid(row=iter, column=0, padx=15, pady=15)

                    tk.Label(self.content_frame, text= data_fields[data_label], font= self.normal_font, bg= self.main_color_theme_light).grid(row=iter, column=1, padx=15, pady=15)

                # buttons for extra data for extra window 
                tk.Button(self.content_frame, text= "Class Subject wise Average Marks", font= self.sub_headings_font, bg= self.main_color_theme_dark, fg="white", command= lambda: self.print_details(Class.calculate_class_subject_wise_average(Class_Id))).grid(padx=7, pady=7)

                tk.Button(self.content_frame, text= "Class Student wise Average Marks", font= self.sub_headings_font, bg= self.main_color_theme_dark, fg="white", command= lambda: self.print_details(Class.get_class_student_wise_average(Class_Id))).grid(padx=7, pady=7)


    def entry_submission(self, function, f_parameters):
        """ Get the entires form the entry tab and pass it to the other functions to provide user with specific functionality """

        self.arguments = {}
        for iter, data in enumerate(f_parameters):
            # resolving empty entries
            if data["entry_widget"].get() == "":
                self.status_update(f"EMPTY FIELD: Please provide VALUE in { data['label'] } field", self.status_red_color)
                return
            
            # extracting values form the entry field
            if data["label"] in ("Marks", "Max_Marks", "Number_Of_Top_Students"):
                try:
                    self.arguments[data["label"]] = int(data["entry_widget"].get())
                except ValueError:
                    self.status_update(f"INVALID DATA: Please provide valid INTEGER in {data['label']} field", self.status_red_color)
                    return
            else:
                self.arguments[data["label"]] = data["entry_widget"].get()

        self.clear_status_frame()
        # sending the submitted values for the functionality implementation
        self.entry_functionality(function, self.arguments)


    def entry_functionality(self, func, func_argument):
        """ Responding to user submitted values form the entry window """

        message = ""

        # Student
        if func == "Add Student":
            data, message = Student.new_student(**func_argument)

        elif func == "Delete Student":
            data, message = Student.delete_student(**func_argument)

        elif func == "Student Details":
            data, message = Student.get_student_details(**func_argument)

        elif func == "Add Student Marks":
            data, message = Marks.add_student_subject_marks(**func_argument)

        elif func == "Update Student Marks":
            data, message = Marks.update_student_subject_marks(**func_argument)

        elif func == "Delete Student Marks":
            data, message = Marks.delete_student_subject_marks(**func_argument)

        elif func == "Student Subject Marks":
            data, message = Marks.get_student_subject_marks(**func_argument)


        # Subject
        elif func == "Subject Details":
            data, message = Subject.get_subject_details(**func_argument)

        elif func == "Add New Subject":
            data, message = Subject.new_subject(**func_argument)

        elif func == "Delete Subject":
            data, message = Subject.delete_subject(**func_argument)


        # Class
        elif func == "Class Details":
            data, message = Class.get_class_details(**func_argument)

        elif func == "Class Student List":
            data, message = Class.get_student_list(**func_argument)

        elif func == "Class Subject List":
            data, message = Class.get_class_subjects(**func_argument)


        # Semester
        elif func == "Semester Subjects":
            data, message = Semester.get_sem_subjects(**func_argument)


        # Course
        elif func == "Course Subjects":
            data, message = Course.get_course_subjects(**func_argument)


        # Branch
        elif func == "Branch Subjects":
            data, message = Branch.get_branch_subjects(**func_argument)


        # Report
        elif func == "Student Report":
            data, details, message = Report.generate_student_report(**func_argument)
            if data: 
                self.show_graph(7, **func_argument)
                self.set_up_extra_details_window(func, details)

        elif func == "Class Report":
            data, details, message = Report.generate_class_report(**func_argument)
            if data:
                self.set_up_extra_details_window(func, details)

        elif func == "Overall Report":
                self.set_up_extra_details_window(func)
                return

        elif func == "College Toppers Report":
            data, message = Report.get_college_toppers_students(**func_argument)
            self.show_graph(6, func_argument["Number_Of_Top_Students"])

        # Others
        elif func == "Update Password":
            data, message = Login.update_login_pwd(Id = self.ID, **func_argument)

        # Login
        elif func == "Register":
            data, message = Login.create_login_id(**func_argument)
            self.entry_box_setup()

        elif func == "login":
            data, message = Login.login(**func_argument)
            if data:
                # clearing login page components from root
                for widget in self.root.winfo_children():
                    widget.destroy()

                # adding college grade management class components
                College_Grade_Management(self.root, Id = func_argument["Id"])
                return
            self.entry_box_setup()

        elif func == "delete_login_id":
            data, message = Login.delete_login_id(**func_argument)
            self.entry_box_setup()


        else:
            return
        
        if data:
            if func not in ["Update Password", "Register", "login", "delete_login_id"]:
                self.print_details(data)
            self.status_update(f"SUCCESSFUL {message}")
        else:
            self.status_update(f"UNSUCCESSFUL {message}", self.status_red_color)


    def entry_box_setup(self):
        "void function for inheriting"
        pass    


    def print_details(self, data):
        """ Print the provided data in tabular fashion on the screen """

        if not data:
            self.status_update("UNSUCCESSFUL :Details not found!", self.status_red_color)
            return
        
        for widget in self.main_details_frame.winfo_children():
            widget.destroy()

        self.generate_heading(self.main_details_frame, "Details", font= self.sub_headings_font)

        headers = []
        values = []
        if type(data) == type([]):
            headers = [item for item in data[0]]
            values = [item.values() for item in data]
        elif type(data) == type({}):
            headers = data.keys()
            values = data.values()
        else:
            return
        
        self.table = ttk.Treeview(self.main_details_frame, columns = tuple(headers), show = 'headings')
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Arial", 14))

        for item in headers:
            self.table.heading(item, text = f'{item}')
        self.table.pack(fill= 'both', expand = True)

        for index in range(len(values)):
            self.table.insert(parent='', index= index, values = tuple(values[index]))
        
        return True


    def exit_app(self):
        """ Exits the app """
        self.root.quit()


    def show_about(self):
        """ Tells about the software """
        messagebox.showinfo("About", "Grade Management and analysis application using Tkinter\n")


class Login_Grade_Management(College_Grade_Management):
    """ inherits the College_Grade_Management class and adds the login functionality to the app """

    def __init__(self, root):

        self.root = root
        self.root.attributes(type_of_window, True)
        self.root.title(self.main_title)

        self.fullscreen = True
        self.root.bind("<F11>", lambda event: self.toggle_fullscreen())
        self.root.bind("<Escape>", lambda event: self.exit_fullscreen())

        """ Part for main heading area """

        self.main_viewing_heading_sub_frame = self.generate_heading(self.root, self.main_title, font= self.main_heading_font)

        """ Creating main frame """      

        self.main_viewing_canvas = tk.Canvas(self.root, bg= self.main_color_theme_light)
        self.main_viewing_canvas.pack(fill=tk.BOTH, expand=1, pady=4)

        self.bg = tk.PhotoImage(file = self.main_bg_img)
        self.main_viewing_canvas.create_image( 950, 500, image = self.bg, anchor = "center") 

        # Status part        
        self.clear_status_frame()

        # Entry part
        self.entry_frame_parent = tk.LabelFrame(self.main_viewing_canvas, bg= self.main_color_theme_light, bd=1, relief="solid")
        self.entry_frame_parent.pack(anchor="center", expand=1)

        # setting up the entry box for the login page
        self.entry_box_setup()

    def entry_box_setup(self):
        """ set/reset the entry frame for login window"""

        # clearing the entry frame
        self.clear_entry_frame()

        # adding register, login, delete id buttons in entry frame
        self.register_button = tk.Button(self.entry_frame_parent, text= "Register", font= self.sub_headings_font, bg= self.main_color_theme_dark, fg="white", command= lambda: self.set_up_entry_window("Register", LOGIN["Register"]))
        self.register_button.pack(anchor="center", padx= 10, pady= 10)

        self.login_button = tk.Button(self.entry_frame_parent, text= "Login", font= self.sub_headings_font, bg= self.main_color_theme_dark, fg="white", command= lambda: self.set_up_entry_window("login", LOGIN["login"]))
        self.login_button.pack(anchor="center", padx= 10, pady= 10)

        self.delete_login_id_button = tk.Button(self.entry_frame_parent, text= "Delete Id", font= self.sub_headings_font, bg= self.main_color_theme_dark, fg="white", command= lambda: self.set_up_entry_window("delete_login_id", LOGIN["delete_login_id"]))
        self.delete_login_id_button.pack(anchor="center", padx= 10, pady= 10)


def main():
    root = tk.Tk()
    Login_Grade_Management(root)
    root.mainloop()

if __name__ == "__main__":
    main()