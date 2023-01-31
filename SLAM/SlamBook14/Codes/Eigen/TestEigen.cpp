#include <iostream>
#include <ctime>
#include <complex.h>

#include <eigen3/Eigen/Core>
#include <eigen3/Eigen/Dense>

using namespace std;

using Eigen::Matrix;
using Eigen::MatrixXd;
using Eigen::MatrixXf;



int main()
{
    // // ------------------------------------------------
    // // Matrix Class
    // Matrix<float,3,3>Test1 = Matrix<float,3,3>::Random();
    // cout<<Test1<<endl<<endl;
    
    // MatrixXd Test2(2,2);
    // Test2(1,1)=999;  // Coefficient accessors  // 注意使用括号
    // Test2(0,1)=1;  // All Eigen matrices default to column-major storage order（存储和索引不同）
    // cout<<Test2<<endl<<endl;

    // Eigen::RowVectorXd Test3(3);
    // cout<<Test3<<endl;

    // Eigen::RowVector2d Test4(987,666);
    // cout<<Test4<<endl<<endl;

    // Matrix<double,2,2> Test5;
    // Test5<<1.1, 2.2, 3.3, 4.4;  // Comma-initialization  // comma-initializer syntax
    // cout<<Test5<<endl<<endl;

    // MatrixXd Test6(4,2);  // Resizing：似乎只用MatrixX这种才能，Matrix<>这种无法resize
    // // Trying to change a fixed size to an actually different value will trigger an assertion failure
    // // 例如Matrix<double,2,2>
    // Test6.resize(2,4);
    // cout<<"Rows:"<<Test5.rows()<<"\nCols"<<Test5.cols()<<"\nSize:"<<Test5.size()<<endl;
    // // size of a matrix can be retrieved by rows(), cols() and size()
    // cout<<Test6<<endl<<endl;

    // MatrixXf Test7(2,2);
    // std::cout << "Test7 is of size " << Test7.rows() << "x" << Test7.cols() << std::endl;
    // MatrixXf Test8(3,3);
    // Test7 = Test8;  // Assignment is the action of copying a matrix into another, using operator=
    // // Eigen resizes the matrix on the left-hand side automatically so that it matches the size of the matrix on the right-hand size
    // // if the left-hand side is of fixed size, resizing it is not allowed
    // std::cout << "Test7 is now of size " << Test7.rows() << "x" << Test7.cols() << std::endl;
    // cout<<endl;

    // // ------------------------------------------------
    // // Matrix and Arithmetics
    // // Addition and subtraction & Scalar multiplication and division
    // Eigen::Matrix2cd cplx1 = Eigen::Matrix2cd::Random();  // 复数矩阵
    // // 复数矩阵赋值方法
    // cplx1.real()<<1,2,3,4;
    // cplx1.imag()<<4,3,2,1;
    // cout<<cplx1<<endl;
    // Eigen::Matrix2cd cplx2 = cplx1*-2.0;
    // cout<<cplx1+cplx2<<endl<<endl;

    // // Transposition and conjugation(共轭)
    // Eigen::Matrix2cd cplx_transpose = cplx1.transpose();
    // Eigen::Matrix2cd cplx_conjugate = cplx1.conjugate();
    // Eigen::Matrix2cd cplx_adjoint = cplx1.adjoint();
    // cout<<cplx_transpose<<endl<<cplx_conjugate<<endl<<cplx_adjoint<<endl<<endl;

    // // Matrix-matrix and matrix-vector multiplication
    // Matrix<int,2,2> TestMultiMat;
    // TestMultiMat<<1,2,3,4;
    // Matrix<int,2,1> TestMultiVec;
    // TestMultiVec<<1,2;
    // cout<<TestMultiMat<<endl<<TestMultiVec<<endl;
    // cout<<TestMultiMat*TestMultiVec<<endl;
    // cout<<TestMultiVec.transpose()*TestMultiMat<<endl;


    // // Dot product and cross product
    // Eigen::Vector3d v(1,2,3);
    // Eigen::Vector3d w(0,1,2);
    // std::cout << "Dot product: " << v.dot(w) << std::endl;
    // double dp = v.adjoint()*w; // automatic conversion of the inner product to a scalar
    // std::cout << "Dot product via a matrix product: " << dp << std::endl;
    // std::cout << "Cross product:\n" << v.cross(w) << std::endl;

    // // Basic arithmetic reduction operations
    // Eigen::Matrix2d Reduction1;
    // Reduction1 << 1, 2,
    //             3, 4;
    // cout << "Here is mat.sum():       " << Reduction1.sum()       << endl;
    // cout << "Here is mat.prod():      " << Reduction1.prod()      << endl;
    // cout << "Here is mat.mean():      " << Reduction1.mean()      << endl;
    // cout << "Here is mat.minCoeff():  " << Reduction1.minCoeff()  << endl;
    // cout << "Here is mat.maxCoeff():  " << Reduction1.maxCoeff()  << endl;
    // cout << "Here is mat.trace():     " << Reduction1.trace()     << endl;
    // // 得到最小值的位置（将ij传入）
    // Eigen::Matrix3f Reduction2 = Eigen::Matrix3f::Random();
    // // std::ptrdiff_t i, j;
    // int i,j;
    // float minCoeff = Reduction2.minCoeff(&i,&j);
    // cout << "Here is the matrix m:\n" << Reduction2 << endl;
    // cout << "Its minimum coefficient (" << minCoeff 
    //     << ") is at position (" << i << "," << j << ")\n\n";

    return 0;
}

// g++ TestEigen.cpp -o TestEigen
// ./TestEigen