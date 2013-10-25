import os

print __file__
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
print os.path.join(SITE_ROOT, 'media/uploads/')
