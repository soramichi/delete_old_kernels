# delete_old_kernels
Delete old kernel images and related files under `/boot` and `/lib`. Must be executed with a root privilege.

# Usage
```
$ uname -r
5.4.10

$ sudo ./delete_old_kernels.py 
Found installed kernels older than the current one (5.4.10):
5.4.8

Do you wish to delete them? [y/n]: 
y
Deleted. You can manually execute 'update-grub'
```
