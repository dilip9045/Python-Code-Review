import subprocess

def main():
    diff = subprocess.check_output('diff', 'show' , text = True)
    
    print("hello world")
    
main()