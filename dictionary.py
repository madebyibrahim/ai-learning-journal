import requests


def get_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    headers = {}

    try:
        response = requests.get(url=url, headers=headers, timeout=10)
        if response.status_code == 200:
            try:

                data = response.json()
                my_data=data[0]
                meanings = my_data["meanings"]
                final_res = []
                for meaning in meanings:
                    pos=meaning["partOfSpeech"]
                    for def_item in meaning["definitions"]:
                        text = def_item["definition"]
                        partial_res = f"({pos}): {text}"
                        final_res.append(partial_res)
                if not final_res:
                    return (None, "\nNo definitions found.\n")
                return (final_res, "")
            
            except (KeyError, IndexError):
                return (None, "\nUnexpected response format.\n")
        
        elif response.status_code == 404:
            return (None, "\nWord not found. Please check your spelling.\n")

        else:
            return (None, f"\nAPI returned unexpected status code {response.status_code}\n")
        

    except requests.exceptions.RequestException:
        return (None, "\nNetwork Error; please try again.\n")


def main():

    print("\nWelcome to the API dictionary. Type any word into the terminal to get its definition or press 'q' to quit.\n")
    
    while True:
        raw_input = input("You: ")
        clean_input = raw_input.strip()
        if clean_input.lower() == "q":
            print("\nGoodbye!\n")
            break

        if not clean_input.isalpha():
            print("\nPlease enter a valid alphabetic English word\n")
            continue

        the_input = clean_input.split()[0]
        res, print_comment = get_definition(the_input)
        if print_comment:
            print(print_comment)
        if res is None:
            continue
        print(f"\nThe word {clean_input.capitalize()} means:\n")
        for item in res:
            print(f"{item}\n")
        


if __name__ == "__main__":
    main()