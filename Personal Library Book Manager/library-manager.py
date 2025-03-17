import json
import os
import streamlit as st

data_file = 'library.txt'

# Load and save library functions
def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file)

# Function to add book
def add_book(library):
    st.subheader("Add Book")
    
    title = st.text_input("Enter book title:")
    author = st.text_input("Enter author:")
    year = st.text_input("Enter publication year:")
    genre = st.text_input("Enter genre:")
    read = st.radio("Have you read this book?", ("Yes", "No")) == "Yes"
    
    if st.button("Add Book"):
        if title and author and year and genre:
            new_book = {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read": read
            }
            library.append(new_book)
            save_library(library)
            st.success(f'Book "{title}" added successfully!')
        else:
            st.error("Please fill in all fields.")

# Function to remove book
def remove_book(library):
    st.subheader("Remove Book")
    
    title = st.text_input("Enter the title of the book to remove:")
    
    if st.button("Remove Book"):
        initial_length = len(library)
        library[:] = [book for book in library if book['title'].lower() != title.lower()]
        if len(library) < initial_length:
            save_library(library)
            st.success(f'Book "{title}" removed successfully!')
        else:
            st.error(f'Book "{title}" not found.')

# Function to search books
def search_books(library):
    st.subheader("Search Books")
    
    search_by = st.selectbox("Search by", ["Title", "Author"])
    search_term = st.text_input(f"Enter the {search_by.lower()}:")
    
    if st.button("Search"):
        results = [book for book in library if search_term.lower() in book[search_by.lower()].lower()]
        
        if results:
            for book in results:
                status = "Read" if book['read'] else "Unread"
                st.write(f'{book["title"]} by {book["author"]} ({book["year"]}) - {book["genre"]} - {status}')
        else:
            st.warning("No matching books found.")

# Function to display all books
def display_all_books(library):
    st.subheader("Display All Books")
    
    if library:
        for book in library:
            status = "Read" if book['read'] else "Unread"
            st.write(f'{book["title"]} by {book["author"]} ({book["year"]}) - {book["genre"]} - {status}')
    else:
        st.warning("No books in the library.")

# Function to display statistics
def display_statistics(library):
    st.subheader("Library Statistics")
    
    total_books = len(library)
    read_books = len([book for book in library if book['read']])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    st.write(f"Total Books: {total_books}")
    st.write(f"Percentage Read: {percentage_read:.2f}%")

# Main function for UI
def main():
    # Custom CSS for styling
    st.markdown("""
    <style>
        body {
            background-color: #f4f6f8;
            font-family: 'Arial', sans-serif;
        }
        .stButton>button {
            background-color: #0b74e5;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #0066cc;
        }
        .stTextInput>div>input {
            padding: 10px;
            font-size: 16px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        .stRadio>div>div>label {
            font-size: 14px;
            color: #333;
        }
        .stSubheader {
            color: #0b74e5;
            font-weight: bold;
        }
        .welcome-text {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            color: #0b74e5;
            background: linear-gradient(45deg, #0b74e5, #e8a400);
            -webkit-background-clip: text;
            color: transparent;
            padding: 20px 0;
        }
        .stSidebar {
            background-color: #0b74e5;
        }
    </style>
    """, unsafe_allow_html=True)

    # Welcome message with gradient
    st.markdown('<div class="welcome-text">Welcome to the Library Manager</div>', unsafe_allow_html=True)

    # Load the library data
    library = load_library()

    # Sidebar for navigation
    menu = ["Add Book", "Remove Book", "Search Book", "Display All Books", "Display Statistics", "Exit"]
    choice = st.sidebar.radio("Menu", menu)

    # Create main content based on user selection
    if choice == "Add Book":
        add_book(library)
    elif choice == "Remove Book":
        remove_book(library)
    elif choice == "Search Book":
        search_books(library)
    elif choice == "Display All Books":
        display_all_books(library)
    elif choice == "Display Statistics":
        display_statistics(library)
    elif choice == "Exit":
        st.write("Exiting the Library Manager.")

if __name__ == "__main__":
    main()
