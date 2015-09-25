# The-Collector
A bot that searches and collects things from Thingiverse

Built in Python

Dependencies:
Selenium 
Firefox
Beautiful Soup
randomWords

Also it logs into a Thingiverse account so get one of those and 
put in your account email and psswrd into the settings file


Like an archeologist visiting a burial site, the bot makes no value judgements, it ammasses all it finds as an assemblage of objects that belong to a shared 'search space'. The objects are carefully collected into folder structures that retain their search space identity. The bot makes random searches by pulling a word from a dictionary, avoiding the usual 3D print terminology and biases, and instead seeking things that answer to diverse words such as 'insertions', 'fasteners','till', 'example'. 

The bot still needs some work. It only downloads STL files for now. This can be fixed. One method would be to download the zip file with all the files in it instead of individual files. To specify what file formats it should take, you need to find the MIME type for each file format and add it to the list inside the main python file.

