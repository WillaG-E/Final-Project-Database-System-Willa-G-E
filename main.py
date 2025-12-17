#Author: Willa Galipeau-Eldridge
#Date: 12/16/2025
#Purpose: Menu for Database System and user input

from database import Database

def main():

    SEARCHABLE_FIELDS = ["movie_title","release_date", "genre", "rating", "box_office_revenue"]
    database = Database(SEARCHABLE_FIELDS)
    results = None #stores the set of objects returned by a search
    
    print("\n================ Database System ================")

    while(True):
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

        if (user_input == "1"):
            #Load the data from the CSV file (MOCKDATA.CSV)
            file = "MOCK_DATA.csv"
            database.load_csv(file)
            results = []
            print("Data is loaded from CSV file.")
        elif (user_input == "2"):
            #Create a field to index
            field = input("Field: ")
            if (field in SEARCHABLE_FIELDS):
                database.create_index(field)
                print(f"Index created on {field}")
            else:
                    print("Invalid field name.")

        elif (user_input == "3"):
            #Exact search
            field = input("Search field: ")
            value = input("Search value: ")

            if field not in SEARCHABLE_FIELDS:
                print(f"Invalid searchable field: {field}")
                results = []
                continue

            #function that sends the field and value variables to get an exact search
            results = database.exact_search(field, value)
            for r in results:
                print(r)
            print(f"Found {len(results)} records.")

        elif (user_input == "4"):
            #Range queries
            field = input("Indexed field: ")
            low = input("Low bound: ")
            high = input("High bound: ")

            if field not in SEARCHABLE_FIELDS:
                print(f"Invalid field: {field}")
                results = []
                continue
            results = database.range_search(field, low, high)
            print(f"Found {len(results)} records.")
            for r in results:
                print(r)

        elif (user_input == "5"):
            #Export functionality
            if results is None or len(results) == 0:
                print("No search results to export.")
                continue

            filename = input("Export filename: ")
            with open(filename, "w", newline="") as f:
                for row in results:
                    f.write(",".join(row.csvRow()) + "\n")
            print(f"Successfully exported file: ${filename}")

        elif (user_input == "6"):
            #Delete functionality
            if (results == None or len(results) == 0):
                print("No search results to delete")
                continue

            count = database.delete_records(results)
            print(f"Deleted {count} records.")
            results = [] #clears the results after deletion
        
        elif (user_input == "0"):
            return




if __name__ == "__main__":
    main()