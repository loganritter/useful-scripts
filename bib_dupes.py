import re
import argparse

def readBibFile(file_path):
    """
    Reads a .bib file and extracts DOIs, URLs, and Titles.

    Args:
        file_path (str): Path to the .bib file.

    Returns:
        list: A list of identifiers (DOIs, URLs, or Titles).
    """
    identifiers = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            entry_content = ''
            for line in file:
                if line.startswith('@'):
                    # When encountering a new entry, process the previous entry content
                    if entry_content:
                        identifier = extractIdentifier(entry_content)
                        if identifier:
                            identifiers.append(identifier)
                        entry_content = ''  # Reset for next entry
                entry_content += line
            # Process the last entry
            if entry_content:
                identifier = extractIdentifier(entry_content)
                if identifier:
                    identifiers.append(identifier)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return identifiers

def extractIdentifier(entry_content):
    """
    Extracts the DOI, URL, or Title from a single BibTeX entry, in that order of priority.

    Args:
        entry_content (str): The BibTeX entry content.

    Returns:
        str: The extracted DOI, URL, or Title, or None if none are found.
    """
    # Regex patterns to find the DOI, URL, or Title within the entry
    doi_pattern = re.compile(r'doi\s*=\s*[{"]([^}"]+)[}"]', re.IGNORECASE)
    url_pattern = re.compile(r'url\s*=\s*[{"]([^}"]+)[}"]', re.IGNORECASE)
    title_pattern = re.compile(r'title\s*=\s*[{"]([^}"]+)[}"]', re.IGNORECASE)
    
    doi_match = doi_pattern.search(entry_content)
    if doi_match:
        return doi_match.group(1).strip()
    
    url_match = url_pattern.search(entry_content)
    if url_match:
        return url_match.group(1).strip()
    
    title_match = title_pattern.search(entry_content)
    if title_match:
        return title_match.group(1).strip().lower()  # Convert title to lowercase to standardize
    
    return None

def findDuplicates(identifiers):
    """
    Identifies and returns duplicate identifiers (DOIs, URLs, or Titles).

    Args:
        identifiers (list): List of DOIs, URLs, or Titles.

    Returns:
        list: A list of duplicate identifiers.
    """
    seen = set()
    duplicates = set()

    for identifier in identifiers:
        if identifier in seen:
            duplicates.add(identifier)
        else:
            seen.add(identifier)

    return list(duplicates)

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Check for duplicate entries in a .bib file based on DOI, URL, or Title.")
    parser.add_argument('file_path', help='Path to the .bib file to be checked for duplicates')
    args = parser.parse_args()
    
    identifiers = readBibFile(args.file_path)

    if identifiers:
        duplicates = findDuplicates(identifiers)
        if duplicates:
            print("Duplicate entries found based on DOI, URL, or Title:")
            for dupes in duplicates:
                print(dupes)
        else:
            print("No duplicate entries found.")
    else:
        print("No DOIs, URLs, or Titles found in the file.")

if __name__ == "__main__":
    main()
