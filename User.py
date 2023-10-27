class UserAccount:
    account_number = 1
    loan_feature = True


    def __init__(self, name, email, address, account_type) -> None:
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.initial_balance = 0
        self.current_balance = 0
        self.Transactions = []
        self.max_loans_can_take = 2
        self.account_number = UserAccount.account_number
        UserAccount.account_number += 1
        self.password = None  



    def set_password(self, password):
        self.password = password



    def deposit_amount(self, amount):
        if amount > 0:
            self.initial_balance += amount
            self.current_balance += amount
            Admin.total_balance += amount
            self.Transactions.append(f"Deposited money {amount}")
            print(f'Deposited money = {amount} is added successfully.')
        else:
            print(f'Invalid deposit amount')



    def withdraw(self, withdrawal_amount):
        if withdrawal_amount <= self.current_balance:
            self.initial_balance -= withdrawal_amount
            self.current_balance -= withdrawal_amount
            Admin.total_balance -= withdrawal_amount
            self.Transactions.append(f"Withdrew money {withdrawal_amount}")
            print(f'Withdrew money {withdrawal_amount} successfully.')
        else:
            print(f'Withdrawal amount exceeded')



    def check_balance(self):
        print(f"Current balance is: {self.current_balance}")



    def check_transaction_history(self):
        for history in self.Transactions:
            print(history)



    def request_for_loan(self, amount):
        if self.loan_feature:
            if self.max_loans_can_take > 0:
                self.max_loans_can_take -= 1
                self.current_balance += amount
                Admin.total_balance -= amount
                Admin.total_loan_amount += amount
                self.Transactions.append(f"Taken a loan money {amount}.")
                print(f"Loan of money = {amount} taken successfully")
            else:
                print(f"Loan limit exceeded. Cannot take more loans. Please pay off the previous loans")
        else:
            print("Authority has turned off the loan-taking feature")



    def transfer_money(self, amount, recipient_account_number):
        if amount <= self.current_balance:
            recipient_account = None
            for user in Admin.users_account:
                if user.account_number == recipient_account_number:
                    recipient_account = user
                    break


            if recipient_account:
                self.current_balance -= amount
                recipient_account.current_balance += amount
                self.Transactions.append(f"Transferred money {amount} to Account #{recipient_account_number}")
                recipient_account.Transactions.append(f"Received money {amount} from Account #{self.account_number}")
                print(f"Transferred money = {amount} to Account #{recipient_account_number} successfully.")
            else:
                print("Recipient's account does not exist. Please enter a valid account number.")


        else:
            print("Insufficient money to transfer")



class Admin:
    users_account = []
    total_balance = 0
    total_loan_amount = 0  


    @classmethod
    def create_account(cls, name, email, address, account_type):
        account_creates = UserAccount(name, email, address, account_type)
        cls.users_account.append(account_creates)
        cls.total_balance += account_creates.current_balance
        print(f"Account for {name} created successfully with Account Number {account_creates.account_number}.")


    @classmethod
    def delete_account(cls, account_number):
        for account in cls.users_account:
            if account.account_number == account_number:
                cls.users_account.remove(account)
                cls.total_balance -= account.current_balance
                cls.total_loan_amount -= (account.initial_balance - account.current_balance)
                print(f'Account {account_number} deleted successfully')
                return
        print("Account does not exist")



    @classmethod
    def calculate_total_balance(cls):
        print(f"Total balance of the bank is: {cls.total_balance}")



    @classmethod
    def see_users_accounts(cls):
        for account in cls.users_account:
            print(f"Account #{account.account_number}: {account.name} : {account.email} : {account.account_number}")



    @classmethod
    def total_loan_given(cls):
        print(f"Total Loan Amount is: {cls.total_loan_amount}")



    @classmethod
    def change_loan_feature(cls, status):
        UserAccount.loan_feature = status
        if status:
            print("Loan feature is turned on.")
        else:
            print("Loan feature is turned off.")



