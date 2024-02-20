# Team Purple
# Title: InCollege Epic #1
# Description: Basic features for InCollege
import csv
import os

def passwordCheck(username, password):
    if len(password) < 8 or len(password) > 12:
        print("\nPassword must be between 8 and 12 characters long.")
        print("Please try again.")
        createAccount()
    elif not any(char.isdigit() for char in password):
        print("\nPassword must contain at least one digit.")
        print("Please try again.")
        createAccount()
    elif not any(char.isupper() for char in password):
        print("\nPassword must contain at least one uppercase letter.")
        print("Please try again.")
        createAccount()
    elif not any(not char.isalnum() for char in password):
        print("\nPassword must contain at least one special character.")
        print("Please try again.")
        createAccount()
    elif " " in password:
      print("\nPassword cannot contain a space.")
      print("Please try again.")
      createAccount()
    else:
        # Password meets requirements, get first and last name, then create account
        print("\nPassword Accepted!")
        firstName = input("\nFirst Name: ")
        lastName = input("Last Name: ")
        # Open file for append, write username, password, first name, and last name to file
        with open("accounts.txt", "a") as file2:
            file2.write('\n' + username + " " + password + " " + firstName + " " + lastName)
        print("\nAccount created successfully!")
   

def createAccount():
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
                createAccount()
                return
            elif numUsers == 7:
                print("\nAll permitted accounts have been created, please come back later")
                exit()
    print("\nUsername is Available!\n")

    # Output messages to user and take password input
    print("(password must be a minimum of 8 characters, maximum of 12 characters, contain"
          " at least one uppercase letter, one digit, and one special character)")
    password = input("Password: ")

    # Checking if password meets requirements
    passwordCheck(username, password)
    userLogin()
    return


def userLogin():
    # Output messages to user and take username input
    print("\nPlease enter your username and password to login.\n")
    username = input("Username: ")
    password = input("Password: ")
    combo = username + " " + password
    # Open file for read, check for existing username and password
    with open("accounts.txt", "r") as file3:
        for line in file3:
            n = len(combo)
            if combo in line[0:n+1]:
                print("\nYou have successfully logged in!")
                memberOptions()
                return username, password
    print("Incorrect username / password, please try again.")
    userLogin()


# This function is used at main login screen to search for an existing InCollege Member
def connectWithSomeone():
    # Output message to user & take input
    print("\nYou selected to Find Someone You Know! \n\nPlease enter their name below.")
    firstName = input("First Name: ")
    lastName = input("Last Name: ")
    # Open file for read, check for existing username and password
    with open("accounts.txt", "r") as file4:
      for line in file4:
        if firstName + " " + lastName in line:
          print("\nThey are a part of the InCollege system!")
          print("\nPlease join InCollege with one of the following options below: ")
          print("1. Login to an Existing InCollege Account")
          print("2. Sign up and join " + firstName + " " + lastName + "!")
          print("3. Return to previous menu")
          selection = input("Selection: ")
          if selection == "1":
            userLogin()
          elif selection == "2":
            createAccount()
          elif selection == "3":
            userDisplay()
          else:
            print("\nInvalid selection, please try again.")
            connectWithSomeone()
          return
    print("\nThey are not yet a part of the InCollege system yet.\n")
    userDisplay()
    return


# This function is used for all job features in InCollege
def jobSearch():
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
        jobSearch()
      # Output messages to user and take input
      print("\nPlease enter the following information to post a job.\n")
      title = input("Job Title: ")
      description = input("Job Description: ")
      employer = input("Employer: ")
      location = input("Location: ")
      try: 
          salary = int(input("Salary: "))
      except ValueError:
          print("invalid input, enter a number")
          jobSearch()
      creator = input("Username; ")
      jobEntry = [title, description, employer, location, salary, creator]

      # Open file for append, write job information to file
      with open("InCollege_Jobs.csv", "a") as file5:
        writer = csv.writer(file5)
        writer.writerow(jobEntry)

      print("\nJob posted successfully!")
      jobSearch()
    elif selection == "2":
      # Return to previous menu
      memberOptions()
    else:
      print("\nInvalid choice. Please try again.")
      jobSearch()


def findSomeone():
    # Output message to user
    print("\nunder construction")
    memberOptions()
    return


def learnSkill():
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
        memberOptions()
        return
    print("\nunder construction")
    memberOptions()
    return

def useful_links():
    print("\nUseful Links:")
    print("1. General")
    print("2. Browse InCollege")
    print("3. Business Solutions")
    print("4. Directories")
    selection = input("Selection: ")

    if selection == "1":
        print("\nGeneral:")
        print("1. Sign Up")
        print("2. Help Center")
        print("3. About")
        print("4. Press")
        print("5. Blog")
        print("6. Careers")
        print("7. Developers")
        option = input("Selection: ")
        if option == "1":
            createAccount()
        elif option == "2":
            print("\nWe're here to help.")
        elif option == "3":
            print("\nIn College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide.")
        elif option == "4":
            print("\nIn College Pressroom: Stay on top of the latest news, updates, and reports.")
        elif option in ["5", "6", "7"]:
            print("\nUnder construction.")
        else:
            print("\nInvalid selection.")
        useful_links()
    elif selection in ["2", "3", "4"]:
        print("\nUnder construction.")
        useful_links()
    else:
        print("\nInvalid selection.")


