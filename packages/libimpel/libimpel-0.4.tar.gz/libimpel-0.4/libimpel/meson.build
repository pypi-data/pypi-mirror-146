want_python = get_option('python')
if want_python != 'false'
    python3 = import('python').find_installation('python3')
    py3_dep = python3.dependency(required: want_python == 'true')
    swig = find_program('swig', required: want_python == 'true')
    header_found = cc.has_header('Python.h', dependencies: py3_dep)
    have_python_support = py3_dep.found() and swig.found() and header_found
else
    have_python_support = false
endif

if have_python_support
    pymod_swig = custom_target(
        'impel.py',
        input:   ['impel.i'],
        output:  ['impel.py', 'impel_wrap.c'],
        command: [swig, '-python', '-py3', '-o', '@OUTPUT1@', '@INPUT0@'],
        install: true,
        install_dir: [python3.get_install_dir(pure: false, subdir: 'libimpel'), false],
    )

    pyimpel_clib = python3.extension_module(
        '_impel',
        pymod_swig[1],
        dependencies : py3_dep,
        include_directories: [incdir, private_incdir],
        link_with: [libimpel],
        install: true,
        subdir: 'libimpel',
    )

    # Little hack to copy file __init__.py to the build directory.
    # This is needed to create the proper directory layout to run the tests.
    # It's a hack because we don't really "configure" file __init__.py and we
    # could simply install directly from the source tree with:
    #   python3.install_sources(['__init__.py', ], pure:false, subdir:'libimpel')
    # However, since we need __init__.py in the build directory to run the tests
    # we resort to this hack to copy it.
    configure_file(
        input:  '__init__.py',
        output: '__init__.py',
        copy: true,
        install_dir: python3.get_install_dir(pure: false, subdir: 'libimpel'),
    )

    # Set the PYTHONPATH so that we can run the
    # tests directly from the build directory.
    test_env = environment()
    test_env.append('MALLOC_PERTURB_', '0')
    test_env.append('PYTHONPATH', join_paths(meson.current_build_dir(), '..'))
    test_env.append('PYTHONMALLOC', 'malloc')

    # Test section
    test('[Python] import libimpel', python3, args: ['-c', 'from libimpel import impel'], env: test_env, depends: pyimpel_clib)

    py_tests = [
        [ 'simple smoke test', files('tests/smoke.py') ],
    ]
    foreach test: py_tests
        description = test[0]
        py_script   = test[1]
        test('[Python] ' + description, python3, args: [py_script, ], env: test_env, depends: pyimpel_clib)
    endforeach
endif
