# ui.py



from pathlib import Path
from Profile import Post, Profile, DsuFileError, DsuProfileError
import time

# Global variable to store the path to the DSU file
global_path = None

  


def output_path(path, file, search, extension):
    if file and path.is_dir():
        return False
    if search and search not in path.name:
        return False
    if extension and not path.name.endswith('.' + extension):
        return False
    return True

def list_content(currentPath, recursive, file, search, extension):
    for entry in sorted(currentPath.iterdir(), key=lambda e: (e.is_file(), e.name)):
        if recursive and entry.is_dir():
            list_content(entry, recursive, file, search, extension)
        elif output_path(entry, file, search, extension):
            print(entry)

def list_directory(path, recursive=False, file=False, search=None, extension=None):
    list_content(Path(path), recursive, file, search, extension)

def delete_file(file_path):
    if file_path.suffix != '.dsu':
        print("ERROR")
        return
    file_path.unlink()
    print(f"{file_path} DELETED")

def read_file(file_path):
    if file_path.suffix != '.dsu':
        print("ERROR")
        return
    if file_path.stat().st_size == 0:
        print("EMPTY")
        return
    with file_path.open('r') as file:
        print(file.read())

def create_file(directory, name):
  # Use the global variable
    global global_path
    try:
        # Create new file with .dsu extension
        file_path = Path(directory) / f"{name}.dsu"
        if file_path.exists():
            raise FileExistsError(f"The file {name}.dsu already exists.")
        file_path.touch()

        username = input("Enter username: ")
        password = input("Enter password: ")
        bio = input("Enter bio: ")

        profile = Profile(username=username, password=password, bio=bio)
        profile.save_profile(str(file_path))
        

        global_path = str(file_path)  # Update the global path
        print(f"Profile saved to {file_path}")
    except Exception as e:
        print(f"Error creating file: {e}")
        profile = None ###
    return profile
        

def open_dsu_file(file_path):

    # Use the global variable
    global global_path

    profile = Profile()
    global_path = file_path ###
    try:
        profile.load_profile(file_path)
        global_path = file_path  # Update the global path
        print(f"Profile loaded successfully from {file_path}.")
        print(f"Username: {profile.username}, Password: {profile.password}, Bio: {profile.bio}")
    except DsuFileError as e:
        print(f"Error loading DSU file: {e}")
        profile = None ###
    except DsuProfileError as e:
        print(f"Error processing DSU file content: {e}")
        profile = None ###
    except Exception as e:
        print(f"Unexpected error: {e}")
        profile = None ###
    return profile
        

def edit_file(profile, operate, value):
    if operate == '-usr' and  value:
        profile.username = value  # Directly set the new username
        print(f"Username updated to {profile.username}")
    elif operate == '-pwd' and value:
        profile.password = value  # Directly set the new password
        print(f"Password updated to {profile.password}")
    elif operate == '-bio' and value:
        
        profile.bio = value
        print(f"Bio has updated to {profile.bio}")  
                      
    elif operate == "-addpost":
       
        # entry = ' '.join(options)
        new_post = Post(entry=value)
        profile.add_post(new_post)     
        print(f'Post has been updated to {global_path}')
        
    elif operate == "-delpost":
        print("tesing delete feature....")
        post_id = int(value) - 1 # index start at  0
        if profile.del_post(post_id):
            print(f'Post ID {post_id + 1} has been deleted.')
        else:
            print("Invalid post ID.")
    else:
        print("Invalid operation.")
    profile.save_profile(global_path)

def print_file(profile, operate, value):

    if operate == '-usr':
        print(f'Username: {profile.username}')
    elif operate == "-pwd":
        print(f'Password: {profile.password}')
    elif operate == "-bio":
        print(f"Bio :{profile.bio}")
    elif operate == '-posts':
        content = profile.get_posts()
        print("Here are your post: ")
        if content:
            for i, post in enumerate(content):
                entry = post.entry
                timestamp = post.timestamp
                print(f'Post ID {i+1}: {entry} at {time.ctime(timestamp)}')

    elif operate == "-post":
        
        print("tesing print post by ID....")
        post_id = int(value) - 1 # index start at  0
        content = profile.get_posts()
        post = content[post_id]
        entry = post.get_entry()
        timestamp = post.get_time()
        for i, post in enumerate(content):
            if i == post_id:
                print(f'Post ID {i+1}: {entry} at {time.ctime(timestamp)}')
        

    elif operate == '-all':
        print(f'Username: {profile.username}')
        print(f'Password: {profile.password}')
        print(f'Bio: {profile.bio}')
        
        content = profile.get_posts()
        if content:
            for i, post in enumerate(content):
                entry = post.entry
                timestamp = post.timestamp
                                    
                print(f'Post ID {i+1}: {entry} at {time.ctime(timestamp)}')
        else: 
            print("No content avaliable")
  


def parse_command(user_input):

    parts = user_input.split()
    if not parts:
        return "", []
    command = parts[0]
    options = parts[1:]
    return command, [option.strip('\"\'') for option in options]
##################################################################



def list_directory_flow():
    path = input("Enter the directory path to list: ")
    recursive = input("Do you want to list contents recursively? (yes/no): ").lower() == 'yes'
    file_only = input("Should we list files only? (yes/no): ").lower() == 'yes'
    search = input("Enter search term for filenames (leave blank for no search): ").strip() or None
    extension = input("List files with what extension? (leave blank for no filter): ").strip() or None
    list_directory(path, recursive, file_only, search, extension)

