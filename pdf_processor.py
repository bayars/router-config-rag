"""PDF processor for extracting and chunking text from SR Linux documentation."""

from pypdf import PdfReader
from typing import List, Dict


class PDFProcessor:
    """Processes PDF documents and extracts text in chunks."""

    def __init__(self, pdf_path: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize PDF processor.

        Args:
            pdf_path: Path to the PDF file
            chunk_size: Maximum size of each text chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.pdf_path = pdf_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def extract_text(self) -> str:
        """Extract all text from the PDF."""
        reader = PdfReader(self.pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def chunk_text(self, text: str) -> List[Dict[str, str]]:
        """
        Split text into overlapping chunks.

        Args:
            text: Text to chunk

        Returns:
            List of dictionaries containing chunk text and metadata
        """
        chunks = []
        start = 0
        chunk_id = 0

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
                "id": f"chunk_{chunk_id}",
                "text": chunk.strip(),
                "start_pos": start,
                "end_pos": end
            })

            chunk_id += 1
            start = end - self.chunk_overlap

        return chunks

    def process(self) -> List[Dict[str, str]]:
        """
        Process the PDF and return chunks.

        Returns:
            List of text chunks with metadata
        """
        text = self.extract_text()
        chunks = self.chunk_text(text)
        print(f"Processed PDF into {len(chunks)} chunks")
        return chunks
