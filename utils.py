import os, errno

def create_dir(path):
    p = os.path.abspath(path)
    try:
        os.makedirs(p)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise

def debug(args):
	print "debug: %s" % (args)
