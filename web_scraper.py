"""Web scraper for extracting and chunking text from websites."""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import hashlib


class WebScraper:
    """Scrapes web content and creates chunks for vector storage."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize web scraper.

        Args:
            chunk_size: Maximum size of each text chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def fetch_url(self, url: str) -> str:
        """
        Fetch and extract text from a URL.

        Args:
            url: URL to fetch

        Returns:
            Extracted text content
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()

            # Get text
            text = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            return text

        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""

    def chunk_text(self, text: str, source_url: str) -> List[Dict[str, str]]:
        """
        Split text into overlapping chunks.

        Args:
            text: Text to chunk
            source_url: Source URL for metadata

        Returns:
            List of dictionaries containing chunk text and metadata
        """
        chunks = []
        start = 0
        chunk_id = 0

        # Create a unique prefix based on URL
        url_hash = hashlib.md5(source_url.encode()).hexdigest()[:8]

        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]

            # Try to break at a sentence or paragraph boundary
            if end < len(text):
                # Look for paragraph break first
                last_para = chunk.rfind('\n\n')
                if last_para > self.chunk_size // 2:
                    end = start + last_para
                    chunk = text[start:end]
                else:
                    # Look for sentence break
                    last_period = max(chunk.rfind('. '), chunk.rfind('.\n'))
                    if last_period > self.chunk_size // 2:
                        end = start + last_period + 1
                        chunk = text[start:end]

            chunks.append({
                "id": f"web_{url_hash}_{chunk_id}",
                "text": chunk.strip(),
                "start_pos": start,
                "end_pos": end,
                "source": source_url
            })

            chunk_id += 1
            start = end - self.chunk_overlap

        return chunks

    def process_url(self, url: str) -> List[Dict[str, str]]:
        """
        Fetch and chunk content from a URL.

        Args:
            url: URL to process

        Returns:
            List of text chunks with metadata
        """
        print(f"Fetching {url}...")
        text = self.fetch_url(url)

        if not text:
            print(f"  No content extracted from {url}")
            return []

        chunks = self.chunk_text(text, url)
        print(f"  Extracted {len(chunks)} chunks from {url}")
        return chunks

    def process_urls(self, urls: List[str]) -> List[Dict[str, str]]:
        """
        Process multiple URLs.

        Args:
            urls: List of URLs to process

        Returns:
            Combined list of all chunks
        """
        all_chunks = []
        for url in urls:
            chunks = self.process_url(url)
            all_chunks.extend(chunks)

        print(f"\nTotal: {len(all_chunks)} chunks from {len(urls)} URLs")
        return all_chunks
