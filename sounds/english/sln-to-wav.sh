#! /bin/sh

for i in *.sln ; do echo $i; sox -r 8000 -s2 -t raw $i "`echo $i|sed -e s/sln//`wav"; done

#sox -t raw -r 8000 -u -c1 -s2 ok-01.sln stream.wav
