
import os, sys
import subprocess

def call_shell(cmd):
    
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    std_out, std_err = p.communicate()
    
    if int(p.returncode) != 0:
        return False, std_err.decode("utf-8")
    
    return True, std_out.decode("utf-8")


def call_check_shell(cmd):

    success, message = call_shell(cmd)

    if not success:
        print()
        print("catched error : failed call shell")
        print()
        print("the command is below")
        print("="*30)
        print(cmd)
        print("="*30)
        print()
        print("the error message is below")
        print("="*30)
        print(message)
        print("="*30)
