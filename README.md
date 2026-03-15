Hey guys! 
This project is an expanded version of my backend program with DNA sequence analyzer. Files will be moved to new folders

Project structure - 
egen 

folder [static] {
logo.png
style.css
flu_detector.css
script.js
}

folder [templates] {
index.html
flu-detector.html
main.html
}

# eGen

**eGen** is a DNA sequence analysis program designed for educational and bioinformatics practice purposes.  
The project helps check biological sequences, detect basic anomalies, and generate a structured analysis report in a simple and readable form.

## About the project

The main goal of **eGen** is to make primary DNA analysis more understandable and accessible for students who study programming, biology, and bioinformatics.

The program can work with DNA sequences entered manually or loaded from a file.  
After processing the sequence, it performs validation, divides the chain into codons, and checks a set of biological and logical conditions.

## Main features

- cleaning the input sequence from spaces and extra symbols
- converting input to uppercase for stable analysis
- validation of nucleotide symbols
- codon extraction
- codon count calculation
- start codon check
- stop codon check
- stop codon count
- detection of premature stop codons
- detection of internal start codons
- codon frequency analysis
- repeat detection
- palindrome detection
- mutation search
- RNA transcription
- file-based input support
- summary generation for the user

## What the program analyzes

The program can detect:

- whether the sequence starts correctly
- whether the sequence ends with a stop codon
- whether there are invalid codons
- whether premature stop codons appear inside the sequence
- whether suspicious repetitions are present
- whether palindrome-like codons appear
- whether known mutation patterns are found
- how many codons the sequence contains
- what RNA transcript corresponds to the DNA chain

## Example workflow

1. The user enters a DNA sequence manually or loads it from a text file.
2. The program cleans and normalizes the input.
3. The sequence is split into codons.
4. The analyzer checks important biological markers.
5. The user receives a summary with the analysis results.

```text
ATGGATGATTAG
