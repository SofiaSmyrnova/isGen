from constants import valid_nucleotides


def extract_codons(line: str) -> tuple[list[str], int]:
    
    if not line:
        return [], 0

    cleaned = "".join(c.upper() for c in line if c.upper() in valid_nucleotides)
    if not cleaned:
        return [], 0

    codons = [
        cleaned[i:i + 3]
        for i in range(0, len(cleaned), 3)
        if i + 3 <= len(cleaned)
    ]

    remainder = len(cleaned) % 3
    return codons, remainder


def is_validcodon(codon: str) -> bool:
    
    if not isinstance(codon, str) or len(codon) != 3:
        return False

    codon = codon.upper()
    return all(c in valid_nucleotides for c in codon)
