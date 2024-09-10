import re
import logging
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
from typing import List, Dict, Tuple, DefaultDict, Iterable
import requests
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Stop words list (you can expand it or use libraries like nltk)
STOP_WORDS = {"a", "the", "in", "at", "on", "for", "with", "to", "is", "it", "and", "but", "or", "of", "an"}

def fetch_text_from_url(url: str, timeout: int = 10) -> str:
    """
    Fetches the text content from a given URL with a specified timeout.

    Args:
        url (str): The URL to fetch the text from.
        timeout (int): The maximum time (in seconds) to wait for a response. Default is 10 seconds.

    Returns:
        str: The text content from the URL.
    
    Raises:
        requests.RequestException: If there is any issue with the URL fetching.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching URL {url}: {e}")
        raise

def map_function(text: str) -> List[Tuple[str, int]]:
    """
    Map function that splits the text into words and assigns a count of 1 to each word.

    Args:
        text (str): The input text.

    Returns:
        List[Tuple[str, int]]: A list of tuples where each tuple contains a word and its count (1).
    """
    words = re.findall(r'\b\w+\b', text.lower())
    # Filter out stop words
    filtered_words = [word for word in words if word not in STOP_WORDS]

    return [(word, 1) for word in filtered_words]

def shuffle_function(mapped_values: List[Tuple[str, int]]) -> Iterable[Tuple[str, List[int]]]:
    """
    Shuffle function that groups the mapped values by word.

    Args:
        mapped_values (List[Tuple[str, int]]): A list of tuples (word, 1).

    Returns:
        Iterable[Tuple[str, List[int]]]: Grouped items where each word is a key and the values are a list of counts.
    """
    shuffled: DefaultDict[str, List[int]] = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(shuffled_values: Iterable[Tuple[str, List[int]]]) -> Dict[str, int]:
    """
    Reduce function that sums the word counts for each word.

    Args:
        shuffled_values (Iterable[Tuple[str, List[int]]]): Grouped word counts.

    Returns:
        Dict[str, int]: A dictionary where keys are words and values are their total counts.
    """
    reduced: Dict[str, int] = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced

def map_reduce(text: str) -> Dict[str, int]:
    """
    Executes the MapReduce process on the input text.

    Args:
        text (str): The input text to be processed.

    Returns:
        Dict[str, int]: A dictionary with word counts.
    """
    try:
        # Step 1: Mapping
        mapped_values = map_function(text)

        # Step 2: Shuffle
        shuffled_values = shuffle_function(mapped_values)

        # Step 3: Reduce
        reduced_values = reduce_function(shuffled_values)

        return reduced_values
    except Exception as e:
        logging.error(f"Error during MapReduce: {e}")
        return {}

def visualize_top_words(word_counts: Dict[str, int], top_n: int = 10) -> None:
    """
    Visualizes the top N words by frequency.

    Args:
        word_counts (Dict[str, int]): A dictionary of word counts.
        top_n (int): The number of top words to display.

    Returns:
        None
    """
    try:
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
        words, counts = zip(*sorted_words)

        plt.figure(figsize=(10, 5))
        plt.bar(words, counts, color='skyblue')
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.title(f'Top {top_n} Words by Frequency')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        logging.error(f"Error during visualization: {e}")

def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments to get the URLs and maximum workers.

    Returns:
        argparse.Namespace: Parsed command-line arguments containing the URLs and max_workers.
    """
    parser = argparse.ArgumentParser(description="Analyze word frequency from multiple URLs using MapReduce.")
    parser.add_argument('urls', nargs='+', type=str, help='The URLs to fetch the text from.')
    parser.add_argument('--max-workers', type=int, default=5, help='The maximum number of concurrent requests.')
    return parser.parse_args()

if __name__ == '__main__':
    # Parse the URLs and max_workers from command line arguments
    args = parse_arguments()
    urls = args.urls
    max_workers = args.max_workers
    
    # Fetch text and perform MapReduce in parallel for multiple URLs
    try:
        all_word_counts = defaultdict(int)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(fetch_text_from_url, url): url for url in urls}

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    text = future.result()
                    # Perform MapReduce for each text
                    word_counts = map_reduce(text)

                    # Aggregate results from all URLs
                    for word, count in word_counts.items():
                        all_word_counts[word] += count

                except Exception as e:
                    logging.error(f"Error processing {url}: {e}")

        # Visualize top 10 most frequent words across all URLs
        visualize_top_words(all_word_counts, top_n=10)
    except Exception as e:
        logging.error(f"Error in main execution: {e}")

