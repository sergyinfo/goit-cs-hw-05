
# Asynchronous File Sorter by Extension

This application asynchronously reads files from a specified source folder, sorts them based 
on their extensions, and copies them to corresponding subfolders in a target folder. 
It is optimized to handle a large number of files with parallel task limits.

## Features

- Asynchronous file operations for faster sorting
- Supports copying files into subfolders based on their extensions
- Limits the number of concurrent tasks to avoid overloading
- Command-line arguments for source folder, target folder, and parallel task limit

## Requirements

- Python 3.7 or later
- `aiofiles` library for asynchronous file handling

### Install dependencies

```bash
pip install aiofiles
```

## Usage

1. **Create a mock source folder for testing** (optional):
   
   Run the provided script to create a folder with test files:

   ```bash
   python mock_source_folder.py
   ```

   This will create a `mock_source_folder` in your current directory with test files.

2. **Run the file sorter**:

   To run the file sorter, use the following command:

   ```bash
   python main.py <source_folder> <output_folder> --max-tasks <number_of_parallel_tasks>
   ```

   - `<source_folder>`: The path to the folder containing the files you want to sort.
   - `<output_folder>`: The path to the folder where you want the sorted files to be copied.
   - `--max-tasks`: (Optional) The maximum number of parallel tasks. Default is 5.

   Example:
   
   ```bash
   python main.py mock_source_folder sorted_files --max-tasks 10
   ```

   This will sort files from `mock_source_folder` into `sorted_files` folder, copying files into subfolders based on their extensions, with a maximum of 10 parallel tasks.

## Example

If you create a `mock_source_folder` with the provided script, running the sorter will copy files into subfolders like this:

```
sorted_files/
├── jpg/
│   ├── image1.jpg
│   └── root_image.jpg
├── mp4/
│   └── video1.mp4
├── pdf/
│   └── test2.pdf
├── txt/
│   ├── root_file1.txt
│   └── test1.txt
└── ...
```