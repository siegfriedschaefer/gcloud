
import argparse
import fileinput
import sys

def replace_pattern(path, pattern1, pattern2):
    try:
        with fileinput.FileInput(path, inplace=True, encoding='utf-8', backup='.org') as file:
            for line in file:
                line = line.replace(pattern1, pattern2)
                sys.stdout.write(line)

    except FileNotFoundError:
        print(f"File {path} not found.")
    except Exception as e:
        print(f"Error occured: {e}")

    return None


def main():

    path_file = None
    pattern1 = None
    pattern2 = None

    print("exchange v0.0.1")

    parser = argparse.ArgumentParser(description="replace pattern1 with pattern2 in a text file")
    parser.add_argument("--fname", help="Input file")
    parser.add_argument("--p1", help="pattern 1")
    parser.add_argument("--p2", help="pattern 2")

    args = parser.parse_args()
    
    if args.fname:
        path_file = args.fname

    if args.p1:
        pattern1 = args.p1

    if args.p2:
        pattern2 = args.p2

    if path_file and pattern1 and pattern2:
        replace_pattern(path_file, pattern1, pattern2)

    return None

if __name__ == "__main__":
    main()
