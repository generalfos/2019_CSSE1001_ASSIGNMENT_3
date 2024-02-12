"""
Initialise Ninedraft App.
"""

__author__ = "Joel Foster - 45820384"
__date__ = "22/05/2019"
__version__ = "1.1.0"
__copyright__ = "The University of Queensland, 2019"

import tkinter as tk
from ninedraft import Ninedraft

def main():
    root = tk.Tk()
    root.title('Ninedraft')
    app = Ninedraft(root)
    root.mainloop()

if __name__ == '__main__':
    main()
