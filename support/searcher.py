import os


def search_keyword(directory, keyword):
    results = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_number, line in enumerate(f, 1):
                        if keyword in line:
                            result = {
                                'file_path': file_path,
                                'line_number': line_number,
                                'line_content': line.strip()
                            }
                            results.append(result)
    return results


# Usage example
directory = r'C:\Program Files (x86)\CODESYS 3.5.16.40\CODESYS\ScriptLib\3.5.10.40'  # Replace with the directory you want to search
keyword = 'librarymanager'  # Replace with the keyword you want to search
results = search_keyword(directory, keyword)

if results:
    print(f"Found {len(results)} occurrences of '{keyword}':")
    for result in results:
        print(f"File: {result['file_path']}, Line: {result['line_number']}")
        print(f"Content: {result['line_content']}")
        print('-' * 40)
else:
    print(f"No occurrences of '{keyword}' found.")