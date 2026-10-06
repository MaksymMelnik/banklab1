import random
from datetime import datetime


class Account:

    def __init__(self, balance, pin, iban=None):
        if iban is None:
            random_digits = str(random.randint(100000000000000000, 999999999999999999))
            self.iban = "UA8930000100000" + random_digits
        else:
            self.iban = iban

        self.balance = balance
        self.pin = str(pin)

    def verify_pin(self, entered_pin):
        return self.pin == str(entered_pin)

    def withdraw(self, amount):
        if amount <= 0 or amount > self.balance:
            return False
        self.balance -= amount
        return True

    def deposit(self, amount):
        if amount > 0:1
            self.balance += amount
            return True
        return False


class SavingsAccount(Account):

    def __init__(self, balance, percent, pin, iban=None):
        super().__init__(balance, pin, iban)
        self.percent = percent

    def add_percent(self):
        bonus = self.balance * (self.percent / 100)
        self.balance += bonus
        print(f"Нараховано відсотки: {bonus:.2f} грн")


class Client:

    def __init__(self, name):
        self.name = name
        self.client_accounts = []

    def add_account(self, account):
        self.client_accounts.append(account)


class Transaction:

    def __init__(self, sender, receiver, amount, status):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.status = status
        self.date = datetime.now()


class Bank:

    def __init__(self):
        self.accounts = {}
        self.clients = []
        self.transactions = []

    def add_client(self, client):
        self.clients.append(client)
        for acc in client.client_accounts:
            self.add_account(acc)

    def add_account(self, account):
        account_key = account.iban
        self.accounts[account_key] = account

    def get_client_by_name(self, name):
        for client in self.clients:
            if client.name.lower() == name.lower():
                return client
        return None

    def print_all_clients(self):
        print("\n--- СПИСОК КЛІЄНТІВ ТА ЇХ РАХУНКІВ ---")
        for client in self.clients:
            for acc in client.client_accounts:
                print(f"{client.name} | {acc.iban} (Баланс: {acc.balance:.2f} грн)")

    def atm_deposit(self, iban):
        if iban not in self.accounts:
            print("Рахунок не знайдено")
            return

        try:
            amount = float(input("Введіть суму для поповнення: "))
        except ValueError:
            print("Некоректний ввід суми.")
            return

        if amount <= 0:
            print("Некоректна сума")
            return

        account = self.accounts[iban]
        account.deposit(amount)

        log = Transaction("ATM", iban, amount, "Успішно")
        self.transactions.append(log)
        print(f"Банкомат: Рахунок поповнено на {amount} грн")

    def atm_withdraw(self, iban):
        if iban not in self.accounts:
            print("Рахунок не знайдено")
            return

        account = self.accounts[iban]
        user_pin = input("Введіть PIN-код картки для зняття: ")

        if not account.verify_pin(user_pin):
            print("Невірний PIN-код! Операцію зняття скасовано.")
            log = Transaction(iban, "ATM", 0, "Відхилено (Невірний PIN)")
            self.transactions.append(log)
            return

        try:
            amount = float(input("Введіть суму для зняття з банкомату: "))
        except ValueError:
            print("Некоректний ввід суми.")
            return

        if account.withdraw(amount):
            log = Transaction(iban, "ATM", amount, "Успішно")
            self.transactions.append(log)
            print(f"Банкомат: Заберіть ваші {amount} грн")
        else:
            log = Transaction(iban, "ATM", amount, "Відхилено")
            self.transactions.append(log)
            print("Банкомат: Недостатньо коштів або некоректна сума")

    def transfer(self, sender_iban):
        receiver_iban = input("Введіть IBAN отримувача: ").strip()

        if sender_iban == receiver_iban:
            print("Переказ на той самий рахунок заборонено")
            return

        if sender_iban not in self.accounts:
            print("Рахунок відправника не знайдено")
            return

        if receiver_iban not in self.accounts:
            print("Рахунок отримувача не знайдено")
            return

        sender_account = self.accounts[sender_iban]
        receiver_account = self.accounts[receiver_iban]

        try:
            amount = float(input("Введіть суму переказу: "))
        except ValueError:
            print("Некоректна сума.")
            return

        user_pin = input("Введіть PIN-код для підтвердження переказу: ")

        if not sender_account.verify_pin(user_pin):
            print("Невірний PIN-код! Переказ скасовано.")
            failed_log = Transaction(sender_iban, receiver_iban, amount, "Відхилено (Невірний PIN)")
            self.transactions.append(failed_log)
            return

        fee = amount * 0.01
        total_amount = amount + fee

        if sender_account.withdraw(total_amount):
            receiver_account.deposit(amount)
            new_log = Transaction(sender_iban, receiver_iban, amount, "Успішно")
            self.transactions.append(new_log)
            print(f"Переказ виконано (комісія: {fee:.2f} грн)")
        else:
            failed_log = Transaction(sender_iban, receiver_iban, amount, "Відхилено")
            self.transactions.append(failed_log)
            print("Переказ відхилено: недостатньо коштів з урахуванням комісії")


