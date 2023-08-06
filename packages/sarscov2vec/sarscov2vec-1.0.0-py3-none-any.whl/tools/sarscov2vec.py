import os

from typing import Set

import pandas as pd
from pandas.core.series import Series

from Bio.SeqIO.FastaIO import FastaIterator
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq


class FastaReader:
    """
    Parse FASTA file with nucleotide sequences
    """
    
    def __init__(self, fasta_file_path: str):
        self.fasta_file_path = fasta_file_path
        self.fasta_name = os.path.basename(self.fasta_file_path)
        self.sequence = None
        self.entities = 0

    @staticmethod
    def _fasta_reader(filename: str) -> SeqRecord:
        with open(filename) as handle:
            for record in FastaIterator(handle):
                yield record

    @staticmethod
    def _normalise_sequence(entry: SeqRecord) -> str:
        """
        Normalize sequence to upper case (remove blank chars at the end of sequence)
        """
        
        return str(entry.seq).upper().strip()

    def get_sequence(self) -> str:
        """
        Return all entities as one long string
        """

        sequences = []

        for entry in self._fasta_reader(self.fasta_file_path):
            sequences.append(self._normalise_sequence(entry))
            self.entities += 1

        self.sequence = " ".join(sequences)

        return self.sequence


class KMersTransformer:
    """
    K-mer transformer is responsible to extract set of words -
    using configurable sliding window - which are subsequences
    of length (6 by default) contained within a biological sequence

    Each of the word is called k-mer and are composed of nucleotides
    (i.e. A, T, G, and C). Each word which includes other characters
    is removed from the output
    """

    def __init__(self, size: int = 6, sliding_window: int = 1):
        self.accepted_chars: Set[str] = {"A", "C", "T", "G"}
        self.size: int = size
        self.sliding_window: int = sliding_window

    def _normalise_sequence(self, sequence: str) -> str:
        """
        Return normalised upper-case sequence without blank chars 
        """

        return sequence.strip().upper()
        
    def _extract_kmers_from_sequence(self, sequence: str) -> str:
        """
        K-mer transformer with sliding window method,
        where each k-mer has size of 6 (by default)

        A sliding window is used to scan the entire sequence,
        if the k-mer contains unsupported character then the
        whole k-mer is ignored (not included in final string)

        Method return a string with k-mers separated by space
        what is expected as input for embedding
        """

        # Genome normalization
        sequence = self._normalise_sequence(sequence)
        
        seq_length = len(sequence)

        kmers = " ".join(
            [
                sequence[x : x + self.size]
                for x in range(0, seq_length - self.size + 1, self.sliding_window)
                if not set(sequence[x : x + self.size]) - self.accepted_chars
            ]
        )

        # If sequence length is not div by sliding window value
        # then the last k-mer need to be added
        if self.sliding_window > 1 and (seq_length - self.size) % self.sliding_window != 0:
            # Last k-mer
            kmers += f" {sequence[-self.size:]}"

        return kmers

    def transform(self, df: pd.DataFrame) -> Series:
        """
        Execute k-mer transformer on each DNA sequence
        and return it as Series with k-mers strings
        """

        # sequence column is expected
        assert list(df.columns) == ["sequence"]

        return df.sequence.apply(self._extract_kmers_from_sequence)
