import testcaseanalytical
import numpy as np
import stokes_analytic

#================================================================#
class TestAnalyticalStokes(testcaseanalytical.TestCaseAnalytical):
    def __init__(self, args):
        args['exactsolution'] = 'Linear'
        args['verbose'] = 0
        args['linearsolver'] = 'spsolve'
        super().__init__(args)
    def runTest(self):
        errors = stokes_analytic.test(**self.args).errors
        self.checkerrors(errors)

#================================================================#
from simfempy.tools import tools
paramsdicts = {'dim':[2,3], 'dirichletmethod':['nitsche','strong']}
testcaseanalytical.run(testcase=TestAnalyticalStokes, argss=tools.dictproduct(paramsdicts))
