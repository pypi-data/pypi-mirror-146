"""
Top level file for the application.
"""
import os
import sys
import src.crypto_util
import src.gui

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

