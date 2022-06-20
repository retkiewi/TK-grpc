cmake_minimum_required(VERSION 3.21.0)
project(peopleServer)

set(CMAKE_CXX_STANDARD 17)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/bin)


find_package(OpenCV REQUIRED)
find_package(gRPC REQUIRED)
find_package(Protobuf REQUIRED)
find_package(argparse REQUIRED)

find_program(_PROTOBUF_PROTOC protoc)
find_program(_GRPC_CPP_PLUGIN_EXECUTABLE grpc_cpp_plugin)

set(PEOPLE_PROTO core-people.proto)

add_custom_command(
    OUTPUT ${CMAKE_SOURCE_DIR}/src/core-people.pb.cc
           ${CMAKE_SOURCE_DIR}/src/core-people.pb.h
           ${CMAKE_SOURCE_DIR}/src/core-people.grpc.pb.cc
           ${CMAKE_SOURCE_DIR}/src/core-people.grpc.pb.h
    COMMAND ${_PROTOBUF_PROTOC}
    ARGS --grpc_out src
         --cpp_out src
         -I ../Client/protos
         --plugin=protoc-gen-grpc=${_GRPC_CPP_PLUGIN_EXECUTABLE}
         ${PEOPLE_PROTO}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    DEPENDS ../Client/protos/${PEOPLE_PROTO})

add_library(people_grpc_proto
    ${CMAKE_SOURCE_DIR}/src/core-people.pb.cc
    ${CMAKE_SOURCE_DIR}/src/core-people.grpc.pb.cc
)
target_link_libraries(people_grpc_proto
    gRPC::grpc++
    gRPC::grpc++_reflection
    protobuf::libprotobuf
)

add_library(people_lib
    src/PeopleDetector.cpp
    src/processRequest.cpp
)
target_link_libraries(people_lib
    ${OpenCV_LIBRARIES}
    gRPC::grpc++
)

add_executable(peopleServer src/peopleServer.cpp)
target_link_libraries(peopleServer
    ${OpenCV_LIBRARIES}
    grpc::grpc
    argparse::argparse
    people_grpc_proto
    people_lib
)

file(COPY ${CMAKE_SOURCE_DIR}/src/cascades DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
