#!/usr/bin/env bash
pip install black

# MS default image uses streamlit package,
# but `streamlit` command not in $PATH,
# uninstall it
pip uninstall -y streamlit

pip install -r ./requirements.txt