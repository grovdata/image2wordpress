#!/usr/bin/python
import os
import sys
import tempfile
import time
from PIL import Image
import xmlrpclib
import wordpresslib
import shutil

WP_HOST='http://mywordpresshost.com/xmlrpc.php'
WP_USER='user'
WP_PASS='pass'
MAX_SIZE=1200
TEMP_DIR=tempfile.mkdtemp()

wp = wordpresslib.WordPressClient(WP_HOST, WP_USER, WP_PASS)
wp.selectBlog(0)

def cleanup():
    print "Cleaning up %s..." % TEMP_DIR
    shutil.rmtree(TEMP_DIR)

def fix_image(image, force=False):
    img = Image.open(image)
    w,h = img.size
    if (w > MAX_SIZE) or force:
        filename = os.path.split(image)[1]
        print "Resizing image %s before upload..." % filename
        img.thumbnail((480,480), Image.ANTIALIAS)
        img.save(os.path.join(TEMP_DIR, filename), quality=90)
        return os.path.join(TEMP_DIR, filename)
    return image

def upload_wp(image):
    epic_win = False
    got_error = False

    while not epic_win:
        try:
            got_error = False
            imageSrc = wp.newMediaObject(fix_image(image, force=got_error))
            print "Uploading %s..." % image
            epic_win = True
        except xmlrpclib.ProtocolError:
            print "Forcing image resize..."
            got_error = True

if __name__ == '__main__':
    progress = 0

    for image in sys.argv[1:]:
        upload_wp(image)

    cleanup()
    print "Done!"