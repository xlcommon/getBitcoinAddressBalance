import csv
import requests

mempool_api = "mempool.space/api/address/" #Change to local mempool instance
csv_filename = "address.csv"  # Change to the actual file path

def get_balance(address):
    url = f"{mempool_api}{address}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        confirmed = result.get("chain_stats", {}).get("funded_txo_sum", 0) - result.get("chain_stats", {}).get("spent_txo_sum", 0)
        return confirmed
    except Exception as e:
        print(f"Error fetching balance for {address}: {e}")
        return None

def read_csv_and_get_balances(csv_file):
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 2:
                continue
            name, address = row[0], row[1]
            balance = get_balance(address)
            if balance is not None:
                print(f"{name}\nAddress: \"{address}\"\nBalance: {balance} sats\n---------------------------")
            else:
                print(f"{name}: Balance could not be retrieved.\n---------------------------")

if __name__ == "__main__":
    read_csv_and_get_balances(csv_filename)