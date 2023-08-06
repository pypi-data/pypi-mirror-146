# WbSearch

Search anything on main browser directly from terminal (both words and links).

`Installation:`

    $ pip install wbsearch

`Usage:`

    $ wbsearch argument

Replace argument with your own research. 
In case you want to search multiple words, you may need to use "\" before each space, 
or use double quotes around, depending on your operating system.

    $ wbsearch --set keyword link
    
    $ wbsearch -s keyword link

Replace keyword with your own keyword, and link with your own link. 
This method allows to locally set constant keywords.
The same method allows to edit the content of the keyword, simply entering the keword and then the new associated link 


For example, typing:
    
    $ wbsearch -s youtube https://www.youtube.com/ 

Typing in terminal "wbsearch youtube", wbsearch will open the \
saved link referring to "youtube" keyword.

    $ wbsearch --remove keyword
    
    $ wbsearch -r keyword

Replace keyword with the keyword you want to remove from wbsearch user keywords.

    $ wbsearch --help

Type this command to get help.