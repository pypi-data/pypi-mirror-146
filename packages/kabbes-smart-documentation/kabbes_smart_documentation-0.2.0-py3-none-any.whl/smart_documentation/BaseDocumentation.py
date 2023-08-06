from pypi_builder import BasePackage
import py_starter as ps


class BaseDocumentation( BasePackage ):

    DEFAULT_KWARGS = {

    }

    def __init__( self, *args, **kwargs ):

        joined_kwargs = ps.merge_dicts( BaseDocumentation.DEFAULT_KWARGS, kwargs )
        BasePackage.__init__( self, *args, **joined_kwargs )


    