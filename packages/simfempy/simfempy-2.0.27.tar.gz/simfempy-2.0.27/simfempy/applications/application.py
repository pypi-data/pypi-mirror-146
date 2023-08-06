# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 18:14:29 2016

@author: becker
"""

import numpy as np
import scipy.sparse as spsp
import scipy.sparse.linalg as splinalg
from scipy.optimize import root

import simfempy.tools.analyticalfunction
import simfempy.tools.timer
import simfempy.tools.iterationcounter
import simfempy.applications.problemdata
from simfempy.tools.analyticalfunction import AnalyticalFunction
import simfempy.solvers

# import warnings
# warnings.filterwarnings("error")

#=================================================================#
class Application(object):
    def __format__(self, spec):
        if spec=='-':
            repr = f"fem={self.fem}"
            repr += f"\tlinearsolver={self.linearsolver}"
            return repr
        return self.__repr__()
    def __repr__(self):
        if hasattr(self, 'mesh'):
            repr = f"mesh={self.mesh}"
        else:
            repr = "no mesh\n"
        repr += f"problemdata={self.problemdata}"
        repr += f"\nlinearsolver={self.linearsolver}"
        repr += f"\n{self.timer}"
        return repr
    def __init__(self, **kwargs):
        #TODO separate parameters in physical/numerical
        self.linearsolver = kwargs.pop('linearsolver', 'spsolve')
        self.linearsolvers=['spsolve', 'lgmres', 'bicgstab']
        try:
            import pyamg
            self.linearsolvers.append('pyamg')
        except:
            if self.linearsolver=='pyamg':
                import warnings
                warnings.warn("*** pyamg not found (spsolve used instead)***")
        self.mode = kwargs.pop('mode', 'linear')
        self.verbose = kwargs.pop('verbose', 0)
        self.timer = simfempy.tools.timer.Timer(verbose=self.verbose)
        if 'problemdata' in kwargs:
            self.problemdata = kwargs.pop('problemdata')
            self.ncomp = self.problemdata.ncomp
        if 'exactsolution' in kwargs:
            self.exactsolution = kwargs.pop('exactsolution')
            self._generatePDforES = True
            self.random_exactsolution = kwargs.pop('random',False)
        else:
            self._generatePDforES = False
        if 'geom' in kwargs:
            self.geom = kwargs.pop('geom')
            print(f"{self.geom=}")
            mesh = self.geom.generate_mesh()
            self.mesh = simfempy.meshes.simplexmesh.SimplexMesh(mesh=mesh)
        if 'mesh' in kwargs:
            # self.mesh = kwargs.pop('mesh')
            self.setMesh(kwargs.pop('mesh'))
        else:
            self._setMeshCalled = False
        if len(kwargs.keys()):
            raise ValueError(f"*** unused arguments {kwargs=}")
    def setMesh(self, mesh):
        self.timer.reset_all()
        self.problemdata.check(mesh)
        self.mesh = mesh
        if self.verbose: print(f"{self.mesh=}")
        self._setMeshCalled = True
        if hasattr(self,'_generatePDforES') and self._generatePDforES:
            self.generatePoblemDataForAnalyticalSolution()
            self._generatePDforES = False
    def solve(self, dirname="Run"): return self.static(dirname=dirname, mode=self.mode)
    # def setParameter(self, paramname, param):
    #     assert 0
    def dirichletfct(self):
        if self.ncomp > 1:
            # def _solexactdir(x, y, z):
            #     return [self.problemdata.solexact[icomp](x, y, z) for icomp in range(self.ncomp)]
            # return _solexactdir
            from functools import partial
            solexact = self.problemdata.solexact
            def _solexactdir(x, y, z, icomp):
                return solexact[icomp](x, y, z)
            return [partial(_solexactdir, icomp=icomp) for icomp in range(self.ncomp)]
        else:
            return self.problemdata.solexact
            def _solexactdir(x, y, z):
                return self.problemdata.solexact(x, y, z)
        return _solexactdir
    def generatePoblemDataForAnalyticalSolution(self):
        bdrycond = self.problemdata.bdrycond
        self.problemdata.solexact = self.defineAnalyticalSolution(exactsolution=self.exactsolution, random=self.random_exactsolution)
        # print("self.problemdata.solexact", self.problemdata.solexact)
        solexact = self.problemdata.solexact
        self.problemdata.params.fct_glob['rhs'] = self.defineRhsAnalyticalSolution(solexact)
        for color in self.mesh.bdrylabels:
            if color in bdrycond.type and bdrycond.type[color] in ["Dirichlet","dirichlet"]:
                bdrycond.fct[color] = self.dirichletfct()
            else:
                if color in bdrycond.type:
                    cmd = "self.define{}AnalyticalSolution(self.problemdata,{})".format(bdrycond.type[color], color)
                    # print(f"cmd={cmd}")
                    bdrycond.fct[color] = eval(cmd)
                else:
                    bdrycond.fct[color] = self.defineBdryFctAnalyticalSolution(color, solexact)
    def defineAnalyticalSolution(self, exactsolution, random=True):
        dim = self.mesh.dimension
        # print(f"defineAnalyticalSolution: {dim=} {self.ncomp=}")
        return simfempy.tools.analyticalfunction.analyticalSolution(exactsolution, dim, self.ncomp, random)
    def compute_cell_vector_from_params(self, name, params):
        if name in params.fct_glob:
            fct = np.vectorize(params.fct_glob[name])
            arr = np.empty(self.mesh.ncells)
            for color, cells in self.mesh.cellsoflabel.items():
                xc, yc, zc = self.mesh.pointsc[cells].T
                arr[cells] = fct(color, xc, yc, zc)
        elif name in params.scal_glob:
            arr = np.full(self.mesh.ncells, params.scal_glob[name])
        elif name in params.scal_cells:
            arr = np.empty(self.mesh.ncells)
            for color in params.scal_cells[name]:
                arr[self.mesh.cellsoflabel[color]] = params.scal_cells[name][color]
        else:
            msg = f"{name} should be given in 'fct_glob' or 'scal_glob' or 'scal_cells' (problemdata.params)"
            raise ValueError(msg)
        return arr
    def initsolution(self, b):
        if isinstance(b,tuple):
            return [np.copy(bi) for bi in b]
        return np.copy(b)
    def static(self, **kwargs):
        dirname = kwargs.pop('dirname','Run')
        mode = kwargs.pop('mode','linear')
        # self.timer.reset_all()
        result = simfempy.applications.problemdata.Results()
        if not self._setMeshCalled: self.setMesh(self.mesh)
        self.timer.add('setMesh')
        self.A = self.computeMatrix()
        self.timer.add('matrix')
        self.b = self.computeRhs()
        u = self.initsolution(self.b)
        self.timer.add('rhs')
        if mode == 'linear':
            try:
                u, niterlin = self.linearSolver(self.A, self.b, u)
            except Warning:
                raise ValueError(f"matrix is singular {self.A.shape=} {self.A.diagonal()=}")
            self.timer.add('solve')
            iter={'lin':niterlin}
        else:
            if 'sdata' in kwargs:
                sdata = kwargs.pop('sdata')
            else:
                maxiter = kwargs.pop('maxiter', 100)
                sdata = simfempy.solvers.newtondata.StoppingData(maxiter=maxiter)
            sdata.addname = self.linearsolver
            if mode == 'newton':
                info = simfempy.solvers.newton.newton(u, f=self.computeDefect, computedx=self.computeDx, verbose=True, sdata=sdata)
                # print(f"{info=}")
                u,niter,niterlin = info
                iter={'lin':niterlin, 'nlin':niter}
                if niter==sdata.maxiter: raise ValueError(f"*** Attained maxiter {sdata.maxiter=}")
            elif mode == 'newtonkrylov':
                counter = simfempy.tools.iterationcounter.IterationCounterWithRes(name=mode, disp=1, callback_type='x,Fx')
                n = u.shape[0]
                prec = splinalg.LinearOperator(shape=(n,n), matvec=lambda x: self.computePrec(x))
                root(fun=self.computeDefect, x0=u, args=(), method='krylov', tol=sdata.rtol, callback=counter, 
                options={'inner_M': prec})
            else:
                raise ValueError(f"unknwon {mode=}")
        pp = self.postProcess(u)
        if hasattr(self.problemdata.postproc, "changepostproc"):
            self.problemdata.postproc.changepostproc(pp['global'])
        self.timer.add('postp')
        result.setData(pp, timer=self.timer, iter=iter)
        return result
    def computeDefect(self, u):
        return self.computeForm(u)-self.b
    def computeForm(self, u):
        return self.A@u
    def computeDx(self, b, u, info):
        # if it>1:
        self.A = self.computeMatrix(u=u)           
        try:
            u, niter = self.linearSolver(self.A, b, u)
        except Warning:
            raise ValueError(f"matrix is singular {self.A.shape=} {self.A.diagonal()=}")
        self.timer.add('solve')
        return u, niter
    def initialCondition(self, interpolate=True):
        #TODO: higher order interpolation
        if not 'initial_condition' in self.problemdata.params.fct_glob:
            raise ValueError(f"missing 'initial_condition' in {self.problemdata.params.fct_glob=}")
        if not self._setMeshCalled: self.setMesh(self.mesh)
        ic = AnalyticalFunction(self.problemdata.params.fct_glob['initial_condition'])
        fp1 = self.fem.interpolate(ic)
        if interpolate:
            return fp1
        self.Mass = self.fem.computeMassMatrix()
        b = np.zeros(self.fem.nunknowns())
        self.fem.massDot(b, fp1)
        u, niter = self.linearSolver(self.Mass, b, u=fp1)
        return u
    def dynamic(self, u0, t_span, nframes, dt=None, mode='linear', callback=None, method='BE', verbose=1):
        if mode=='linear': return self.dynamic_linear(u0, t_span, nframes, dt, callback, method, verbose)
        raise NotImplementedError()
    def dynamic_linear(self, u0, t_span, nframes, dt=None, callback=None, method='CN', verbose=1):
        # TODO: passing time
        """
        u_t + A u = f, u(t_0) = u_0
        M(u^{n+1}-u^n)/dt + a Au^{n+1} + (1-a) A u^n = f
        (M/dt+aA) u^{n+1} =  f + (M/dt -(1-a)A)u^n
                          =  f + 1/a (M/dt) u^n - (1-a)/a (M/dt+aA)u^n
        (M/(a*dt)+A) u^{n+1} =  (1/a)*f + (M/(a*dt)-(1-a)/a A)u^n
                             =  (1/a)*f + 1/(a*a*dt) M u^n  - (1-a)/a*(M/(a*dt)+A)u^n
        :param u0: initial condition
        :param t_span: time interval bounds (tuple)
        :param nframes: number of frames to store
        :param dt: time-step (fixed for the moment!)
        :param mode: (only linear for the moment!)
        :param callback: if given function called for each frame with argumntes t, u
        :param method: CN or BE for Crank-Nicolson (a=1/2) or backward Euler (a=1)
        :return: results with data per frame
        """
        if not dt or dt<=0: raise NotImplementedError(f"needs constant positive 'dt")
        if t_span[0]>=t_span[1]: raise ValueError(f"something wrong in {t_span=}")
        if method not in ['BE','CN']: raise ValueError(f"unknown method {method=}")
        if method == 'BE': a = 1
        else: a = 0.5
        import math
        nitertotal = math.ceil((t_span[1]-t_span[0])/dt)
        if nframes > nitertotal:
            raise ValueError(f"Maximum valiue for nframes is {nitertotal=}")
        niter = nitertotal//nframes
        result = simfempy.applications.problemdata.Results(nframes)
        self.timer.add('init')
        if not hasattr(self, 'Mass'):
            self.Mass = self.fem.computeMassMatrix()
        if not hasattr(self, 'A'):
            self.Aimp = self.computeMatrix(coeffmass=1/dt/a)
            if self.linearsolver=="pyamg":
                self.pyamgml = self.build_pyamg(self.Aimp)
        self.timer.add('matrix')
        u = u0
        self.time = t_span[0]
        # rhs=None
        rhs = np.empty_like(u, dtype=float)
        # will be create by computeRhs()
        niterslinsol = np.zeros(niter, dtype=int)
        expl = (a-1)/a
        for iframe in range(nframes):
            if verbose: print(f"*** {self.time=} {iframe=} {niter=} {nframes=} {a=}")
            for iter in range(niter):
                self.time += dt
                rhs.fill(0)
                rhs += 1/(a*a*dt)*self.Mass.dot(u)
                rhs += expl*self.Aimp.dot(u)
                # print(f"@1@{np.min(u)=} {np.max(u)=} {np.min(rhs)=} {np.max(rhs)=}")
                rhs2 = self.computeRhs()
                rhs += (1/a)*rhs2
                # print(f"@2@{np.min(u)=} {np.max(u)=} {np.min(rhs)=} {np.max(rhs)=}")
                self.timer.add('rhs')
                # u, niterslinsol[iter] = self.linearSolver(self.ml, rhs, u=u, verbose=0)
                #TODO organiser solveur linéaire
                u, niterslinsol[iter] = self.linearSolver(self.Aimp, b=rhs, u=u)
                # print(f"{niterslinsol=} {np.linalg.norm(u)=}")
                # u, res = self.solve_pyamg(self.pyamgml, rhs, u=u, maxiter = 100)
                # u, niterslinsol[iter] = u, len(res)
                # print(f"@3@{np.min(u)=} {np.max(u)=} {np.min(rhs)=} {np.max(rhs)=}")
                self.timer.add('solve')
            result.addData(iframe, self.postProcess(u), time=self.time, iter=niterslinsol.mean())
            if callback: callback(self.time, u)
        return result

    def linearSolver(self, A, b, u=None, verbose=0, disp=0):
        if spsp.issparse(A):
            if len(b.shape)!=1 or len(A.shape)!=2 or b.shape[0] != A.shape[0]:
                raise ValueError(f"{A.shape=} {b.shape=}")
        if self.linearsolver is None: solver = self.linearsolver
        if not hasattr(self, 'info'): self.info={}
        if self.linearsolver not in self.linearsolvers: solver = "spsolve"
        if self.linearsolver == 'spsolve':
            return splinalg.spsolve(A, b), 1
            return splinalg.spsolve(A, b, permc_spec='COLAMD'), 1
        elif self.linearsolver in ['gmres','lgmres','bicgstab','cg','gcrotmk']:
            if self.linearsolver == 'cg':
                def gaussSeidel(A):
                    dd = A.diagonal()
                    D = spsp.dia_matrix(A.shape)
                    D.setdiag(dd)
                    L = spsp.tril(A, -1)
                    U = spsp.triu(A, 1)
                    return splinalg.factorized(D + L)
                M2 = gaussSeidel(A)
            else:
                # defaults: drop_tol=0.0001, fill_factor=10
                M2 = splinalg.spilu(A.tocsc(), drop_tol=0.1, fill_factor=3)
            M = splinalg.LinearOperator(A.shape, lambda x: M2.solve(x))
            counter = simfempy.tools.iterationcounter.IterationCounter(name=self.linearsolver, disp=disp)
            args=""
            cmd = "splinalg.{}(A, b, M=M, tol=1e-14, callback=counter {})".format(self.linearsolver,args)
            u, info = eval(cmd)
            # print(f"{u=}")
            return u, counter.niter
        elif self.linearsolver == 'pyamg':
            if not hasattr(self, 'pyamgml'):
                self.pyamgml = self.build_pyamg(A)
            maxiter = 100
            u, res = self.solve_pyamg(self.pyamgml, b, u, maxiter)
            if len(res) >= maxiter: raise ValueError(f"***no convergence {res=}")
            if(verbose): print('niter ({}) {:4d} ({:7.1e})'.format(solver, len(res),res[-1]/res[0]))
            return u, len(res)
        else:
            raise NotImplementedError("unknown solve '{}'".format(self.linearsolver))
    def pyamg_solver_args(self, maxiter):
        return {'cycle': 'V', 'maxiter': maxiter, 'tol': 1e-12, 'accel': 'gmres'}
    def solve_pyamg(self, ml, b, u, maxiter):
        res = []
        solver_args = self.pyamg_solver_args(maxiter=maxiter)
        u = ml.solve(b=b, x0=u, residuals=res, **solver_args)
        return u, res
    def build_pyamg(self,A):
        try:
            import pyamg
        except:
            raise ImportError(f"*** pyamg not found {self.linearsolver=} ***")
        return pyamg.smoothed_aggregation_solver(A)


# ------------------------------------- #

if __name__ == '__main__':
    raise ValueError("unit test to be written")