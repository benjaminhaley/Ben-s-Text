# date.py
# Ben Haley - Feb 2010

# This is a series of functions and classes that will identify hand written dates
# in their various formats from text and produce a report of dates, location,
# and surrounding text.

# In the future it will be expanded to make these items searchable, identify
# more date formats, and search through new formats (like gDocs).


class Entry_Collection:
    def __init__( self ):
        self.entries = []

    def add_entry( self, entry ):
        self.entries.append( entry )

    def merge_collections( self, Collection ):
        self.entries.extend( Collection.entries )

    def sort_collection( self ):
        self.entries.sort( reverse=True, key=lambda x:x.date_object.toordinal() )

    def print_collection( self ):
        for entry in self.entries:
            entry.print_entry()


class Dated_Entry:
    def __init__( self ):
        self.content = ''
        self.path = ''
        self.date_line = ''
        self.date_object = None

    def set_date( self, date_object, date_line ):
        self.date_object = date_object
        self.date_line = date_line.strip()

    def set_path( self, path ):
        self.path = path

    def add_content( self, line ):
        self.content += line.strip() + '\n'

    def print_entry( self ):
        print(  self.date_line, self.content[ 0:200 ].strip() + '...', self.path +" ("+self.date_object.isoformat()+")", sep='\n', end='\n\n')


def get_dated_entries( filepath ):
    #seperates a documents by the dates found and returns all but the begining
    dated_entries = []
    f = open( filepath )
    lines = f.readlines()
    f.close()
    Collection = Entry_Collection()
    for line in lines:
        match = match_date( line )
        if match:
            try:
                Collection.add_entry( entry )
            except:
                pass
            entry = match
            entry.set_path( filepath )
        else:
            try:
                entry.add_content( line )
            except:
                pass
    return Collection


def file_list( dirpath ):
    #returns a list of filenames from a directory
    import os
    files = []
    generator = os.walk( dirpath )
    while True:
        try:
            directory_content = generator.send( None )
            new_files = directory_content[2]
            new_directory = directory_content[0]
            for f in new_files:
                extension = os.path.splitext(f)[1]
                if extension == ".txt":
                    path = new_directory + "\\" + f
                    files.append( path )
        except:
            return files

def match_date( line ):
    if len(line) > 100:
        return None
    import re
    DAY = "([0-3]{0,1}[0-9]{1})"
    MONTH = "([0-1]{0,1}[0-9]{1})"
    YEAR = "([0-9]{2,4})"
    SEP = "([\/\-]{1})"
    date = MONTH + SEP + DAY + SEP + YEAR
    matched_line = re.search( date, line )
    
    if matched_line:
        import datetime
        month = matched_line.group(1)
        day = matched_line.group(3)
        year = matched_line.group(5)
        if len(year) == 2:
            year = '20' + year
        elif len(year) == 0:
            now = datetime.datetime.now()
            year = now.year
        try:
            date = datetime.date( int(year), int(month), int(day) )
            entry = Dated_Entry()
            entry.set_date( date, line )
            return entry
        except:
            return None
    else:
        return None
        

import os
this_directory = os.curdir 
all_files = file_list(this_directory)
All_Entries = Entry_Collection()
for path in all_files:
    Collection = get_dated_entries( path )
    All_Entries.merge_collections( Collection )
All_Entries.sort_collection()
All_Entries.print_collection()
