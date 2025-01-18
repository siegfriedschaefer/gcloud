
import argparse

def extract_transcript(input_file, output_file, pattern):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                if pattern in line:
                    outfile.write(line)
    except FileNotFoundError:
         print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")

    return None

def main():

    input_file = None
    output_file = None
    pattern = "Sprecher A"

    print("extract_transcript v0.0.1")

    parser = argparse.ArgumentParser(description="extract lines which contains a given pattern in a text file")
    parser.add_argument("--ifile", help="File to analyse")
    parser.add_argument("--ofile", help="output file")
    parser.add_argument("--p", help="pattern")

    args = parser.parse_args()
    
    if args.ifile:
        input_file = args.ifile
    if args.ofile:
        output_file = args.ofile
    if args.p:
        pattern = args.p

    extract_transcript(input_file, output_file, pattern)

    return None

if __name__ == "__main__":
    main()
