__version__ = "1.0.1"

def show_version():
    # import re
    # VERSIONFILE="__version__.py"
    # verstrline = open(VERSIONFILE, "rt").read()
    # VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    # mo = re.search(VSRE, verstrline, re.M)
    # if mo:
    #     verstr = mo.group(1)
    # else:
    #     raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))
    print("version {}".format(__version__))