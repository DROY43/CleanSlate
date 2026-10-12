
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def require_exiftool():
    executable = shutil.which("exiftool")

    if executable is None:
        print("Error: ExifTool is not installed or not in PATH.", file=sys.stderr)
        sys.exit(1)

    return executable


def inspect_file(path, executable):
    result = subprocess.run(
        [executable, "-json", "-G1", "-a", "-s", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        print(f"Could not inspect: {path}")
        if result.stderr.strip():
            print(result.stderr.strip())
        return False

    try:
        records = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Could not read metadata report for: {path}")
        return False

    if not records or not isinstance(records[0], dict):
        print(f"No metadata report available: {path}")
        return False

    metadata = records[0]
    ignored = {"SourceFile", "ExifToolVersion"}

    print(f"\nFile: {path}")
    found = 0

    for key, value in metadata.items():
        if key in ignored:
            continue

        print(f"  {key}: {value}")
        found += 1

    if found == 0:
        print("  No additional metadata fields reported.")

    return True


def scrub_file(source, destination, executable):
    source = source.resolve()
    destination = destination.resolve()

    if not source.is_file() or source.is_symlink():
        print(f"Error: Not a regular file: {source}")
        return False

    if source == destination:
        print("Error: Cannot overwrite the original file.")
        return False

    if destination.exists():
        print(f"Error: Destination already exists: {destination}")
        return False

    destination.parent.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [
            executable,
            "-all=",
            "-o",
            str(destination),
            str(source),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0 or not destination.is_file():
        print(f"Error: Could not scrub {source}")
        if result.stderr.strip():
            print(result.stderr.strip())
        if destination.exists():
            destination.unlink()
        return False

    print(f"Original preserved: {source}")
    print(f"Cleaned copy created: {destination}")

    if result.stderr.strip():
        print(result.stderr.strip())

    print("Inspect the output to check for remaining metadata.")
    return True

def main():
    parser = argparse.ArgumentParser(
        prog="cleanslate",
        description="Inspect file metadata and create cleaned copies.",
    )

    commands = parser.add_subparsers(dest="command", required=True)

    inspect_parser = commands.add_parser(
        "inspect",
        help="Display metadata found in a file.",
    )
    inspect_parser.add_argument("file", type=Path)

    scrub_parser = commands.add_parser(
        "scrub",
        help="Create a cleaned copy of a file.",
    )
    scrub_parser.add_argument("file", type=Path)
    scrub_parser.add_argument(
        "-o",
        "--output",
        required=True,
        type=Path,
        help="Destination path for the cleaned copy.",
    )
    args = parser.parse_args()
    executable = require_exiftool()


    if args.command == "inspect":
        success = inspect_file(args.file, executable)
    elif args.command == "scrub":
        success = scrub_file(args.file, args.output, executable)
    else:
        success = False

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
