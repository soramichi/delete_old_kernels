#!/usr/bin/env python3

import re
import subprocess
import shutil
from pathlib import Path

# return if v1 is newer than v2
def newer(v1, v2):
    # compare the version numbers
    for vv in zip(v1.split('.'), v2.split('.')):
        if int(vv[0]) > int(vv[1]):
            return True
        elif int(vv[0]) < int(vv[1]):
            return False

    # v1 and v2 are exactly the same
    if len(v1) == len(v2):
        return False
    # if v1 is the same as v2 up to len(v2) and still has something, probably v1 is newer
    # Example: v1 = "5.4.10.1" vs. v2 = "5.4.10"
    elif len(v1) > len(v2):
        return True
    # the other way around
    else:
        return False

def force_delete(path):
    try:
        Path(path).unlink()
    except IsADirectoryError:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass

def delete_files(v):
    files = ["/boot/System.map-", "/boot/config-", "/boot/initrd.img-", "/boot/vmlinuz-", "/lib/modules/"]
    for f in files:
        force_delete(f + v)

if __name__ == "__main__":
    cur_ver = subprocess.check_output(["uname", "-r"], text=True) # => '5.4.10\n'
    cur_ver = cur_ver[0:-1] # delete the tailing '\n'

    installed = []
    p = Path("/lib/modules")

    for d in p.iterdir():
        v = d.parts[-1]
        # matches only "pure" versions, without any suffixes like "-1-amd64"
        if re.fullmatch(r"[1-9]+\.[0-9]+\.[0-9]+", v) != None:
            # collect ones older than cur_ver
            if newer(cur_ver, v):
                installed.append(v)

    if len(installed) == 0:
        print("Nothing is found.")
        exit(1)

    print("Found installed kernels older than the current one (%s):" % cur_ver)
    for v in installed:
        print(v)
    print("\nDo you wish to delete them? [y/n]: ")
    cmd = input()

    if cmd == "y" or cmd == "Y":
        for v in installed:
            delete_files(v)
        print("Deleted. You can manually execute 'update-grub'")
    else:
        print("Canceled.")
