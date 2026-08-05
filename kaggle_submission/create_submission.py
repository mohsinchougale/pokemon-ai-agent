import os
import shutil
import tarfile
from pathlib import Path


SUBMISSION_NAME = "submission_002_strategic_v2"

BASE_DIR = Path(__file__).parent

SRC_DIR = BASE_DIR / SUBMISSION_NAME
TEMP_DIR = BASE_DIR / f"temp_{SUBMISSION_NAME}"
TAR_FILE = BASE_DIR / f"{SUBMISSION_NAME}.tar.gz"


def clean_temp():
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)

    if TAR_FILE.exists():
        TAR_FILE.unlink()


def copy_submission_files():
    print("Copying submission files...")

    TEMP_DIR.mkdir()

    for item in SRC_DIR.iterdir():
        destination = TEMP_DIR / item.name

        if item.is_dir():
            shutil.copytree(item, destination)
        else:
            shutil.copy2(item, destination)


def add_shared_files():
    print("Adding shared files...")

    cg_src = BASE_DIR / "shared" / "cg"
    cards_src = BASE_DIR / "shared" / "cards"

    cg_dest = TEMP_DIR / "cg"
    cards_dest = TEMP_DIR / "cards"

    cg_dest.mkdir()
    cards_dest.mkdir()

    for file in cg_src.iterdir():
        shutil.copy2(file, cg_dest / file.name)

    for file in cards_src.iterdir():
        shutil.copy2(file, cards_dest / file.name)


def remove_python_cache():
    print("Removing __pycache__ and .pyc files...")

    for path in TEMP_DIR.rglob("__pycache__"):
        shutil.rmtree(path)

    for path in TEMP_DIR.rglob("*.pyc"):
        path.unlink()


def create_tar():
    print("Creating tar archive...")

    with tarfile.open(TAR_FILE, "w:gz") as tar:

        # IMPORTANT:
        # Add contents of temp folder, not the folder itself.
        for item in TEMP_DIR.iterdir():
            tar.add(
                item,
                arcname=item.name
            )


def validate_tar():

    print("\nValidating archive:")

    with tarfile.open(TAR_FILE, "r:gz") as tar:

        files = tar.getnames()

        print("\nFirst 20 files:")
        for f in files[:20]:
            print(f)

        print("\nRequired files:")

        required = [
            "main.py",
            "deck.csv",
            "agent",
            "features",
            "cg",
            "cards"
        ]

        for req in required:
            found = any(
                f == req or f.startswith(req + "/")
                for f in files
            )

            print(
                f"{req}:",
                "OK" if found else "MISSING"
            )


        bad_files = [
            f for f in files
            if "__pycache__" in f or f.endswith(".pyc")
        ]

        print()

        if bad_files:
            print("WARNING: pycache files found:")
            for f in bad_files:
                print(f)
        else:
            print("OK: No pycache files")


def main():

    clean_temp()

    copy_submission_files()

    add_shared_files()

    remove_python_cache()

    create_tar()

    validate_tar()

    print("\nCreated:")
    print(TAR_FILE)


if __name__ == "__main__":
    main()