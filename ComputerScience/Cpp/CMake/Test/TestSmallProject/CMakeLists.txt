cmake_minimum_required(VERSION 3.0)

project(SWAP)

include_directories(include)

add_library(mySwap SHARED src/swap.cpp)

add_executable(main main.cpp)

target_link_libraries(main mySwap)