import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.3.0.post153"
version_tuple = (0, 3, 0, 153)
try:
    from packaging.version import Version as V
    pversion = V("0.3.0.post153")
except ImportError:
    pass

# Data version info
data_version_str = "0.3.0.post27"
data_version_tuple = (0, 3, 0, 27)
try:
    from packaging.version import Version as V
    pdata_version = V("0.3.0.post27")
except ImportError:
    pass
data_git_hash = "f9e7cb6e712a4ceff369de8099f85b62b0c2ad4c"
data_git_describe = "0.3.0-27-gf9e7cb6e"
data_git_msg = """\
commit f9e7cb6e712a4ceff369de8099f85b62b0c2ad4c
Merge: 27524327 2a97802e
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Mon Apr 11 09:56:07 2022 +0200

    Merge pull request #506 from silabs-oysteink/silabs-oysteink_clic-mnxti
    
    Implementation of mnxti

"""

# Tool version info
tool_version_str = "0.0.post126"
tool_version_tuple = (0, 0, 126)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post126")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_cv32e40x."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_cv32e40x".format(f))
    return fn
