# Team Purple
# Title: InCollege Epic #1
# Description: Basic features for InCollege
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

    # Asking for first name and last name
    first_name = input("First Name: ")
    last_name = input("Last Name: ")

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
    else:
        # Password meets requirements, create account if password is confirmed
        confirm_password = input("Confirm Password: ")
        if password == confirm_password:
            # Open file for append, write username, password, first name, and last name to file
            with open("accounts.txt", "a") as file2:
                file2.write('\n' + username + " " + password + " " + first_name + " " + last_name)
            print("\nAccount created successfully!")
            member_options()
        else:
            print("\nPasswords do not match. Please try again.")
            create_account()
    return   



def user_login():

  # Display college student success story
    print("\nWelcome to InCollege!")
    print("Here's a success story from one of our college students:")
    print("Jane Doe, a student at University of South Florida, used InCollege to find her dream job at ABC Company. ")
    print("She credits InCollege for helping her build her professional network and discover job opportunities.")
    
    # Prompt user to watch a video
    choice = input("\nWould you like to watch a video about InCollege? (yes/no): ")
    if choice.lower() == "yes":
        print("\nVideo is now playing.")
        # Code to play the video goes here
    else:
        print("You can explore InCollege features further by signing in or creating an account.")

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





def job_search():
  # Output message to user
  print("\nunder construction")
  return



def find_someone():
  # Output message to user
  print("\nunder construction")
  return



def learn_skill():
  # Output message to user
  print("\nPlease select an option from the menu below:")
  print("1. Communication")
  print("2. Leadership")
  print("3. Time Management")
  print("4. Critical Thinking")
  print("5. Creaivity")
  print("6. Return to previous menu")
  choice = input("Selection: ")
  if choice == "6":
    member_options()
    return
  print("\nunder construction")
  return

  

def member_options():
  # Output messages to user and take input
  print("\nPlease select an option from the menu below:\n")
  print("1. Search for a job/internship")
  print("2. Find someone you know")
  print("3. Learn a new skill")
  print("4. Exit")
  choice = input("Enter your choice: ")
  # Check if choice is valid
  if choice == "1":
    print("\nYou have selected to search for a job.\n")
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
  # Output messages to user and get user input
  print("Welcome to InCollege!\n")
  print("Please select one of the following options:")
  print("1. Create a New InCollege Account")
  print("2. Login to an Existing InCollege Account")
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
  else:
    print("Invalid selection. Please try again.\n")
    user_display()



def main():
  user_display()


if __name__ == "__main__":
  main()
