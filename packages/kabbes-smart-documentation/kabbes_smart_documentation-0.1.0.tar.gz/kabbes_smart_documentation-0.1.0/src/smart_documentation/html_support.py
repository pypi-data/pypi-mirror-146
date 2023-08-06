def replace_spaces_in_link( string ):
    return string.replace(' ','%20')

def s( type, string ):
    return '<{type}>{string}</{type}>'.format( type = type, string = string )

def heading( string, level = 1 ):
    return s( 'h'+str(level), string )

def h1( *args ):
    return heading( *args, level=1 )
def h2( *args ):
    return heading( *args, level=2 )
def h3( *args ):
    return heading( *args, level=3 )
def h4( *args ):
    return heading( *args, level=4 )
def h5( *args ):
    return heading( *args, level=5 )
def h6( *args ):
    return heading( *args, level=6 )

def blockquote( string ):
    return s( 'blockquote', string )

def line_break():
    return '<br>'

def link( display, url ):
    url = replace_spaces_in_link( url )
    return '<a href="{url}">{display}</a>'.format( url = url, display = display )
