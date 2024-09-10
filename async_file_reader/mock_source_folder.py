from pathlib import Path

def create_source_folder(base_path: str):
    """
    Creates a mock source folder with a few test files and subfolders for testing.

    Args:
        base_path (str): The base path where the mock folder will be created.

    Returns:
        None
    """
    # Create the base folder
    base_folder = Path(base_path)
    base_folder.mkdir(parents=True, exist_ok=True)

    # Define some subfolders and files
    files = {
        'folder1': ['test1.txt', 'test2.pdf', 'image1.jpg'],
        'folder2': ['test3.docx', 'image2.png', 'video1.mp4'],
        '': ['root_file1.txt', 'root_image.jpg']  # Files in the root of base folder
    }

    # Create subfolders and files
    for folder, file_list in files.items():
        folder_path = base_folder / folder
        if folder:
            folder_path.mkdir(parents=True, exist_ok=True)
        for file_name in file_list:
            file_path = folder_path / file_name
            file_path.write_text(f"This is a mock file: {file_name}")

    print(f"Mock source folder created at: {base_folder.absolute()}")

if __name__ == "__main__":
    create_source_folder("mock_source_folder")
