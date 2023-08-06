from repository_generator import BaseRepository
import py_starter as ps
import user_profile
import datetime

class BasePackage( BaseRepository ):

    PYPI_BASE_URL = 'https://pypi.org/project/'

    DEFAULT_KWARGS = {
        'author': user_profile.profile.name,
        'author_email': user_profile.profile.email,
        'version': '0.1.0',
        'year': str(datetime.datetime.now().year)
    }
    def __init__( self, *args, **kwargs ):

        joined_kwargs = ps.merge_dicts( BasePackage.DEFAULT_KWARGS, kwargs )
        BaseRepository.__init__( self, *args, **joined_kwargs )

    def BasePackage_init( self ):

        if not self.has_attr( 'url_home' ):
            self.set_attr( 'url_home', BasePackage.PYPI_BASE_URL + self.get_attr('pypi_name') )

