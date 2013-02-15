cmake_minimum_required(VERSION 2.8)

project(winrun-server)

#add_definitions(-DUNICODE -D_UNICODE)

find_package(PythonLibs REQUIRED)

include_directories(${PYTHON_INCLUDE_DIRS})

add_executable(winrun-server
	main
	winrun-server.rc
)
target_link_libraries(winrun-server
	${PYTHON_LIBRARIES}
)
