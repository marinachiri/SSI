import hashlib
import os

#trebujie sa decriptam headerul si sa vedem carei poze ii corespunde dimensiunea


# Lista de hash-uri primite
hash_list = [
    "602a4a8fff652291fdc0e049e3900dae608af64e5e4d2c5d4332603c9938171d",
    "f40e838809ddaa770428a4b2adc1fff0c38a84abe496940d534af1232c2467d5",
    "aa105295e25e11c8c42e4393c008428d965d42c6cb1b906e30be99f94f473bb5",
    "70f87d0b880efcdbe159011126db397a1231966991ae9252b278623aeb9c0450",
    "77a39d581d3d469084686c90ba08a5fb6ce621a552155730019f6c02cb4c0cb6",
    "456ae6a020aa2d54c0c00a71d63033f6c7ca6cbc1424507668cf54b80325dc01",
    "bd0fd461d87fba0d5e61bed6a399acdfc92b12769f9b3178f9752e30f1aeb81d",
    "372df01b994c2b14969592fd2e78d27e7ee472a07c7ac3dfdf41d345b2f8e305",
]

# Calea către directorul cu fișierele criptate
folder_path = "/content/sample_data/encrypted_data"

# Verifică dacă hash-ul antetului se potrivește cu cele primite
def is_valid_header(width, height, hashes):
    header_str = f"P6 {width} {height} 255"
    header_hash = hashlib.sha256(header_str.encode()).hexdigest()
    return header_hash in hashes

# Găsește dimensiunea corectă pentru fiecare fișier criptat
def find_dimensions():
    file_solutions = []
    #luam fiecare fisier din folder
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
#
        for padding_size in range(16):
            for width in range(616):
                for height in range(616):
                    if len(encrypted_data) - padding_size == width * height * 3:
                        if is_valid_header(width, height, hash_list):
                            file_solutions.append((file, width, height))
                            break
                else:
                    continue
                break
            else:
                continue
            break

    return file_solutions

# Afișează soluțiile găsite
solutions = find_dimensions()
for solution in solutions:
    print(solution)
import os

def write_new_files_with_updated_headers(solutions, source_folder_path, destination_folder_path):
    # Crează directorul destinație dacă nu există
    if not os.path.exists(destination_folder_path):
        os.makedirs(destination_folder_path)

    for file_name, width, height in solutions:
        source_file_path = os.path.join(source_folder_path, file_name)
        destination_file_path = os.path.join(destination_folder_path, file_name)

        try:
            with open(source_file_path, 'rb') as source_file:
                original_content = source_file.read()

            header_str = f"P6\n{width} {height}\n255\n".encode()

            with open(destination_file_path, 'wb') as destination_file:
                destination_file.write(header_str + original_content)

            print(f"New file created: {destination_file_path}")
        except IOError as e:
            print(f"Error processing file {file_name}: {e}")

# Exemplu de utilizare a funcției:
destination_folder = "/content/sample_data/decriptate"
write_new_files_with_updated_headers(solutions, folder_path, destination_folder)


# <3 love you