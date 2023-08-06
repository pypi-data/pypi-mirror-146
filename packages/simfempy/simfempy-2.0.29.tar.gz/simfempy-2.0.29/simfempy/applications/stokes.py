import copy

from matplotlib import colors
import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as splinalg
from simfempy import fems, tools, solvers
from simfempy.applications.application import Application
from simfempy.tools.analyticalfunction import analyticalSolution
from simfempy.solvers import linalg
from functools import partial

#=================================================================#
class Stokes(Application):
    """
    """
    def __format__(self, spec):
        if spec=='-':
            repr = f"{self.femv=} {self.femp=}"
            if self.linearsolver=='spsolve': return repr + self.linearsolver
            ls = '@'.join([str(v) for v in self.linearsolver.values()])
            vs = '@'.join([str(v) for v in self.solver_v.values()])
            # print(f"{self.solver_p=}")
            ps = '@'.join([str(v) for v in self.solver_p.values()])
            repr += f"\tlinearsolver={ls} V:{vs} P:{ps}"
            return repr
        return self.__repr__()
    def _solvername_to_dict(self, name, type=None):
        nsp = name.split('@')
        if type == 'linearsolver':
            if len(nsp) != 4:
                raise ValueError(f"*** need 'linearsolver' in the form 'method@prec@maxiter@disp' got '{name}'")
            return {'method': nsp[0], 'prec': nsp[1], 'maxiter': int(nsp[2]), 'disp': int(nsp[3])}
        elif type == 'solver_v':
            if nsp[0]=='pyamg':
                if len(nsp)!=6:
                    raise ValueError(f"*** need 'solver_v' in the form 'pyamg@pyamgtype@accel@smoother@maxiter@disp'")
                return {'method':nsp[0], 'pyamgtype':nsp[1], 'accel':nsp[2], 'smoother':nsp[3],
                            'maxiter':int(nsp[4]), 'disp':int(nsp[5])}
            else:
                return {'method': nsp[0], 'prec': nsp[1], 'maxiter': int(nsp[2]), 'disp': int(nsp[3])}
        elif type == 'solver_p':
            if nsp[0] == 'scale': return {'type': 'scale'}
            if len(nsp)<2:
                raise ValueError(f"*** need 'solver_p' in the form 'tye@method@...@disp'")
            elif nsp[1]=='pyamg':
                if len(nsp) != 7:
                    raise ValueError(
                        f"*** need 'solver_p' in the form 'type@pyamg@pyamgtype@accel@smoother@maxiter@disp'")
                return {'type':nsp[0], 'method':nsp[1], 'pyamgtype':nsp[2], 'accel':nsp[3], 'smoother':nsp[4],
                        'maxiter':int(nsp[5]), 'disp':int(nsp[6])}
            else:
                if len(nsp) != 5:
                    raise ValueError(
                        f"*** need 'solver_p' in the form 'type@method@prec@maxiter@disp'")
                return {'type':nsp[0], 'method': nsp[1], 'prec': nsp[2], 'maxiter': int(nsp[3]), 'disp': int(nsp[4])}
        else: raise ValueError(f"*** unknown {type=}")
    def __init__(self, **kwargs):
        if 'dirichletmethod' in kwargs and kwargs['dirichletmethod']=='nitsche':
            # correct value ?!
            kwargs['nitscheparam'] = 10
        self.dirichletmethod = kwargs.get('dirichletmethod', 'nitsche')
        self.problemdata = kwargs.pop('problemdata')
        self.ncomp = self.problemdata.ncomp
        self.femv = fems.cr1sys.CR1sys(self.ncomp, kwargs)
        self.femp = fems.d0.D0()
        self.hdivpenalty = kwargs.pop('hdivpenalty', 0)
        self.divdivparam = kwargs.pop('divdivparam', 0)
        self.scalels = kwargs.pop('scalels', False)
        if not 'linearsolver' in kwargs:
            linearsolver_def = {'method': 'pyamg_gmres', 'prec':'full', 'maxiter': 200, 'disp':0}
            kwargs['linearsolver'] = linearsolver_def
        else:
            linearsolver = kwargs['linearsolver']
            if not isinstance(linearsolver, str):
                raise ValueError(f"*** need 'linearsolver' as str")
            if not kwargs['linearsolver'] == 'spsolve':
                kwargs['linearsolver'] = self._solvername_to_dict(linearsolver, type='linearsolver')
        if not 'solver_p' in kwargs:
            self.solver_p = {'type': 'scale'}
        else:
            solver_p = kwargs.pop('solver_p')
            if isinstance(solver_p, str):
                self.solver_p = self._solvername_to_dict(solver_p, type='solver_p')
                # print(f"???? {self.solver_p=}")
            else:
                raise ValueError(f"*** need 'solver_p' as str")
        if not 'solver_v' in kwargs:
            solver_v_def = {'method': 'pyamg', 'pyamgtype': 'aggregation', 'accel': 'none', 'smoother': 'gauss_seidel',
                            'maxiter': 1, 'disp': 0}
            self.solver_v = solver_v_def
        else:
            solver_v = kwargs.pop('solver_v')
            if isinstance(solver_v, str):
                self.solver_v = self._solvername_to_dict(solver_v, type='solver_v')
            else:
                raise ValueError(f"*** need 'solver_v' in the form 'method@prec@maxiter@disp'")
        super().__init__(**kwargs)
    def _zeros(self):
        nv = self.mesh.dimension*self.mesh.nfaces
        n = nv+self.mesh.ncells
        if self.pmean: n += 1
        return np.zeros(n)
    def _split(self, x):
        nv = self.mesh.dimension*self.mesh.nfaces
        ind = [nv]
        if self.pmean: ind.append(nv+self.mesh.ncells)
        # print(f"{ind=} {np.split(x, ind)=}")
        return np.split(x, ind)
    def setMesh(self, mesh):
        super().setMesh(mesh)
        self._checkProblemData()
        assert self.ncomp==self.mesh.dimension
        self.femv.setMesh(self.mesh)
        self.femp.setMesh(self.mesh)
        self.mucell = self.compute_cell_vector_from_params('mu', self.problemdata.params)
        self.pmean = not ('Neumann' in self.problemdata.bdrycond.type.values() or 'Pressure' in self.problemdata.bdrycond.type.values())
        if self.dirichletmethod=='strong':
            assert 'Navier' not in self.problemdata.bdrycond.type.values()
            colorsdirichlet = self.problemdata.bdrycond.colorsOfType("Dirichlet")
            colorsflux = self.problemdata.postproc.colorsOfType("bdry_nflux")
            self.bdrydata = self.femv.prepareBoundary(colorsdirichlet, colorsflux)
    def _checkProblemData(self):
        # TODO checkProblemData() incomplete
        for col, fct in self.problemdata.bdrycond.fct.items():
            type = self.problemdata.bdrycond.type[col]
            if type == "Dirichlet":
                if len(fct) != self.mesh.dimension: raise ValueError(f"*** {type=} {len(fct)=} {self.mesh.dimension=}")
    def defineAnalyticalSolution(self, exactsolution, random=True):
        dim = self.mesh.dimension
        # print(f"defineAnalyticalSolution: {dim=} {self.ncomp=}")
        if exactsolution=="Linear":
            exactsolution = ["Linear", "Constant"]
        elif exactsolution=="Quadratic":
            exactsolution = ["Quadratic", "Linear"]
        v = analyticalSolution(exactsolution[0], dim, dim, random)
        p = analyticalSolution(exactsolution[1], dim, 1, random)
        return v,p
    def dirichletfct(self):
        solexact = self.problemdata.solexact
        v,p = solexact
        # def _solexactdirv(x, y, z):
        #     return [v[icomp](x, y, z) for icomp in range(self.ncomp)]
        def _solexactdirp(x, y, z, nx, ny, nz):
            return p(x, y, z)
        from functools import partial
        def _solexactdirv(x, y, z, icomp):
            # print(f"{icomp=}")
            return v[icomp](x, y, z)
        return [partial(_solexactdirv, icomp=icomp) for icomp in range(self.ncomp)]
        # return _solexactdirv
    def defineRhsAnalyticalSolution(self, solexact):
        v,p = solexact
        mu = self.problemdata.params.scal_glob['mu']
        def _fctrhsv(x, y, z):
            rhsv = np.zeros(shape=(self.ncomp, *x.shape))
            for i in range(self.ncomp):
                for j in range(self.ncomp):
                    rhsv[i] -= mu * v[i].dd(j, j, x, y, z)
                rhsv[i] += p.d(i, x, y, z)
            # print(f"{rhsv=}")
            return rhsv
        def _fctrhsp(x, y, z):
            rhsp = np.zeros(x.shape)
            for i in range(self.ncomp):
                rhsp += v[i].d(i, x, y, z)
            return rhsp
        return _fctrhsv, _fctrhsp
    def defineNeumannAnalyticalSolution(self, problemdata, color):
        solexact = problemdata.solexact
        mu = self.problemdata.params.scal_glob['mu']
        def _fctneumannv(x, y, z, nx, ny, nz, icomp):
            v, p = solexact
            rhsv = np.zeros(shape=x.shape)
            normals = nx, ny, nz
            # for i in range(self.ncomp):
            for j in range(self.ncomp):
                rhsv += mu  * v[icomp].d(j, x, y, z) * normals[j]
            rhsv -= p(x, y, z) * normals[icomp]
            return rhsv
        return [partial(_fctneumannv, icomp=icomp) for icomp in range(self.ncomp)]
    def defineNavierAnalyticalSolution(self, problemdata, color):
        solexact = problemdata.solexact
        mu = self.problemdata.params.scal_glob['mu']
        lambdaR = self.problemdata.params.scal_glob['navier']
        def _fctnaviervn(x, y, z, nx, ny, nz):
            v, p = solexact
            rhs = np.zeros(shape=x.shape)
            normals = nx, ny, nz
            # print(f"{x.shape=} {nx.shape=} {normals[0].shape=}")
            for i in range(self.ncomp):
                rhs += v[i](x, y, z) * normals[i]
            return rhs
        def _fctnaviertangent(x, y, z, nx, ny, nz, icomp):
            v, p = solexact
            rhs = np.zeros(shape=x.shape)
            # h = np.zeros(shape=(self.ncomp, x.shape[0]))
            normals = nx, ny, nz
            rhs = lambdaR*v[icomp](x, y, z)
            for j in range(self.ncomp):
                rhs += mu*v[icomp].d(j, x, y, z) * normals[j]
            return rhs
        return {'vn':_fctnaviervn, 'g':[partial(_fctnaviertangent, icomp=icomp) for icomp in range(self.ncomp)]}
    def definePressureAnalyticalSolution(self, problemdata, color):
        solexact = problemdata.solexact
        mu = self.problemdata.params.scal_glob['mu']
        lambdaR = self.problemdata.params.scal_glob['navier']
        def _fctpressure(x, y, z, nx, ny, nz):
            v, p = solexact
            # rhs = np.zeros(shape=x.shape)
            normals = nx, ny, nz
            # print(f"{x.shape=} {nx.shape=} {normals[0].shape=}")
            rhs = 1.0*p(x,y,z)
            for i in range(self.ncomp):
                for j in range(self.ncomp):
                    rhs -= mu*v[j].d(i, x, y, z) * normals[i]* normals[j]
            return rhs
        def _fctpressurevtang(x, y, z, nx, ny, nz, icomp):
            v, p = solexact
            return v[icomp](x,y,z)
        return {'p':_fctpressure, 'v':[partial(_fctpressurevtang, icomp=icomp) for icomp in range(self.ncomp)]}
    def postProcess(self, u):
        if self.pmean: v, p, lam = self._split(u)
        else: v, p = self._split(u)
        # if self.pmean:
        #     v,p,lam =  u
        #     print(f"{lam=}")
        # else: v,p =  u
        data = {'point':{}, 'cell':{}, 'global':{}}
        for icomp in range(self.ncomp):
            data['point'][f'V_{icomp:01d}'] = self.femv.fem.tonode(v[icomp::self.ncomp])
        data['cell']['P'] = p
        if self.problemdata.solexact:
            err, e = self.femv.computeErrorL2(self.problemdata.solexact[0], v)
            data['global']['error_V_L2'] = np.sum(err)
            err, e = self.femp.computeErrorL2(self.problemdata.solexact[1], p)
            data['global']['error_P_L2'] = err
        if self.problemdata.postproc:
            types = ["bdry_pmean", "bdry_vmean", "bdry_nflux"]
            for name, type in self.problemdata.postproc.type.items():
                colors = self.problemdata.postproc.colors(name)
                if type == types[0]:
                    data['global'][name] = self.femp.computeBdryMean(p, colors)
                elif type == types[1]:
                    data['global'][name] = self.femv.computeBdryMean(v, colors)
                elif type == types[2]:
                    if self.dirichletmethod=='strong':
                        data['global'][name] = self.computeBdryNormalFluxStrong(v, p, colors)
                    else:
                        data['global'][name] = self.computeBdryNormalFluxNitsche(v, p, colors)
                else:
                    raise ValueError(f"unknown postprocess type '{type}' for key '{name}'\nknown types={types=}")
        return data
    def linearSolver(self, Ain, bin, uin=None, verbose=0, atol=1e-16, rtol=1e-10):
        if self.linearsolver == 'spsolve':
            Aall = Ain.to_single_matrix()
            uall =  splinalg.spsolve(Aall, bin, permc_spec='COLAMD')
            self.timer.add("linearsolve")
            return uall, 1
        else:
            linearsolver = copy.deepcopy(self.linearsolver)
            solver_p = copy.deepcopy(self.solver_p)
            # print(f"{self.solver_p=}")
            solver_v = copy.deepcopy(self.solver_v)
            prec = linearsolver.pop("prec", "full")
            if solver_p['type']=='scale':
                solver_p['coeff'] = self.mesh.dV/self.mucell
            print(f"{self.scalels=}")
            if self.scalels: Ain.scaleAb(bin)
            P = linalg.SaddlePointPreconditioner(Ain, solver_v=solver_v, solver_p=solver_p, method=prec)
            assert isinstance(self.linearsolver, dict)
            linearsolver['counter'] = 'sys '
            linearsolver['matvec'] = Ain.matvec
            linearsolver['matvecprec'] = P.matvecprec
            linearsolver['n'] = Ain.nall
            S = linalg.getSolver(args=linearsolver)
            maxiter = S.maxiter
            uall =  S.solve(b=bin, x0=uin)
            if self.scalels: Ain.scaleu(uall)
            self.timer.add("linearsolve")
            it = S.counter.niter
            if it==maxiter or np.linalg.norm(uall)<atol:
                msg = f"*** linear system solver not converged in {maxiter=}"
                msg += f"\n{np.linalg.norm(uall)=} {np.linalg.norm(bin)=}"
                msg += f"\n{S=}"
                msg += f"\n{P=}"
                msg += f"\n{S.counter=}"
                # raise ValueError(msg)
                print(msg)
                it = -1
            return uall, it
    def computeRhs(self, b=None, u=None, coeffmass=None):
        b = self._zeros()
        bs  = self._split(b)
        bv,bp = bs[0], bs[1]
        if 'rhs' in self.problemdata.params.fct_glob:
            rhsv, rhsp = self.problemdata.params.fct_glob['rhs']
            if rhsv: self.femv.computeRhsCells(bv, rhsv)
            if rhsp: self.femp.computeRhsCells(bp, rhsp)
        colorsdir = self.problemdata.bdrycond.colorsOfType("Dirichlet")
        colorsneu = self.problemdata.bdrycond.colorsOfType("Neumann")
        colorsnav = self.problemdata.bdrycond.colorsOfType("Navier")
        colorsp = self.problemdata.bdrycond.colorsOfType("Pressure")
        self.femv.computeRhsBoundary(bv, colorsneu, self.problemdata.bdrycond.fct)
        if self.dirichletmethod=='strong':
            self.vectorBoundaryStrong((bv, bp), self.problemdata.bdrycond.fct, self.bdrydata, self.dirichletmethod)
        else:
            vdir = self.femv.interpolateBoundary(colorsdir, self.problemdata.bdrycond.fct)
            self.computeRhsBdryNitscheDirichlet((bv,bp), colorsdir, vdir, self.mucell)
            bdryfct = self.problemdata.bdrycond.fct
            # Navier condition
            colors = set(bdryfct.keys()).intersection(colorsnav)
            if len(colors):
                if not isinstance(bdryfct[next(iter(colors))],dict):
                    msg = """
                    For Navier b.c. please give a dictionary {vn:fct_scal, g:fvt_vec} with fct_scal scalar and fvt_vec a list of dim functions
                    """
                    raise ValueError(msg+f"\ngiven: {bdryfct[next(iter(colors))]=}")
                vnfct, gfct = {}, {}
                for col in colors:
                    if 'vn' in bdryfct[col].keys() : 
                        if not callable(bdryfct[col]['vn']):
                            raise ValueError(f"'vn' must be a function. Given:{bdryfct[col]['vn']=}")
                        vnfct[col] = bdryfct[col]['vn']
                    if 'g' in bdryfct[col].keys() : 
                        if not isinstance(bdryfct[col]['g'], list) or len(bdryfct[col]['g'])!=self.ncomp:
                            raise ValueError(f"'g' must be a list of functions with {self.ncomp} elements. Given:{bdryfct[col]['g']=}")
                        gfct[col] = bdryfct[col]['g']
                if len(vnfct): 
                    vn = self.femv.fem.interpolateBoundary(colorsnav, vnfct, lumped=False)
                    self.computeRhsBdryNitscheNavierNormal((bv,bp), colorsnav, self.mucell, vn)
                if len(gfct): 
                    gt = self.femv.interpolateBoundary(colorsnav, gfct)
                    self.computeRhsBdryNitscheNavierTangent((bv,bp), colorsnav, self.mucell, gt)
            # Pressure condition
            colors = set(bdryfct.keys()).intersection(colorsp)
            if len(colors):
                if not isinstance(bdryfct[next(iter(colors))],dict):
                    msg = """
                    For Pressure b.c. please give a dictionary {p:fct_scal, v:fvt_vec} with fct_scal scalar and fvt_vec a list of dim functions
                    """
                    raise ValueError(msg+f"\ngiven: {bdryfct[next(iter(colors))]=}")
                pfct, vfct = {}, {}
                for col in colors:
                    if 'p' in bdryfct[col].keys() : 
                        if not callable(bdryfct[col]['p']):
                            raise ValueError(f"'vn' must be a function. Given:{bdryfct[col]['p']=}")
                        pfct[col] = bdryfct[col]['p']
                    if 'v' in bdryfct[col].keys() : 
                        if not isinstance(bdryfct[col]['v'], list) or len(bdryfct[col]['v'])!=self.ncomp:
                            raise ValueError(f"'v' must be a list of functions with {self.ncomp} elements. Given:{bdryfct[col]['v']=}")
                        vfct[col] = bdryfct[col]['v']
                if len(pfct):
                    p = self.femv.fem.interpolateBoundary(colorsp, pfct, lumped=False)
                    self.computeRhsBdryNitschePressureNormal((bv,bp), colorsp, self.mucell, p)
                if len(vfct): 
                    v = self.femv.interpolateBoundary(colorsp, vfct)
                    self.computeRhsBdryNitschePressureTangent((bv,bp), colorsp, self.mucell, v)
        if not self.pmean: return b
        if self.problemdata.solexact is not None:
            p = self.problemdata.solexact[1]
            bmean = self.femp.computeMean(p)
        else: bmean=0
        b[-1] = bmean
        return b
    def computeForm(self, u):
        d = np.zeros_like(u)
        if self.pmean: 
            v, p, lam = self._split(u)
            dv, dp, dlam = self._split(d)
        else: 
            v, p = self._split(u)
            dv, dp = self._split(d)
        # d2 = self.matrixVector(self.A, u)
        self.femv.computeFormLaplace(self.mucell, dv, v)
        self.femv.computeFormDivGrad(dv, dp, v, p)
        colorsdir = self.problemdata.bdrycond.colorsOfType("Dirichlet")
        colorsnav = self.problemdata.bdrycond.colorsOfType("Navier")
        if self.dirichletmethod == 'strong':
            self.femv.formBoundary(dv, self.bdrydata, self.dirichletmethod)
        else:
            self.computeFormBdryNitscheDirichlet(dv, dp, v, p, colorsdir, self.mucell)
            self.computeFormBdryNitscheNavier(dv, dp, v, p, colorsnav, self.mucell)
        if self.pmean:
            self.computeFormMeanPressure(dp, dlam, p, lam)
        # if not np.allclose(d,d2):
        #     raise ValueError(f"{d=}\n{d2=}")
        return d
    def computeMatrix(self, u=None):
        A = self.femv.computeMatrixLaplace(self.mucell)
        B = self.femv.computeMatrixDivergence()
        colorsdir = self.problemdata.bdrycond.colorsOfType("Dirichlet")
        colorsnav = self.problemdata.bdrycond.colorsOfType("Navier")
        colorsp = self.problemdata.bdrycond.colorsOfType("Pressure")
        if self.dirichletmethod == 'strong':
            A, B = self.matrixBoundaryStrong(A, B, self.bdrydata, self.dirichletmethod)
        else:
            #TODO eviter le retour de A,B
            # print(f"{id(A)=} {id(B)=}")
            A, B = self.computeMatrixBdryNitscheDirichlet(A, B, colorsdir, self.mucell)
            # print(f"{id(A)=} {id(B)=}")
            lam = self.problemdata.params.scal_glob.get('navier',0) 
            A, B = self.computeMatrixBdryNitscheNavier(A, B, colorsnav, self.mucell, lam)
            A, B = self.computeMatrixBdryNitschePressure(A, B, colorsp, self.mucell)
            # print(f"{id(A)=} {id(B)=}")
        if self.hdivpenalty:
            if not hasattr(self.mesh,'innerfaces'): self.mesh.constructInnerFaces()
            A += self.femv.computeMatrixHdivPenaly(self.hdivpenalty)
        if self.divdivparam:
            A += self.femv.computeMatrixDivDiv(self.divdivparam)
        if not self.pmean:
            return linalg.SaddlePointSystem(A, B)
        ncells = self.mesh.ncells
        rows = np.zeros(ncells, dtype=int)
        cols = np.arange(0, ncells)
        C = sparse.coo_matrix((self.mesh.dV, (rows, cols)), shape=(1, ncells)).tocsr()
        return linalg.SaddlePointSystem(A, B, C)
    def computeFormMeanPressure(self,dp, dlam, p, lam):
        dlam += self.mesh.dV.dot(p)
        dp += lam*self.mesh.dV
    def computeBdryNormalFluxNitsche(self, v, p, colors):
        ncomp, bdryfct = self.ncomp, self.problemdata.bdrycond.fct
        flux = np.zeros(shape=(ncomp,len(colors)))
        vdir = self.femv.interpolateBoundary(colors, bdryfct).ravel()
        for icomp in range(ncomp):
            flux[icomp] = self.femv.fem.computeBdryNormalFluxNitsche(v[icomp::ncomp], colors, vdir[icomp::ncomp], self.mucell)
            for i,color in enumerate(colors):
                faces = self.mesh.bdrylabels[color]
                cells = self.mesh.cellsOfFaces[faces,0]
                normalsS = self.mesh.normals[faces][:,:ncomp]
                dS = np.linalg.norm(normalsS, axis=1)
                flux[icomp,i] -= p[cells].dot(normalsS[:,icomp])
        return flux
    def computeRhsBdryNitscheDirichlet(self, b, colors, vdir, mucell, coeff=1):
        bv, bp = b
        ncomp  = self.ncomp
        faces = self.mesh.bdryFaces(colors)
        cells = self.mesh.cellsOfFaces[faces,0]
        normalsS = self.mesh.normals[faces][:,:ncomp]
        np.add.at(bp, cells, -np.einsum('nk,nk->n', coeff*vdir[faces], normalsS))
        self.femv.computeRhsNitscheDiffusion(bv, mucell, colors, vdir, ncomp)
    def computeRhsBdryNitscheNavierNormal(self, b, colors, mucell, vn):
        bv, bp = b
        ncomp, dim  = self.ncomp, self.mesh.dimension
        faces = self.mesh.bdryFaces(colors)
        cells = self.mesh.cellsOfFaces[faces,0]
        normalsS = self.mesh.normals[faces][:,:ncomp]
        dS = np.linalg.norm(normalsS, axis=1)
        # normals = normalsS/dS[:,np.newaxis]
        # foc = self.mesh.facesOfCells[cells]
        np.add.at(bp, cells, -dS*vn[faces])
        self.femv.computeRhsNitscheDiffusionNormal(bv, mucell, colors, vn, ncomp)
    def computeRhsBdryNitscheNavierTangent(self, b, colors, mucell, gt):
        bv, bp = b
        ncomp, dim  = self.ncomp, self.mesh.dimension
        self.femv.massDotBoundary(bv, gt.ravel(), colors=colors, ncomp=ncomp, coeff=1)
        self.femv.massDotBoundaryNormal(bv, -gt.ravel(), colors=colors, ncomp=ncomp, coeff=1)
    def computeRhsBdryNitschePressureNormal(self, b, colors, mucell, p):
        bv, bp = b
        self.femv.massDotBoundaryNormal(bv, -p, colors=colors, ncomp=self.ncomp, coeff=1)
    def computeRhsBdryNitschePressureTangent(self, b, colors, mucell, v):
        bv, bp = b
        ncomp, dim  = self.ncomp, self.mesh.dimension
        self.femv.computeRhsNitscheDiffusion(bv, mucell, colors, v, ncomp)
        self.femv.computeRhsNitscheDiffusionNormal(bv, mucell, colors, -v.ravel(), ncomp)
    def computeFormBdryNitscheDirichlet(self, dv, dp, v, p, colorsdir, mu):
        ncomp, dim  = self.femv.ncomp, self.mesh.dimension
        self.femv.computeFormNitscheDiffusion(dv, v, mu, colorsdir, ncomp)
        faces = self.mesh.bdryFaces(colorsdir)
        cells = self.mesh.cellsOfFaces[faces, 0]
        normalsS = self.mesh.normals[faces][:, :self.ncomp]
        for icomp in range(ncomp):
            r = np.einsum('f,f->f', p[cells], normalsS[:,icomp])
            np.add.at(dv[icomp::ncomp], faces, r)
            r = np.einsum('f,f->f', normalsS[:,icomp], v[icomp::ncomp][faces])
            np.add.at(dp, cells, -r)
    def computeFormBdryNitscheNavier(self, dv, dp, v, p, colors, mu):
        if not len(colors): return
        raise NotImplementedError()
    def computeMatrixBdryNitscheDirichlet(self, A, B, colors, mucell):
        nfaces, ncells, ncomp, dim  = self.mesh.nfaces, self.mesh.ncells, self.femv.ncomp, self.mesh.dimension
        A += self.femv.computeMatrixNitscheDiffusion(mucell, colors, ncomp)
        #grad-div
        faces = self.mesh.bdryFaces(colors)
        cells = self.mesh.cellsOfFaces[faces, 0]
        normalsS = self.mesh.normals[faces][:, :self.ncomp]
        indfaces = np.repeat(ncomp * faces, ncomp)
        for icomp in range(ncomp): indfaces[icomp::ncomp] += icomp
        cols = indfaces.ravel()
        rows = cells.repeat(ncomp).ravel()
        mat = normalsS.ravel()
        B -= sparse.coo_matrix((mat, (rows, cols)), shape=(ncells, ncomp*nfaces))
        return A,B
    def computeMatrixBdryNitscheNavier(self, A, B, colors, mucell, lambdaR):
        nfaces, ncells, ncomp, dim  = self.mesh.nfaces, self.mesh.ncells, self.femv.ncomp, self.mesh.dimension
        faces = self.mesh.bdryFaces(colors)
        cells = self.mesh.cellsOfFaces[faces, 0]
        normalsS = self.mesh.normals[faces][:, :dim]
        #grad-div
        indfaces = np.repeat(ncomp * faces, ncomp)
        for icomp in range(ncomp): indfaces[icomp::ncomp] += icomp
        cols = indfaces.ravel()
        rows = cells.repeat(ncomp).ravel()
        B -= sparse.coo_matrix((normalsS.ravel(), (rows, cols)), shape=(ncells, ncomp*nfaces))
        #vitesses
        A += self.femv.computeMatrixNitscheDiffusionNormal(mucell, colors, ncomp)
        A += self.femv.computeMassMatrixBoundary(colors, ncomp, coeff=lambdaR)-self.femv.computeMassMatrixBoundaryNormal(colors, ncomp, coeff=lambdaR)
        return A,B
    def computeMatrixBdryNitschePressure(self, A, B, colors, mucell):
        #vitesses
        A += self.femv.computeMatrixNitscheDiffusion(mucell, colors, self.ncomp)
        A -= self.femv.computeMatrixNitscheDiffusionNormal(mucell, colors, self.ncomp)
        return A,B
    def vectorBoundaryStrong(self, b, bdryfctv, bdrydata, method):
        bv, bp = b
        bv = self.femv.vectorBoundaryStrong(bv, bdryfctv, bdrydata, method)
        facesdirall, facesinner, colorsdir, facesdirflux = bdrydata.facesdirall, bdrydata.facesinner, bdrydata.colorsdir, bdrydata.facesdirflux
        nfaces, ncells, ncomp  = self.mesh.nfaces, self.mesh.ncells, self.femv.ncomp
        bdrydata.bsaved = {}
        for key, faces in facesdirflux.items():
            indfaces = np.repeat(ncomp * faces, ncomp)
            for icomp in range(ncomp): indfaces[icomp::ncomp] += icomp
            bdrydata.bsaved[key] = bv[indfaces]
        inddir = np.repeat(ncomp * facesdirall, ncomp)
        for icomp in range(ncomp): inddir[icomp::ncomp] += icomp
        #suppose strong-trad
        bp -= bdrydata.B_inner_dir * bv[inddir]
        return (bv,bp)
    def matrixBoundaryStrong(self, A, B, bdrydata, method):
        A = self.femv.matrixBoundaryStrong(A, bdrydata, method)
        facesdirall, facesinner, colorsdir, facesdirflux = bdrydata.facesdirall, bdrydata.facesinner, bdrydata.colorsdir, bdrydata.facesdirflux
        nfaces, ncells, ncomp  = self.mesh.nfaces, self.mesh.ncells, self.femv.ncomp
        bdrydata.Bsaved = {}
        for key, faces in facesdirflux.items():
            nb = faces.shape[0]
            helpB = sparse.dok_matrix((ncomp*nfaces, ncomp*nb))
            for icomp in range(ncomp):
                for i in range(nb): helpB[icomp + ncomp*faces[i], icomp + ncomp*i] = 1
            bdrydata.Bsaved[key] = B.dot(helpB)
        inddir = np.repeat(ncomp * facesdirall, ncomp)
        for icomp in range(ncomp): inddir[icomp::ncomp] += icomp
        bdrydata.B_inner_dir = B[:,:][:,inddir]
        help = np.ones((ncomp * nfaces))
        help[inddir] = 0
        help = sparse.dia_matrix((help, 0), shape=(ncomp * nfaces, ncomp * nfaces))
        B = B.dot(help)
        return A,B
    def computeBdryNormalFluxStrong(self, v, p, colors):
        nfaces, ncells, ncomp, bdrydata  = self.mesh.nfaces, self.mesh.ncells, self.ncomp, self.bdrydata
        flux, omega = np.zeros(shape=(ncomp,len(colors))), np.zeros(len(colors))
        for i,color in enumerate(colors):
            faces = self.mesh.bdrylabels[color]
            normalsS = self.mesh.normals[faces]
            dS = np.linalg.norm(normalsS, axis=1)
            omega[i] = np.sum(dS)
            As = bdrydata.Asaved[color]
            Bs = bdrydata.Bsaved[color]
            res = bdrydata.bsaved[color] - As * v + Bs.T * p
            for icomp in range(ncomp):
                flux[icomp, i] = np.sum(res[icomp::ncomp])
            # print(f"{flux=}")
            #TODO flux Stokes Dirichlet strong wrong
        return flux

#=================================================================#
if __name__ == '__main__':
    raise NotImplementedError("Pas encore de test")
