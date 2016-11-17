#!/bin/bash

echo "Hello World  for tar file"
for f in /home/*.tar
do
  tar xvf "$f" -C /home/ 
done
