# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.20

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
CMAKE_COMMAND = /snap/cmake/876/bin/cmake

# The command to remove a file.
RM = /snap/cmake/876/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/kiui/lab.git/resources/radiotap-library

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/kiui/lab.git/resources/build

# Utility rule file for radiotap_check.

# Include any custom commands dependencies for this target.
include CMakeFiles/radiotap_check.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/radiotap_check.dir/progress.make

CMakeFiles/radiotap_check: /home/kiui/lab.git/resources/radiotap-library/check/*
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/kiui/lab.git/resources/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Check examples"
	cd /home/kiui/lab.git/resources/radiotap-library/check && /home/kiui/lab.git/resources/radiotap-library/check/check.sh /home/kiui/lab.git/resources/build

radiotap_check: CMakeFiles/radiotap_check
radiotap_check: CMakeFiles/radiotap_check.dir/build.make
.PHONY : radiotap_check

# Rule to build all files generated by this target.
CMakeFiles/radiotap_check.dir/build: radiotap_check
.PHONY : CMakeFiles/radiotap_check.dir/build

CMakeFiles/radiotap_check.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/radiotap_check.dir/cmake_clean.cmake
.PHONY : CMakeFiles/radiotap_check.dir/clean

CMakeFiles/radiotap_check.dir/depend:
	cd /home/kiui/lab.git/resources/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/kiui/lab.git/resources/radiotap-library /home/kiui/lab.git/resources/radiotap-library /home/kiui/lab.git/resources/build /home/kiui/lab.git/resources/build /home/kiui/lab.git/resources/build/CMakeFiles/radiotap_check.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/radiotap_check.dir/depend
