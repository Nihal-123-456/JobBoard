import cloudinary
from decouple import config

CLOUDINARY_CLOUDNAME=config('CLOUDINARY_CLOUDNAME', default='')
CLOUDINARY_API_KEY=config('CLOUDINARY_API_KEY', default='')
CLOUDINARY_API_SECRET=config('CLOUDINARY_API_SECRET', default='')

# this function is used for initializing cloudinary
def cloudinary_init():
    cloudinary.config( 
        cloud_name = CLOUDINARY_CLOUDNAME,
        api_key = CLOUDINARY_API_KEY, 
        api_secret = CLOUDINARY_API_SECRET
    )