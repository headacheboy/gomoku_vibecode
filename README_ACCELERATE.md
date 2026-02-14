# Optional Cython acceleration

Steps to build the optional Cython-accelerated AI module:

1. Install a C compiler (on Windows install Visual Studio Build Tools).
2. Install build deps in your Python env:

```bash
pip install cython setuptools
```

3. From the project root run:

```bash
python setup_cython.py build_ext --inplace
```

This will produce a compiled `gomoku.ai_cy` extension. The codebase includes
`gomoku/ai_cy.pyx` as a scaffold; to get real speedups implement the hot
routines (`evaluate_board`, move generation and the search core) in typed
Cython (avoid Python object allocations in tight loops).

If building is difficult on Windows, consider using WSL or a Linux build host.
