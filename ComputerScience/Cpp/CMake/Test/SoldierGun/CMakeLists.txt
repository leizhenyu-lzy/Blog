cmake_minimum_required(VERSION 3.0)

project(SoldierGun)

set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall")  # 追加编译选项

set (CMAKE_BUILD_TYPE Debug)

add_subdirectory(hellolib)

# include_directories(./include)

add_library(MyGun SHARED src/gun.cpp)
target_include_directories(MyGun PRIVATE include)

add_library(MySoldier SHARED src/soldier.cpp)
target_include_directories(MySoldier PRIVATE include)

add_executable(main_cmake main.cpp)
target_include_directories(main_cmake PRIVATE include)

target_link_libraries(main_cmake MyGun MySoldier hellolib)


