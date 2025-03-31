import subprocess

try:
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True, capture_output=True, text=True)
    print("Dependencies installed successfully!")
except subprocess.CalledProcessError as e:
    error_message = ""

    if "Could not find a version that satisfies the requirement" in e.stderr:
        error_message = "A dependency is not available, which is weird because these are popular libraries, please check PyPi or open an issue in the repo"

    elif "No matching distribution found" in e.stderr:
        error_message = "Package is incompatible with your version, check PyPi to see if your version is supported or open an issue in the repo"

    elif "Permission denied" in e.stderr:
        error_message = "Permission denied, if using Linux try sudo and if in Windows try giving admin privilege when running"

    elif "pip: command not found" in e.stderr or "No such file or directory" in e.stderr:
        error_message = "Looks like pip is not installed or not found in the system path."

    elif "Could not open requirements file" in e.stderr:
        error_message = "The requirements.txt file could not be found or opened. Check your clone for it and also check permissions (although it is readable, your system may handle it differently)"
    else:
        error_message = f"An unknown error occurred during installation: {e.stderr.strip()}"

    print(error_message)
