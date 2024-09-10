"""
A simple asynchronous file reader that reads files from a source folder and copies them to a target folder

To run the script, you can provide the source and target folder paths as command-line arguments:
    python main.py source_folder target_folder --max-tasks 5


"""
import os
import asyncio
from pathlib import Path
import logging
import argparse
import aiofiles

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def read_folder(source_folder: Path, output_folder: Path, semaphore: asyncio.Semaphore):
    """
    Asynchronously reads all files from the source folder and its subfolders
    and copies them to the target folder based on their file extension.

    Args:
        source_folder (Path): The path to the source folder containing files.
        output_folder (Path): The path to the target folder where sorted files will be copied.
        semaphore (asyncio.Semaphore): Semaphore to limit the number of parallel tasks.
    
    Returns:
        None
    """
    tasks = []
    try:
        for root, _, files in os.walk(source_folder):  # dirs is ignored as it's not used
            for file in files:
                file_path = Path(root) / file
                tasks.append(copy_file(file_path, output_folder, semaphore))

        await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f"Error while reading folder {source_folder}: {e}")


async def copy_file(file_path: Path, output_folder: Path, semaphore: asyncio.Semaphore):
    """
    Asynchronously copies a file to a subfolder in the target folder based on its extension.

    Args:
        file_path (Path): The path to the file to be copied.
        output_folder (Path): The path to the folder where files will be copied.
        semaphore (asyncio.Semaphore): Semaphore to limit the number of parallel tasks.

    Returns:
        None
    """
    async with semaphore:
        extension = file_path.suffix[1:].lower()  # Get the file extension
        target_folder = output_folder / extension

        try:
            # Create target folder if it doesn't exist
            if not target_folder.exists():
                logging.info(f'Creating directory: {target_folder}')
                target_folder.mkdir(parents=True, exist_ok=True)

            target_path = target_folder / file_path.name

            # Asynchronously copy the file
            logging.info(f'Copying {file_path} to {target_path}')
            async with aiofiles.open(file_path, 'rb') as fsrc:
                data = await fsrc.read()
                async with aiofiles.open(target_path, 'wb') as fdst:
                    await fdst.write(data)

        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
        except PermissionError:
            logging.error(f"Permission denied: {file_path}")
        except Exception as e:
            logging.error(f"Error copying {file_path} to {target_path}: {e}")


def parse_arguments():
    """
    Parses command-line arguments to get the source and output folder paths.

    Returns:
        argparse.Namespace: Parsed arguments containing the paths to source_folder and output_folder.
    """
    parser = argparse.ArgumentParser(description="Asynchronous file sorting by extension.")
    parser.add_argument('source_folder', type=str, default="source", help='The source folder containing the files.')
    parser.add_argument('output_folder', type=str, default="destination", help='The target folder to store sorted files.')
    parser.add_argument('--max-tasks', type=int, default=5, help='Maximum number of parallel tasks (default is 5).')
    
    return parser.parse_args()


async def main():
    """
    The main asynchronous function that coordinates the reading and copying of files.
    It parses command-line arguments, validates folders, and starts the file sorting process.

    Returns:
        None
    """
    try:
        args = parse_arguments()

        source_folder = Path(args.source_folder)
        output_folder = Path(args.output_folder)
        max_tasks = args.max_tasks

        if not source_folder.exists():
            logging.error(f'Source folder {source_folder} does not exist!')
            return

        if not output_folder.exists():
            logging.info(f'Creating output directory: {output_folder}')
            output_folder.mkdir(parents=True, exist_ok=True)

        # Create a semaphore to limit the number of concurrent tasks
        semaphore = asyncio.Semaphore(max_tasks)

        await read_folder(source_folder, output_folder, semaphore)
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")


if __name__ == "__main__":
    # Start the asynchronous event loop
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Process interrupted by user.")
    except Exception as e:
        logging.error(f"Error running the main function: {e}")
