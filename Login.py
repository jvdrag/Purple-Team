# Team Purple
# Title: InCollege Epic #1
# Description: Basic features for InCollege
import csv
import os



def create_account():
    # Output messages to user and take username input
    print("\nPlease enter the following information to create an account.\n")
    username = input("Username: ")

    # Open file for read, check for existing username and number of users
    numUsers = 1
    with open("accounts.txt", "r+") as file1:
        for line in file1:
            numUsers += 1
            if username in line:
                print("\nUsername already exists. Please try again.")
                create_account()
                return
            elif numUsers == 6:
                print("\nAll permitted accounts have been created, please come back later")
                exit()
    print("\nUsername is Available!\n")

    # Output messages to user and take password input
    print("(password must be a minimum of 8 characters, maximum of 12 characters, contain"
          " at least one uppercase letter, one digit, and one special character)")
    password = input("Password: ")

    # Checking if password meets requirements
    if len(password) < 8 or len(password) > 12:
        print("\nPassword must be between 8 and 12 characters long.")
        print("Please try again.")
        create_account()
    elif not any(char.isdigit() for char in password):
        print("\nPassword must contain at least one digit.")
        print("Please try again.")
        create_account()
    elif not any(char.isupper() for char in password):
        print("\nPassword must contain at least one uppercase letter.")
        print("Please try again.")
        create_account()
    elif not any(not char.isalnum() for char in password):
        print("\nPassword must contain at least one special character.")
        print("Please try again.")
        create_account()
    elif " " in password:
      print("\nPassword cannot contain a space.")
      print("Please try again.")
      create_account()
    else:
        # Password meets requirements, get first and last name, then create account
        first_name = input("\nFirst Name: ")
        last_name = input("Last Name: ")
        # Open file for append, write username, password, first name, and last name to file
        with open("accounts.txt", "a") as file2:
            file2.write('\n' + username + " " + password + " " + first_name + " " + last_name)
        print("\nAccount created successfully!")
        member_options()
    return



def user_login():
    # Output messages to user and take username input
    print("\nPlease enter your username and password to login.\n")
    username = input("Username: ")
    password = input("Password: ")
    combo = username + " " + password
    # Open file for read, check for existing username and password
    with open("accounts.txt", "r") as file3:
        for line in file3:
            if combo in line:
                print("\nYou have successfully logged in!")
                member_options()
                return
    print("Incorrect username / password, please try again.")
    user_login()



# This function is used at main login screen to search for an existing InCollege Member
def connect_with_someone():
    # Output message to user & take input
    print("\nYou selected to Find Someone You Know! \n\nPlease enter their name below.")
    firstName = input("First Name: ")
    lastName = input("Last Name: ")
    # Open file for read, check for existing username and password
    with open("accounts.txt", "r") as file4:
      for line in file4:
        if firstName + " " + lastName in line:
          print("\nThey are a part of the InCollege system.")
          print("\nPlease join InCollege with one of the following options below: ")
          print("1. Login to an Existing InCollege Account")
          print("2. Sign up and join " + firstName + " " + lastName + "!")
          print("3. Return to previous menu")
          selection = input("Selection: ")
          if selection == "1":
            user_login()
          elif selection == "2":
            create_account()
          elif selection == "3":
            user_display()
          else:
            print("\nInvalid selection, please try again.")
            connect_with_someone()
          return
    print("\nThey are not yet a part of the InCollege system yet.\n")
    user_display()
    return



# This function is used for all job features in InCollege
def job_search():
    # Checks if jobs file exists, creates it if not
    if not os.path.exists("InCollege_Jobs.csv"):
      with open("InCollege_Jobs.csv", "a") as file4:
        # Field names for the CSV header
        fieldnames = ['Title', 'Description', 'Employer', 'Location', 'Salary', 'Creator']
        # Write the header row
        writer = csv.writer(file4)
        writer.writerow(fieldnames)
  
    # Output menu to user and take input
    print("\nPlease select an option from the menu below:")
    print("1. Post a job")
    print("2. Return to previous menu")
    selection = input("Selection: ")
  
    # Check user's selection
    if selection == "1":
      # Check current number of jobs, MAX = 5, deny if full
      numJobs = 1
      with open("InCollege_Jobs.csv", "r") as file5:
        for line in file5:
          numJobs += 1
      if numJobs == 7:
        print("\nMaximum number of jobs reached, please come back later.")
        job_search()
      # Output messages to user and take input
      print("\nPlease enter the following information to post a job.\n")
      title = input("Job Title: ")
      description = input("Job Description: ")
      employer = input("Employer: ")
      location = input("Location: ")
      salary = input("Salary: ")
      creator = input("Username: ")
      jobEntry = [title, description, employer, location, salary, creator]

      # Open file for append, write job information to file
      with open("InCollege_Jobs.csv", "a") as file5:
        writer = csv.writer(file5)
        writer.writerow(jobEntry)

      print("\nJob posted successfully!")
      job_search()
    elif selection == "2":
      # Return to previous menu
      member_options()
    else:
      print("\nInvalid choice. Please try again.")
      job_search()


def find_someone():
    # Output message to user
    print("\nunder construction")
    member_options()
    return



def learn_skill():
    # Output message to user
    print("\nPlease select an option from the menu below:")
    print("1. Communication")
    print("2. Leadership")
    print("3. Time Management")
    print("4. Critical Thinking")
    print("5. Creativity")
    print("6. Return to previous menu")
    choice = input("Selection: ")
    if choice == "6":
        member_options()
        return
    print("\nunder construction")
    member_options()
    return



def member_options():
    # Output messages to user and take input
    print("\nPlease select an option from the menu below: ")
    print("1. Job/Internship opportunities")
    print("2. Find someone you know")
    print("3. Learn a new skill")
    print("4. Exit")
    choice = input("Enter your choice: ")
    # Check if choice is valid
    if choice == "1":
        print("\nYou have selected to search for a job.")
        job_search()
    elif choice == "2":
        print("\nYou have selected to find someone you know.")
        find_someone()
    elif choice == "3":
        print("\nYou have selected to learn a new skill.")
        learn_skill()
    elif choice == "4":
        print("\nYou have selected to exit.")
        exit()
    else:
        print("\nInvalid choice. Please try again.")
        member_options()



def user_display():
    # Display college student success story
    print("\nWelcome to InCollege!\n")
    print("Here's a success story from one of our InCollege members -")
    print("Jane Doe, a student at University of South Florida, used InCollege to find her dream job at ABC Company. ")
    print("She credits InCollege for helping her build her professional network and discover job opportunities.")
  
    # Output messages to user and get user input
    print("\nPlease select one of the following options:")
    print("1. Create a New InCollege Account")
    print("2. Login to an Existing InCollege Account")
    print("3. Connect with an existing member")
    print("4. Watch InCollege introduction video")
    print("5. Exit")
    selection = input("Selection: ")

    # Check which selection was made by the user
    if selection == "1":
        if not os.path.exists("accounts.txt"):
            with open("accounts.txt", "w"):
                pass
        create_account()
    elif selection == "2":
        if not os.path.exists("accounts.txt"):
            with open("accounts.txt", "w"):
                pass
        user_login()
    elif selection == "3":
        connect_with_someone()
    elif selection == "4":
        print("\nVideo is now playing.\n")
        print("Please select one of the following options:")
        print("1. Return to main menu")
        selection = input("Selection: ")
        user_display()
    elif selection == "5":
        exit()
    else:
        print("Invalid selection. Please try again.\n")
        user_display()



def main():
    user_display()


if __name__ == "__main__":
    main()

