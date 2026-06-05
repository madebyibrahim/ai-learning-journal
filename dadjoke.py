import requests

def get_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"} # tells API to return JSON
    try:
        
        response = requests.get(url, headers=headers, timeout=10)  
        if response.status_code == 200:
            joke_data = response.json()
            return joke_data["joke"]
        else:
            return None

    except requests.exceptions.RequestException:
        return None


def main():
    print(f"\nHello and welcome to the dad joke factory. Enter the number of jokes you would like to hear (e.g. 3), otherwise, enter \"q\" to quit.\n")
    while True:
        my_input = input("You: ")
        clean_input = my_input.strip().split()
        if not clean_input:
            print(f"\nNothing entered, please enter a valid value.\n")
            continue

        the_input = clean_input[0]
        if the_input == "q":
            print("\nGoodbye!\n")
            break

        elif the_input.isnumeric():
            int_input = int(the_input)
            if int_input <1:
                print(f"\nPlease enter a positive integer number for the number of jokes.\n")
                continue
            for i in range(int_input):
                joke = get_joke()
                if joke:
                    print("\n"+ joke +"\n")
                else:                
                    print("\nSkipping joke, unable to fetch.\n")


        elif not the_input.isnumeric():
            print("\nPlease enter a positive integer value for the number of jokes.\n")
            continue    




        
if __name__ == "__main__":
    main()

