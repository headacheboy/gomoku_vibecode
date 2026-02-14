#!/usr/bin/env python
"""
Gomoku Game Launcher
Simple wrapper to ensure dependencies are installed and launch the game.
"""
import sys
import subprocess
import importlib.util

def check_module(module_name):
    """Check if a module is installed."""
    spec = importlib.util.find_spec(module_name)
    return spec is not None


def install_dependencies():
    """Install required modules if missing."""
    required = ['pygame', 'numba', 'numpy']
    missing = [m for m in required if not check_module(m)]
    
    if missing:
        print("Installing missing dependencies: {}".format(', '.join(missing)))
        for module in missing:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])
        print("Dependencies installed successfully!")


def launch_game():
    """Launch the Gomoku game."""
    try:
        from gomoku.main import main
        print("Starting Gomoku Game...")
        main()
    except Exception as e:
        print("Error launching game: {}".format(e))
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == '__main__':
    check_and_install = '--install' in sys.argv or '--check' in sys.argv
    
    if check_and_install:
        check_dependencies = not check_module('pygame') or not check_module('numba') or not check_module('numpy')
        if check_dependencies:
            install_dependencies()
    
    launch_game()
