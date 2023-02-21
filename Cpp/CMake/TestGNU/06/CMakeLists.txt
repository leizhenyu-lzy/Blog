cmake_minimum_required(VERSION 3.22)
project(hellosub LANGUAGES CXX)

add_subdirectory(lib)

add_executable(main.out main.cpp)
target_link_libraries(main.out PUBLIC hellolibSO)
