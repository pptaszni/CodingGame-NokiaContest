cmake_minimum_required( VERSION 2.6.2 )
project(NokiaCodingGameContest)

include_directories(inc)

add_subdirectory(lib)

include_directories(lib/googlemock/include lib/googletest/include tests/mocks)

add_subdirectory(src)

add_subdirectory(tests)