def delete_file_flow():
    file_path = input("Enter the full path of the file you wish to delete: ")
    confirm = input(f"Are you sure you want to delete {file_path}? This cannot be undone. (yes/no): ").lower()
    if confirm == 'yes':
        delete_file(Path(file_path))
    else:
        print("File deletion cancelled.")

def read_file_flow():
    file_path = input("Enter the full path of the file you wish to read: ")
    read_file(Path(file_path))


def open_dsu_file_flow():
    file_path = input("Enter the path to the DSU file: ")
    profile = open_dsu_file(file_path)  # Assuming this returns a profile object or None
    if profile:
        print("Profile loaded successfully.")
    else:
        print("Failed to load profile.")
    return profile

def create_file_flow():
    directory = input("Enter the directory path for the new DSU file: ")
    name = input("Enter the name for the DSU file: ")
    create_file(directory, name)

def load_file_flow():
    file_path = input("Enter the path to the DSU file: ")
    open_dsu_file(file_path)

def edit_profile_flow(profile):
    while True:
        print("\nEdit Profile Options:")
        print("1. Change Username")
        print("2. Change Password")
        print("3. Update Bio")
        print("4. Add Post")
        print("5. Delete Post")
        print("B. Back")
        choice = input("Choose an option: ").lower()

        if choice == '1':
            new_username = input("Enter the new username: ")
            edit_file(profile, '-usr', new_username)
        elif choice == '2':
            new_password = input("Enter the new password: ")
            edit_file(profile, '-pwd', new_password)
        elif choice == '3':
            new_bio = input("Enter the new bio: ")
            edit_file(profile, '-bio', new_bio)
        elif choice == '4':
            new_post_content = input("Enter the content of the new post: ")
            edit_file(profile, '-addpost', new_post_content)
        elif choice == '5':
            post_id_to_delete = input("Enter the post ID to delete: ")
            edit_file(profile, '-delpost', post_id_to_delete)
        elif choice == 'b':
            break
        else:
            print("Invalid choice. Please try again.")


def print_profile_flow(profile):
    while True:
        print("\nPrint Profile Options:")
        print("1. Print Username")
        print("2. Print Password")
        print("3. Print Bio")
        print("4. Print All Posts")
        print("5. Print Specific Post by ID")
        print("6. Print All Profile Information")
        print("B. Back")
        choice = input("Choose an option: ").lower()

        if choice == '1':
            print_file(profile, '-usr', '')
        elif choice == '2':
            print_file(profile, '-pwd', '')
        elif choice == '3':
            print_file(profile, '-bio', '')
        elif choice == '4':
            print_file(profile, '-posts', '')
        elif choice == '5':
            post_id_to_print = input("Enter the post ID to print: ")
            print_file(profile, '-post', post_id_to_print)
        elif choice == '6':
            print_file(profile, '-all', '')
        elif choice == 'b':
            break
        else:
            print("Invalid choice. Please try again.")



def admin_mode(profile):
    global global_path

    print("Admin mode activated. Type 'exit' to leave admin mode.")
    while True:
        command_line = input()
        if command_line.lower() == 'exit':
            break
        command, options = parse_command(command_line)
        handle_admin_command(command, options)

def handle_admin_command(command, options):
    global global_path
    if command == 'C':
        create_file(*options)
    elif command == "O":
        open_dsu_file(options[0])
    elif command == 'E':
        edit_file(global_path, *options)
    elif command == "P":
        print_file(global_path, *options)
 
    elif command == "L":
        path = args.get('path')
        recursive = args.get('recursive', False)
        file = args.get('file', False)
        search = args.get('search')
        extension = args.get('extension')
        list_directory(path, recursive, file, search, extension)
    elif command == 'D':
        # Extract the argument for the file path
        file_path = Path(args.get('path'))
        delete_file(file_path)
    elif command == 'R':
        # Extract the argument for the file path
        file_path = Path(args.get('path'))
        read_file(file_path)
    elif command == 'E':
        edit_file(global_path, *options)
    elif command == "P":
        print_file(global_path, *options) 
    else:
        print("Invalid command")

def menu(current_profile):
    current_profile = None
    while True:
        print("\nWelcome to the DSU file manager.")
        print("1. Create a DSU file")
        print("2. Load a DSU file")
        print("3. List directory contents")
        print("4. Delete a file")
        print("5. Read a file")
        print("6. Edit a file")
        print("7. Print a file")
        print("Q. Quit")
        choice = input("Please choose an option or 'admin' to enter admin mode: ").lower()

        if choice == '1':
            current_profile= create_file_flow()
        elif choice == '2':
            # open_dsu_file_flow()
            current_profile = open_dsu_file_flow()
        
        elif choice == '3':
            list_directory_flow()
        elif choice == '4':
            delete_file_flow()
        elif choice == '5':
            read_file_flow()
        elif choice == '6':
            print('testing')
            if current_profile:
                print('testing if file exsits...')
                edit_profile_flow(current_profile)
            else:
                print("No profile is loaded.")
        
            
        elif choice == '7':
            if current_profile:
                print("testing print file....")
                print_profile_flow(current_profile)
            else:
                print('No profile is loaded for listing')
        elif choice == 'q':
            print("Exiting program.")
            break
        elif choice == 'admin':
            admin_mode(current_profile)
            
        else:
            print("Invalid option, please try again.")