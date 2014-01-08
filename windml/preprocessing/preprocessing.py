"""
Copyright (c) 2013,
Fabian Gieseke, Justin P. Heinermann, Oliver Kramer, Jendrik Poloczek,
Nils A. Treiber
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

    Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

    Neither the name of the Computational Intelligence Group of the University
    of Oldenburg nor the names of its contributors may be used to endorse or
    promote products derived from this software without specific prior written
    permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from windml.preprocessing.topologic_interpolation import TopologicInterpolation
from windml.preprocessing.backward_copy import BackwardCopy
from windml.preprocessing.forward_copy import ForwardCopy
from windml.preprocessing.linear_interpolation import LinearInterpolation
from windml.preprocessing.override_missing import OverrideMissing
from windml.preprocessing.mar_destroyer import MARDestroyer
from windml.preprocessing.nmar_destroyer import NMARDestroyer
from windml.preprocessing.marthres_destroyer import MARThresDestroyer
from windml.preprocessing.duplicate_remover import DuplicateRemover
from windml.preprocessing.nrel_repair import NRELRepair
from windml.preprocessing.mreg_interpolation import MRegInterpolation
from windml.preprocessing.smoother import Smoother

def smoothen(timeseries, **args):
    return Smoother().smooth(timeseries, args)

def repair_nrel(timeseries):
    return NRELRepair().repair(timeseries)

def override_missing(timeseries, timestep, override_val):
    return OverrideMissing().override(timeseries, timestep, override_val)

def interpolate(timeseries, method, **args):
    methods = {'linear': LinearInterpolation().interpolate,
               'topologic': TopologicInterpolation().interpolate,
               'forwardcopy': ForwardCopy().interpolate,
               'backwardcopy': BackwardCopy().interpolate,
               'mreg': MRegInterpolation().interpolate}

    return methods[method](timeseries, **args)

def destroy(timeseries, method, **args):
    methods = {'mar': MARDestroyer().destroy,
               'nmar': NMARDestroyer().destroy,
               'mar_with_threshold': MARThresDestroyer().destroy}

    return methods[method](timeseries, **args)

def remove_duplicates(timeseries):
    return DuplicateRemover().remove(timeseries)

def normalize(timeseries):
    pass
