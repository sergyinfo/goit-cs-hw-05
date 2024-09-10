
# Asynchronous Word Frequency Analyzer

This Python application asynchronously fetches text from multiple URLs, analyzes the word frequency using the MapReduce paradigm, and visualizes the most frequent words while excluding common stop words.

## Features

- Asynchronous fetching of text from multiple URLs.
- Stop words filtering to exclude common words like 'a', 'the', 'in', etc.
- MapReduce processing for efficient word count analysis.
- Visualization of the top N most frequent words.

## Requirements

- Python 3.7 or later
- `requests` library for HTTP requests
- `matplotlib` library for visualization

### Install dependencies

```bash
pip install requests matplotlib
```

## Usage

### Command-Line Arguments

1. **URLs**: Provide one or more URLs to fetch the text from. Each URL should be a valid HTTP/HTTPS link.
2. **--max-workers**: (Optional) Specifies the maximum number of concurrent requests. The default is 5.

### Example

To analyze word frequency from multiple URLs:

```bash
python word_frequency.py https://example.com/text1 https://example.com/text2 --max-workers 3
```

### Visualization

The application will display a bar chart showing the top 10 most frequent words after filtering out common stop words.

## Stop Words

By default, the application filters out common stop words like:

```
"a", "the", "in", "at", "on", "for", "with", "to", "is", "it", "and", "but", "or", "of", "an"
```

You can easily modify the list of stop words in the code by updating the `STOP_WORDS` set.
