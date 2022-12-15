#!/usr/bin/python3

import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo
import tkinter as tk
import pandas as pd
import sys, os

def importData(excelFile): #Function that extracts column 1 in excel file
    workbook = pd.read_excel(excelFile, usecols = 'C')
    workbook.head()
    workbook.dropna(
    axis=0,
    how ='any',
    subset=None,
    inplace=True
    )

    return workbook.values[1:]

def generate(): #Supposed to generate receipt
    try:
        fileName = "receipt.txt"
        receiptFile = open(fileName, "x")
    except FileExistsError:
        print("Receipt file is Ready.")

    with open("parser.txt", "r") as parser:
        for lines in parser:
            lines = lines.strip("\n").split("~")
            current = open("dependencies/log.txt")
            for i in current:
                print(i)
                currentUser = open("dependencies/compiledTreasurer.txt")
                for user in currentUser:
                    user = user.split("~")
                    lines.append(i)


                receipt = open(fileName, "a")
                receipt.write('~'.join(map(str, lines)) + "\n")



    popupMsg("Receipt Saved", "Receipt saved successfully.")

def openFile(): #Used to give the user freedom to choose excel file
    global myFile
    myFile = filedialog.askopenfilename(title='Open a file',initialdir='/')

def createRecord(): #Creates a record (a function in treasurerView)
    try:
        parserFile = open("parser.txt", "x")
    except FileExistsError:
        print("Parser is ready.")

    def importexcel():
        openFile()
        with open("data.txt", "w") as data:
            data.write('\n'. join(map(str, myFile)))

    def save():
        try:
            compiledInfo = recTitle.get() + "~" + recDesc.get("1.0", "end-1c") + "~" + recDue.get() + "~" + recAmount.get() + "~"  + '\n'
            with open("contribution.txt", "a") as contri:
                contri.write(compiledInfo)

                record.destroy()
            popupMsg("Record Saved", "Record is saved successfully.")
        except FileNotFoundError:
            contriFile = open("contribution.txt", "x")
            print("Contribution File Created.")


    record = Tk()
    record.title("Create Records")
    record.geometry("290x360")
    record.config(bg = "lightblue")

    recTitle = Entry(record, width = 35)
    recTitle.insert(0,"Name")
    recTitle.grid(row = 0, column = 0, pady = 5)
    recDesc = Text(record, width = 35, height = 10)
    recDesc.insert(END, "Description of the Contribution")
    recDesc.grid(row = 1, column = 0, pady = 5)
    recDue = Entry(record, width = 35)
    recDue.insert(0,"Due Date")
    recDue.grid(row = 2, column = 0, pady = 5)
    recAmount = Entry(record, width = 35)
    recAmount.insert(0,"Amount")
    recAmount.grid(row = 3, column = 0, pady = 5)

    importButton = Button(record, width = 15, text = "Import Excel", command = importexcel)
    importButton.grid(row =4, column =0)
    recButton = Button(record, width = 15, text = "Save", command = save)
    recButton.grid(row =5, column =0, pady = 5)

    record.mainloop()

def editingTable(): #Creates an editable table (a function in treasurerView)
    def extract_table(): #Extract information from user table to the parser file
        try:
            with open("parser.txt", "w") as dataFilter:
                rowCount = table.rowCount()
                colCount = table.columnCount()
                for row in range(rowCount):
                    rowData = " "
                    for cols in range(colCount):
                        tableWidget = table.item(row, cols)
                        if tableWidget and tableWidget.text:
                            rowData = rowData + "~" + tableWidget.text()
                        else:
                            rowData = rowData + "~" + 'NULL'
                    dataFilter.write(rowData + '\n')

        except FileNotFoundError:
            parserFile = open("parser.txt", "x")
            print("Parser File Created.")

    def loadExcelData(): #Extract information from the active excel file(myFile)
        try:
            with open("data.txt", "w") as data:
                for info in importData(str(myFile)):
                    info = "~".join(map(str, info))
                    info = info + "~"
                    data.write(info)

            with open("data.txt", "r") as data:
                dataStorage = []
                for line in data:
                    line = line.split("~")
                    if len(dataStorage) < len(importData(str(myFile))):
                        dataStorage.append(line)

                for i in dataStorage:
                    for row in range(len(line)):
                        for col in range(1):
                            detail = QTableWidgetItem(i[row])
                            table.setItem(row, col, detail)
        except FileNotFoundError:
            dataFile = open("data.txt", "x")
            print("Data File Created.")

    app = QApplication(sys.argv)
    screen = QWidget()
    screen.setGeometry(0,0, 700, 400)
    table = QTableWidget()
    table.setRowCount(len(importData(str(myFile))))
    table.setColumnCount(6)
    table.setHorizontalHeaderLabels(['Name', 'Status', 'Amount', 'Name of Contribution','Date of Payment', 'Due Date'])
    layout = QVBoxLayout()
    layout.addWidget(table)
    button = QPushButton('Load Data')
    layout.addWidget(button)
    button.clicked.connect(loadExcelData)
    button1 = QPushButton('Export Data')
    button1.clicked.connect(extract_table)
    layout.addWidget(button1)
    screen.setLayout(layout)

    screen.show()


    app.exec_()

