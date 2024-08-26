# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Debug")
  file(REMOVE_RECURSE
  "CMakeFiles\\testing_autogen.dir\\AutogenUsed.txt"
  "CMakeFiles\\testing_autogen.dir\\ParseCache.txt"
  "testing_autogen"
  )
endif()
