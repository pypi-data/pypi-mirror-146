import sys
from os import path
simfempypath = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.insert(0,simfempypath)

import simfempy.meshes.testmeshes as testmeshes
from simfempy.applications.beam import Beam
import simfempy.applications.problemdata
from simfempy.tools.comparemethods import CompareMethods

#----------------------------------------------------------------#
def test(**kwargs):
    data = simfempy.applications.problemdata.ProblemData()
    exactsolution = kwargs.pop('exactsolution', 'Linear')
    paramsdict = {}
    data.params.scal_glob['EI'] = kwargs.pop('EI', 1)
    createMesh = testmeshes.unitline
    # data.bdrycond.set("Clamped", [10000, 10001])
    data.bdrycond.set("Clamped", [10000])
    # data.bdrycond.set("SimplySupported", [10001])
    data.bdrycond.set("Forces", [10001])
    linearsolver = kwargs.pop('linearsolver', 'spsolve')
    applicationargs= {'problemdata': data, 'exactsolution': exactsolution, 'linearsolver': linearsolver}
    comp =  CompareMethods(createMesh=createMesh, paramsdict=paramsdict, application=Beam, applicationargs=applicationargs, **kwargs)
    return comp.compare()

#================================================================#
if __name__ == '__main__':
    # test(exactsolution = '(x-0.5)**2', niter=8, h1=0.5, linearsolver='spsolve', plotsolution=True)
    test(niter=6, h1=0.5, linearsolver='spsolve', plotsolution=True)
