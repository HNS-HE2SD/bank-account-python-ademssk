# Class Client
class Client:
    __next_id = 1

    def __init__(self, cin, firstName, lastName, tel=""):
        # unique identifier allowing duplicate CIN/name/tel across different client objects
        self.__id = Client.__next_id
        Client.__next_id += 1

        self.__CIN = cin
        self.__firstName = firstName
        self.__lastName = lastName
        self.__tel = tel

        # hold accounts created via this client (optional, helps manage multiple accounts)
        self.__accounts = []

        # history records: list of dicts with keys like type, amount, balance_after
        self.__history = []

    # Getters and setters for all attributes
    def get_id(self): return self.__id
    def get_CIN(self): return self.__CIN
    def get_firstName(self): return self.__firstName
    def get_lastName(self): return self.__lastName
    def get_tel(self): return self.__tel

    def set_tel(self, tel): self.__tel = tel

    # Account management helpers (create or register accounts)
    def open_account(self):
        # Lazy import: Account class is defined later in file, so instantiate when called
        acc = Account(self)
        self.__accounts.append(acc)
        return acc

    def register_account(self, account):
        # If an account was created externally, register it to this client
        if account not in self.__accounts:
            self.__accounts.append(account)

    def get_accounts(self):
        return list(self.__accounts)

    # History management
    def _record_history(self, entry):
        # Keep history simple: do not add timestamps or account codes
        self.__history.append(entry)

    def get_history(self):
        return list(self.__history)

    def display_history(self):
        for e in self.__history:
            typ = e.get('type')
            amt = e.get('amount')
            bal = e.get('balance_after')
            if typ == 'transfer':
                print(f"{typ.title()}: {amt} DA. Balance after: {bal} DA")
            else:
                print(f"{typ.title()}: {amt} DA. Balance after: {bal} DA")

    # High-level operations that validate amounts and record history.
    def deposit_to_account(self, account, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        # perform deposit
        account.credit(amount)
        # register account if owned by this client
        if account.get_owner() is self and account not in self.__accounts:
            self.__accounts.append(account)
        # record (no account codes or timestamps)
        self._record_history({
            'type': 'deposit',
            'amount': amount,
            'balance_after': account.get_balance()
        })

    def withdraw_from_account(self, account, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if account.get_balance() < amount:
            print("Insufficient balance.")
            return
        account.debit(amount)
        # record
        self._record_history({
            'type': 'withdraw',
            'amount': amount,
            'balance_after': account.get_balance()
        })

    def transfer(self, from_account, to_account, amount):
        if amount <= 0:
            print("Transfer amount must be positive.")
            return
        if from_account.get_balance() < amount:
            print("Insufficient balance for transfer.")
            return
        # perform transfer using Account.debit(account=...) so balance updates are consistent
        from_account.debit(amount, account=to_account)

        # record for sender (no account codes)
        self._record_history({
            'type': 'transfer',
            'amount': amount,
            'balance_after': from_account.get_balance()
        })

        # record for recipient owner (if different or same client)
        recipient = to_account.get_owner()
        if hasattr(recipient, '_Client__history'):  # ensure it's a Client-like object
            recipient._record_history({
                'type': 'transfer',
                'amount': amount,
                'balance_after': to_account.get_balance()
            })

    def display(self):
        print(f"CIN: {self.__CIN}, Name: {self.__firstName} {self.__lastName}, Tel: {self.__tel}, ID: {self.__id}")

# Class Account
class Account:
    __nbAccounts = 0  # static variable for sequential codes

    def __init__(self, owner):
        Account.__nbAccounts += 1
        self.__code = Account.__nbAccounts
        self.__balance = 0.0
        self.__owner = owner

    # Access methods
    def get_code(self): return self.__code
    def get_balance(self): return self.__balance
    def get_owner(self): return self.__owner

    # Credit and debit methods
    def credit(self, amount, account=None):
        if account is None:
            self.__balance += amount
        else:
            self.__balance += amount
            account.debit(amount)

    def debit(self, amount, account=None):
        if self.__balance >= amount:
            self.__balance -= amount
            if account is not None:
                account.credit(amount)
        else:
            print("Insufficient balance.")

    def display(self):
        print(f"Account Code: {self.__code}")
        print(f"Owner: {self.__owner.get_firstName()} {self.__owner.get_lastName()}")
        print(f"Balance: {self.__balance} DA")

    @staticmethod
    def displayNbAccounts():
        print("Total accounts created:", Account.__nbAccounts)
