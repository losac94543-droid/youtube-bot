#!/usr/bin/env python3
import os
import subprocess
import sys


def run_command(command, shell=True):
    """Run a shell command and handle errors."""
    print(f"[CODEX] Running: {command}")
    result = subprocess.run(
        command, shell=shell, text=True, capture_output=True
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        print(
            f"[CODEX] Error: Command failed with exit code {result.returncode}",
            file=sys.stderr,
        )
        sys.exit(result.returncode)


def create_dummy_output_if_missing():
    """Ensure ~/output.py exists so the copy commands don't fail on a fresh run."""
    home_dir = os.path.expanduser("~")
    output_path = os.path.join(home_dir, "output.py")
    if not os.path.exists(output_path):
        print(
            f"[CODEX] {output_path} not found. Creating a default template..."
        )
        dummy_code = '''#!/usr/bin/env python3
print("Hello from YouTube Bot Module / Main!")
'''.strip()
        with open(output_path, "w") as f:
            f.write(dummy_code)


def main():
    # Define paths
    home_dir = os.path.expanduser("~")
    bot_dir = os.path.join(home_dir, "youtube-bot")
    output_py = os.path.join(home_dir, "output.py")

    # 0. Setup prerequisite file
    create_dummy_output_if_missing()

    # 1. cd ~/youtube-bot && mkdir -p modules output logs data
    print(f"[CODEX] Setting up directory structure in {bot_dir}")
    os.makedirs(bot_dir, exist_ok=True)
    os.chdir(bot_dir)

    for d in ["modules", "output", "logs", "data"]:
        os.makedirs(d, exist_ok=True)

    # 2. cp ~/output.py main.py && cp ~/output.py modules/script_generator.py ...
    print("[CODEX] Copying files...")
    files_to_create = [
        "main.py",
        "modules/script_generator.py",
        "modules/voiceover.py",
        "modules/video_maker.py",
        "out.py",
    ]

    for target in files_to_create:
        run_command(f"cp '{output_py}' '{target}'")

    # 3. ls -lh main.py modules/
    print("[CODEX] Checking generated files...")
    run_command("ls -lh main.py modules/")

    # 4. python3 main.py
    print("[CODEX] Executing main.py...")
    run_command("python3 main.py")


if __name__ == "__main__":
    main()