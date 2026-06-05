
import requests


def main():

    while True:
        crypto =  input("Enter a cryptocurrency (e.g., bitcoin, ethereum): ").lower().strip()
        if crypto.strip().lower() == "q":
            print("\nGoodbye!\n")
            exit(0)
        currency = input("Enter a currency (e.g., usd, eur, gbp): ").lower().strip()
        if currency.strip().lower() == "q":
            print("\nGoodbye!\n")
            exit(0)
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies={currency}"
            response = requests.get(url)
            if response.status_code != 200:
                print(f"System Error: API returned status code {response.status_code}")
                continue
            data = response.json()
            price = data[crypto][currency]
            print(f"{crypto.capitalize()} price: {price} {currency.upper()}")
            continue

        except requests.exceptions.RequestException as e:
            print(f"Network or Request error: {e}")
            continue
        except KeyError:
            print("Unexpected response format: could not find the price in the response.")
            continue

if __name__ == "__main__":
    main()