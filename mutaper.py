#!/usr/bin/env python3

"""# MutaPer

### Is a script that can help to personalize and expand a wordlist.

## Description

With mutaper you can generate permutation of words, chosing the words count and specify the if has separator between the words or not, you can also add sufixes or prefixes to each words, generate l33t versions, capitalyze, reverse and more...

The script is writed in Python 3 and is compatible with Python 3.6+."""

import sys, os
import argparse
from pathlib import Path
import logging
from datetime import datetime

class MutaPer:
    def __init__(self, input_file, output_file, min_words=1, max_words=2, separators=[], prefixes=[], suffixes=[], leet=False, capitalize=False, reverse=False):
        self.input_file = input_file
        self.output_file = output_file
        self.min_words = min_words
        self.max_words = max_words
        self.separator = separators
        self.prefixes = prefixes
        self.suffixes = suffixes
        self.leet = leet
        self.capitalize = capitalize
        self.reverse = reverse
        self.words = []
        self.permutations = set()
        self.leet_dict = {
	        's': ['$', 'z', '5'],
	        'e': ['3', '€'],
	        'a': ['4', '@'],
	        'o': ['0', '()'],
            'g': ['9', '6'],
	        'i': ['1', '!'],
	        'l': ['1', '!'],
	        't': ['7', '+'],
	        'b': ['8', '6'],
	        'z': ['2', 's']
        }
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def load_words(self):
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                self.words = [line.strip() for line in f if line.strip()]
            logging.info(f"Loaded {len(self.words)} words from {self.input_file}")
        except Exception as e:
            logging.error(f"Error loading words from {self.input_file}: {e}")
            sys.exit(1)
    
    def save_permutations(self):
        try:
            if self.output_file:
                with open(self.output_file, 'w', encoding='utf-8') as f:
                    for perm in sorted(self.permutations):
                        f.write(perm + '\n')
            else:
                for perm in sorted(self.permutations):
                    print(perm)
        except Exception as e:
            logging.error(f"Error saving permutations to {self.output_file}: {e}")
            sys.exit(1)

    def calculate_size_on_disk(self):
        if self.leet:
            logging.info("Size on disk estimation is not available when l33t transformations are enabled.")
            logging.info("beware that the output file can be very large!")
            return
        if self.min_words > 1 or self.max_words > 1:
            total_permutations = 0
            for count in range(self.min_words, self.max_words + 1):
                total_permutations += len(self.words) ** count
            avg_word_length = (sum(len(word) for word in self.words) + sum(len(prefix) for prefix in self.prefixes) + sum(len(sufix) for sufix in self.suffixes)) / len(self.words)
            avg_separator_length = sum(len(sep) for sep in self.separator) / len(self.separator) if self.separator else 0
            estimated_size = total_permutations * (avg_word_length * self.max_words + (avg_separator_length * (self.max_words - 1)))
            estimated_size = estimated_size * (len(self.prefixes) if self.prefixes else 1) 
            estimated_size = estimated_size * (len(self.separator) if self.separator else 1)
            estimated_size = estimated_size * (len(self.suffixes) if self.suffixes else 1)
            logging.info(f"Estimated size on disk: {estimated_size / (1024 * 1024):.2f} MB")
        else:
            logging.info("Size on disk estimation is only available for min_words and max_words greater than 1.")

    def generate_permutations(self):
        from itertools import permutations

        def apply_transformations(word):
            variations = {word}
            if self.capitalize:
                variations.add(word.capitalize())
                variations.add(word.upper())
            if self.reverse:
                variations.add(word[::-1])
            if self.leet:
                leet_variations = {word}
                for char, subs in self.leet_dict.items():
                    new_variations = set()
                    for var in leet_variations:
                        for sub in subs:
                            new_variations.add(var.replace(char, sub))
                    leet_variations.update(new_variations)
                variations.update(leet_variations)
            return variations

        transformed_words = set()
        for word in self.words:
            transformed_words.update(apply_transformations(word))

        transformed_words = list(transformed_words)

        for count in range(self.min_words, self.max_words + 1):
            for combo in permutations(transformed_words, count):
                permutationslist = []
                #base = self.separator.join(combo) if self.separator else ''.join(combo)
                for sep in self.separator if self.separator else ['']:
                    base = sep.join(combo)    
                    for prefix in self.prefixes:
                        permutationslist.append(prefix + base)
                    for suffix in self.suffixes:
                        for base in permutationslist[0:len(self.prefixes)] if permutationslist and self.prefixes else [base]:
                            permutationslist.append(base + suffix)
                    if self.prefixes and self.suffixes:
                        for _ in range(len(self.prefixes)):
                            permutationslist.pop(0)
                    for item in permutationslist if permutationslist else [base]:
                        self.permutations.add(item)

        logging.info(f"Generated {len(self.permutations)} unique permutations")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MutaPer - A wordlist personalizer and expander")
    parser.add_argument("input_file", help="Path to the input wordlist file")
    parser.add_argument("--output", required=False, help="Path to the output file for the generated permutations")
    parser.add_argument("--min-words", type=int, default=1, help="Minimum number of words in each permutation (default: 1)")
    parser.add_argument("--max-words", type=int, default=2, help="Maximum number of words in each permutation (default: 2)")
    parser.add_argument("--separators", nargs='*', default=[], help="Separator to use between words (default: no separator)")
    parser.add_argument("--capitalize", action='store_true', default=False, help="Enable capitalization of words")
    parser.add_argument("--reverse", action='store_true', default=False, help="Enable reversing of words")
    parser.add_argument("--prefixes", nargs='*', default=[], help="List of prefixes to add to each word")
    parser.add_argument("--suffixes", nargs='*', default=[], help="List of suffixes to add to each word")
    parser.add_argument("--leet", action='store_true', default=False, help="Enable l33t speak variations")
    
    args = parser.parse_args()

    mutaper = MutaPer(
        input_file=args.input_file,
        output_file=args.output,
        min_words=args.min_words,
        max_words=args.max_words,
        separators=args.separators,
        capitalize=args.capitalize,
        reverse=args.reverse,
        prefixes=args.prefixes,
        suffixes=args.suffixes,
        leet=args.leet
    )

    mutaper.load_words()
    mutaper.calculate_size_on_disk()
    wanttocontinue = input("Do you want to continue? (y/n): ").strip().lower()
    if wanttocontinue != 'y':
        logging.info("Operation cancelled by user.")
        sys.exit(0)
    mutaper.generate_permutations()
    mutaper.save_permutations()
    logging.info(f"Generated {len(mutaper.permutations)} permutations and saved to {args.output if args.output else 'stdout'}")
    logging.info("MutaPer completed successfully.")