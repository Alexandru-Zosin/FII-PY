import sys
import os
import re

def read_file(filepath):
    """Required for --help and version options."""
    try:
        with open(filepath, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        sys.exit(1)

def on_same_file_system(path1, path2):
    """Required for --one-file-system and --preserve-root=all."""
    # https://stackoverflow.com/questions/970742/is-a-file-on-the-same-filesystem-as-another-file-in-python
    # https://unix.stackexchange.com/questions/44249/how-to-check-if-two-directories-or-files-belong-to-same-filesystem
    # for consistency, using absolute paths is a good idea (even though os.stat() might resolve the path)
    abs_path1 = os.path.abspath(path1)
    abs_path2 = os.path.abspath(path2)
    if os.name == "nt": # windows
        return os.path.splitdrive(abs_path1)[0] == os.path.splitdrive(abs_path2)[0]
    else: # unix
        return os.stat(abs_path1).st_dev == os.stat(abs_path2).st_dev

def verify_pr_ofs_and_exists(path, options):
    """ Verifies - --preserve-root=all, --one-file-system and the existence of the file/directory for
        remove_file() and remove_empty_dir().
        Returns True if all checks pass, otherwise False. """
    # --preserve-root=all check
    if options["preserve_root"] == "all":
        parent_dir = os.path.abspath(os.path.join(path, os.pardir))
        try:
            if not on_same_file_system(path, parent_dir):
                print(f"rm: '{path}' is on a different file system from its parent")
                return False
        except Exception as e:
            print(f"rm: cannot access '{path}' to verify file system: {e}")
            return False

    # --one-file-system check
    if options["one_file_system"]:
        root_path = options["root_path"]  # start root path set during remove_dir() recursive delete
        try:
            if not on_same_file_system(path, root_path) and root_path:
                print(f"rm: skipping '{path}': different file system")
                return False
        except Exception as e:
            print(f"rm: cannot access '{path}' to verify file system: {e}")
            return False

    # existance check (without -f)
    if not os.path.exists(path):
        if not options["force"]:
            print(f"rm: cannot remove '{path}': No such file or directory")
        return False

    return True

def remove_file(filepath, options):
    """Removes a file."""
    if not verify_pr_ofs_and_exists(filepath, options): # some preliminary option checks
        return

    if options["dry_run"]:
        print(f"rm: would remove '{path}'")
        return

    try:
        """Otherwise, if a file is unwritable, standard input is a terminal, and the -f is not given,
        OR the -i or --interactive=always option is given, rm prompts the user for file removal."""
        if options["interactive"] == "always" or not options["force"] and not os.access(filepath, os.W_OK):
            prompt = input(f"rm: remove file '{filepath}'? [y/N] ").lower()
            if prompt != "y":
                return

        os.remove(filepath) # unlink would work as well
        if options["verbose"]:
            print(f"removed '{filepath}'")
    except Exception as e:
        print(f"rm: cannot remove '{filepath}': {e}")

def remove_empty_dir(dirpath, options):
    """Checks if a directory is empty, then deletes it."""
    if not verify_pr_ofs_and_exists(dirpath, options): # some preliminary option checks
        return

    if os.listdir(dirpath):  # checks if the directory is empty
        print(f"rm: cannot remove '{dirpath}': Directory not empty")
        return

    if options["dry_run"]:
        print(f"rm: would remove empty '{dirpath}'")
        return

    try:
        if options["interactive"] == "always":
            prompt = input(f"rm: remove empty directory '{dirpath}'? [y/N] ").lower()
            if prompt != "y":
                return
        
        os.rmdir(dirpath) # removedirs would work as well
        if options["verbose"]:
            print(f"removed empty directory '{dirpath}'")
    except Exception as e:
        print(f"rm: cannot remove '{dirpath}': {e}")

def remove_dir(dirpath, options):   
    """Removes a directory by using both remove_file() and remove_empty_dir()."""
    if options["dry_run"]:
        print(f"rm: would remove {dirpath} and its contents recursively")
        return

    if options["one_file_system"]:      # sets "corresponding command line argument" root path 
        options["root_path"] = dirpath  # for --one-file-system

    try:
        # https://stackoverflow.com/questions/10989005/do-i-understand-os-walk-right
        # root - root directory of each step (currently being processed); 
        # dirs - subdirs (one level) inside root - only their names^ 
        # files - files (one level) in the root - only their names^
        # topdown = False  ------ deepest subdirectories first (so we can delete empty folders)
        for (root, dirs, files) in os.walk(dirpath, topdown=False):
            for file_name in files: # deletes all files
                remove_file(os.path.join(root, file_name), options) 
            for empty_dir_name in dirs: # deletes directories AFTER they've been emptied 
                dir_to_remove = os.path.join(root, empty_dir_name)
                remove_empty_dir(dir_to_remove, options) 
    
        remove_empty_dir(dirpath, options) # at last, we remove the now empty main directory
    except Exception as e:
        print(f"rm: cannot remove '{dirpath}': {e}")

def parse_command(args):
    """Parses the command into options and paths."""
    options = {
        "force": False,
        "interactive": "never",
        "one_file_system": False,  # applies only during recursion
        "preserve_root": True,
        "recursive": False,
        "dir": False,
        "verbose": False,
        "dry_run": False,
    }
    short_options = ["f", "i", "I", "r", "R", "d", "v"]
    long_options = [
        "--force",
        "--interactive", "--interactive=never", "--interactive=once", "--interactive=always",
        "--one-file-system", # applies only during recursion
        "--dry-run",
        "--no-preserve-root", # does not treat '/' specially
        "--preserve-root", # protects "/" (NOT REMOVABLE)
        "--preserve-root=all", # extends --p-r and applies individually (paths and parent on the same FS)
        "--recursive",
        "--dir",
        "--verbose",
        "--help",
        "--version",
    ]
    paths = []

    for arg in args:
        """To remove a file whose name starts with a '-', for example
           '-foo', use rm ./-foo"""
        if arg.startswith("-") and not os.path.exists(arg): 
            if arg.startswith("--"): # LONG option
                if arg not in long_options:
                    print(f"rm: invalid option '{arg}'")
                    print("Try 'rm --help' for more information.")
                    sys.exit(1)

                if arg == "--force":
                    options["force"] = True
                elif arg.startswith("--interactive"):
                    if "=" in arg:
                        options["interactive"] = arg.split("=", 1)[1]
                    else:
                        options["interactive"] = "always"
                elif arg == "--one-file-system":
                    options["one_file_system"] = True
                elif arg == "--dry-run":
                    options["dry_run"] = True
                elif arg == "--no-preserve-root":
                    options["preserve_root"] = False
                elif arg == "--preserve-root=all":
                    options["preserve_root"] = "all"
                elif arg == "--preserve-root":
                    options["preserve_root"] = True
                elif arg == "--recursive":
                    options["recursive"] = True
                elif arg == "--dir":
                    options["dir"] = True
                elif arg == "--verbose":
                    options["verbose"] = True
                elif arg == "--help":
                    print(read_file("help.txt"))
                    sys.exit(0)
                elif arg == "--version":
                    print(read_file("version.txt"))
                    sys.exit(0)
            else: # SHORT option
                for char in arg[1:]: # supports "chained" options (e.g. -rf...)
                    if char not in short_options:
                        print(f"rm: invalid option '-{char}'")
                        print("Try 'rm --help' for more information.")
                        sys.exit(1)

                    if char == "f":
                        options["force"] = True
                    elif char == "i":
                        options["interactive"] = "always"
                    elif char == "I":
                        options["interactive"] = "once"
                    elif char == "r" or char == "R":
                        options["recursive"] = True
                    elif char == "d":
                        options["dir"] = True
                    elif char == "v":
                        options["verbose"] = True
        else:
            paths.append(arg)

    return options, paths

def expand_wildcards_with_regex(paths):
    """Supports * and ? for filenames."""
    expanded_paths = []
    for path in paths:
        if '*' in path or '?' in path:  # supported wildcards by our OwnRM
            dir_name, pattern = os.path.split(path) # (head, tail<=>last component) | ("...", "head.txt")
            if not dir_name: # for example, for an original path like "*.txt"
                dir_name = '.' # program search defaults to current directory correctly
            try:
                """escape() is required so we avoid interpreting (other) special regex characters,
                   as it returns string with all non-alphanumerics backslashed (which will later
                   get restored to the original literal in regex (slash being the escape code); 
                   it's useful when matching a string with regex metacharacters in it."""
                # replace "\*" with .(all chars w\o \n)*(>=0 reps); replace "\?" with .(1 rep)
                # according to course 8, "$" matches end of the string (JUST BEFORE a newline \n),
                # while apparently "\Z" is better (includes string ending with \n)
                regex_pattern = re.escape(pattern).replace(r'\*', '.*').replace(r'\?', '.') + "$"
                regex = re.compile(regex_pattern)
                for entry in os.listdir(dir_name): # all files & directories in this path
                    if regex.match(entry):
                        expanded_paths.append(os.path.join(dir_name, entry))
            except Exception as e:
                print(f"rm: cannot access '{dir_name}': {e}")
        else:
            expanded_paths.append(path)
    return expanded_paths

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("rm: missing operand")
        print("Try 'rm --help' for more information.")
        sys.exit(1)

    options, paths = parse_command(sys.argv[1:])
    paths = expand_wildcards_with_regex(paths)
    
    ### --no-preserve-root check (os.remove() does NOT have built-in safeguards)
    if options["preserve_root"] and "/" in paths: # includes --preserve-root=all
        print("rm: it is dangerous to operate recursively on '/'")
        print("Use '--no-preserve-root' to override this failsafe (not allowed on Windows).")
        sys.exit(1)
    if not options["preserve_root"] and os.name == "nt":
        print("rm: the option '--no-preserve-root' is not allowed on Windows for safety reasons.")
        sys.exit(1)
    
    # after this, IF not options["preserve_root"] <==> preserve_root = False <==> --no-preserve-root,
    # ANY POSSIBLE DELETE IS PERMITTED!
    
    """If the -I or --interactive=once is given, and there are more than 3 files or the -r is given,
       then rm prompts the user to proceed with the entire operation (or entirely abort it)."""
    if options["interactive"] == "once" and (options["recursive"] or len(paths) > 3):
        prompt = input("rm: remove multiple files or directories recursively? [y/N] ").lower()
        if prompt != "y":
            sys.exit(1)
    # after this, -I or --interactive=once DOESN'T NEED to be checked again, only NEVER or ALWAYS

    for path in paths:
        """Any attempt to remove a file whose last file name component is
           . or ..  is rejected with a diagnostic. """
        # https://docs.python.org/3/library/os.path.html#os.path.basename
        base_name = os.path.basename(path)
        if base_name in [".", ".."]:
            print(f"rm: cannot remove '{path}': Invalid argument")
            continue

        if os.path.isdir(path):
            if options["recursive"]:
                remove_dir(path, options)
            elif options["dir"]:
                remove_empty_dir(path, options)
            else:
                print(f"rm: cannot remove '{path}': Is a directory")
        else:
            remove_file(path, options)