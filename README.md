# Final-Project-Database-System-Willa-G-E
Final Project: Database System for UMaine COS226
Author: Willa Galipeau-Eldridge
Date: 12/17/2025
Course: COS226 - Intro Data Struct & Algorithms

Instructions on how to run your program

      1. Ensure that the dataset "MOCK_DATA.csv" is in the project folder
      2. Run the python file: main.py
      3. Enter command: 1, to load the data
      4. Enter command: 2, until you enter all of the searchable fields
      5. Enter command: 3, to find an exact search
              -enter the searchable field
              -enter what you want from that field (example: genre, Horror)
      7. Enter command: 4, to find a range search
              -enter the searchable field
              -enter the lower bound you want to look at
              -enter the higher bound you want to look at
      8. Enter command: 5, to delete the data you searched from a modified database
      9. Enter command: 0, to exit the Database System

Explaination and analysis of the efficiency of:
    * Initialization of the database
    * creation of indexes
    * queries
    * deletions

    
Example commands and their expected outputs

      Load Data:
      Index Field:
      Exact Search:
      Range Search:
      Delete:
      
Explanation of your hash function design choices.

      Hash Function (FNV-1a)
            I used the FNV-1a hash function from my homework assignment exploring and navigating hash functions. This hash function was used since it provided a consistently strong performance. This method kept collisions and wasted space low for the title and quote hash tables in my earlier homework assignment. For this reason, I believed that this hash function would offer a good balance between the time taken and keeping the number of collisions and wasted space lower. It would work excellent with my chosen searchable fields.
            
Discussion of your B+ tree implementation approach.

      The B+ Tree uses updated and modified code from my previous homework assignment. This implementation approach used bulk loading to reduce the constant rebalancing that normally occurs from the insertions. The tree is built from sorted data that makes sure the nodes are filled to 3/4 capacity to optimize the space and leave room for future nodes. This B+ Tree uses leaf node linkage with next and prev pointers to help with the range search in finding the results from a low to high value without having to traverse through the nodes repeatedly.

Explaination of why you chose certain fields to be searchable and which should not be.

      Searchable Fields:
            movie_title: primary identifier for the movie
            release_date: primary identifier for the movie
            genre: offers a categorical search for exact search (can find all of the movies in a specific genre)
            rating: helpful for range searches with a numerical search (can find movies between two ratings)
            box_office_revenue: helpful for range searches with a numerical search (can find movies between two revenues)

      Not Searchable Fields:
            director: could be useful, but would significantly increase the memory footprint in the Hash Tables
            duration_minutes: less prioritized/important compared to rating and revenue
            production_company: could be useful, but would significantly increase the memory footprint in the Hash Tables
            quote: more suited for searching through unique strings with a full-text search engine than a structured B+ Tree
      
Any known limitations or issues