client1 = Client("Максим")
client2 = Client("Ілля")

account1 = Account(balance=1000, pin="1234", iban="UA893000010000011111111111111")
account2 = SavingsAccount(balance=200, percent=5, pin="4321", iban="UA893000010000022222222222222")
account3 = Account(balance=1500, pin="5678", iban="UA893000010000011111111122222")

client1.add_account(account1)
client1.add_account(account2)
client2.add_account(account3)

my_bank = Bank()
my_bank.add_client(client1)
my_bank.add_client(client2)


def main():
    while True:
        print("\n==========================================")
        print("          БАНКІВСЬКА СИСТЕМА              ")
        print("==========================================")
        print("1. Почати роботу (обрати клієнта)")
        print("2. Завершити роботу")
        
        choice = input("Оберіть дію (1 або 2): ").strip()

        if choice == "2":
            print("\nРоботу завершено.")
            break
        elif choice != "1":
            print("Некоректний вибір. Спробуйте ще раз.")
            continue

        client_name = input("\nВведіть ім'я клієнта: ").strip()
        client = my_bank.get_client_by_name(client_name)

        if not client:
            print("Клієнта з таким ім'ям не знайдено.")
            continue

        print(f"\nЗнайдено клієнта: {client.name}")
        print("Доступні рахунки:")
        for idx, acc in enumerate(client.client_accounts, 1):
            print(f"  {idx}. IBAN: {acc.iban} | Баланс: {acc.balance:.2f} грн")

        try:
            acc_choice = int(input("Оберіть номер рахунку: ")) - 1
            if acc_choice < 0 or acc_choice >= len(client.client_accounts):
                print("Некоректний номер рахунку.")
                continue
            selected_account = client.client_accounts[acc_choice]
        except ValueError:
            print("Будь ласка, введіть число.")
            continue

        while True:
            print(f"\n--- Операції для рахунку {selected_account.iban} ---")
            print("1. Поповнити (через банкомат)")
            print("2. Зняти готівку")
            print("3. Зробити переказ")
            print("4. Перевірити баланс")
            if isinstance(selected_account, SavingsAccount):
                print("5. Нарахувати відсотки (накопичувальний)")
            print("0. Назад до головного меню")

            op = input("Оберіть операцію: ").strip()

            if op == "1":
                my_bank.atm_deposit(selected_account.iban)
            elif op == "2":
                my_bank.atm_withdraw(selected_account.iban)
            elif op == "3":
                my_bank.transfer(selected_account.iban)
            elif op == "4":
                print(f"Поточний баланс: {selected_account.balance:.2f} грн")
            elif op == "5" and isinstance(selected_account, SavingsAccount):
                selected_account.add_percent()
            elif op == "0":
                break
            else:
                print("Некоректна опція.")

            cont = input("\nБажаєте виконати іншу операцію з цим рахунком? (так/ні): ").strip().lower()
            if cont not in ["так", "yes", "y", "t"]:
                break

    my_bank.print_all_clients()



if __name__ == "__main__":
    main()