def popupMsg(title, message): #Custom Popup Message. For Error and Notice.
    popup = Tk()
    popup.title(title)
    popup.geometry("300x100")
    popup.resizable(0,0)
    Msg = Label(popup, text = message)
    Msg.pack()
    popup.mainloop()

def treasurerView(): #GUI for treasurer access
    def saveExit():
        try:
            def create():
                fileVar.set("Output/ " + name_entry.get() + ".csv")
                out_csv = csv.writer(open(fileVar.get(), "w"))
                out_csv.writerows(in_txt)
                del out_csv
                fileName.destroy()
                root.destroy()

            in_txt = csv.reader(open("receipt.txt", "r"), delimiter = "~")
            fileName = Tk()
            fileName.title("Output")
            fileName.resizable(0,0)
            label = Label(fileName, text = "Please enter filename for the output:\nDefaulf file extension: .csv ")
            label.grid(row = 0, column = 0)
            name_entry = Entry(fileName, width = 30)

            fileVar = StringVar(fileName)
            name_entry.grid(row = 1, column =0)
            myButton = Button(fileName, text = "Create", command = create)
            myButton.grid(row = 2, column = 0)
            fileName.mainloop()
        except:
            root.destroy()
            signIn()

    root = Tk()
    root.title("Student Fee Collection System")
    root.geometry("700x495")
    root.resizable(0,0)
    root.config(bg = "lightblue")

    ButtonFrame = Frame(root)
    ButtonFrame.grid(row = 0, column = 0, padx = 10)

    TableFrame = Frame(root)
    TableFrame.grid(row = 0, column = 1)

    #PanedWindow
    createTable = PanedWindow(TableFrame, width =570, height = 450, bg = "black")
    createTable.grid(row = 0, column = 0 )

    msg = '''>>> Welcome to Student Fee Collection System.\n>>> Create New Record: Use to create new contribution record.
>>> Update Records: Use to manipulate imported spreadsheet file.\n>>> Generate Receipt: Use for generating receipt for students.
>>> Delete Records: Use to delete exising records.\n>>> Save and Exit: Use to save data in csv file.\n\n\n
-----------------------Things to keep in mind-------------------------\n
!!! Please read carefully.
>>> Create data only when necessary.
>>> Updating will overwrite data from excel file,
    but the receipt data will not be affected.
>>> After clicking the export button, exit the update table manually.
>>> Generating receipt will automatically update student view.
>>> Delete at your own risk.
>>> Always click name and save your file accordingly.
>>> Using a name of an existing file will overwrite it.\n
>>> Be Happy:)
            '''
    welcomeLabel = Text(createTable,  bg = "black", fg = "green")
    welcomeLabel.insert(INSERT, msg)
    welcomeLabel.config(state = DISABLED)
    createTable.add(welcomeLabel)

    #Buttons

    WIDTH = 8
    HEIGHT = 5

    createButton = Button(ButtonFrame, text = "Create\nNew\nRecords", width = WIDTH, height = HEIGHT, command = createRecord)
    createButton.grid(row = 0, column =0)
    updateButton = Button(ButtonFrame, text = "Update\nRecords", width = WIDTH, height = HEIGHT, command = editingTable)
    updateButton.grid(row = 1, column =0)
    generateButton = Button(ButtonFrame, text = "Generate\nReceipt", width = WIDTH, height = HEIGHT, command = generate)
    generateButton.grid(row = 2, column =0)
    deleteButton = Button(ButtonFrame, text = "Delete\nRecords", width = WIDTH, height = HEIGHT, command = delete)
    deleteButton.grid(row = 3, column =0)
    saveButton = Button(ButtonFrame, text = "Save\nand\nExit", width = WIDTH, height = HEIGHT, command = saveExit)
    saveButton.grid(row = 4, column =0)


    root.mainloop()

