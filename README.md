# MutaPer

### Is a script that can help to personalize and expand a wordlist.

Author: Fagner Alves (SoenShem)

## Description

With mutaper you can generate permutation of words, chosing the words count and specify the if has separator between the words or not, you can also add sufixes or prefixes to each words, generate l33t versions and more...

The script was writed in Python.

## Features

- Generate permutations of words from a wordlist.
- Choose the minimum and maximum number of words per permutation.
- Specify custom separators between words.
- Add prefixes and suffixes to each permutation.
- Generate l33t (leet speak) variations. (Beware can generate large files.)
- Capitalize or reverse words.
- Estimate the output file size before generation.
- Save results to a file or print to stdout.

## Requirements

- Python 3.6 or higher

## Instalation

You can install just by giving execution permission, and put in a PATH dir.

example:

    # mv mutaper.py mutaper && chmod +x mutaper && cp mutaper /usr/bin


## Usage

```bash
python3 mutaper.py <input_wordlist> [--output <output_file>] [--min-words N] [--max-words N] [--separators SEP [SEP ...]] [--capitalize] [--reverse] [--prefixes PFX [PFX ...]] [--suffixes SFX [SFX ...]] [--leet]
```

### Example

```bash
python3 mutaper.py --separators "_de_" "_of_" "_com_" --suffixes ".db"  --m
in-words 1 --max-words 2 --output output2.txt dblist.txt
```

```bash
python3 mutaper.py --separators "_" --suffixes ".db" --max-words 3 --min-words 3  dblist.txt 
```

## License

GNU V3