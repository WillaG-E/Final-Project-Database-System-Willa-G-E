def main():
    print("\n================ Database System ================")
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
            pass
        elif (user_input == "4"):
            #Range queries
            pass
        elif (user_input == "5"):
            #Export functionality
            pass
        elif (user_input == "6"):
            #Delete functionality
            pass
        elif (user_input == "0"):
            return




if __name__ == "__main__":
    main()