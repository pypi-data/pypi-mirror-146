# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 18:14:29 2016

@author: becker
"""
import numpy as np
import numpy.linalg as linalg
import scipy.sparse as sparse
from simfempy.meshes.simplexmesh import SimplexMesh
from simfempy.fems import fem


#=================================================================#
class P1general(fem.Fem):
    def setMesh(self, mesh, innersides=False):
        super().setMesh(mesh)
        self.nloc = self.nlocal()
        if innersides: self.mesh.constructInnerFaces()
    def computeStencilCell(self, dofspercell):
        self.cols = np.tile(dofspercell, self.nloc).ravel()
        self.rows = np.repeat(dofspercell, self.nloc).ravel()
    def interpolateCell(self, f):
        if isinstance(f, dict):
            b = np.zeros(self.mesh.ncells)
            for label, fct in f.items():
                if fct is None: continue
                cells = self.mesh.cellsoflabel[label]
                xc, yc, zc = self.mesh.pointsc[cells].T
                b[cells] = fct(xc, yc, zc)
            return b
        else:
            xc, yc, zc = self.mesh.pointsc.T
            return f(xc, yc, zc)
    def computeMatrixDiffusion(self, coeff):
        ndofs = self.nunknowns()
        # matxx = np.einsum('nk,nl->nkl', self.cellgrads[:, :, 0], self.cellgrads[:, :, 0])
        # matyy = np.einsum('nk,nl->nkl', self.cellgrads[:, :, 1], self.cellgrads[:, :, 1])
        # matzz = np.einsum('nk,nl->nkl', self.cellgrads[:, :, 2], self.cellgrads[:, :, 2])
        # mat = ( (matxx+matyy+matzz).T*self.mesh.dV*coeff).T.ravel()
        cellgrads = self.cellgrads[:,:,:self.mesh.dimension]
        mat = np.einsum('n,nil,njl->nij', self.mesh.dV*coeff, cellgrads, cellgrads).ravel()
        return sparse.coo_matrix((mat, (self.rows, self.cols)), shape=(ndofs, ndofs)).tocsr()
    def computeFormDiffusion(self, du, u, coeff):
        doc = self.dofspercell()
        cellgrads = self.cellgrads[:,:,:self.mesh.dimension]
        r = np.einsum('n,nil,njl,nj->ni', self.mesh.dV*coeff, cellgrads, cellgrads, u[doc])
        np.add.at(du, doc, r)
    def computeMatrixLps(self, betart, **kwargs):
        param = kwargs.pop('lpsparam', 0.1)
        dimension, dV, ndofs = self.mesh.dimension, self.mesh.dV, self.nunknowns()
        nloc, dofspercell = self.nlocal(), self.dofspercell()
        ci = self.mesh.cellsOfInteriorFaces
        ci0, ci1 = ci[:,0], ci[:,1]
        normalsS = self.mesh.normals[self.mesh.innerfaces]
        dS = linalg.norm(normalsS, axis=1)
        scale = 0.5*(dV[ci0]+ dV[ci1])
        betan = np.absolute(betart[self.mesh.innerfaces])
        # betan = 0.5*(np.linalg.norm(betaC[ci0],axis=1)+ np.linalg.norm(betaC[ci1],axis=1))
        scale *= param*dS*betan
        cg0 = self.cellgrads[ci0, :, :]
        cg1 = self.cellgrads[ci1, :, :]
        mat00 = np.einsum('nki,nli,n->nkl', cg0, cg0, scale)
        mat01 = np.einsum('nki,nli,n->nkl', cg0, cg1, -scale)
        mat10 = np.einsum('nki,nli,n->nkl', cg1, cg0, -scale)
        mat11 = np.einsum('nki,nli,n->nkl', cg1, cg1, scale)
        rows0 = dofspercell[ci0,:].repeat(nloc)
        cols0 = np.tile(dofspercell[ci0,:],nloc).reshape(-1)
        rows1 = dofspercell[ci1,:].repeat(nloc)
        cols1 = np.tile(dofspercell[ci1,:],nloc).reshape(-1)
        A00 = sparse.coo_matrix((mat00.reshape(-1), (rows0, cols0)), shape=(ndofs, ndofs))
        A01 = sparse.coo_matrix((mat01.reshape(-1), (rows0, cols1)), shape=(ndofs, ndofs))
        A10 = sparse.coo_matrix((mat10.reshape(-1), (rows1, cols0)), shape=(ndofs, ndofs))
        A11 = sparse.coo_matrix((mat11.reshape(-1), (rows1, cols1)), shape=(ndofs, ndofs))
        return A00+A01+A10+A11
    def computeFormLps(self, du, u, betart, **kwargs):
        param = kwargs.pop('lpsparam', 0.1)
        dimension, dV, ndofs = self.mesh.dimension, self.mesh.dV, self.nunknowns()
        nloc, dofspercell = self.nlocal(), self.dofspercell()
        ci = self.mesh.cellsOfInteriorFaces
        ci0, ci1 = ci[:,0], ci[:,1]
        normalsS = self.mesh.normals[self.mesh.innerfaces]
        dS = linalg.norm(normalsS, axis=1)
        scale = 0.5*(dV[ci0]+ dV[ci1])
        betan = np.absolute(betart[self.mesh.innerfaces])
        scale *= param*dS*betan
        cg0 = self.cellgrads[ci0, :, :]
        cg1 = self.cellgrads[ci1, :, :]
        r = np.einsum('nki,nli,n,nl->nk', cg0, cg0, scale, u[dofspercell[ci0,:]]-u[dofspercell[ci1,:]])
        np.add.at(du, dofspercell[ci0,:], r)
        # mat01 = np.einsum('nki,nli,n,nl->nk', cg0, cg1, -scale, u[dofspercell[ci1,:]])
        # np.add.at(du, dofspercell[ci0,:], mat01)
        r = np.einsum('nki,nli,n,nl->nk', cg1, cg0, -scale, u[dofspercell[ci0,:]]-u[dofspercell[ci1,:]])
        np.add.at(du, dofspercell[ci1,:], r)
        # mat11 = np.einsum('nki,nli,n,nl->nk', cg1, cg1, scale, u[dofspercell[ci1,:]])
        # np.add.at(du, dofspercell[ci1,:], mat11)
    def computeFormConvection(self, du, u, data, **kwargs):
        method = self.params_str['convmethod']
        if method[:4] == 'supg':
            self.computeFormTransportSupg(du, u, data, method)
        elif method == 'upwalg':
            self.computeFormTransportUpwindAlg(du, u, data)
        elif method[:3] == 'upw':
            self.computeFormTransportUpwind(du, u, data, method)
        elif method == 'lps':
            self.computeFormTransportLps(du, u, data, **kwargs)
        else:
            raise NotImplementedError(f"{method=}")
    def computeMatrixConvection(self, data, **kwargs):
        method = self.params_str['convmethod']
        if method[:4] == 'supg':
            return self.computeMatrixTransportSupg(data, method)
        elif method == 'upwalg':
            return self.computeMatrixTransportUpwindAlg(data)
        elif method[:3] == 'upw':
            return self.computeMatrixTransportUpwind(data, method)
        elif method == 'lps':
            return self.computeMatrixTransportLps(data, **kwargs)
        else:
            raise NotImplementedError(f"{method=}")

#====================================================================================
    def prepareBoundary(self, colorsdirichlet, colorsflux):
        if self.params_str['dirichletmethod'] == 'nitsche': return None
        return self._prepareBoundary(colorsdirichlet, colorsflux)
    # def computeBdryMassMatrix(self, colorsrobin, param, lumped=False):
    #     return self.computeBdryMassMatrix(colorsrobin, param, lumped)

# ====================================================================================

    #------------------------------
    def test(self):
        import scipy.sparse.linalg as splinalg
        colors = self.mesh.bdrylabels.keys()
        bdrydata = self.prepareBoundary(colorsdir=colors)
        A = self.computeMatrixDiffusion(coeff=1)
        A = self.matrixBoundaryStrong(A, bdrydata=bdrydata)
        b = np.zeros(self.nunknowns())
        rhs = np.vectorize(lambda x,y,z: 1)
        b = self.computeRhsCell(b, rhs)
        self.vectorBoundaryStrongZero(b, bdrydata)
        return self.tonode(splinalg.spsolve(A, b))

# ------------------------------------- #

if __name__ == '__main__':
    trimesh = SimplexMesh(geomname="backwardfacingstep", hmean=0.3)
