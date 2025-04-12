#!/bin/sh
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then 
    echo "Python version is $PYTHON_VERSION, which is >= $REQUIRED_VERSION"
else
    echo "Python version is $PYTHON_VERSION, which is < $REQUIRED_VERSION"
    exit 1
fi

git clone --depth=1 https://github.com/colmmurphyxyz/pseudo-code-compiler.git
cd pseudo-code-compiler;

read -p "Do you want to create a virtual environment? [y/N]: " create_venv
if [ "$create_venv" = "y" ]; then
    python3 -m venv ./venv
    echo "Virtual environment created."
    . ./venv/bin/activate
    echo "Virtual environment activated."
else
    echo "Skipping virtual environment creation."
fi

pip install -r requirements.txt;

cd res
chmod +x transpile_pc_examples.sh;
./transpile_pc_examples.sh;

cd ..;

read -p "Do you want to install the VScode extension for CLRS pseudocode? [Y/n]: " install_ext
if [ "$install_ext" = "n" ]; then
    echo "fine...";
else
    git clone --depth=1 https://github.com/colmmurphyxyz/clrs-pseudocode-vscode.git;
    mv clrs-pseudocode-vscode ~/.vscode/extensions;
    rm ~/.vscode/extensions/extensions.json;
fi

echo "Finished";
echo "The glorious Pseudocode Compiler is installed";
echo "Transpile your first pseudocode program with 'python pcc/pcc.py \path\to\program.pc'";

exit 0