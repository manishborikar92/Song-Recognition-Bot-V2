import os

def search_file(path):
    file_path = path
    if os.path.exists(file_path):
        return file_path
    
    # If the file is not found, return a message indicating so
    return None

# # Example usage
# path = input("Enter the path to search: ")
# result = search_file(path)
# print(result)
