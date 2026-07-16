import subprocess

def main():
    diff = subprocess.check_output(["git", "diff"],text=True)

    print(diff)

main()