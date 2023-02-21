cmake_minimum_required(VERSION 3.12)
project(hellocmake LANGUAGES CXX)

add_library(helloA STATIC hello.cpp)  # 静态库 .a
add_library(helloSO SHARED hello.cpp)  # 动态库 .so

add_executable(main.out main.cpp)
target_link_libraries(main.out PUBLIC helloA)  # 用 .so 也行