def signIn(): # as the mainloop or the main application
    global currentUser
    def validate():
        with open("dependencies/studentList.txt", "r") as studentList:
            for list in studentList:
                list = list.strip().split("~")
                if name.get() in list:
                    if password.get() in list:
                        if departmentVar.get() in list:
                            if courseVar.get() in list:
                                if blockVar.get() in list:
                                    if v.get() == "1":
                                        with open("dependencies/treasurer.txt", "r") as tres:
                                            logFile = open("dependencies/log.txt", "w")
                                            for assigned in tres:
                                                logFile.write(name.get())
                                                if name.get() in assigned:
                                                    signScr.destroy()
                                                    logFile.close()
                                                    treasurerView()
                                                else:
                                                    pass
                                    elif v.get() == "0" in list:
                                        with open("dependencies/log.txt", "w") as logFile:
                                            logFile.write(str(name.get()))
                                        signScr.destroy()
                                        studentView()
                                    else: continue
                                else: continue
                            else: continue
                        else: continue
                    else: continue
                else: continue

    signScr=Tk()
    signScr.geometry('410x400')

    signScr.config(bg='lightblue')
    signScr.title('Sign-In')

    name = Entry(signScr,width=45)
    name.insert(0, "Surname, Firstname MI.")

    password = Entry(signScr, width=45)
    password.insert(0, "Password")

    options = ["ICS", "CAS", "CBPA","COENG",]
    optionMo = ["BSIT","BSIS","BSB", "BSDC", "BSAP", "BAS", "BAH", "BSBE", "BSMM", "BSHRM", "BSFM", "BPA", "BSHM", "BSA", "BSOA", "BSE", "BSCE", "BSEE", "BSME"]
    option1 = ['1A','1B','1C', "1D", "2A", "2B", "2C", "2D", "3A", "3B", "3C", "3D", "4A", "4B", "4C", "4D"]

    departmentVar = StringVar()
    departmentVar.set("Department")

    courseVar = StringVar()
    courseVar.set("Course")

    blockVar = StringVar()
    blockVar.set('Block and Year Level')

    department = tk.OptionMenu(signScr,departmentVar, *options)
    department.config(width=25)

    course = tk.OptionMenu(signScr,courseVar, *optionMo)
    course.config(width=25)

    block = tk.OptionMenu(signScr,blockVar, *option1)
    block.config(width=25)

    department.grid(row=2, column = 0,padx=70,pady=3)
    course.grid(row=3, column= 0, padx=70,pady=3)
    block.grid(row=4, column = 0, padx=70,pady=3)

    #Treasurer or Student

    v = StringVar(signScr, "1")
    values = {"Treasurer": "1",
            "Student": "0"}

    i = 5
    for (text, value) in values.items():
        Radiobutton(signScr, text = text, variable= v, value = value).grid(row = i, column =0,pady=5)
        i += 1

    btn=tk.Button(signScr, text="Sign In",width=20, height=1, relief='ridge', command = validate)
    btn.grid(row=7,column=0, pady= 10)

    Signup=tk.Label(signScr,bg='lightblue',text="Don't have an account? Sign up here.", font=('Helvetica 8 underline'))
    Signup.grid(row=8,column=0)
    Signup.bind("<Button-1>", signUp)

    name.grid(row=0, column =0,padx=25,pady=6)
    password.grid(row=1, column=0,padx=25,pady=6)

    signScr.mainloop()

def signUp(default = " "): #Stores an information that will be checked manually
    def storeReq():
        with open("dependencies/request.txt", "a") as newFile:
            if password.get() == confirm.get():
                newFile.write(name.get() + "~" + email.get() + "~" + id.get() + "~" + password.get() + "~" + confirm.get() + "\n")
                root.destroy()
                popupMsg("Notice", "Please wait for a few days to be verify.\nWe will notice you if your account \nhad been created.\nIf problem persist please contact \nthe IT support of your department.")
            else:
                popupMsg("Login Error","Password do not match.")


    root = Tk()
    root.geometry('380x250')
    root.config(bg='lightblue')
    root.title('Sign Up')

    name = Entry(root,width= 40)
    name.insert(0, "Name")

    email = Entry(root, width = 40)
    email.insert(0, "Email")

    id = Entry(root,width= 40)
    id.insert(0, 'Student ID')

    password = Entry(root,width= 40)
    password.insert(0,'Password')

    confirm = Entry(root,width= 40)
    confirm.insert(0,'Confirm Password')

    name.grid(row=0, column=0,padx=25,pady=9)
    email.grid(row = 1, column = 0, padx = 25, pady =9)
    id.grid(row=2, column=0,padx=25,pady=9)
    password.grid(row=3,column=0,padx=25,pady=9)
    confirm.grid(row=4,column=0,padx=25,pady=9)

    sign_button=Button(root, text='Sign Up', command = storeReq).grid(row=5, column=0, padx=30, pady=5)

    root.mainloop()

