# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.25

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/lzy/Projects/Blog/ComputerScience/Cpp/CMake/Test/SoldierGun

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/lzy/Projects/Blog/ComputerScience/Cpp/CMake/Test/SoldierGun/build

# Include any dependencies generated for this target.
include CMakeFiles/MyGun.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/MyGun.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/MyGun.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/MyGun.dir/flags.make

CMakeFiles/MyGun.dir/src/gun.cpp.o: CMakeFiles/MyGun.dir/flags.make
CMakeFiles/MyGun.dir/src/gun.cpp.o: /home/lzy/Projects/Blog/ComputerScience/Cpp/CMake/Test/SoldierGun/src/gun.cpp
CMakeFiles/MyGun.dir/src/gun.cpp.o: CMakeFiles/MyGun.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/lzy/Projects/Blog/ComputerScience/Cpp/CMake/Test/SoldierGun/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/MyGun.dir/src/gun.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/MyGun.dir/src/gun.cpp.o -MF CMakeFiles/MyGun.dir/src/gun.cpp.o.d -o CMakeFiles/MyGun.dir/src/gun.cpp.o -c /home/lzy/Projects/Blog/ComputerScience/Cpp/CMake/Test/SoldierGun/src/gun.cpp

CMakeFiles/MyGun.dir/src/gun.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/MyGun.dir/src/gun.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/lzy/Projects/Blog/ComputerScience/Cpp/CMake/Test/SoldierGun/src/gun.cpp > CMakeFiles/MyGun.dir/src/gun.cpp.i

CMakeFiles/MyGun.dir/src/gun.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/MyGun.dir/src/gun.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/lzy/Projects/Blog/ComputerScience/Cpp/CMake/Test/SoldierGun/src/gun.cpp -o CMakeFiles/MyGun.dir/src/gun.cpp.s

# Object files for target MyGun
MyGun_OBJECTS = \
"CMakeFiles/MyGun.dir/src/gun.cpp.o"

# External object files for target MyGun
MyGun_EXTERNAL_OBJECTS =

libMyGun.so: CMakeFiles/MyGun.dir/src/gun.cpp.o
libMyGun.so: CMakeFiles/MyGun.dir/build.make
libMyGun.so: CMakeFiles/MyGun.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/lzy/Projects/Blog/ComputerScience/Cpp/CMake/Test/SoldierGun/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared library libMyGun.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/MyGun.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/MyGun.dir/build: libMyGun.so
.PHONY : CMakeFiles/MyGun.dir/build

CMakeFiles/MyGun.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/MyGun.dir/cmake_clean.cmake
.PHONY : CMakeFiles/MyGun.dir/clean

CMakeFiles/MyGun.dir/depend:
	cd /home/lzy/Projects/Blog/ComputerScience/Cpp/CMake/Test/SoldierGun/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/lzy/Projects/Blog/ComputerScience/Cpp/CMake/Test/SoldierGun /home/lzy/Projects/Blog/ComputerScience/Cpp/CMake/Test/SoldierGun /home/lzy/Projects/Blog/ComputerScience/Cpp/CMake/Test/SoldierGun/build /home/lzy/Projects/Blog/ComputerScience/Cpp/CMake/Test/SoldierGun/build /home/lzy/Projects/Blog/ComputerScience/Cpp/CMake/Test/SoldierGun/build/CMakeFiles/MyGun.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/MyGun.dir/depend

