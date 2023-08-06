import os
from dir_ops import dir_ops as do
from user_profile.ProfileParent import ProfileParent

class Profile( ProfileParent ):

    def __init__( self ):

        ProfileParent.__init__( self )

        self.id = 'james'
        self.email = 'james.kabbes@gmail.com'
        self.first_name = 'James'
        self.last_name = 'Kabbes'
        self.name = ' '.join( [self.first_name, self.last_name] )
        self.Path = do.Path( os.path.abspath( __file__ ) )

        #Fill this in with the default location for the 
        self.default_repo_parent_Dir = do.Dir( '/Users/james/Documents/Repos' )

        #  Add relevant paths and other user variables
        self.dropbox_home_Dir = do.Dir( '/Users/james/Dropbox' )
        self.credentials_Dir =  do.Dir( self.dropbox_home_Dir.join('Credentials') ) 

        self.connected_user_profiles = {
            'pi': {
            'path': '/Volumes/pi/Repos/User-Profile/Users/pi.py',
            'home_dir_mapping': { '/Volumes': '/home' }
            }
        }

        #photo import locations
        self.raw_photos_staging_Dir = do.Dir( '/Users/james/Documents/Raw-Quick-Pics' )
        self.kabbes_photography_Dir = do.Dir( self.dropbox_home_Dir.join( 'Kabbes Photography' ) )

        # list of all possible Databases to choose from
        self.Events_db_paths = do.Paths( paths = [ self.kabbes_photography_Dir.join('Kabbes Photography Events.db')  ] )

        qr_code_logo_templates = {
        'kabbesphotography': self.kabbes_photography_Dir.p + '/QR-Code Logo.png' # solely used for QR-Code repo
        }

        self.import_presets = {
        'DSLR':
        {
        'import_dir' : '/Volumes/NO NAME/DCIM/104CANON',
        'endings_to_keep': ['CR2','JPG','JPEG'],
        'prefix' : 'D'
        },

        'GoPro':
        {
        'import_dir' : '/Volumes/NO NAME/DCIM/100GOPRO',
        'endings_to_keep': ['MP4','JPG','JPEG'],
        'prefix' : 'G'
        },
        'Fake Flash Drive':
        {
        'import_dir' : '/Users/james/Desktop/Fake Flash Drive',
        'endings_to_keep': ['CR2','JPG','JPEG','PNG','MP4','HEIC'],
        'prefix' : 'F'
        },
        'Default':
        {
        'import_dir' : '',
        'endings_to_keep': ['CR2','JPG','JPEG','PNG','MP4','HEIC'],
        'prefix' : 'P'
        }
        }


        self.init_user()







