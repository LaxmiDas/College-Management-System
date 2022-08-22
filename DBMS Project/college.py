
#Connect to the database & named mysql
import mysql.connector as mysql


#Naming Database as db
db = mysql.connect(host="localhost", user="root", password= "", database="college")

#"command_handler" = an object of db.cursor() to run different queries
#(buffered = True) is to run multiple queries without error
command_handler = db.cursor(buffered = True)




#Function for Student session
def student_session(username):
    while 1:
        print("")
        print("Student Menu")
        print("")
        print("1. View Register")
        print("2. Download Register")
        print("3. Logout")

        user_option = input(str("Option : "))
        if user_option == "1":
            print("Displaying register for " +username)
            
            #In place of query_vals used username variable
            username = (str(username),)

            #To run a command
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s", username)
            
            #A student can view his registers only
            #To fetch all records
            records = command_handler.fetchall()

            #To show specific record of that student
            for record in records:
                print(record)

        elif user_option == "2":
            print("Downloading Register")
            username = (str(username),)
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s", username)
            
            #A student can download his registers only
            #To fetch all records
            records = command_handler.fetchall()

            #To store records of that student in a file
            for record in records:

                #To open a file called 'Register.txt'
                #Location of the file is set to be in 'C:\Users\User\Desktop'
                with open("C:/Users/User/Desktop/Register.txt", "w") as f:    #file opening is referred as 'f'
                    
                    #for every new record we will write that in the file
                    #We can access the Register file from our computer
                    f.write(str(records) + "\n")

                #Will close the file after all the records are written
                f.close()
                print("All Records Saved")


        #To Logout from Student Menu
        elif user_option == "3":
            break

        #If no valid option is chosen
        else:
            print("No valid option is selected.")



#Function for Teacher session
def teacher_session():
    while 1:
        print("")
        print("Teacher menu")
        print("1. Mark Student Register")
        print("2. View Register")
        print("3. Logout")

        user_option = input(str("Option : "))
        if user_option == "1":
            print("")

            #To Get the name of the students registered
            print("Mark student register")
            command_handler.execute("SELECT username FROM users WHERE privilege = 'student'")
            
            #To store the records of student into records variable
            records = command_handler.fetchall()

            #To store the date of the student registered
            date = input(str("Date : DD/MM/YYYY : "))


            #for loop for registering students into records
            for record in records:
                record = str(record).replace("'","")    #the record is returned as tuple with comma & brackets
                record = str(record).replace(",","")    #comma & brackets are replaced with blank space
                record = str(record).replace("(","")    #only the username of students will be returned
                record = str(record).replace(")","")


                #Status can be Present/ Absent/ Late
                #Setting Status
                status = input(str("Status for " + str(record) + " is Present / Absent / Late : "))

                #All info of the student put into query_vals variable
                query_vals = (str(record), date, status)


                #To run a command
                command_handler.execute("INSERT INTO attendance (username, date, status) VALUES (%s, %s, %s)",query_vals)

                #To save the changes in Database
                db.commit()

                #To show if the student is marked present or absent or late
                print(record + " Marked as " + status)

        #To Show the register of students
        elif user_option == "2":
            print("")

            #To run a command
            command_handler.execute("SELECT username, date, status FROM attendance")
            
            #To store the records we will get from the query above
            records = command_handler.fetchall()
            print("Displaying all Registers below")

            #for loop to print records of each student who has been registered
            for record in records:
                print(record)

        
        #To Logout from Teacher Menu2
        elif user_option == "3":
            break

        #If no valid option is chosen
        else:
            print("No valid option is selected.")




