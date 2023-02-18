#!/bin/bash
set -e

# check python
pyver=$(python3 --version)
echo "$pyver"
if [[ -z $pyver ]]; then
    echo -e "\033[31mpython3 not found! please install python3! exit now\033[0m"
    exit 1
fi

echo "Installing python dependencies!"
python3 -m pip install notebook pandas numpy matplotlib

# install sdkman
curl -s "https://get.sdkman.io" | bash
. "$HOME/.sdkman/bin/sdkman-init.sh"

sdk install java 17.0.5-oracle
sdk install scala 2.13.8

