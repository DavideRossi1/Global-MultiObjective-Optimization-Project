#!/bin/bash
search_dir="scores/AgentGA"
for space in "$search_dir"/*
do
    for boost in "$space"/*
    do
        for counter in "$boost"/*
        do 
            file=Constants.py
            currentFile=${counter}/${file}
            mv "$currentFile" "source_files/Constants.py"
            python source_files/main.py
            mv "source_files/Constants.py" "$currentFile"
            echo "Done with ${counter}"
        done
    done
done


