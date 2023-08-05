from typing import List, Union, Optional, Dict
import os
import glob

import quickstats

def compile_macros(macros:Optional[Union[str, List[str]]]=None):
    """
    Compile ROOT macros
    
    Arguments:
        macros: (Optional) str or list of str
            If str, it is a string containing comma delimited list of macro names to be compiled.
            If list of str, it is the list of macro names to be compiled.
    """
    if macros is None:
        macros = get_all_macros()
    elif isinstance(macros, str):
        macros = macros.split(',')
    from quickstats.utils.root_utils import compile_macro
    for macro in macros:
        if (macro == "FlexibleInterpVarMkII") and (quickstats.root_version >= (6, 26, 0)):
            quickstats._PRINT_.info("INFO: Skip compiling macro \"FlexibleInterpVarMkII\" which is "
                                    "deprecated since ROOT 6.26/00")
            continue
        compile_macro(macro)
        
def get_all_macros():
    """
    Get the list of macros names
    
    Note: Only macros ending in .cxx will be considered
    """
    macros_dir = os.path.join(quickstats.macro_path, 'macros')
    macro_paths = glob.glob(os.path.join(macros_dir, "*/*.cxx"))
    macros = [os.path.os.path.splitext(os.path.basename(path))[0] for path in macro_paths]
    return macros


def set_verbosity(verbosity:Union[str, int]="INFO"):
    quickstats._PRINT_.verbosity = verbosity
    
    
def get_root_version():
    from quickstats.root_checker import ROOTChecker, ROOTVersion
    try:
        root_config_cmd = ROOTChecker.get_root_config_cmd()
        root_version = ROOTChecker.get_installed_root_version(root_config_cmd)
    except:
        root_version = ROOTVersion((0, 0, 0))
    return root_version