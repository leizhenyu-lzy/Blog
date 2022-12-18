import numpy as np


def mySVD(originMat):
    r"""
    FunctionName    :   
    FunctionDescribe:   Singular Value Decomposition(``A=U@Σ@V^T``)，将原始矩阵分解为：正交阵×对角阵(广义)×正交阵
    InputParameter  :   ①
    OutputParameter :   ①orthogonal
                        ②diagonal
                        ③orthogonal
    Specification   :   OpenCV's API:
                        u,s,vh = np.linalg.svd(matrix, ...)
                        ``u @ np.diag(s) @ vh = (u * s) @ vh``
    """
    # TODO
    pass


if __name__ == "__main__":
    A = np.random.randint(1,10,(8,4))
    print(A)
    U,S,V = np.linalg.svd(A,full_matrices=True)
    print(U.shape,S.shape,V.shape)
    print(U,"\n",S,"\n",V)
    print(np.diag(S))

    mySVD()
    pass