def studentView(): #GUI for student access
    def items_selected(event): #Will show the text in contribution.txt file in the form of List Widget
        i =  str(' '.join(map(str, listbox.curselection())))
        contriInfo = []
        with open("contribution.txt", "r") as receipt:
            for contri in enumerate(receipt):
                contri = '~'.join(map(str, contri))
                contri = contri.split("~")
                contriInfo.append(contri)

            for desc in contriInfo:
                if i in desc:
                    descVar.set("\t"+desc[2])

            text.delete("1.0", "end")
            text.insert(INSERT, "Description of contribution here:\n"+descVar.get())
            amountVar.set([desc[4] for desc in contriInfo if i in desc])
            dueVar.set([desc[3] for desc in contriInfo if i in desc])

    def logout():
        screen.destroy()
        signIn()


    #Student View Screen
    screen = Tk()
    screen.title("Student Fee Collection System")
    screen.config(bg = "lightblue")
    screen.geometry("720x480")
    screen.resizable(0,0)

    #Frame
    contriframe = Frame(screen, bg = "lightblue")
    contriframe.grid(row = 0, column = 0, padx = 5)
    descframe = Frame(screen, bg = "lightblue")
    descframe.grid(row = 0, column = 1)
    button_frame = Frame(screen, bg = "lightblue")
    button_frame.grid(row = 1, column = 1)


    #Canvas
    listSection = PanedWindow(contriframe, height = 425, bg = "white", relief='ridge')
    listSection.grid(row = 0, column = 0, padx = 10)
    descSection = PanedWindow(descframe, height = 430, width = 500,bg = "white",  relief='ridge')
    descSection.grid(row = 1, column = 0)


    #Contribution List
    contri_label = LabelFrame(listSection)
    label = Label(contri_label, text="List of Contribution: ")
    label.grid(row = 0, column = 0)
    listSection.add(contri_label)
    listbox = Listbox(contri_label, height = 40,
                  width = 15,
                  bg = "grey",
                  activestyle = 'dotbox',
                  font = "Helvetica",
                  fg = "white",
                  selectmode = SINGLE)
    listbox.grid(row = 1, column = 0)

    try:
        with open("contribution.txt", "r") as info:
            for lines in info:
                lines = lines.split("~")
                listbox.insert(END, lines[0])
    except FileNotFoundError:
        popupMsg("File Not Found","Contribution file is missing.")

    #Description
    desc_label = LabelFrame(descSection)
    descVar = StringVar(screen)
    text= Text(desc_label,wrap=WORD)
    text.insert(INSERT, "Description of contribution here: ")
    text.grid(row = 0, column= 0)
    text.config(width = 61, height = 21)

    descSection.add(desc_label)

    myFrame = Frame(desc_label)
    myFrame.grid(row = 1, column = 0)

    #Price
    mlabel = Label(myFrame, text = "Amount: ")
    mlabel.grid(row = 1, column = 0)
    amountVar = StringVar(screen)
    amountText = Label(myFrame, textvariable = amountVar)
    amountText.grid(row = 2, column = 0)

    #Blank
    nlabel = Label(myFrame, text = "         ")
    nlabel.grid(row = 1, column = 1)

    #Due Date
    olabel = Label(myFrame, text = "Due Date: ")
    olabel.grid(row = 1, column = 2)
    dueVar = StringVar(screen)
    dueText = Label(myFrame, textvariable = dueVar)
    dueText.grid(row = 2, column = 2)
    listbox.bind('<<ListboxSelect>>', items_selected)

    #Show Receipt
    showReceipt = Button(button_frame, text = "Show Receipt", command = generateReceipt)
    showReceipt.grid(row = 1, column = 0, pady = 3)

    logoutButton = Button(button_frame, text = "Sign Out", command = logout)
    logoutButton.grid(row = 1, column = 1, pady = 3)


    screen.mainloop()

