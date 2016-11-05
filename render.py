"""
File with functions to render and update aquarium state
"""

import fish


#test for moving fish
a = fish.Fish()

a.print_pos()
i=0
while (i != 10):
    print 'i = ' + str(i)
    a.move(1)
    a.print_pos()

    if ( i % 3  == 0):
        a.accelarate()
    i +=1