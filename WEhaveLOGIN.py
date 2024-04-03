import os
import time
from tqdm import tqdm
import urllib.parse

def search_and_write_lines_with_keyword(file_name, keyword):
    relevant_content = ""  
    decoding_errors = 0
    with open(file_name, 'r', encoding='utf-8') as file:
        for row in file:
            try:
                if keyword in row: 
                    relevant_content += row.strip() + "\n"  
            except UnicodeDecodeError:
                decoding_errors += 1
    return relevant_content, decoding_errors

def clean_file_name(file_name):
    invalid_characters = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_characters:
        file_name = file_name.replace(char, '_')
    return file_name

def main():
    print("\u001b[92m.        WEhaveLOGIN\u001b[0m")
    db_folder = "/sdcard/WEhaveLOGIN/"
    
    if not os.path.isdir(db_folder):
        print(f"\u001b[35mThe directory '{db_folder}' does not exist.\u001b[0m")
        return

    keyword = input("\u001b[35mType the site or URL: \u001b[0m")
    encoded_keyword = urllib.parse.quote(keyword)

    output_file_name = f"{clean_file_name(encoded_keyword)}.txt"

    txt_files = [file for file in os.listdir(db_folder) if file.endswith('.txt')]

    if not txt_files:
        print(f"\u001b[35mNo text files found in '{db_folder}'.\u001b[0m")
        return
        
    with tqdm(total=len(txt_files), desc="Searching files...") as progress_bar:
        total_lines_found = 0
        total_decoding_errors = 0
        with open(output_file_name, 'w') as output_file:
            for txt_file in txt_files:
                file_path = os.path.join(db_folder, txt_file)
                relevant_content, decoding_errors = search_and_write_lines_with_keyword(file_path, keyword)
                total_lines_found += len(relevant_content.splitlines()) 
                total_decoding_errors += decoding_errors
                if relevant_content:
                    output_file.write(relevant_content) 
                    output_file.write("\n\n")
                progress_bar.update(1)
                time.sleep(0.1)
                
               
               
    if total_lines_found == 0:
        print("\u001b[35mNo logins found.\u001b[0m")
    else:
        print(" " * 50000);
    print(f"\u001b[35m Logins found: {total_lines_found}.\u001b[0m")
    show_output = input("\u001b[35m Do you want to continue and view the logins? (yes/no): \u001b[0m")
    if show_output.lower() == "yes":
        print("\nContents of the output file:")
        with open(output_file_name, 'r') as output_file:
            for line in output_file:
                print(line.strip())
    else:
        print("\u001b[35mOkay, exiting.\u001b[0m");
       

if __name__ == "__main__":
    main()
    
