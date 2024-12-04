@echo off
cd "C:\Users\Admin\Documents\PY-Projects\Proiect C(8) - OwnRM" :: change to your script location
mkdir C:\test-root
mkdir C:\test-root\parent-dir
echo File in parent-dir > C:\test-root\parent-dir\file1.txt
mkdir C:\test-root\child-dir
echo File in child-dir > C:\test-root\child-dir\file2.txt
mkdir D:\cross-fs-dir
echo File on different FS > D:\cross-fs-dir\file3.txt
mklink /D C:\test-root\child-dir\cross-link D:\cross-fs-dir
python rm.py --one-file-system --recursive --dry-run C:\test-root
pause
:: return in rm.py (line109 should be removed to use --dry-run)