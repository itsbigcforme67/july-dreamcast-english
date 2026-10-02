"""Shared locations. R = repo root, W = work dir holding YOUR copy of the game
(track01.bin, track02.raw, track03.bin, *.gdi) plus everything generated from it.
Override the work dir with the JULY_WORK environment variable."""
import os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W=os.environ.get('JULY_WORK',os.path.join(R,'work'))
