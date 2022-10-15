# This helper script scans folders for wildcards and embeddings and writes them
# to a temporary file to expose it to the javascript side

import os
import pathlib

# The path to the folder containing the wildcards and embeddings
FILE_DIR = pathlib.Path(os.path.dirname(os.path.realpath("__file__")))
WILDCARD_PATH = pathlib.Path.joinpath(FILE_DIR, 'scripts/wildcards').resolve()
EMB_PATH = pathlib.Path.joinpath(FILE_DIR, 'embeddings')
# The path to the temporary file
TEMP_PATH = pathlib.Path.joinpath(FILE_DIR, 'tags/temp')


def get_wildcards():
    """Returns a list of all wildcards"""
    wildcard_files = list(WILDCARD_PATH.rglob("*.txt"))
    relative_wildcards = [str(w.relative_to(WILDCARD_PATH)) for w in wildcard_files]
    return relative_wildcards


def get_embeddings():
    """Returns a list of all embeddings"""
    return filter(lambda f: f.endswith(".bin") or f.endswith(".pt"), os.listdir(EMB_PATH))


def write_to_temp_file(name, data):
    """Writes the given data to a temporary file"""
    with open(pathlib.Path.joinpath(TEMP_PATH, name), 'w', encoding="utf-8") as f:
        f.write(('\n'.join(data)))


# Check if the temp path exists and create it if not
if not pathlib.Path.exists(TEMP_PATH):
    pathlib.Path.mkdir(TEMP_PATH, parents=True)
    # Set up files to ensure the script doesn't fail to load them
    # even if no wildcards or embeddings are found
    write_to_temp_file('wc.txt', [])
    write_to_temp_file('emb.txt', [])

# Write wildcards to wc.txt if found
if pathlib.Path.exists(WILDCARD_PATH):
    wildcards = get_wildcards()
    if wildcards:
        write_to_temp_file('wc.txt', wildcards)

# Write embeddings to emb.txt if found
if pathlib.Path.exists(EMB_PATH):
    embeddings = get_embeddings()
    if embeddings:
        write_to_temp_file('emb.txt', embeddings)
