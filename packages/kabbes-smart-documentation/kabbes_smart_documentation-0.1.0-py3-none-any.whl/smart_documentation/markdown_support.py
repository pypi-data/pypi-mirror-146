indent = '  '

def heading( string, level = 1 ):
    return '#'*level + ' {string}'.format(string = string)

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
    return '> {string}'.format( string = string )

def replace_spaces_in_link( string ):
    return string.replace(' ','%20')

def link( display, url ):
    url = replace_spaces_in_link( url )
    return '[{display}]({url})'.format( display = display, url = url )

def image( display, image_path ):
    return '![{display}]({image_path})'.format( display = display, image_path = image_path )

def bold( string ):
    return '**{string}**'.format( string )

def italic( string ):
    return '*{string}*'.format( string )

def strikethrough( string ):
    return '~~{string}~~'.format( string = string )

def code( string, block = False ):

    if block:
        return code_block(string)
    return '`{string}`'.format( string = string )

def code_block( string ):

    new_string = '''```
    {string}
```'''.format( string = string )

    return new_string

def subscript( string ):
    return '~{string}~'.format( string = string )

def superscript( string ):
    return '^{string}^'.format( string = string )

def ordered_list( string, number, indent_level = 0 ):
    return indent*indent_level + str(number) + '. {string}'.format(string=string)

def unordered_list( string, indent_level = 0 ):
    return indent*indent_level + '- {string}'.format(string=string)











#end
