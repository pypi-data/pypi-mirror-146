// SPDX-License-Identifier: GPL-2.0-only

%module(docstring="Python bindings for libimpel") impel
%feature("autodoc", "1");

%{
#include "getters.h"
%}

%include "../src/getters.h"