def generateReceipt(): #Generates a receipt(a function in studentView)
    def showDesc(default = " "):
        with open("contribution.txt", "r") as descContainer:
            for k in descContainer:
                k = k.split("~")
                if contrib.get() in k:
                    descheader.delete("1.0", "end")
                    descheader.insert(INSERT, k[1])

        with open("dependencies/log.txt", "r") as activeUser:
            for user in activeUser:
                user = user.strip()

        with open("receipt.txt", "r") as paymentData:
            paymentList = []
            for data in paymentData:
                data = data.strip("\n").split("~")
                paymentList.append(data)
                nameData.set("-")
                statData.set("-")
                amountData.set("-")
                contriData.set("-")
                dateData.set("-")
                noteData.set("-")

                [nameData.set(name[1]) for name in paymentList if user in name]
                for stat in paymentList:
                    if contrib.get() in stat and user in stat:
                        statData.set(stat[2])
                        #[statData.set(stat[2]) for stat in paymentList if user in stat]

                for amount in paymentList:
                    #[amountData.set(amount[3]) for amount in paymentList if user in amount]
                    if contrib.get() in amount and user in amount:
                        amountData.set(amount[3])

                for contri in paymentList:
                    #[contriData.set(contri[4]) for contri in paymentList if user in contri]
                    if contrib.get() in contri and user in contri:
                        contriData.set(contri[4])

                for date in paymentList:
                    #[dateData.set(date[5]) for date in paymentList if user in date]
                    if contrib.get() in date and user in date:
                        dateData.set(date[5])

                for note in paymentList:
                    if contrib.get() in note and user in note:
                        noteData.set(note[7])
                        #[noteData.set(note[7]) for note in paymentList if user in note]




    root=Tk()
    root.geometry('770x360')
    root.config(bg='lightblue')
    root.title('Receipt')
    root.resizable(0,0)

    infoframe= Frame(root, bg='lightblue', padx=10, relief= 'ridge')
    infoframe.grid(row=0, column=0)

    nameData = StringVar(root, "-")
    statData = StringVar(root, "-")
    amountData = StringVar(root, "-")
    contriData = StringVar(root, "-")
    dateData = StringVar(root, "-")
    noteData = StringVar(root, "-")


    name=Label(infoframe,textvariable = nameData ,width=50, height=2, relief= 'ridge').grid(row=2,column=0, pady= 10)
    status=Label(infoframe,textvariable = statData ,width=50, height=2, relief= 'ridge').grid(row=4,column=0, pady= 10)
    amount=Label(infoframe,textvariable= amountData ,width=50, height=2,  relief='ridge').grid(row=6,column=0, pady= 10)
    contribute =Label(infoframe,textvariable= contriData ,width=50, height=2,  relief='ridge').grid(row=8,column=0, pady= 10)
    date=Label(infoframe,textvariable = dateData , width = 50, height=2, relief= 'ridge').grid(row=10,column=0, pady= 10)
    noted=Label(infoframe,textvariable= noteData ,width=50, height=2, relief= 'ridge').grid(row=12,column=0, pady= 10)

    descriptionframe= Frame(root, bg='lightblue')
    descriptionframe.grid(row=0, column=1)


    try:
        with open("contribution.txt", "r") as contriFile:
            for description in contriFile:
                description = description.split("~")

        descheader=Text(descriptionframe, height=17,width='40')
        descheader.grid(row=1, column=0)
        descheader.insert(INSERT, "Description of Contribution")

        conOptions = []

        with open("contribution.txt", "r") as options:
            for i in options:
                i = i.split("~")
                conOptions.append(i[0])

        contrib = StringVar(root)
        contrib.set( "Contribution" )
        contriOption = OptionMenu(descriptionframe, contrib , *conOptions, command = showDesc)
        contriOption.config(width = 35)
        contriOption.grid(row=0, column=0)

    except FileNotFoundError:
        popupMsg("File Not Found","Contribution file not found.")

    root.mainloop()

def delete(): #Deletes the parser file (a function in treasuserView)
    try:
        os.remove("parser.txt")
        os.remove("data.txt")
        os.remove("contribution.txt")
        os.remove("receipt.txt")
        popupMsg("File Deleted", "Files were successfully deleted.")
    except FileNotFoundError:
        popupMsg("File Not Found", "Parser not found.")

myFile = "dependencies/empty.xlsx"


if __name__ == '__main__':
   signIn()
