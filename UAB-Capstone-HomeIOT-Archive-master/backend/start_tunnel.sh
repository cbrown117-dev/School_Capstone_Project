# Script to initiate a ssh tunnel to local port 5432 for postgresql

read -p 'UAB Username: ' username

ssh -L5432:164.111.161.173:5432 $username@138.26.64.12
