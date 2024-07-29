def symlink_directory(source, target):
    """Symlink all first-level contents of source to target."""

    for source_file in source.listdir():
        # We need to be careful not to override existing symlinks,
        # which is why we can't blindly symlink everything.
        if os.path.isfile(source_file):
            # Check if symlink at target exists
            symlink_target = os.path.join(target, source_file)
            if not os.path.islink(symlink_target):
                # No existing link, so make a new one
                os.symlink(os.path.abspath(source_file), symlink_target)

        else:
            # Is a directory, symlink the contents of the directory
            symlink_directory(
                os.path.abspath(source_file),
                os.path.join(target, source_file
                )

    return 0

def apply_namelist(nml1_path, nml2_path):
    """Combine the namelists at nml1_path and nml2_path, with nml2_path taking precedence."""
    
    # Open each using f90nml and then pass to recursive patcher
    nml1 = f90nml.read(nml1_path)
    nml2 = f90nml.read(nml2_path)

    recursive_patch(nml1, nml2)

    return nml1

def recursive_patch(nml1, nml2):
    """Deep patch of namelist nml1 with nml2."""

    for opt in nml2.keys():
        if opt in nml1:
            # In the case where nml1 contains the given option,
            # we need to either
            #   - update the existing value, if it's a scalar
            #   - pass the namelist (i.e. nested struct) to recursive patch
            if isinstance(nml2[opt], dict):
                recursive_patch(nml1[opt], nml2[opt])
            else:
                nml1[opt] = nml2[opt]
        else:
            # nml1 doesn't have this entry, so just update it
            nml1[opt] = nml2[opt]

    return 0
