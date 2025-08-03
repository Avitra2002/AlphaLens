import os
import pickle

# def fix_meta_file(meta_path):
#     print(f"Processing: {meta_path}")

#     with open(meta_path, "rb") as f:
#         chunks = pickle.load(f)

#     fixed_chunks = []
#     for c in chunks:
#         if isinstance(c, dict) and "metadata" in c:
#             # Already correct format
#             fixed_chunks.append(c)
#         elif isinstance(c, dict):
#             # This is just metadata — wrap it in a chunk
#             fixed_chunks.append({"text": "", "metadata": c})
#         else:
#             print(f"⚠️ Unexpected entry type in {meta_path}: {type(c)}")
#             fixed_chunks.append(c)

#     with open(meta_path, "wb") as f:
#         pickle.dump(fixed_chunks, f)

#     print(f"✅ Fixed {meta_path} ({len(fixed_chunks)} entries)")

# def fix_all_vector_db(vector_db_dir="vector_db"):
#     for file in os.listdir(vector_db_dir):
#         if file.endswith("_meta.pkl"):
#             fix_meta_file(os.path.join(vector_db_dir, file))

# if __name__ == "__main__":
#     fix_all_vector_db("../vector_db")  # adjust path if needed

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.vector_store import LocalFAISS

vector_store = LocalFAISS()
namespace = "AAPL_2024_10k"

# Where to save the section text
output_dir = "output_sections"
os.makedirs(output_dir, exist_ok=True)

# Function to save section text to file
def save_section_to_file(section_id, text):
    filename = os.path.join(output_dir, f"{namespace}_section_{section_id}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Section {section_id} saved to {filename}")

# Read Section 1
section_id = "1"
if section_id in vector_store.list_sections(namespace):
    chunks = vector_store.get_chunks_by_section(namespace, section_id)
    # Merge all chunk text into one big string
    section_text = "\n\n".join(chunk["text"] for chunk in chunks if chunk["text"].strip())
    save_section_to_file(section_id, section_text)
else:
    print(f"Section {section_id} not found in namespace {namespace}")

