import csv
import os
import sqlite3


class UserAccountManager:
    def __init__(self, db_name='user_accounts.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.createUsersTable()
        self.createFriendsTable()
        self.createJobsTable()
        self.createJobApplicationTable()
        self.logged_in_username = None

    def createUsersTable(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                username TEXT PRIMARY KEY,
                                password TEXT,
                                firstname TEXT,
                                lastname TEXT,
                                university TEXT,
                                major TEXT
                            )''')
        self.conn.commit()

    def createFriendsTable(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS friends (
                                user_id TEXT,
                                friend_id TEXT,
                                FOREIGN KEY (user_id) REFERENCES users(username),
                                FOREIGN KEY (friend_id) REFERENCES users(username)
                            )''')
        self.conn.commit()

    def createJobsTable(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
                                job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT,
                                description TEXT,
                                employer TEXT,
                                location TEXT,
                                salary TEXT,
                                creator_username TEXT,
                                FOREIGN KEY (creator_username) REFERENCES users(username)
                            )''')
        self.conn.commit()

    def createJobApplicationTable(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS job_applications (
                                job_title TEXT,
                                applicant_username TEXT,
                                graduation_date TEXT,
                                start_date TEXT,
                                why_fit TEXT
                            )''')
        self.conn.commit()

    def createAccount(self):
        if self.TableFull():
            print("\nTable contains 10 records, cannot add more\n")
            self.userDisplay()
            return
        print("\nPlease enter the following information to create an account.\n")
        username = input("Username: ")
        if self.usernameExists(username):
            print("\nUsername already exists. Please try again.")
            self.createAccount()
            return
        password = self.passwordCheck()
        firstname = input("\nFirst Name: ")
        lastname = input("Last Name: ")
        university = input("University: ")
        major = input("Major: ")
        self.cursor.execute("INSERT INTO users (username, password, firstname, lastname, university, major) VALUES (?, ?, ?, ?, ?, ?)",
                            (username, password, firstname, lastname, university, major))
        self.conn.commit()
        print("\nAccount created successfully!")
        self.userLogin()

    def usernameExists(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        return self.cursor.fetchone() is not None

    def TableFull(self):
        self.cursor.execute("SELECT COUNT(*) FROM users")
        rowcount = self.cursor.fetchone()
        if rowcount[0] > 9:
            return True
        else:
            return False

    def passwordCheck(self):
        password = input("Password: ")
        if len(password) < 8 or len(password) > 12:
            print("\nPassword must be between 8 and 12 characters long.")
            print("Please try again.")
            return self.passwordCheck()
        elif not any(char.isdigit() for char in password):
            print("\nPassword must contain at least one digit.")
            print("Please try again.")
            return self.passwordCheck()
        elif not any(char.isupper() for char in password):
            print("\nPassword must contain at least one uppercase letter.")
            print("Please try again.")
            return self.passwordCheck()
        elif not any(not char.isalnum() for char in password):
            print("\nPassword must contain at least one special character.")
            print("Please try again.")
            return self.passwordCheck()
        elif " " in password:
            print("\nPassword cannot contain a space.")
            print("Please try again.")
            return self.passwordCheck()
        else:
            print("\nPassword Accepted!")
            return password

    def accept_friend_request(self,receiver,sender):
        self.cursor.execute("SELECT * FROM friends WHERE user_id=?", (receiver,))
        receiver_friends = self.cursor.fetchall()
        if sender not in receiver_friends:
            self.cursor.execute("INSERT INTO friends (user_id,friend_id) VALUES (?,?)", (receiver,sender))
            self.conn.commit()
            print("Friend added!")

    def reject_friend_request(self,receiver,sender):
        self.cursor.execute("DELETE FROM friends WHERE user_id = ? AND friend_id = ?",(sender,receiver))
        self.cursor.execute("DELETE FROM friends WHERE user_id = ? AND friend_id = ?",(receiver,sender))
        self.conn.commit()
        print(f"friend request from {sender} rejected")

    def remove_friend(self,receiver,sender):
        self.cursor.execute("DELETE FROM friends WHERE user_id = ? AND friend_id = ?",(sender,receiver))
        self.cursor.execute("DELETE FROM friends WHERE user_id = ? AND friend_id = ?",(receiver,sender))
        self.conn.commit()
        print(f"{sender} was removed from your friends list")

    def userLogin(self):
        username = input("\nUsername: ")
        if not self.usernameExists(username):
            print("Username does not exist. Try again.")
            self.userLogin()

        password = input("Password: ")
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = self.cursor.fetchone()
        if user:
            print("\nYou have successfully logged in!")

            # Check for pending friend requests
            self.cursor.execute("SELECT user_id FROM friends WHERE friend_id=?", (username,))
            pending_requests = self.cursor.fetchall()

            if pending_requests:
                print("You have friend requests!")
                for i in pending_requests:
                    print("Pending friend request from", i[0])  # Access the sender's username using i[0]
                    ans = input("Do you accept? Enter Y or N: ")
                    if ans.lower() == "y":
                        self.accept_friend_request(username, i[0])  # Pass the logged-in user's username and sender's username
                        self.cursor.execute("DELETE FROM friends WHERE user_id=? AND friend_id=?", (i[0], username))
                    else:
                        self.reject_friend_request(username, i[0])  # Pass the logged-in user's username and sender's username
                        self.cursor.execute("DELETE FROM friends WHERE user_id=? AND friend_id=?", (i[0], username))
                self.conn.commit()  # Commit changes to the database

            self.logged_in_username = username
            self.memberOptions()
        else:
            print("Incorrect username / password, please try again.")
            self.userLogin()

    def connectWithSomeone(self):
        print("\nYou selected to Find Someone You Know!\n\nPlease enter their name below.")
        firstName = input("First Name: ")
        lastName = input("Last Name: ")

        self.cursor.execute("SELECT * FROM users WHERE firstname=? AND lastname=?", (firstName, lastName))
        match = self.cursor.fetchone()

        if match:
            print("\nThey are a part of the InCollege system!")
            print("\nPlease join InCollege with one of the following options below: ")
            print("1. Login to an Existing InCollege Account")
            print("2. Sign up and join " + firstName + " " + lastName + "!")
            print("3. Return to previous menu")
            selection = input("Selection: ")
            if selection == "1":
                self.userLogin()
            elif selection == "2":
                self.createAccount()
            elif selection == "3":
                self.userDisplay()
            else:
                print("\nInvalid selection, please try again.")
                self.connectWithSomeone()                    
            return
        print("\nThey are not yet a part of the InCollege system yet.\n")
        self.userDisplay()
        return

    def memberOptions(self):
        print("\nPlease select an option from the menu below: ")
        print("1. Job/Internship opportunities")
        print("2. Friends")
        print("3. Learn a new skill")
        print("4. Create your profile")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            print("\nYou have selected to search for a job/internship.")
            self.jobSearch()
        elif choice == "2":
            print("\nYou have selected Friends.")
            self.friends()
        elif choice == "3":
            print("\nYou have selected to learn a new skill.")
            self.learnSkill()
        elif choice == "4":
            print("\nYou have selected to create your profile.")
            self.createProfile()
        elif choice == "5":
            print("\nYou have selected to exit.")
            exit()
        else:
            print("\nInvalid choice. Please try again.")
            self.memberOptions()

    def createProfile(self):
      user_id = self.logged_in_username
      current_profile = self.getProfile(user_id)

      print("Create or update your profile")
      title = input("Enter a line of text for your title (leave blank to keep existing): ")
      title = title or current_profile.get('Title', '')


      major = input("Enter your major (leave blank to keep existing): ")
      major = ' '.join(word.capitalize() for word in (major or current_profile.get('Major', '')).split())

      university = input("Enter your university (leave blank to keep existing): ")
      university = ' '.join(word.capitalize() for word in (university or current_profile.get('University', '')).split())

      about = input("Share about yourself for your profile's About section (leave blank to keep existing): ")
      about = about or current_profile.get('About', '')

      school_name = input("Enter your school's name (leave blank to keep existing): ")
      school_name = school_name or current_profile.get('School', '')

      degree = input("Enter the degree (leave blank to keep existing): ")
      degree = degree or current_profile.get('Degree', '')

      years_attended = input("Enter the number of years attended (leave blank to keep existing): ")
      years_attended = years_attended if years_attended else str(current_profile.get('Years_attended', ''))


      experiences = current_profile.get('Experiences', [])
      for i in range(1, 4):  
          print(f"Enter details for past job {i} (leave blank to skip):")
          title = input("Job title: ")
          employer = input("Employer: ")
          date_started = input("Date started: ")
          date_ended = input("Date ended: ")
          location = input("Location: ")
          description = input("Job description: ")

          if any([title, employer, date_started, date_ended, location, description]): 
              experiences.append([title, employer, date_started, date_ended, location, description])
              if len(experiences) >= 3:  
                  break

      profile_entry = [user_id, title, major, university, about, school_name, degree, years_attended, experiences]
      self.updateProfileCSV(profile_entry)


      updated_profile = self.getProfile(user_id)
      print("\nYour updated profile:")
      print(f"Title: {updated_profile.get('Title', 'Not set')}")
      print(f"Major: {updated_profile.get('Major', 'Not set')}")
      print(f"University: {updated_profile.get('University', 'Not set')}")
      print(f"About: {updated_profile.get('About', 'Not set')}")
      print(f"School Name: {updated_profile.get('School', 'Not set')}")
      print(f"Degree: {updated_profile.get('Degree', 'Not set')}")
      print(f"Years Attended: {updated_profile.get('Years_attended', 'Not set')}")
      # Print experiences
      if 'Experiences' in updated_profile:
          for i, experience in enumerate(updated_profile['Experiences'], start=1):
              print(f"\nExperience {i}:")
              print(f"Job Title: {experience[0]}, Employer: {experience[1]}, Dates: {experience[2]} - {experience[3]}, Location: {experience[4]}, Description: {experience[5]}")

      self.memberOptions()

    def updateProfileCSV(self, profile_entry):
      with open("Profiles.csv", "a+", newline='') as pf:
          pf.seek(0)
          existing_entries = list(csv.reader(pf))
          writer = csv.writer(pf)

          updated = False
          for i, entry in enumerate(existing_entries):
              if entry and entry[0] == profile_entry[0]:  
                  existing_entries[i] = profile_entry
                  updated = True
                  break
          if updated:
              pf.truncate(0)  # Clear file
              writer.writerows(existing_entries)  
          else:
              writer.writerow(profile_entry) 

    def getProfile(self, user_id):
      if os.path.exists("Profiles.csv"):
          with open("Profiles.csv", "r") as pf:
              reader = csv.reader(pf)
              for row in reader:
                  if row and row[0] == user_id:
                      experiences = eval(row[8]) if len(row) > 8 and row[8] else []  
                      return {
                          'Title': row[1], 
                          'Major': row[2], 
                          'University': row[3], 
                          'About': row[4], 
                          'School': row[5], 
                          'Degree': row[6], 
                          'Years_attended': row[7],
                          'Experiences': experiences 
                      }
      return {}


    def jobSearch(self):
        # Output menu to user and take input
        print("\nPlease select an option from the menu below:")
        print("1. Post a job")
        print("2. View all jobs")
        print("3. View applied jobs")
        print("4. View unapplied jobs")
        print("5. Return to previous menu")
        selection = input("Selection: ")
        if selection == "1":
            print("\nPlease enter the following information to post a job.\n")
            title = input("Job Title: ")
            description = input("Job Description: ")
            employer = input("Employer: ")
            location = input("Location: ")
            salary = input("Salary: ")
            creator = self.logged_in_username  # Use the logged-in username as the creator
            self.cursor.execute("INSERT INTO jobs (title, description, employer, location, salary, creator_username) VALUES (?, ?, ?, ?, ?, ?)",
                              (title, description, employer, location, salary, creator))
            self.conn.commit()
            print("\nJob posted successfully!")
            self.jobSearch()
        elif selection == "2":
            # Fetch all jobs from the database
            self.cursor.execute("SELECT * FROM jobs")
            jobs = self.cursor.fetchall()

            print("\nList of all jobs:")
            for job in jobs:
                print(job[1])  # Output title of jobs
            self.viewJobDetails(jobs)
        elif selection == "3": # View applied jobs
            self.cursor.execute("SELECT * FROM job_applications WHERE applicant_username = ?", (self.logged_in_username,))
            applied_jobs = self.cursor.fetchall()
            print("\nList of applied jobs:")
            for job in applied_jobs:
                print(job[0])  # Output title of jobs
            self.jobSearch()
        elif selection == "4": # View unapplied jobs
            self.cursor.execute("SELECT * FROM jobs WHERE title NOT IN (SELECT job_title FROM job_applications WHERE applicant_username = ?)", (self.logged_in_username,))
            unapplied_jobs = self.cursor.fetchall()
            print("\nList of unapplied jobs:")
            for job in unapplied_jobs:
                print(job[1])  # Output title of jobs
            self.viewJobDetails(unapplied_jobs)
        elif selection == "5": # Return to previous menu
            self.memberOptions()
        else:
            print("\nInvalid choice. Please try again.")
            self.jobSearch()


    def viewJobDetails(self, jobs):
      selection = input("\nEnter the title of the job to view details (or type '1' to return to previous menu): ")
      if selection == "1":
          self.jobSearch()
      else:
          job_found = False
          for job in jobs:
              if job[1] == selection:
                  job_found = True
                  job_title = job[1]
                  print("\nJob Title:", job[1])
                  print("Description:", job[2])
                  print("Employer:", job[3])
                  print("Location:", job[4])
                  print("Salary:", job[5])
                        
                  # Check if the student has already applied for this job
                  canApply = True
                  self.cursor.execute("SELECT * FROM job_applications WHERE job_title = ? AND applicant_username = ?", (job_title, self.logged_in_username))
                  if self.cursor.fetchone():
                      print("You have applied for this job!")
                      canApply = False
                        
                  # Check if the student is the creator of the job
                  self.cursor.execute("SELECT creator_username FROM jobs WHERE title = ?", (job_title,))
                  creator_username = self.cursor.fetchone()[0]
                  if creator_username == self.logged_in_username:
                      print("You are the creator of this job!")
                      canApply = False
                        
                  if canApply:
                      print("You have not applied for this job.")
                      choice = input("Would you like to? (y/n): ")
                      if choice.lower() == "y":
                          graduation_date = input("Enter your graduation date (mm/dd/yyyy): ")
                          start_date = input("Enter the date you can start working (mm/dd/yyyy): ")
                          why_fit = input("Explain why you think you would be a good fit for this job: ")

                          # Insert application into the database
                          self.cursor.execute("INSERT INTO job_applications (job_title, applicant_username, graduation_date, start_date, why_fit) VALUES (?, ?, ?, ?, ?)",
                                              (job_title, self.logged_in_username, graduation_date, start_date, why_fit))
                          self.conn.commit()
                          print("\nApplication submitted successfully!")      
                  self.jobSearch()
          if not job_found:
              print("Job not found.")
              self.jobSearch()

                                 
    def friends(self):
        print("\n1. Show My Network")
        print("2. Add Friend")
        print("3. Go Back")
        choice = input("Enter Your Choice: ")
        if choice == '1':
            self.showFriends()
        elif choice == '2':
            self.addFriend()
        elif choice == '3':
            #self.pendingRequests()
            self.memberOptions()
        else:
            print("\nInvalid Choice!")
            self.memberOptions()
        return

    def searchUsers(self):
        print("\nYou selected to search for friends.")
        search_criteria = input("Enter the last name, university, or major of the person you are looking for: ")

        # Search for users based on last name, university, or major
        self.cursor.execute("SELECT username, firstname, lastname, university, major FROM users WHERE lastname=? OR university=? OR major=?", 
                            (search_criteria, search_criteria, search_criteria))
        matching_users = self.cursor.fetchall()

        if matching_users:
            print("\nMatching users:")
            for user in matching_users:
                username, firstname, lastname, university, major = user
                print("------------------------------------------------------------------------------------------------------------------")
                print(f"Username: {username} | Name: {firstname} {lastname} | University: {university} | Major: {major}\n")

        else:
            print("\nNo users found matching the criteria.")


    def addFriend(self):

        self.searchUsers()
        friend_username = input("Enter the username of the person you want to add as a friend: ")

        # Check if the entered username exists in the users table
        self.cursor.execute("SELECT * FROM users WHERE username=?", (friend_username,))
        friend = self.cursor.fetchone()

        if friend:
            # Insert a new row into the friends table for the current user
            print("A friend request was sent to", friend_username)
            self.cursor.execute("INSERT INTO friends (user_id, friend_id) VALUES (?, ?)", (self.logged_in_username, friend_username))

            # Insert a new row into the friends table for the friend
            #self.cursor.execute("INSERT INTO friends (user_id, friend_id) VALUES (?, ?)", (friend_username, self.logged_in_username))
            self.conn.commit()

            self.memberOptions()
        else:
            print(f"User with username '{friend_username}' does not exist.")
            self.friends()

    def showFriends(self):
      self.cursor.execute("SELECT username, firstname, lastname, university, major FROM users WHERE username IN (SELECT friend_id FROM friends WHERE user_id=?)", (self.logged_in_username,))
      friends_info = self.cursor.fetchall()

      if friends_info:
          print("\nYour Friends:")
          for friend_info in friends_info:
              username, firstname, lastname, university, major = friend_info
              print(f"Username: {username}, Name: {firstname} {lastname}, University: {university}, Major: {major}", end='')
              if self.getProfile(username):  
                  print(", Profile", end='')  
              print()  

          print("\n1. Go Back")
          print("2. Remove Friend")
          print("3. View Friend's Profile")
          choice = input("Selection: ")
          if choice == "1":
              self.memberOptions()
          elif choice == "2":
              friend_to_remove = input("\nEnter the username of the person you want to remove as a friend: ")
              self.remove_friend(self.logged_in_username, friend_to_remove)
          elif choice == "3":
              friend_to_view = input("\nEnter the username of the friend whose profile you want to view: ")
              self.viewFriendProfile(friend_to_view)
          else:
              print("Invalid Choice.")
              self.showFriends()
      else:
          print("\nNo friends.")
          self.memberOptions()
    def viewFriendProfile(self, friend_username):
      self.cursor.execute("SELECT * FROM friends WHERE user_id = ? AND friend_id = ?", (self.logged_in_username, friend_username))
      if self.cursor.fetchone():
          friend_profile = self.getProfile(friend_username)
          if friend_profile:
              print(f"\nProfile of {friend_username}:")
              for key, value in friend_profile.items():
                  print(f"{key}: {value}")
          else:
              print("\nThis friend has not created a profile yet.")
      else:
          print("\nYou are not friends with this user.")
      self.memberOptions()



    def learnSkill(self):
        print("\nPlease select an option from the menu below:")
        print("1. Communication")
        print("2. Leadership")
        print("3. Time Management")
        print("4. Critical Thinking")
        print("5. Creativity")
        print("6. Return to previous menu")
        choice = input("Selection: ")
        if choice == "6":
            self.memberOptions()
            return
        print("\nunder construction")
        self.memberOptions()

    def usefulLinks(self):
        print("\nUseful Links:")
        print("1. General")
        print("2. Browse InCollege")
        print("3. Business Solutions")
        print("4. Directories")
        print("5. Go Back")
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
            print("8. Go Back")
            option = input("Selection: ")
            if option == "1":
                self.createAccount()
            elif option == "2":
                print("\nWe're here to help.")
            elif option == "3":
                print("\nIn College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide.")
            elif option == "4":
                print("\nIn College Pressroom: Stay on top of the latest news, updates, and reports.")
            elif option in ["5", "6", "7"]:
                print("\nUnder construction.")
            elif option == "8":
                self.usefulLinks()
            else:
                print("\nInvalid selection.")
            self.usefulLinks()
        elif selection in ["2", "3", "4"]:
            print("\nUnder construction.")
            self.usefulLinks()
        elif selection == "5":
            self.userDisplay()
        else:
            print("\nInvalid selection.")

    def importantLinks(self):
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
                    self.importantLinks()
                else:
                    print("Invalid Choice")
                    break

            elif choice == '2':
                print("\nAbout: InCollege, established in 2024, stands as a premier professional networking platform dedicated to empowering individuals in their pursuit of career advancement and personal growth. Our platform serves as a dynamic hub where students, alumni, and professionals converge to cultivate meaningful connections, foster mentorship opportunities, and explore avenues for professional development. Rooted in a commitment to excellence, InCollege endeavors to facilitate transformative experiences that transcend traditional networking paradigms. By providing a multifaceted ecosystem of resources, insights, and networking opportunities, InCollege seeks to equip its users with the tools and support necessary to navigate and thrive in today's competitive professional landscape.\n")
                secondChoice = input("\nOptions\n1. Go back: ")
                if secondChoice == '1':
                    self.importantLinks()
                else:
                    print("Invalid Choice")
                    break

            elif choice == '3':
                print("\nAccessibility: At InCollege, we firmly believe in the fundamental principle of inclusivity and are dedicated to ensuring that our platform remains accessible to all individuals, regardless of disability or impairment. Our commitment to accessibility is manifested through the implementation of a comprehensive suite of features and functionalities designed to accommodate diverse user needs. From intuitive interface design to robust assistive technologies, such as screen readers and keyboard navigation, InCollege endeavors to create an inclusive digital environment that fosters equitable participation and engagement for all users. We recognize the importance of accessibility as a cornerstone of our platform's ethos and remain steadfast in our pursuit of excellence in this regard.\n")
                secondChoice = input("\nOptions\n1. Go back: ")
                if secondChoice == '1':
                    self.importantLinks()
                else:
                    print("Invalid Choice")
                    break

            elif choice == '4':
                print("\nUser Agreement: InCollege's user agreement serves as the cornerstone of our platform's operational framework, delineating the terms and conditions that govern user interactions and engagements within our ecosystem. By accessing or utilizing InCollege's services, you are expressly consenting to abide by the stipulations outlined in our user agreement. This comprehensive document encompasses a myriad of provisions, ranging from user rights and responsibilities to guidelines for acceptable usage and conduct. Through adherence to our user agreement, InCollege seeks to foster a cohesive and mutually beneficial community characterized by respect, integrity, and collaboration. We encourage all users to familiarize themselves with the contents of our user agreement and to approach their interactions on our platform with diligence and mindfulness.\n")
                secondChoice = input("\nOptions\n1. Go back: ")
                if secondChoice == '1':
                    self.importantLinks()
                else:
                    print("Invalid Choice")
                    break

            elif choice == '5':
                print("\nPrivacy Policy: InCollege is deeply committed to safeguarding the privacy and confidentiality of its users' personal information. Our privacy policy articulates the principles and practices that govern the collection, usage, and protection of user data within our platform. Rooted in principles of transparency, accountability, and user empowerment, our privacy policy serves as a testament to our unwavering dedication to maintaining the trust and confidence of our user community. Whether you are navigating our website, engaging with our services, or participating in our community forums, rest assured that your privacy rights are of paramount importance to us. We invite you to peruse our privacy policy to gain a comprehensive understanding of how we handle and protect your personal information.\n")
                secondChoice = input("\nOptions\n1. Go back: ")
                if secondChoice == '1':
                    self.importantLinks()
                else:
                    print("Invalid Choice")
                    break

            elif choice == '6':
                print("\nCookie Policy: InCollege's cookie policy elucidates the manner in which we utilize cookies and similar technologies to enhance user experience and optimize the functionality of our platform. Cookies, small text files stored on your device, serve as invaluable tools that enable us to deliver personalized content, analyze user behavior, and improve overall website performance. Our cookie policy provides detailed insights into the types of cookies utilized, their respective purposes, and the mechanisms through which users can manage their cookie preferences. By consenting to the use of cookies in accordance with our policy, users can enjoy a more tailored and seamless browsing experience on InCollege.\n")
                secondChoice = input("\nOptions\n1. Go back: ")
                if secondChoice == '1':
                    self.importantLinks()
                else:
                    print("Invalid Choice")
                    break

            elif choice == '7':
                print("\nCopyright Policy: InCollege remains steadfast in its commitment to upholding the principles of intellectual property rights and recognizes the importance of addressing copyright infringement in a timely and effective manner. Our copyright policy outlines the procedures and protocols governing the submission and resolution of copyright infringement claims within our platform. As a responsible digital entity, InCollege is dedicated to facilitating a robust framework for copyright enforcement that prioritizes fairness, accountability, and due process. Users are encouraged to familiarize themselves with the provisions outlined in our copyright policy and to engage in responsible content sharing practices that respect the intellectual property rights of others.\n")
                secondChoice = input("\nOptions\n1. Go back: ")
                if secondChoice == '1':
                    self.importantLinks()
                else:
                    print("Invalid Choice")
                    break

            elif choice == '8':
                print("\nBrand Policy: InCollege's brand policy serves as a comprehensive guidebook for the proper usage and representation of our brand assets, including logos, trademarks, and brand colors. Upholding the integrity and consistency of our brand identity is of paramount importance to us, and our brand policy endeavors to provide clear and concise directives for brand usage across various contexts and mediums. Whether you are a user, partner, or affiliate of InCollege, adherence to our brand policy ensures that our brand is represented in a manner that is cohesive, professional, and reflective of our core values and mission. We invite you to review our brand policy and to join us in upholding the integrity of the InCollege brand.\n")
                secondChoice = input("\nOptions\n1. Go back: ")
                if secondChoice == '1':
                    self.importantLinks()
                else:
                    print("Invalid Choice")
                    break

            elif choice == '9':
                print("\nGuest Controls: InCollege's guest controls empower users to customize and personalize their browsing experience within our platform. Whether you are exploring career opportunities, networking with peers, or accessing educational resources, our guest controls afford you the flexibility to tailor your preferences and settings to align with your unique needs and preferences. From managing visibility settings to configuring notification preferences, our intuitive guest controls interface offers a seamless and intuitive user experience that puts you in control of your InCollege journey. We invite you to leverage the power of guest controls to enhance your browsing experience and maximize your engagement within our platform.\n")
                secondChoice = input("\nOptions\n1. Go back: ")
                if secondChoice == '1':
                    self.importantLinks()
                else:
                    print("Invalid Choice")
                    break

            elif choice == '10':
                print("\nLanguages: InCollege supports multiple languages to accommodate users from diverse linguistic backgrounds. Select your preferred language to view our website and content in your native language, ensuring a seamless browsing experience for all users.")
                secondChoice = input("\nOptions\n1. Go back: ")
                if secondChoice == '1':
                    self.importantLinks()
                else:
                    print("Invalid Choice")
                    break

            elif choice == '11':
                print("\nYou selected: Go back")
                self.userDisplay()
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 11.")

    def userDisplay(self):
        print("\nWelcome to InCollege!\n")
        print("Here's a success story from one of our InCollege members -")
        print("Jane Doe, a student at University of South Florida, used InCollege to find her dream job at ABC Company. ")
        print("She credits InCollege for helping her build her professional network and discover job opportunities.")
        print("\nPlease select one of the following options:")
        print("1. Create a New InCollege Account")
        print("2. Login to an Existing InCollege Account")
        print("3. Connect with an existing member")
        print("4. Watch InCollege introduction video")
        print("5. Useful Links")
        print("6. InCollege Important Links")
        print("7. Exit")
        selection = input("Selection: ")
        if selection == "1":
            self.createAccount()
        elif selection == "2":
            self.userLogin()
        elif selection == "3":
            self.connectWithSomeone()
        elif selection == "4":
            print("\nVideo is now playing.\n")
            print("Please select one of the following options:")
            print("1. Return to main menu")
            selection = input("Selection: ")
            self.userDisplay()
        elif selection == "5":
            print("\nYou have selected Useful Links.")
            self.usefulLinks()
        elif selection == "6":
            print("\nYou have selected InCollege Important Links.\n")
            self.importantLinks()
        elif selection == "7":
            print("\nYou have chosen to exit.\n")
            exit()
        else:
            print("Invalid selection. Please try again.\n")
            self.userDisplay()

def main():
    user = UserAccountManager()
    user.userDisplay()

if __name__ == "__main__":
    main()