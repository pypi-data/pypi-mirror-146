#!/usr/bin/env bash
for name in "$@"; do
    panqec merge-dirs -o temp/paper/$name/results
    cd temp/paper/$name/
    zip -r $name.zip inputs results
    cd -
    mv temp/paper/$name/$name.zip temp/paper/share
done
