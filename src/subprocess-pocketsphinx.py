#!/usr/bin/env python2
import subprocess

# Reaches out to the terminal to run continuous speech recognition with a provide
# language model and dictionary.
subprocess.call(["pocketsphinx_continuous", "-inmic", "yes", "-lm", "TAR2860/2860.lm", "-dict", "TAR2860/2860.dic"])
