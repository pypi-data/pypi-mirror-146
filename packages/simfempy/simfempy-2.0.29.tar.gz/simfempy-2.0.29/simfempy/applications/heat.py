import numpy as np
from simfempy import fems
from simfempy.applications.application import Application
from simfempy.tools.analyticalfunction import AnalyticalFunction

# ================================================================= #
class Heat(Application):
    """
    Class for the (stationary) heat equation
    $$
    rhoCp (T_t + beta\cdot\nabla T) -\div(kheat \nabla T) = f         domain
    kheat\nabla\cdot n + alpha T = g  bdry
    $$
    After initialization, the function setMesh(mesh) has to be called
    Then, solve() solves the stationary problem
    Parameters in the constructor:
        fem: only p1 or cr1
        problemdata
        method
        masslumpedbdry, masslumpedvol
    Paramaters used from problemdata:
        rhocp
        kheat
        reaction
        alpha
        they can either be given as global constant, cell-wise constants, or global function
        - global constant is taken from problemdata.paramglobal
        - cell-wise constants are taken from problemdata.paramcells
        - problemdata.paramglobal is taken from problemdata.datafct and are called with arguments (color, xc, yc, zc)
    Possible parameters for computaion of postprocess:
        errors
        bdry_mean: computes mean temperature over boundary parts according to given color
        bdry_nflux: computes mean normal flux over boundary parts according to given color
    """
    def __format__(self, spec):
        if spec=='-':
            repr = super(Heat, self).__format__(spec)
            repr += f"\nfem={self.fem}"
            return repr
        return self.__repr__()
    def __repr__(self):
        repr = super(Heat, self).__repr__()
        repr += f"\nfem={self.fem}"
        return repr
    def __init__(self, **kwargs):
        fem = kwargs.pop('fem','p1')
        if fem == 'p1': self.fem = fems.p1.P1(kwargs)
        elif fem == 'cr1': self.fem = fems.cr1.CR1(kwargs)
        else: raise ValueError("unknown fem '{}'".format(fem))
        self.convection = 'convection' in kwargs['problemdata'].params.fct_glob.keys()
        super().__init__(**kwargs)
    def setMesh(self, mesh):
        super().setMesh(mesh)
        # if mesh is not None: self.mesh = mesh
        self._checkProblemData()
        self.fem.setMesh(self.mesh)
        # colorsdirichlet = self.problemdata.bdrycond.colorsOfType("Dirichlet")
        # colorsflux = self.problemdata.postproc.colorsOfType("bdry_nflux")
        # self.bdrydata = self.fem.prepareBoundary(colorsdirichlet, colorsflux)

        self.bdrydata = self.fem.prepareBoundary(self.problemdata.bdrycond, self.problemdata.postproc)


        self.kheatcell = self.compute_cell_vector_from_params('kheat', self.problemdata.params)
        self.problemdata.params.scal_glob.setdefault('rhocp',1)
        # TODO: non-constant rhocp
        rhocp = self.problemdata.params.scal_glob.setdefault('rhocp', 1)
        if self.convection:
            convectionfct = self.problemdata.params.fct_glob['convection']
            self.convdata = self.fem.prepareAdvection(convectionfct, rhocp)
            colorsinflow = self.findInflowColors()
            colorsdir = self.problemdata.bdrycond.colorsOfType("Dirichlet")
            if not set(colorsinflow).issubset(set(colorsdir)):
                raise ValueError(f"Inflow boundaries need to be subset of Dirichlet boundaries {colorsinflow=} {colorsdir=}")
    def findInflowColors(self):
        colors=[]
        for color in self.mesh.bdrylabels.keys():
            faces = self.mesh.bdrylabels[color]
            if np.any(self.convdata.betart[faces]<-1e-10): colors.append(color)
        return colors
    def _checkProblemData(self):
        if self.verbose: print(f"checking problem data {self.problemdata=}")
        if self.convection:
            convection_given = self.problemdata.params.fct_glob['convection']
            if not isinstance(convection_given, list):
                p = "problemdata.params.fct_glob['convection']"
                raise ValueError(f"need '{p}' as a list of length dim of str or AnalyticalSolution")
            elif isinstance(convection_given[0],str):
                self.problemdata.params.fct_glob['convection'] = [AnalyticalFunction(expr=e) for e in convection_given]
            else:
                if not isinstance(convection_given[0], AnalyticalFunction):
                    raise ValueError(f"convection should be given as 'str' and not '{type(convection_given[0])}'")
            if len(self.problemdata.params.fct_glob['convection']) != self.mesh.dimension:
                raise ValueError(f"{self.mesh.dimension=} {self.problemdata.params.fct_glob['convection']=}")
        bdrycond = self.problemdata.bdrycond
        for color in self.mesh.bdrylabels:
            if not color in bdrycond.type: raise ValueError(f"color={color} not in bdrycond={bdrycond}")
            if bdrycond.type[color] in ["Robin"]:
                if not color in bdrycond.param:
                    raise ValueError(f"Robin condition needs paral 'alpha' color={color} bdrycond={bdrycond}")
    def defineRhsAnalyticalSolution(self, solexact):
        def _fctu(x, y, z):
            kheat = self.problemdata.params.scal_glob['kheat']
            beta = self.problemdata.params.fct_glob['convection']
            rhs = np.zeros(x.shape)
            for i in range(self.mesh.dimension):
                rhs += beta[i](x,y,z) * solexact.d(i, x, y, z)
                rhs -= kheat * solexact.dd(i, i, x, y, z)
            return rhs
        def _fctu2(x, y, z):
            kheat = self.problemdata.params.scal_glob['kheat']
            rhs = np.zeros(x.shape)
            for i in range(self.mesh.dimension):
                rhs -= kheat * solexact.dd(i, i, x, y, z)
            return rhs
        if self.convection: return _fctu
        return _fctu2
    def defineNeumannAnalyticalSolution(self, problemdata, color):
        solexact = problemdata.solexact
        def _fctneumann(x, y, z, nx, ny, nz):
            kheat = self.problemdata.params.scal_glob['kheat']
            rhs = np.zeros(x.shape)
            normals = nx, ny, nz
            for i in range(self.mesh.dimension):
                rhs += kheat * solexact.d(i, x, y, z) * normals[i]
            return rhs
        return _fctneumann
    def defineRobinAnalyticalSolution(self, problemdata, color):
        solexact = problemdata.solexact
        alpha = problemdata.bdrycond.param[color]
        # alpha = 1
        def _fctrobin(x, y, z, nx, ny, nz):
            kheat = self.problemdata.params.scal_glob['kheat']
            rhs = np.zeros(x.shape)
            normals = nx, ny, nz
            # print(f"{alpha=}")
            # rhs += alpha*solexact(x, y, z)
            rhs += solexact(x, y, z)
            for i in range(self.mesh.dimension):
                # rhs += kheat * solexact.d(i, x, y, z) * normals[i]
                rhs += kheat * solexact.d(i, x, y, z) * normals[i]/alpha
            return rhs
        return _fctrobin
    def setParameter(self, paramname, param):
        if paramname == "dirichlet_strong": self.fem.dirichlet_strong = param
        else:
            if not hasattr(self, self.paramname):
                raise NotImplementedError("{} has no paramater '{}'".format(self, self.paramname))
            cmd = "self.{} = {}".format(self.paramname, param)
            eval(cmd)
    def computeForm(self, u, coeffmass=None):
        du2 = self.A@u
        du = np.zeros_like(u)
        bdrycond = self.problemdata.bdrycond
        colorsrobin = bdrycond.colorsOfType("Robin")
        colorsdir = bdrycond.colorsOfType("Dirichlet")
        self.fem.computeFormDiffusion(du, u, self.kheatcell)
        self.fem.formBoundary(du, u, self.bdrydata, self.kheatcell, colorsdir)
        if self.convection:
            self.fem.computeFormConvection(du, u, self.convdata)
        if coeffmass is not None:
            self.fem.massDot(du, u, coeff=coeffmass)
        self.fem.vectorBoundaryStrongEqual(du, u, self.bdrydata)
        if not np.allclose(du,du2):
            # f = (f"\n{du[self.bdrydata.facesdirall]}\n{du2[self.bdrydata.facesdirall]}")
            raise ValueError(f"\n{du=}\n{du2=}")
        return du
    def computeMatrix(self, u=None, coeffmass=None):
        bdrycond = self.problemdata.bdrycond
        colorsrobin = bdrycond.colorsOfType("Robin")
        # colorsneumann = bdrycond.colorsOfType("Neumann")
        colorsdir = bdrycond.colorsOfType("Dirichlet")
        A = self.fem.computeMatrixDiffusion(self.kheatcell)
        A += self.fem.computeMatrixNitscheDiffusion(diffcoff=self.kheatcell, colors=colorsdir)
        A += self.fem.computeBdryMassMatrix(colorsrobin, bdrycond.param, lumped=True)
        # A += self.fem.computeMatrixNeumann(colorsneumann, bdrycond.param)
        if self.convection:
            A += self.fem.computeMatrixConvection(self.convdata)
        if coeffmass is not None:
            A += self.fem.computeMassMatrix(coeff=coeffmass)
        # if hasattr(self, 'bdrydata'):
        if self.bdrydata:
            A = self.fem.matrixBoundaryStrong(A, self.bdrydata)
        return A
    def computeRhs(self, b=None, coeffmass=None, u=None):
        if b is None:
            b = np.zeros(self.fem.nunknowns())
        else:
            if b.shape[0] != self.fem.nunknowns(): raise ValueError(f"{b.shape=} {self.fem.nunknowns()=}")
        bdrycond = self.problemdata.bdrycond
        colorsrobin = bdrycond.colorsOfType("Robin")
        colorsdir = bdrycond.colorsOfType("Dirichlet")
        colorsneu = bdrycond.colorsOfType("Neumann")
        if 'rhs' in self.problemdata.params.fct_glob:
            fp1 = self.fem.interpolate(self.problemdata.params.fct_glob['rhs'])
            self.fem.massDot(b, fp1)
            if hasattr(self, 'convdata'): self.fem.massDotSupg(b, fp1, self.convdata)
        if 'rhscell' in self.problemdata.params.fct_glob:
            fp1 = self.fem.interpolateCell(self.problemdata.params.fct_glob['rhscell'])
            self.fem.massDotCell(b, fp1)
        if 'rhspoint' in self.problemdata.params.fct_glob:
            self.fem.computeRhsPoint(b, self.problemdata.params.fct_glob['rhspoint'])
        # if self.fem.params_str['dirichletmethod'] in ['strong','new'] and not hasattr(self.bdrydata,"A_inner_dir"):
        #     raise ValueError(f"matrix() has to be called before computeRhs() {self.fem.params_str['dirichletmethod']=}")

        # if self.fem.params_str['dirichletmethod']=="new":
        #     self.fem.vectorBoundaryStrong(b, bdrycond, self.bdrydata, self.fem.params_str['dirichletmethod'])
        # if self.fem.params_str['dirichletmethod']=="nitsche":
        #     fp1 = self.fem.interpolateBoundary(colorsdir, bdrycond.fct)
        #     self.fem.computeRhsNitscheDiffusion(b, self.kheatcell, colorsdir, fp1)
        # print(f"{type(bdrycond.fct)=}")
        self.fem.computeRhsNitscheDiffusion(b, self.kheatcell, colorsdir, udir=None, bdrycondfct=bdrycond.fct)
        self.fem.vectorBoundaryStrong(b, bdrycond, self.bdrydata)

        if self.convection:
            fp1 = self.fem.interpolateBoundary(self.mesh.bdrylabels.keys(), bdrycond.fct)
            self.fem.massDotBoundary(b, fp1, coeff=-np.minimum(self.convdata.betart, 0))
        #Fourier-Robin
        fp1 = self.fem.interpolateBoundary(colorsrobin, bdrycond.fct, lumped=True)
        self.fem.massDotBoundary(b, fp1, colors=colorsrobin, lumped=True, coeff=bdrycond.param)
        #Neumann
        fp1 = self.fem.interpolateBoundary(colorsneu, bdrycond.fct)
        self.fem.massDotBoundary(b, fp1, colorsneu)
        if coeffmass is not None:
            assert u is not None
            self.fem.massDot(b, u, coeff=coeffmass)
        if hasattr(self, 'bdrydata'):
            self.fem.vectorBoundaryStrong(b, bdrycond, self.bdrydata)
        return b
    def postProcess(self, u):
        # TODO: virer 'error' et 'postproc'
        data = {'point':{}, 'cell':{}, 'global':{}}
        # point_data, side_data, cell_data, global_data = {}, {}, {}, {}
        data['point']['U'] = self.fem.tonode(u)
        if self.problemdata.solexact:
            data['global']['err_L2c'], ec = self.fem.computeErrorL2Cell(self.problemdata.solexact, u)
            data['global']['err_L2n'], en = self.fem.computeErrorL2(self.problemdata.solexact, u)
            data['global']['err_H1'] = self.fem.computeErrorFluxL2(self.problemdata.solexact, u)
            data['global']['err_Flux'] = self.fem.computeErrorFluxL2(self.problemdata.solexact, u, self.kheatcell)
            data['cell']['err'] = ec
        if self.problemdata.postproc:
            types = ["bdry_mean", "bdry_fct", "bdry_nflux", "pointvalues", "meanvalues", "linemeans"]
            for name, type in self.problemdata.postproc.type.items():
                colors = self.problemdata.postproc.colors(name)
                if type == types[0]:
                    data['global'][name] = self.fem.computeBdryMean(u, colors)
                elif type == types[1]:
                    data['global'][name] = self.fem.computeBdryFct(u, colors)
                elif type == types[2]:
                    if self.fem.params_str['dirichletmethod'] == 'nitsche':
                        udir = self.fem.interpolateBoundary(colors, self.problemdata.bdrycond.fct)
                        data['global'][name] = self.fem.computeBdryNormalFluxNitsche(u, colors, udir, self.kheatcell)
                    else:
                        data['global'][name] = self.fem.computeBdryNormalFlux(u, colors, self.bdrydata, self.problemdata.bdrycond, self.kheatcell)
                elif type == types[3]:
                    data['global'][name] = self.fem.computePointValues(u, colors)
                elif type == types[4]:
                    data['global'][name] = self.fem.computeMeanValues(u, colors)
                elif type == types[5]:
                    data['global'][name] = self.fem.computeLineValues(u, colors)
                else:
                    raise ValueError(f"unknown postprocess type '{type}' for key '{name}'\nknown types={types=}")
        return data
    # def pyamg_solver_args(self, maxiter):
    #     return {'cycle': 'W', 'maxiter': maxiter, 'tol': 1e-12, 'accel': 'bicgstab'}
    def setup_own_gs(**kwargs):
        print(f"{kwargs=}")
    def own_gs(A, b):
        x = np.zeros_like(b)
        return x
    def pyamg_solver_args(self, maxiter):
        if self.convection:
            return {'cycle': 'V', 'maxiter': maxiter, 'tol': 1e-10, 'accel': 'bicgstab'}
        return {'cycle': 'V', 'maxiter': maxiter, 'tol': 1e-10, 'accel': 'cg'}
    def build_pyamg(self, A):
        try:
            import pyamg
        except:
            raise ImportError(f"*** pyamg not found {self.linearsolver=} ***")
        # return pyamg.smoothed_aggregation_solver(A)
        B = np.ones((A.shape[0], 1))
        B = pyamg.solver_configuration(A, verb=False)['B']
        if self.convection:
            symmetry = 'nonsymmetric'
            # smoother = 'gauss_seidel_nr'
            smoother = 'gauss_seidel'
            smoother = 'block_gauss_seidel'
            smoother = 'strength_based_schwarz'
            smoother = 'schwarz'
            # smoother = 'own_gs'
            # smoother = 'gmres'

            # global setup_own_gs
            # def setup_own_gs(lvl, iterations=2, sweep='forward'):
            #     def smoother(A, x, b):
            #         pyamg.relaxation.gauss_seidel(A, x, b, iterations=iterations, sweep=sweep)
            #
            #     return smoother

            # smoother = 'own_gs'
            # smooth = ('energy', {'krylov': 'fgmres'})
            smooth = ('energy', {'krylov': 'bicgstab'})
            # improve_candidates =[ (smoother, {'sweep': 'symmetric', 'iterations': 4}), None]
            improve_candidates = None
        else:
            symmetry = 'hermitian'
            smooth = ('energy', {'krylov': 'cg'})
            smoother = 'gauss_seidel'
            # improve_candidates =[ ('gauss_seidel', {'sweep': 'symmetric', 'iterations': 4}), None]
            improve_candidates = None
        # strength = [('evolution', {'k': 2, 'epsilon': 10.0})]
        strength = [('symmetric', {'theta': 0.05})]
        psmoother = (smoother, {'sweep': 'symmetric', 'iterations': 1})
        # psmoother = (smoother, {'maxiter': 10})
        SA_build_args = {
            'max_levels': 10,
            'max_coarse': 25,
            'coarse_solver': 'pinv2',
            'symmetry': symmetry,
            'smooth': smooth,
            'strength': strength,
            'presmoother': psmoother,
            'presmoother': psmoother,
            'improve_candidates': improve_candidates,
            'diagonal_dominance': False
        }
        # return pyamg.smoothed_aggregation_solver(A, B, **SA_build_args)
        return pyamg.rootnode_solver(A, B, **SA_build_args)


#=================================================================#
if __name__ == '__main__':
    print("Pas de test")
