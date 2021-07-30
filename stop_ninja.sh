#!/bin/bash
kill -9 `cat s$1_pid`
rm s$1_pid
cd profiles 
rm -rf `cat ../s$1_profile`
cd ..
rm s$1_profile
