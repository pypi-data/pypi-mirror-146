"""
Top level file for the application.
"""
import os
import sys
sys.path.insert(0, os.path.abspath('./src'))
import crypto_util
import gui

def gui():
    """
    Start the gui.
    """
    gui.start_gui()

def cli():
    """
    Start the cli
    """
    crypto_util.main()

