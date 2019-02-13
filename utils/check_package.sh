#! /bin/bash -e

if [ $# -eq 0 ]; then
    echo "Nothing to check."
else
    for package in "$@"
    do
	echo "Checking if $package is installed"
	if [ $(dpkg-query -W -f='${Status}' $package 2>/dev/null | grep -c "ok installed") -eq 0 ]; then
	    echo "No $package package found. Installing $package."
	    sudo apt-get --yes install $package
	else
	    echo "Package $package is installed"
	fi
    done
fi
