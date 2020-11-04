import os

platform = platform.system()

while True:
    directory = os.getcwd()
    cmd = input(f"{directory}: ")

    if cmd == "":
        print("\n")
    else:
        # os.system(cmd)
        os.system(f"cmd /c {cmd}") 