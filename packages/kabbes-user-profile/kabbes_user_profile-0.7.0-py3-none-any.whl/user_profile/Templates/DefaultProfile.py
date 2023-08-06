import os
import dir_ops as do
from user_profile.ProfileParent import ProfileParent

class Profile( ProfileParent ):

    def __init__( self ):

        ProfileParent.__init__( self )

        self.id = '{{id}}'
        self.email = '{{email}}'
        self.first_name = '{{first_name}}'
        self.last_name = '{{last_name}}'
        self.name = ' '.join( [self.first_name, self.last_name] )
        self.Path = do.Path( os.path.abspath( __file__ ) )

        #Fill this in with the default location for the 
        self.default_repo_parent_Dir = do.Dir( '{{default_repo_parent_Dir}}' )

        self.init_user()