def importantLinks():
    print("\n1. Copyright Notice")
    print("2. About")
    print("3. Accessibility")
    print("4. User Agreement")
    print("5. Privacy Policy")
    print("6. Cookie Policy")
    print("7. Copyright Policy")
    print("8. Brand Policy")
    print("9. Guest Controls")
    print("10. Languages")
    print("11. Go back")

    while True:
        choice = input("Enter your choice (1-11): ")

        if choice == '1':
            print("\nCopyright Notice: InCollege acknowledges and respects the intellectual property rights of individuals and entities. As a user of InCollege, you are expected to adhere to our copyright notice, which delineates the rights and privileges associated with the content hosted on our platform. Our copyright notice encompasses a wide array of creative works, including but not limited to text, images, videos, and graphics. Any unauthorized reproduction, distribution, or modification of content without explicit consent from the copyright holder is strictly prohibited and may result in legal consequences. We strive to foster an environment that upholds the principles of intellectual property protection and encourages responsible content sharing practices.\n")
            secondChoice = input("\nOptions\n1. Go back: ")
            if secondChoice == '1':
                importantLinks()
            else:
                print("Invalid Choice")
                break

        elif choice == '2':
            print("\nAbout: InCollege, established in 2024, stands as a premier professional networking platform dedicated to empowering individuals in their pursuit of career advancement and personal growth. Our platform serves as a dynamic hub where students, alumni, and professionals converge to cultivate meaningful connections, foster mentorship opportunities, and explore avenues for professional development. Rooted in a commitment to excellence, InCollege endeavors to facilitate transformative experiences that transcend traditional networking paradigms. By providing a multifaceted ecosystem of resources, insights, and networking opportunities, InCollege seeks to equip its users with the tools and support necessary to navigate and thrive in today's competitive professional landscape.\n")
            secondChoice = input("\nOptions\n1. Go back: ")
            if secondChoice == '1':
                importantLinks()
            else:
                print("Invalid Choice")
                break

        elif choice == '3':
            print("\nAccessibility: At InCollege, we firmly believe in the fundamental principle of inclusivity and are dedicated to ensuring that our platform remains accessible to all individuals, regardless of disability or impairment. Our commitment to accessibility is manifested through the implementation of a comprehensive suite of features and functionalities designed to accommodate diverse user needs. From intuitive interface design to robust assistive technologies, such as screen readers and keyboard navigation, InCollege endeavors to create an inclusive digital environment that fosters equitable participation and engagement for all users. We recognize the importance of accessibility as a cornerstone of our platform's ethos and remain steadfast in our pursuit of excellence in this regard.\n")
            secondChoice = input("\nOptions\n1. Go back: ")
            if secondChoice == '1':
                importantLinks()
            else:
                print("Invalid Choice")
                break

        elif choice == '4':
            print("\nUser Agreement: InCollege's user agreement serves as the cornerstone of our platform's operational framework, delineating the terms and conditions that govern user interactions and engagements within our ecosystem. By accessing or utilizing InCollege's services, you are expressly consenting to abide by the stipulations outlined in our user agreement. This comprehensive document encompasses a myriad of provisions, ranging from user rights and responsibilities to guidelines for acceptable usage and conduct. Through adherence to our user agreement, InCollege seeks to foster a cohesive and mutually beneficial community characterized by respect, integrity, and collaboration. We encourage all users to familiarize themselves with the contents of our user agreement and to approach their interactions on our platform with diligence and mindfulness.\n")
            secondChoice = input("\nOptions\n1. Go back: ")
            if secondChoice == '1':
                importantLinks()
            else:
                print("Invalid Choice")
                break

        elif choice == '5':
            print("\nPrivacy Policy: InCollege is deeply committed to safeguarding the privacy and confidentiality of its users' personal information. Our privacy policy articulates the principles and practices that govern the collection, usage, and protection of user data within our platform. Rooted in principles of transparency, accountability, and user empowerment, our privacy policy serves as a testament to our unwavering dedication to maintaining the trust and confidence of our user community. Whether you are navigating our website, engaging with our services, or participating in our community forums, rest assured that your privacy rights are of paramount importance to us. We invite you to peruse our privacy policy to gain a comprehensive understanding of how we handle and protect your personal information.\n")
            secondChoice = input("\nOptions\n1. Go back: ")
            if secondChoice == '1':
                importantLinks()
            else:
                print("Invalid Choice")
                break

        elif choice == '6':
            print("\nCookie Policy: InCollege's cookie policy elucidates the manner in which we utilize cookies and similar technologies to enhance user experience and optimize the functionality of our platform. Cookies, small text files stored on your device, serve as invaluable tools that enable us to deliver personalized content, analyze user behavior, and improve overall website performance. Our cookie policy provides detailed insights into the types of cookies utilized, their respective purposes, and the mechanisms through which users can manage their cookie preferences. By consenting to the use of cookies in accordance with our policy, users can enjoy a more tailored and seamless browsing experience on InCollege.\n")
            secondChoice = input("\nOptions\n1. Go back: ")
            if secondChoice == '1':
                importantLinks()
            else:
                print("Invalid Choice")
                break

        elif choice == '7':
            print("\nCopyright Policy: InCollege remains steadfast in its commitment to upholding the principles of intellectual property rights and recognizes the importance of addressing copyright infringement in a timely and effective manner. Our copyright policy outlines the procedures and protocols governing the submission and resolution of copyright infringement claims within our platform. As a responsible digital entity, InCollege is dedicated to facilitating a robust framework for copyright enforcement that prioritizes fairness, accountability, and due process. Users are encouraged to familiarize themselves with the provisions outlined in our copyright policy and to engage in responsible content sharing practices that respect the intellectual property rights of others.\n")
            secondChoice = input("\nOptions\n1. Go back: ")
            if secondChoice == '1':
                importantLinks()
            else:
                print("Invalid Choice")
                break

        elif choice == '8':
            print("\nBrand Policy: InCollege's brand policy serves as a comprehensive guidebook for the proper usage and representation of our brand assets, including logos, trademarks, and brand colors. Upholding the integrity and consistency of our brand identity is of paramount importance to us, and our brand policy endeavors to provide clear and concise directives for brand usage across various contexts and mediums. Whether you are a user, partner, or affiliate of InCollege, adherence to our brand policy ensures that our brand is represented in a manner that is cohesive, professional, and reflective of our core values and mission. We invite you to review our brand policy and to join us in upholding the integrity of the InCollege brand.\n")
            secondChoice = input("\nOptions\n1. Go back: ")
            if secondChoice == '1':
                importantLinks()
            else:
                print("Invalid Choice")
                break

        elif choice == '9':
            print("\nGuest Controls: InCollege's guest controls empower users to customize and personalize their browsing experience within our platform. Whether you are exploring career opportunities, networking with peers, or accessing educational resources, our guest controls afford you the flexibility to tailor your preferences and settings to align with your unique needs and preferences. From managing visibility settings to configuring notification preferences, our intuitive guest controls interface offers a seamless and intuitive user experience that puts you in control of your InCollege journey. We invite you to leverage the power of guest controls to enhance your browsing experience and maximize your engagement within our platform.\n")
            secondChoice = input("\nOptions\n1. Go back: ")
            if secondChoice == '1':
                importantLinks()
            else:
                print("Invalid Choice")
                break

        elif choice == '10':
            print("\nLanguages: InCollege supports multiple languages to accommodate users from diverse linguistic backgrounds. Select your preferred language to view our website and content in your native language, ensuring a seamless browsing experience for all users.")
            secondChoice = input("\nOptions\n1. Go back: ")
            if secondChoice == '1':
                importantLinks()
            else:
                print("Invalid Choice")
                break

        elif choice == '11':
            print("\nYou selected: Go back")
            userDisplay()
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 11.")





