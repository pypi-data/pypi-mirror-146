import numpy as np
from numpy.lib.function_base import copy
from simfempy.applications.stokes import Stokes
from simfempy import fems, meshes, solvers
import scipy.sparse as sparse

class NavierStokes(Stokes):
    def __format__(self, spec):
        if spec=='-':
            repr = super().__format__(spec)
            repr += f"\tconvmethod={self.convmethod}"
            return repr
        return self.__repr__()
    def __init__(self, **kwargs):
        self.mode='nonlinear'
        self.convdata = fems.data.ConvectionData()
        self.convmethod = kwargs.pop('convmethod', 'lps')
        self.lpsparam = kwargs.pop('lpsparam', 0.01)
        self.newtontol = kwargs.pop('newtontol', 1e-8)
        if kwargs['linearsolver'] != 'spsolve' and not 'precond_p' in kwargs:
            kwargs['precond_p'] = 'schur@diag@3@scipy_gmres'
        if kwargs['linearsolver'] != 'spsolve' and not not 'precond_v' in kwargs:
            defsolvers = ['scipy_lgmres', 'pyamg_gmres']
            defsolvers.append('pyamg@aggregation@none@gauss_seidel')
            defsolvers.append('pyamg@aggregation@none@schwarz')
            # defsolvers.append('pyamg@aggregation@fgmres@gauss_seidel')
            defsolvers.append('pyamg@aggregation@fgmres@schwarz')
            kwargs['precond_v'] = defsolvers
        super().__init__(**kwargs)
    def setMesh(self, mesh):
        super().setMesh(mesh)
        self.Astokes = super().computeMatrix()
    def solve(self, dirname="Run"):
        sdata = solvers.newtondata.StoppingData(maxiter=200, steptype='bt', nbase=1, rtol=self.newtontol)
        return self.static(dirname=dirname, mode='newton',sdata=sdata)
    def computeForm(self, u):
        # if not hasattr(self,'Astokes'): self.Astokes = super().computeMatrix()
        # d = super().matrixVector(self.Astokes,u)
        d = self.Astokes.matvec(u)
        # d = super().computeForm(u)
        v = self._split(u)[0]
        dv = self._split(d)[0]
        self.computeFormConvection(dv, v)
        # self.femv.computeFormHdivPenaly(dv, v, self.hdivpenalty)
        self.timer.add('form')
        return d
    def computeMatrix(self, u=None):
        # if not hasattr(self,'Astokes'): self.Astokes = super().computeMatrix()
        if u is None: return self.Astokes
        # X = [A.copy() for A in self.Astokes]
        # X = super().computeMatrix(u)
        X = self.Astokes.copy()
        v = self._split(u)[0]
        # X[0] += self.computeMatrixConvection(v)
        X.A += self.computeMatrixConvection(v)
        # X[0] += self.femv.computeMatrixHdivPenaly(self.hdivpenalty)
        self.timer.add('matrix')
        return X
    def computeFormConvection(self, dv, v):
        dim = self.mesh.dimension
        rt = fems.rt0.RT0(self.mesh)
        self.convdata.betart = rt.interpolateCR1(v)
        self.convdata.beta = rt.toCell(self.convdata.betart)
        if self.convmethod=='supg' or self.convmethod=='lps':
            if not hasattr(self.mesh,'innerfaces'): self.mesh.constructInnerFaces()
        if self.convmethod=='supg':
            self.convdata.md = meshes.move.move_midpoints(self.mesh, self.convdata.beta, bound=1/dim)
        colorsdirichlet = self.problemdata.bdrycond.colorsOfType("Dirichlet")
        vdir = self.femv.interpolateBoundary(colorsdirichlet, self.problemdata.bdrycond.fct).ravel()
        self.femv.massDotBoundary(dv, vdir, colors=colorsdirichlet, ncomp=self.ncomp, coeff=np.minimum(self.convdata.betart, 0))
        for icomp in range(dim):
            self.femv.fem.computeFormConvection(dv[icomp::dim], v[icomp::dim], self.convdata, method=self.convmethod, lpsparam=self.lpsparam)
    def computeMatrixConvection(self, v):
        A = self.femv.fem.computeMatrixConvection(self.convdata, method=self.convmethod, lpsparam=self.lpsparam)
        return self.femv.matrix2systemdiagonal(A, self.ncomp).tocsr()
    def computeBdryNormalFluxNitsche(self, v, p, colors):
        ncomp, bdryfct = self.ncomp, self.problemdata.bdrycond.fct
        flux = super().computeBdryNormalFluxNitsche(v,p,colors)
        vdir = self.femv.interpolateBoundary(colors, bdryfct).ravel()
        for icomp in range(ncomp):
            for i,color in enumerate(colors):
                flux[icomp,i] -= self.femv.fem.massDotBoundary(b=None, f=v[icomp::ncomp]-vdir[icomp::ncomp], colors=[color], coeff=np.minimum(self.convdata.betart, 0))
        return flux
    def computeDx(self, b, u, info):
        # it,rhor,dx, step, y = info
        if info.iter>1: rtol = min(0.1,info.rhor)
        else: rtol = 0.1
        self.A = self.computeMatrix(u=u) 
        # if dx is not None and it>2:
        #     dv = self._split(dx)[0]
        #     yv = self._split(y)[0]
        #     self.A[0] = tools.matrix.addRankOne(self.A[0], step*dv, yv, relax=1)          
        try:
            # u, niter = self.linearSolver(self.A, bin=b, uin=None, linearsolver=self.linearsolver, rtol=rtol)
            u, niter = self.linearSolver(self.A, bin=b, uin=None, rtol=rtol)
        except Warning:
            raise ValueError(f"matrix is singular {self.A.shape=} {self.A.diagonal()=}")
        self.timer.add('solve')
        return u, niter
    def computePrec(self, b, u=None):
        self.A = self.computeMatrix(u=u) 
        try:
            u, niter = self.linearSolver(self.A, bin=b, uin=u, rtol=0.1)
        except Warning:
            raise ValueError(f"matrix is singular {self.A.shape=} {self.A.diagonal()=}")
        self.timer.add('solve')
        return u
      
