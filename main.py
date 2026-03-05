from constants import endcodons
from io_utils import load_file_safely
from parser_utils import extract_codons, is_validcodon
from report_utils import results


def load_db():
    descriptions = {}

    desc_lines = load_file_safely("descriptions.txt", "Descriptions")
    for line in desc_lines:
        pos = line.find(":")
        if pos != -1:
            codon = line[:pos].strip().upper()
            desc = line[pos + 1:].strip()
            descriptions[codon] = desc

    mut_lines = load_file_safely("mutations.txt", "Mutations")
    known_mutations = set(m.strip().upper() for m in mut_lines if m.strip())

    return descriptions, known_mutations


def analyze_for_web(line: str, descriptions: dict, known_mutations: set) -> dict:

    result = []
    frequency = {}

    cleaned_dna = "".join(c.upper() for c in (line or "") if c.upper() in {"A", "T", "G", "C"})
    codons, remainder = extract_codons(cleaned_dna)

    codon_count = len(cleaned_dna) // 3
    remainder = len(cleaned_dna) % 3

    report = {
        "cleaned_dna": cleaned_dna,
        "codon_count": codon_count,
        "remainder": remainder,
        "rna": cleaned_dna.replace("T", "U") if codon_count <= 20 else None,

        "start_ok": False,
        "start_codon": None,

        "stop_count": 0,
        "premature_stop_positions": [],
        "ends_with_stop": False,

        "internal_atg": False,
        "max_repeat_run": 0,

        "invalid_codons": [],
        "known_mutations_found": [],

        "palindromes": [],
        "frequency": {}
    }

    if not codons:
        report["error"] = "No valid codons found"
        return report

    report["start_codon"] = codons[0]

    if codons[0] == "ATG":
        report["start_ok"] = True

    last_index = len(codons) - 1

    stop_positions = [i for i, c in enumerate(codons) if c in endcodons]
    premature_positions = [i for i in stop_positions if i != last_index]

    report["stop_count"] = len(stop_positions)
    report["premature_stop_positions"] = premature_positions
    report["ends_with_stop"] = codons[last_index] in endcodons

    if "ATG" in codons[1:]:
        report["internal_atg"] = True

    max_run = 1
    current_run = 1

    for i in range(1, len(codons)):
        if codons[i] == codons[i - 1]:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 1

    report["max_repeat_run"] = max_run

    premature_stop_codons = {codons[i] for i in premature_positions}

    for codon in codons:

        frequency[codon] = frequency.get(codon, 0) + 1

        if codon not in endcodons and not is_validcodon(codon):
            report["invalid_codons"].append(codon)

        if codon in known_mutations:

            if codon in endcodons:
                if codon in premature_stop_codons:

                    item = {"codon": codon}

                    if codon in descriptions:
                        item["description"] = descriptions[codon]

                    report["known_mutations_found"].append(item)

            else:

                item = {"codon": codon}

                if codon in descriptions:
                    item["description"] = descriptions[codon]

                report["known_mutations_found"].append(item)

        if len(codon) == 3 and codon[0] == codon[-1]:
            result.append(codon)

    report["palindromes"] = result
    report["frequency"] = frequency

    return report


def main():

    print("DNA SEQUENCE ANALYZER")

    result = []
    frequency = {}

    descriptions, known_mutations = load_db()

    seq_lines = load_file_safely("input.txt", "Sequences")

    if not seq_lines:
        print("\nError: no sequences to analyze")
        print("Please create input.txt with DNA sequences.")
        return

    print("SEQUENCE ANALYSIS")

    for seq_num, line in enumerate(seq_lines, 1):

        print(f"\nAnalyzing sequence #{seq_num}:")

        cleaned_dna = "".join(c.upper() for c in line if c.upper() in {"A", "T", "G", "C"})
        codons, remainder = extract_codons(cleaned_dna)

        codon_count = len(cleaned_dna) // 3
        remainder = len(cleaned_dna) % 3

        if codon_count <= 20:
            rna = cleaned_dna.replace("T", "U")
            print("RNA sequence:", rna)

        if not codons:
            print(f"No valid codons found in sequence #{seq_num}")
            continue

        if codons[0] == "ATG":
            print("Valid start codon ATG found")
        else:
            print(f"Mutation! Expected ATG but found: {codons[0]}")

        last_index = len(codons) - 1

        stop_positions = [i for i, c in enumerate(codons) if c in endcodons]
        premature_positions = [i for i in stop_positions if i != last_index]

        if not stop_positions:
            print("Mutation! No stop codon found (TAA/TAG/TGA).")
        else:

            if premature_positions:
                print(f"Mutation! Premature stop codon found at codon index(es): {premature_positions}")

            if codons[last_index] in endcodons:

                if remainder == 0:
                    print(f"Valid stop codon at the end: the stop position is {last_index + 1}")
                else:
                    print("Stop codon is last full codon, BUT extra nucleotides remain.")

            else:
                print("Mutation! Sequence does not end with a stop codon.")

            print(f"Stop codons found: {len(stop_positions)}")

        if "ATG" in codons[1:]:
            print("Warning! Internal start codon ATG found.")

        max_run = 1
        current_run = 1

        for i in range(1, len(codons)):

            if codons[i] == codons[i - 1]:

                current_run += 1
                max_run = max(max_run, current_run)

            else:
                current_run = 1

        if max_run >= 10:
            print("Warning! Medium codon repetition detected.")

        if max_run >= 20:
            print("Severe mutation pattern detected!")

        premature_stop_codons = {codons[i] for i in premature_positions}

        for codon in codons:

            frequency[codon] = frequency.get(codon, 0) + 1

            if codon not in endcodons and not is_validcodon(codon):
                print(f"Invalid codon found: {codon}")

            if codon in known_mutations:

                if codon in endcodons:

                    if codon in premature_stop_codons:

                        print(f"Known mutation found: {codon}")

                        if codon in descriptions:
                            print(f"     → {descriptions[codon]}")

                else:

                    print(f"Known mutation found: {codon}")

                    if codon in descriptions:
                        print(f"     → {descriptions[codon]}")

            if len(codon) == 3 and codon[0] == codon[-1]:
                result.append(codon)

    print()

    results(result, frequency)


if __name__ == "__main__":
    main()
