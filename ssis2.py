import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import sqlite3

class SSIS:
    def __init__(self,root):
        self.root = root
        self.root.title("Student Information System")
        self.root.geometry("1300x700+0+0")
        self.root.config(bg="plum")
                
        c_code = StringVar()
        c_name = StringVar()
        c_search = StringVar()
        
        stud_id = StringVar()
        stud_name = StringVar()       
        stud_yl = StringVar()
        stud_gender = StringVar()
        stud_course = StringVar()
        search = StringVar()
        
        #======================================COURSE========================================================  
        
        def connectCourse():
            conn = sqlite3.connect("SSIS.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS courses (c_code TEXT PRIMARY KEY, c_name TEXT)") 
            conn.commit() 
            conn.close()
            
        def addCourse():
            try:
                conn = sqlite3.connect("SSIS.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO courses(c_code, c_name) VALUES (?,?)",\
                          (c_code.get(),c_name.get()))        
                conn.commit()       
                clearCourse()
                conn.close() 
                tkinter.messagebox.showinfo("Student Information System", "Course Recorded Successfully")
                displayCourse()
            except:
                tkinter.messagebox.showinfo("Student Information System", "Cannot Add Course")
                
        def displayCourse():
            conn = sqlite3.connect("SSIS.db")
            cur = conn.cursor()
            ctree.delete(*ctree.get_children())
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            for row in rows:
                ctree.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()

        
        def updateCourse():
            for selected in ctree.selection():
                conn = sqlite3.connect("SSIS.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE courses SET c_code=?, c_name=? WHERE c_code=?", \
                            (c_code.get(),c_name.get(), ctree.set(selected, '#1')))                       
                conn.commit()
                tkinter.messagebox.showinfo("Student Information System", "Course Updated Successfully")
                displayCourse()
                clearCourse()
                conn.close()
                
        def editCourse():
            if ctree.focus() == "":
                tkinter.messagebox.showerror("Student Information System", "Please select a record from the table.")
                return
            values = ctree.item(ctree.focus(), "values")
            c_code.set(values[0])
            c_name.set(values[1])
                    
        def deleteCourse(): 
            try:
                messageDelete = tkinter.messagebox.askyesno("SSIS", "Do you want to permanently delete this record?")
                if messageDelete > 0:   
                    conn = sqlite3.connect("SSIS.db")
                    cur = conn.cursor()
                    id_no = ctree.item(ctree.selection()[0])["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("DELETE FROM courses WHERE c_code = ?",(id_no,))                   
                    conn.commit()
                    ctree.delete(ctree.selection()[0])
                    tkinter.messagebox.askyesno("Student Information System", "Course Deleted Successfully")
                    displayCourse()
                    conn.close()                    
            except:
                tkinter.messagebox.showerror("Student Information System", "Students are still enrolled in this course")
                
        def searchCourse():
            conn = sqlite3.connect("SSIS.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses WHERE c_code = ?",(c_search.get(),))
            conn.commit()
            ctree.delete(*ctree.get_children())
            rows = cur.fetchall()
            for row in rows:
                ctree.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
 
        def RefreshCourse():
            displayCourse()
        
        def clearCourse():
            c_code.set('')
            c_name.set('') 

        #======================================STUDENTS========================================================  
       

        def connect():
            conn = sqlite3.connect("SSIS.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS students (stud_id TEXT PRIMARY KEY, stud_name TEXT, stud_course TEXT, \
                      stud_yl TEXT, stud_gender TEXT, \
                      FOREIGN KEY(stud_course) REFERENCES courses(c_code) ON UPDATE CASCADE)") 
            conn.commit() 
            conn.close()    
        
        def addStud():
            if stud_id.get() == "" or stud_name.get() == "" or stud_course.get() == "" or stud_yl.get() == "" or stud_gender.get() == "": 
                tkinter.messagebox.showinfo("Student Information System", "Please fill in the box with *")
            else:  
                ID = stud_id.get()
                ID_list = []
                for i in ID:
                    ID_list.append(i)
                a = ID.split("-")
                if len(a[0]) == 4:        
                    if "-" in ID_list:
                        x = ID.split("-")  
                        year = x[0]
                        number = x[1]
                        if year.isdigit()==False or number.isdigit()==False:
                            try:
                                tkinter.messagebox.showerror("Student Information System", "Invalid ID")
                            except:
                                pass
                        elif year==" " or number==" ":
                            try:
                                tkinter.messagebox.showerror("Student Information System", "Invalid ID")
                            except:
                                pass
                        else:
                            try:
                                conn = sqlite3.connect("SSIS.db")
                                cur = conn.cursor()
                                cur.execute("PRAGMA foreign_keys = ON")                                                                                                              
                                cur.execute("INSERT INTO students(stud_id, stud_name, stud_course, stud_yl, stud_gender) VALUES (?,?,?,?,?)",\
                                          (stud_id.get(),stud_name.get(),stud_course.get(),stud_yl.get(),stud_gender.get()))               
                                tkinter.messagebox.showinfo("Student Information System", "Student Recorded Successfully")
                                conn.commit() 
                                clear()
                                displayStud()
                                conn.close()
                            except:
                                tkinter.messagebox.showerror("Student Information System", "Course Unavailable")
                    else:
                        tkinter.messagebox.showerror("Student Information System", "Invalid ID")
                else:
                    tkinter.messagebox.showerror("Student Information System", "Invalid ID")
                 
        def updateStud():
            if stud_id.get() == "" or stud_name.get() == "" or stud_course.get() == "" or stud_yl.get() == "" or stud_gender.get() == "": 
                tkinter.messagebox.showinfo("Student Information System", "Please select a student")
            else:
                try:
                    for selected in stree.selection():
                        conn = sqlite3.connect("SSIS.db")
                        cur = conn.cursor()
                        cur.execute("PRAGMA foreign_keys = ON")
                        cur.execute("UPDATE students SET stud_id=?, stud_name=?, stud_course=?, stud_yl=?, stud_gender=?\
                              WHERE stud_id=?", (stud_id.get(),stud_name.get(),stud_course.get(),stud_yl.get(),stud_gender.get(),\
                                  stree.set(selected, '#1')))
                        conn.commit()
                        tkinter.messagebox.showinfo("Student Information System", "Student Updated Successfully")
                        displayStud()
                        clear()
                        conn.close()
                except:
                    tkinter.messagebox.showerror("Student Information System", "Cannot Update Student")
        
        def deleteStud():   
            try:
                messageDelete = tkinter.messagebox.askyesno("Student Information System", "Do you want to permanently delete this record?")
                if messageDelete > 0:   
                    conn = sqlite3.connect("SSIS.db")
                    cur = conn.cursor()
                    x = stree.selection()[0]
                    id_no = stree.item(x)["values"][0]
                    cur.execute("DELETE FROM students WHERE stud_id=?",(id_no,))                   
                    conn.commit()
                    stree.delete(x)
                    tkinter.messagebox.showinfo("Student Information System", "Student Deleted Successfully")
                    displayStud()
                    conn.close()                    
            except:
                tkinter.messagebox.showinfo("Student Information System", "Cannot Delete Student")
                
        def searchStud():
            stud_ID = search.get()
            try:  
                conn = sqlite3.connect("SSIS.db")
                cur = conn.cursor()
                cur .execute("PRAGMA foreign_keys = ON")
                cur.execute("SELECT * FROM students")
                conn.commit()
                stree.delete(*stree.get_children())
                rows = cur.fetchall()
                for row in rows:
                    if row[0].startswith(stud_ID):
                        stree.insert("", tk.END, text=row[0], values=row[0:])
                conn.close()
            except:
                tkinter.messagebox.showerror("Student Information System", "Invalid ID")           
                
        def displayStud():
            stree.delete(*stree.get_children())
            conn = sqlite3.connect("SSIS.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM students")
            rows = cur.fetchall()
            for row in rows:
                stree.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
                            
        def editStud():
            x = stree.focus()
            if x == "":
                tkinter.messagebox.showerror("Student Information System", "Please select a record from the table.")
                return
            values = stree.item(x, "values")
            stud_id.set(values[0])
            stud_name.set(values[1])
            stud_course.set(values[2])
            stud_yl.set(values[3])
            stud_gender.set(values[4])
            
        def Refresh():
            displayStud()
        
        def clear():
            stud_id.set("")
            stud_name.set("")
            stud_course.set("")
            stud_yl.set("")
            stud_gender.set("")
            
        #======================================ENTRIES AND WIDGET========================================================   
        
        courseCode = Label(self.root, font=("Poppins", 12, "bold"), text="Course Code:", padx=5, pady=5, bg="plum")
        courseCode.place(x=125,y=500)
        courseCode = Entry(self.root, font=("Poppins", 13), textvariable=c_code, width=33)
        courseCode.place(x=260,y=505)

        courseName = Label(self.root, font=("Poppins", 12,"bold"), text="Course Name:", padx=5, pady=5, bg="plum")
        courseName.place(x=125,y=540)
        courseName = Entry(self.root, font=("Poppins", 13), textvariable=c_name, width=33)
        courseName.place(x=260, y=545)
        
        Search = Entry(self.root, font=("Poppins", 11), textvariable=c_search, width=29)
        Search.place(x=876,y=475)
        Search.insert(0,'Search course code here')
        
        
        StudentID = Label(self.root, font=("Poppins", 12, "bold"), text="Student ID:", padx=5, pady=5, bg="plum")
        StudentID.place(x=125,y=40)
        StudentIDFormat = Label(self.root, font=("Poppins", 8,"bold"), text="(YYYY - NNNN)", bg="plum")
        StudentIDFormat.place(x=255,y=70)
        StudentID = Entry(self.root, font=("Poppins", 13), textvariable=stud_id, width=33)
        StudentID.place(x=255,y=45)

        StudentName = Label(self.root, font=("Poppins", 12,"bold"), text="Full Name:", padx=5, pady=5, bg="plum")
        StudentName.place(x=125,y=100)
        StudentNAMEFormat = Label(self.root, font=("Poppins", 8,"bold"), text="LASTNAME, FISRTNAME MIDDLEINITIAL", bg="plum")
        StudentNAMEFormat.place(x=255,y=130)
        StudentName = Entry(self.root, font=("Poppins", 13), textvariable=stud_name, width=33)
        StudentName.place(x=255,y=105)
        
        StudentCourse = Label(self.root, font=("Poppins", 12,"bold"), text="Course:", padx=5, pady=5, bg="plum")
        StudentCourse.place(x=125,y=160)
        StudentCourse = Entry(self.root, font=("Poppins", 13), textvariable=stud_course, width=33)
        StudentCourse.place(x=255,y=165)

        StudentYearLevel = Label(self.root, font=("Poppins", 12,"bold"), text="Year Level:", padx=5, pady=5, bg="plum")
        StudentYearLevel.place(x=125,y=200)
        StudentYearLevel = ttk.Combobox(self.root,
                                        value=["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"],
                                        state="readonly", font=("Poppins", 13), textvariable=stud_yl,
                                        width=31)
        StudentYearLevel.place(x=255,y=205)

        StudentGender = Label(self.root, font=("Poppins", 12,"bold"), text="Gender:", padx=5, pady=5, bg="plum")
        StudentGender.place(x=125,y=240)
        StudentGender = ttk.Combobox(self.root, value=["Male", "Female"], font=("Poppins", 13),
                                             state="readonly", textvariable=stud_gender, width=31)
        StudentGender.place(x=255,y=245)

        SearchBar = Entry(self.root, font=("Poppins", 11), textvariable=search, width=29)
        SearchBar.place(x=876,y=10)
        SearchBar.insert(0,'Search ID here')
        
        
        
        #======================================TREEVIEW========================================================
        scrollbar = Scrollbar(self.root, orient=VERTICAL)

        ctree = ttk.Treeview(self.root,
                                        columns=("Course Code", "Course Name"),
                                        height = 5,
                                        yscrollcommand=scrollbar.set)

        ctree.heading("Course Code", text="Course Code", anchor=W)
        ctree.heading("Course Name", text="Course Name",anchor=W)
        ctree['show'] = 'headings'

        ctree.column("Course Code", width=200, anchor=W, stretch=False)
        ctree.column("Course Name", width=430, stretch=False)

        ctree.place(x=575,y=500)
        scrollbar.config(command=ctree.yview)
        
        stree = ttk.Treeview(self.root,
                                        columns=("ID Number", "Name", "Course", "Year Level", "Gender"),
                                        height = 13,
                                        yscrollcommand=scrollbar.set)

        stree.heading("ID Number", text="ID Number", anchor=W)
        stree.heading("Name", text="Name",anchor=W)
        stree.heading("Course", text="Course",anchor=W)
        stree.heading("Year Level", text="Year Level",anchor=W)
        stree.heading("Gender", text="Gender",anchor=W)
        stree['show'] = 'headings'

        stree.column("ID Number", width=100, anchor=W, stretch=False)
        stree.column("Name", width=200, stretch=False)
        stree.column("Course", width=130, anchor=W, stretch=False)
        stree.column("Year Level", width=100, anchor=W, stretch=False)
        stree.column("Gender", width=100, anchor=W, stretch=False)

        stree.place(x=575,y=40)
        scrollbar.config(command=stree.yview)
        #======================================BUTTONS========================================================
        
        btnAddCourse = Button(self.root, text="ADD", font=('Poppins', 10), height=1, width=10, bd=4, bg="sky blue",command=addCourse)
        btnAddCourse.place(x=240,y=600)
        
        btnUpdateCourse = Button(self.root, text="UPDATE", font=('Poppins', 10), height=1, width=10, bd=4, bg="sky blue",command=updateCourse)
        btnUpdateCourse.place(x=350,y=600)
        
        btnClearCourse = Button(self.root, text="CLEAR", font=('Poppins', 10), height=1, width=10, bd=4, bg="sky blue",command=clearCourse)
        btnClearCourse.place(x=130,y=600)
        
        btnDeleteCourse = Button(self.root, text="DELETE", font=('Poppins', 10), height=1, width=10, bd=4,bg="sky blue",command=deleteCourse)
        btnDeleteCourse.place(x=460,y=600)
        
        btnSelectCourse = Button(self.root, text="Select", font=('Poppins', 10), height=1, width=11,bg="pink",command=editCourse)
        btnSelectCourse.place(x=575,y=465)
        
        btnSearchCourse = Button(self.root, text="Search", font=('Poppins', 10), height=1, width=10, bg="pink",command=searchCourse)
        btnSearchCourse.place(x=1117,y=465)
        
        btnRefreshCourse = Button(self.root, text="Show All", font=('Poppins', 10), height=1, width=11,bg="pink",command=RefreshCourse)
        btnRefreshCourse.place(x=685,y=465)
        
        
        
        
        btnAddID = Button(self.root, text="Add", font=('Poppins', 10), height=1, width=10, bd=4,bg="sky blue",command=addStud)
        btnAddID.place(x=240,y=300)
        
        btnUpdate = Button(self.root, text="Update", font=('Poppins', 10), height=1, width=10, bd=4, bg="sky blue",command=updateStud)
        btnUpdate.place(x=350,y=300)
        
        btnClear = Button(self.root, text="Clear", font=('Poppins', 10), height=1, width=10, bd=4,bg="sky blue", command=clear)
        btnClear.place(x=130,y=300)
        
        btnDelete = Button(self.root, text="Delete", font=('Poppins', 10), height=1, width=10, bd=4,bg="sky blue",command=deleteStud)
        btnDelete.place(x=460,y=300)
        
        btnSelect = Button(self.root, text="Select", font=('Poppins', 10), height=1, width=11,bg="pink",command=editStud)
        btnSelect.place(x=575,y=10)
        
        btnSearch = Button(self.root, text="Search", font=('Poppins', 10), height=1, width=10, bg="pink",command=searchStud)
        btnSearch.place(x=1117,y=10)
        
        btnRefresh = Button(self.root, text="Show All", font=('Poppins', 10), height=1, width=11,bg="pink",command=Refresh)
        btnRefresh.place(x=685,y=10)
        
        #=======================================================================================================
        connectCourse()
        displayCourse()
        connect()
        displayStud()

if __name__ == '__main__':
    root = Tk()
    application = SSIS(root)
    root.mainloop()