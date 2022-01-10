import json
import requests


CONNECTED_NODE_ADDRESS = None


def send_coins(sender, receiver, amount):
    sender_balance = get_balance(account_id=sender)

    if sender != "tivix-bank" and sender_balance < amount:
        return False

    transactions_url = f"{CONNECTED_NODE_ADDRESS}/new_transaction"
    response = requests.post(transactions_url, json={
        "sender": sender,
        "receiver": receiver,
        "amount": amount
    })
    print(response.status_code)
    return True


def create_fake_transactions(no_of_transactions: int = 5):
    import random
    for _ in range(no_of_transactions):
        send_coins("tivix-bank", "mateusz.jasinski@tivix.com", random.randint(1, 100))


def get_balance(account_id):
    chain_receive_address = f"{CONNECTED_NODE_ADDRESS}/chain"
    response = requests.get(chain_receive_address)
    if response.status_code == 200:
        chain = json.loads(response.content)
        user_income = []
        user_spends = []
        for block in chain["chain"]:
            for transaction in block["transactions"]:
                if transaction["receiver"] == account_id:
                    user_income.append(transaction)
                elif transaction["sender"] == account_id:
                    user_spends.append(transaction)

        return sum(transaction['amount'] for transaction in user_income) - sum(transaction['amount'] for transaction in user_spends)
    return None


if __name__ == '__main__':
    CONNECTED_NODE_ADDRESS = input("Enter node address: ")
    chain_receive_address = f"{CONNECTED_NODE_ADDRESS}/chain"
    response = requests.get(chain_receive_address)
    if response.status_code == 200:
        create_fake_transactions()
        print('Connected to network!')
        while True:
            next_action = input("Hello! Select your action 1) Balance 2) Send")
            if next_action == "1":
                account_id = input("Account id: ")
                print(get_balance(account_id))
            if next_action == "2":
                receiver = input("Receiver id: ")
                amount = input(f"Amount (max.{get_balance('mateusz.jasinski@tivix.com')}): ")
                send_coins("mateusz.jasinski@tivix.com", receiver, float(amount))
