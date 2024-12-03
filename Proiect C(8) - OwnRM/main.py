import sys
import os

def read_file(filepath):
    try:
        with open(filepath, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        sys.exit(1)

def on_same_file_system(path1, path2):
    # https://stackoverflow.com/questions/970742/is-a-file-on-the-same-filesystem-as-another-file-in-python
    return os.stat(path1).st_dev == os.stat(path2).st_dev

def remove_file(filepath, options):
    if options["dry_run"]:
        print(f"rm: would remove {filepath}")
        return

    if not os.path.exists(filepath):
        if not options["force"]:
            print(f"rm: cannot remove '{filepath}': No such file or directory")
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
    if options["dry_run"]:
        print(f"rm: would remove empty directory '{dirpath}'")
        return

    if not os.path.exists(dirpath):
        if not options["force"]:
            print(f"rm: cannot remove '{dirpath}': No such file or directory")
        return

    if os.listdir(dirpath):  # checks if the directory is empty
        print(f"rm: cannot remove '{dirpath}': Directory not empty")
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
    if options["dry_run"]:
        print(f"rm: would remove {dirpath} and its contents recursively")
        return

    try:
        # root - abs. path to directory currently being processed; 
        # dirs - subdirs in root; 
        # files - files in the root
        # topdown = False  ------ deepest subdirectories first (so we can delete empty folders)
        for (root, dirs, files) in os.walk(dirpath, topdown=False): 
            # skips directories on different file systems if --one-file-system is enabled
            if options["one_file_system"] and not on_same_file_system(root, dirpath):
                print(f"Skipping '{root}': different file system")
                continue
            for file_name in files: # deletes all files
                remove_file(os.path.join(root, file_name), options) 
            for empty_dir_name in dirs: # deletes directories AFTER they've been emptied 
                dir_to_remove = os.path.join(root, empty_dir_name)
                remove_empty_dir(dir_to_remove, options) 
    
        remove_empty_dir(dirpath, options) # at last, we remove the now empty main directory
    except Exception as e:
        print(f"rm: cannot remove '{dirpath}': {e}")

def parse_command(args):
    options = {
        "force": False,
        "interactive": "never",
        "one_file_system": False,
        "preserve_root": True,
        "recursive": False,
        "dir": False,
        "verbose": False,
        "dry_run": False,
    }
    short_options = ["-f", "-i", "-I", "-r", "-R", "-d", "-v"]
    long_options = [
        "--force",
        "--interactive", "--interactive=never", "--interactive=once", "--interactive=always",
        "--one-file-system",
        "--dry-run",
        "--no-preserve-root",
        "--preserve-root",
        "--preserve-root=all",
        "--recursive",
        "--dir",
        "--verbose",
        "--help",
        "--version",
    ]
    files = []

    for arg in args:
        if arg.startswith("-"):
            if arg.startswith("--"):
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
            else:
                for char in arg[1:]:
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
            files.append(arg)

    return options, files

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("rm: missing operand")
        print("Try 'rm --help' for more information.")
        sys.exit(1)

    options, files = parse_command(sys.argv[1:])
    
    if options["preserve_root"] and "/" in files:
        print("rm: it is dangerous to operate recursively on '/'")
        print("Use '--no-preserve-root' to override this failsafe (not allowed on Windows).")
        sys.exit(1)
    if not options["preserve_root"] and os.name == "nt":
        print("rm: the option '--no-preserve-root' is not allowed on Windows for safety reasons.")
        sys.exit(1)
    # os.remove() does NOT have built-in safeguards
    
    # after this, IF not options["preserve_root"] <==> preserve_root = False <==> --no-preserve-root,
    # ANY POSSIBLE DELETE IS PERMITTED!
    
    """If the -I or --interactive=once is given, and there are more than 3 files or the -r is given,
       then rm prompts the user to proceed with the entire operation (or entirely abort it)."""
    if options["interactive"] == "once" and (options["recursive"] or len(files) > 3):
        prompt = input("rm: remove multiple files or directories recursively? [y/N] ").lower()
        if prompt != "y":
            sys.exit(1)
    # after this, -I or --interactive=once DOESN'T NEED to be checked again, only NEVER or ALWAYS

    for file in files:
        if os.path.isdir(file):
            if options["recursive"]:
                remove_dir(file, options)
            elif options["dir"]:
                remove_empty_dir(file, options)
            else:
                print(f"rm: cannot remove '{file}': Is a directory")
        else:
            remove_file(file, options)