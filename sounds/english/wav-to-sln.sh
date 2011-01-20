#! /bin/sh

for i in *.wav ; do echo $i; sox $i -t raw -r 8000 -c 1 -s "`echo $i|sed -e s/wav//`sln"; done
