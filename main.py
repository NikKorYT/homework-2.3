# Write a program to process directory, which copies files from the given directory (and all its subdirectories) to the target directory, sorting them by extensions. The program should use multithreading to efficiently process large volumes of files and subdirectories.
import time
import shutil
from pathlib import Path
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor

# Initialize colorama with autoreset set to True. This means that every print statement will be in default color.
init(autoreset=True)


def get_path() -> str:
    """
    This function asks the user to enter a directory path.
    """
    # Get the directory path from the user
    path = input("Enter the directory path: ")
    # Check if the path is valid
    if not Path(path).exists():
        print(Fore.RED + "Invalid path. Please enter a valid directory path.")
        return get_path()
    return path


def get_filtered_path() -> str:

    filtered_path = input("Enter the directory path for filtered files: ")
    # Check if the path is valid
    if not Path(filtered_path).exists():
        print(Fore.RED + "Invalid path. Please enter a valid directory path.")
        return get_path()

    return filtered_path


def get_filtered_path() -> str:
    """
    This function asks the user to enter a directory path.
    """
    # Get the directory path from the user
    path = input("Enter the directory path for filtered files: ")
    # Check if the path is valid
    if not Path(path).exists():
        print(Fore.RED + "Invalid path. Please enter a valid directory path.")
        return get_path()

    return path


def print_dir(path, prefix=""):
    """
    This function prints the directory structure for the given path.
    """
    # Get a list of all items in the directory
    contents = list(path.iterdir())

    # Create a list of pointers. If the item is not the last one, use '┣ ', else use '┗ '
    pointers = ["┣ " if i != len(contents) - 1 else "┗ " for i in range(len(contents))]

    # Loop through each item in the directory
    for pointer, sub_path in zip(pointers, contents):

        # If the item is a directory, print it with the '📂' emoji and recurse into this directory
        if sub_path.is_dir():
            print(prefix + pointer + Fore.GREEN + "📂 " + sub_path.name)
            new_prefix = prefix + ("┃ " if pointer == "┣ " else "  ")
            print_dir(sub_path, new_prefix)

        # If the item is a file, print it with the '📄' emoji
        else:
            print(prefix + pointer + Fore.WHITE + "📄 " + sub_path.name)


def filter_files(path_to_filter: str = None, filtered_path: str = None) -> None:
    """
    This function filters the files in the given directory path based on the file extension.

    """
    path_to_filter = Path(path_to_filter)
    filtered_path = Path(filtered_path)

    # Get a list of all items in the directory
    contents = list(path_to_filter.iterdir())
    # If the item is a file, filter it based on the file extension and if it is a directory, iterate through it contents
    with ThreadPoolExecutor() as executor:
        for sub_path in contents:
            if sub_path.is_dir():
                executor.submit(filter_files, sub_path, filtered_path)
            else:
                # Get the file extension
                file_extension = sub_path.suffix[1:] if sub_path.suffix else "no_extension"
                # Create a new directory with the file extension if it does not exist, and if it does, COPY the file to that directory
                new_dir = filtered_path / file_extension
                new_dir.mkdir(exist_ok=True)
                try:
                    shutil.copy(sub_path, new_dir / sub_path.name)
                except OSError as e:
                    print(
                        f"Error copying file {sub_path} to {new_dir / sub_path.name}: {e}"
                    )
            


if __name__ == "__main__":

    # Get the directory path from the user
    path = Path(get_path())
    filtered_path = Path(get_filtered_path())
    
    # Start timing
    start_time = time.time()
    
    # FIlter the files
    filter_files(path, filtered_path)

    # Print the directory structure
    print("This is the directory structure after filtering:")
    print_dir(Path(filtered_path))

    # End timing
    end_time = time.time()

    # Calculate and print the elapsed time
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