def memberOptions():
    # Output messages to user and take input
    print("\nPlease select an option from the menu below: ")
    print("1. Job/Internship opportunities")
    print("2. Find someone you know")
    print("3. Learn a new skill")
    print("4. Useful Links")
    print("5. InCollege Important Links")
    print("6. Exit")
    choice = input("Enter your choice: ")
    # Check if choice is valid
    if choice == "1":
        print("\nYou have selected to search for a job.")
        jobSearch()
    elif choice == "2":
        print("\nYou have selected to find someone you know.")
        findSomeone()
    elif choice == "3":
        print("\nYou have selected to learn a new skill.")
        learnSkill()
    elif choice == "4":
        print("\nYou have selected Useful Links.")
        useful_links()
    elif choice == "5":
        print("\nYou have selected InCollege Important Links.\n")
        importantLinks()
    elif choice == "6":
        print("\nYou have selected to exit.")
        exit()
    else:
        print("\nInvalid choice. Please try again.")
        memberOptions()



def userDisplay():
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
    print("5. Useful Links")
    print("6. InCollege Important Links")
    print("7. Exit")
    selection = input("Selection: ")

    # Check which selection was made by the user
    if selection == "1":
        if not os.path.exists("accounts.txt"):
            with open("accounts.txt", "w"):
                pass
        createAccount()
    elif selection == "2":
        if not os.path.exists("accounts.txt"):
            with open("accounts.txt", "w"):
                pass
        userLogin()
    elif selection == "3":
        connectWithSomeone()
    elif selection == "4":
        print("\nVideo is now playing.\n")
        print("Please select one of the following options:")
        print("1. Return to main menu")
        selection = input("Selection: ")
        userDisplay()
    elif selection == "5":
        print("\nYou have selected Useful Links.")
        useful_links()
    elif selection == "6":
       print("\nYou have Selected InCollege Important Links.\n")
       importantLinks()
    elif selection == "7":
        exit()
    else:
        print("Invalid selection. Please try again.\n")
        userDisplay()



def main():
    userDisplay()


if __name__ == "__main__":
    main()
