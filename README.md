# CleanSlate
A local CLI tool for inspecting and removing Metadata.
# CleanSlate

CleanSlate is a lightweight, local-first command-line tool for inspecting and removing metadata from files. It uses ExifTool to process supported file formats while preserving the original files.

The project aims to make metadata management accessible through a simple interface, with an emphasis on privacy, transparency, and user control.

## Features

* Inspect metadata associated with supported files.
* Create cleaned copies with metadata removal attempted.
* Preserve original files during processing.
* Run locally without requiring a cloud service or account.
* Use ExifTool for broad file-format support.

## Requirements

* Python 3.10 or later
* ExifTool installed and available in your system PATH

ExifTool is available for Linux, macOS, and Windows. Installation instructions can be found at https://exiftool.org/.

## Installation

Clone the repository:

```
git clone https://github.com/YOUR-USERNAME/cleanslate.git
cd cleanslate
```

Create and activate a virtual environment:

```
python -m venv .venv
```

On Linux and macOS:

```
source .venv/bin/activate
```

On Windows:

```
.venv\Scripts\activate
```

Install ExifTool separately using the instructions for your operating system.

## Usage

Inspect a file's metadata:

```
python cleanslate.py inspect path/to/file.jpg
```

Create a cleaned copy:

```
python cleanslate.py scrub path/to/file.jpg -o path/to/file-clean.jpg
```

Replace the example paths with the actual paths to your files. The scrub command writes to a separate destination and is designed to preserve the original file.

To view available commands and options:

```
python cleanslate.py --help
```

## Privacy and limitations

CleanSlate is designed to run locally. It does not require uploading files to an external service.

Metadata removal depends on the file format and the capabilities of ExifTool. Removing metadata does not guarantee anonymity, and some identifying information may remain in file contents, filenames, or unsupported metadata structures. Always inspect cleaned files before sharing them.

## License

See the repository's license file for terms of use and redistribution.
