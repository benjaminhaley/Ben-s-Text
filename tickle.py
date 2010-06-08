"""returns the most ticklesh file in a directory"""
import os
import time

tickle  = ( 0 , 0, 0, '' )
now     = time.time()

for f in os.listdir(''):

    atime   = os.path.getatime(f)
    mtime   = os.path.getmtime(f)
    accessed = now - atime
    modified = now - mtime
    hilarity = accessed**2 / modified

    if hilarity > tickle[0] and modified > 60*60*24:
        times = ( now, mtime )
        tickle = ( f, hilarity, times )
    
os.utime( tickle[0], tickle[2] )
os.startfile( tickle[0] )