currentUser = None
changeOfUser = True


while True:


    print("\nPlease choose one option:")
    print("1. User")
    print("2. Admin")
    print("3. Exit")


    choice = int(input("Enter choice: "))



    if choice == 1:
        if currentUser is None:
            print("\n\t--->!!! No logged in user\n")

            option = input("Login, Register(L/R): ")

            if option == "L":
                account_number = int(input("\tEnter Account Number: "))
                password = input("\tEnter Password: ")

                user = None
                for u in Admin.users_account:
                    if u.account_number == account_number:
                        user = u
                        break


                if user and user.password == password:
                    currentUser = user
                    changeOfUser = True


                    print("Logged in successfully.")
                   

                else:
                    print("\n\t---> Invalid account number or password!\n")
                    break



            elif option == "R":
                name = input("\tEnter Name: ")
                email = input("\tEnter E-mail: ")
                address = input("\tEnter Address: ")
                account_type = input("\tAccount Type (Savings/Current): ")
                password = input("\tSet a Password: ")


                user = UserAccount(name, email, address, account_type)
                user.set_password(password)
                Admin.users_account.append(user) 



                currentUser = user
                changeOfUser = True
                print(f"Account registered successfully with Account Number {user.account_number}.") 


        if currentUser is not None:


            print(f"\n\t---> Welcome, {currentUser.name}")
            print("Options:\n")
            print("1: Deposit")
            print("2: Withdraw")
            print("3: Check Balance")
            print("4: Check Transactions History")
            print("5: Take Loan")
            print("6: Transfer")
            print("7: Logout")
            

            user_choice = int(input("Enter Option:"))


            if user_choice == 1:
                amount = int(input("\tEnter Amount:"))
                currentUser.deposit_amount(amount)


            elif user_choice == 2:
                amount = int(input("\tEnter Amount:"))
                currentUser.withdraw(amount)


            elif user_choice == 3:
                currentUser.check_balance()


            elif user_choice == 4:
                currentUser.check_transaction_history()


            elif user_choice == 5:               
                amount = int(input("\tEnter Amount:"))
                currentUser.request_for_loan(amount)
                


            elif user_choice == 6:
                recipient_acc_no = int(input("\tEnter Account to Transfer:"))
                amount = int(input("\tEnter Amount:"))
                currentUser.transfer_money(amount, recipient_acc_no)


            elif user_choice == 7:
                currentUser = None


            else:
                print("\n\t---> !!! Choose a Valid Option\n")


    elif choice == 2:

        print("\nChoose an option:")
        print("1: Create Account")
        print("2: Delete Account")
        print("3: Show Users")
        print("4: Check Total Balance")
        print("5: Check Total Loan")
        print("6: Update Loan Feature")
        print("7: Exit")
        admin_choice = int(input("Enter Option: "))


        admin = Admin()


        if admin_choice == 1:
            name = input("Enter Name:")
            email = input("Enter E-mail:")
            address = input("Enter Address:")
            account_type = input("Account Type (Savings/Current):")
            admin.create_account(name, email, address, account_type)


        elif admin_choice == 2:
            acc_no = int(input("Enter Account Number:"))
            admin.delete_account(acc_no)


        elif admin_choice == 3:
            admin.see_users_accounts()


        elif admin_choice == 4:
            admin.calculate_total_balance()


        elif admin_choice == 5:
            admin.total_loan_given()


        elif admin_choice == 6:
            toggle_status = input("Enter 'on' to enable loan feature or 'off' to disable it: ")
            if toggle_status == 'on':
                admin.change_loan_feature(True)
            elif toggle_status == 'off':
                admin.change_loan_feature(False)


        elif admin_choice == 7:
            break


        else:
            print("\n\t---> !!! Choose a Valid Option\n")


    elif choice == 3:
        break


    else:
        print("\n\t---> !!! Choose a Valid Option\n")
