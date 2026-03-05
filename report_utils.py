def results(result: list[str], frequency: dict[str, int]) -> None:

    print("Palindrome codons found:")

    if not result:
        print("No palindrome codons found.")
    else:
        for codon in result:
            print(f"{codon} - nucleotides: {len(codon)}")

    print()
    print("Total palindrome codons:", len(result))

    print()
    print("Codon frequency in sequence:")

    freqvec = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

    for codon, count in freqvec:
        print(f"{codon} -> {count} time(s)")
