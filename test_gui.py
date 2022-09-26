import gugu as g
from tkinter import *

def test_root():
    assert type(g.build_root()) == type(Tk())
