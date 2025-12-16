#Author: Willa Galipeau-Eldridge
#Date: 12/16/2025
#Purpose: Menu for Database System and user input

def main():

    SEARCHABLE_FIELDS = ["movie_title","release_date", "genre", "rating", "box_office_revenue"]
    
    results = [] #stores the set of objects returned by a search
    print("\n================ Database System ================")
    print(f"\nSearchable Fields: {','.join(SEARCHABLE_FIELDS)}")
    print("""
        1 - Load CSV
        2 - Create Index
        3 - Exact Search
        4 - Range Search
        5 - Export
        6 - Delete
        0 - Exit the program
            """)

    user_input = input("Enter a command: ")

    while(user_input < "7" and user_input > "-1"):
        print("""
        1 - Load CSV
        2 - Create Index
        3 - Exact Search
        4 - Range Search
        5 - Export
        6 - Delete
        0 - Exit the program
            """)
        if (user_input == "1"):
            #Load the data from the CSV file (MOCKDATA.CSV)
            pass
        elif (user_input == "2"):
            #Create a field to index
            pass
        elif (user_input == "3"):
            #Exact search
            field = input("Search field: ")
            value = input("Search value: ")

            #function that sends the field and value variables to get an exact search
            
            print(results)

        elif (user_input == "4"):
            #Range queries
            pass
        elif (user_input == "5"):
            #Export functionality
            filename = input("Export filename: ")
            with open(filename, "w") as f:
                for row in results:
                    f.write(",".join(row))
            print(f"Successfully exported file: ${filename}")
            pass
        elif (user_input == "6"):
            #Delete functionality
            pass
        elif (user_input == "0"):
            return




if __name__ == "__main__":
    main()