#Function for Admin session
def admin_session():
    while 1:
        print("")
        print("Admin menu")
        print("1. Register New Student")
        print("2. Register New Teacher")
        print("3. Delete Existing Student")
        print("4. Delete Existing Teacher")
        print("5. Logout")

        #To take input of Option
        user_option = input(str("Select an Option : "))

        #To Register Student
        if user_option == "1":
            print("")
            print("Register New Student Account")
            username = input(str("Student username : "))
            password = input(str("Student password : "))
            query_vals = (username, password)

            #To run command
            command_handler.execute("INSERT INTO users(username, password, privilege) VALUES (%s, %s, 'student')", query_vals)
             
            #To Save changes in Database
            db.commit()
            print(username + " has been regisered as a student")

        #To Register Teacher
        elif user_option == "2":
            print("")
            print("Register New Teacher Account")
            username = input(str("Teacher username : "))
            password = input(str("Teacher password : "))
            query_vals = (username, password)

            #To run command
            command_handler.execute("INSERT INTO users(username, password, privilege) VALUES (%s, %s, 'teacher')", query_vals)
             
            #To Save changes in Database
            db.commit()
            print(username + " has been regisered as a teacher")

        
        #To Delete Exixting Student
        elif user_option == "3":
            print("")
            print("Delete Existing Student Account")
            username = input(str("Student username : "))
            query_vals = (username, 'student')

            #To run command
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s", query_vals)
            
            #To save changes in Database
            db.commit()

            #Command to check how many rows affected
            #If No row is affected that means the row doesn't exist
            if command_handler.rowcount < 1:
                print("User not Found.")
            else:
                print(username + " has been deleted.")


        #To Delete Exixting Teacher
        elif user_option == "4":
            print("")
            print("Delete Existing Teacher Account")
            username = input(str("Teacher username : "))
            query_vals = (username, 'teacher')

            #To run command
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s", query_vals)
            
            #To save changes in Database
            db.commit()

            #Command to check if any row is affected
            #If No row is affected that means the row doesn't exist
            if command_handler.rowcount < 1:
                print("User not Found.")
            else:
                print(username + " has been deleted")


        #To Logout from Admin menu
        elif user_option == "5":
            break


        #If no valid option is chosen
        else:
            print("No valid option is selected")




#Function for Authentication of Student
def auth_student():
    print("")
    print("Student Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))

    query_vals = (username, password, 'student')

    #To run a command
    command_handler.execute("SELECT username FROM users WHERE username = %s AND password = %s AND privilege = %s", query_vals)

    #Command to check if any row is affected
    #If zero row is affected that means the row doesn't exist
    if command_handler.rowcount <= 0:
        print("Invalid Login")
    else:
        student_session(username)

        

#Function for Authentication of Teacher
def auth_teacher():
    print("")
    print("Teacher Login")
    print("")
    username = input(str("Usename : "))
    password = input(str("Password : "))

    query_vals = (username, password)

    #To run command
    command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND privilege = 'teacher'", query_vals)

    #Command to check if any row is affected
    #If zero row is affected that means the row doesn't exist
    if command_handler.rowcount <= 0:
        print("Login not Recognized")
    else:
        teacher_session()


#Function for Authentication of Admin
def auth_admin():
    print("")
    print("Admin Login")
    print("")
    username = input(str("Usename : "))
    password = input(str("Password : "))

    #Checking the username and password
    if username == "admin":
        if password == "password":
            admin_session()
        else:
            print("Incorrect Password")
    else:
        print("Login details incorrect")

 


#Main Function
def main():
    while(1):
        print("Welcome to the College System")
        print("")
        print("1. Login as Student")
        print("2. Login as Teacher ")
        print("3. Login as Admin")


        #To take option from User
        user_option = input(str("Option: "))

        if user_option == "1":
            #To check the authentication of Student
            auth_student()

        elif user_option == "2":
            #To check the authentication of Teacher
            auth_teacher()

        elif user_option == "3":
            #To check the authentication of Admin
            auth_admin()
            
        else:
            print("Invalid Option")


#Run the main function
main()







#Database Management System Project
#Name: Laxmi Rani Das
#Roll: MUH1801023F
