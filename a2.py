# a2.py


from pathlib import Path
from Profile import Post, Profile, DsuFileError, DsuProfileError
import time
import ui
# from ui import menu,parse_command
# Global variable to store the path to the DSU file



def run():
    # global global_path  # Use the global variable

    while True:
        user_input = input()
        command, options = ui.parse_command(user_input)

        try:
            if command == 'Q':
                break
            
            elif command == 'D':
                path = options[0]
                ui.delete_file(Path(path))
            elif command == 'R':
                path = options[0]
                ui.read_file(Path(path))
            elif command == 'L':
                path = options[0] if options else None
                recursive = '-r' in options
                file = '-f' in options
                search = options[options.index('-s') + 1] if '-s' in options else None
                extension = options[options.index('-e') + 1] if '-e' in options else None
                if path is None:
                    print("Please enter the path for 'L' command")
                else:
                    ui.list_directory(path, recursive, file, search, extension)
            elif command == 'C':
                if '-n' in options:
                    name_index = options.index('-n') + 1
                    directory = Path.cwd()  # Current directory, change if needed
                    name = options[name_index] if name_index < len(options) else None
                    ui.create_file(directory, name)
                else:
                    print("Please specify a file name with -n flag.")
                
            elif command == "O":
                if options:
                    file_path = options[0]
                    ui.open_dsu_file(file_path)
                else:
                    print("No file path provided to open.")

                
            elif command == 'E':
                if  ui.global_path:
                    profile = Profile()
                    profile.load_profile(ui.global_path)
                    operate = options[0]
                    value = ' '.join(options[1:])  # Joining all remaining options as the value, assuming space-delimited input 
                    ui.edit_file(profile, operate, value)

            elif command == "P":
                if ui.global_path:
                    profile = Profile()
                    profile.load_profile(ui.global_path)                 
                    operate = options[0]
                    value = ' '.join(options[1:]) 
                    ui.print_file(profile, operate, value)         
                    
            
        except Exception as e:
            print(f"ERROR: {e}")

def main():
    
    profile = None
    ui.menu(profile)

if __name__ == "__main__":
    main()
