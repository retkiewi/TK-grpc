# People server

People server is a component that detects people on images.
Sending data to this server is done by using AMQP.

# Installation

Build steps:

    $ mkdir build && cd build
    $ conan install ..
    $ cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
    $ cmake --build .

To start server run executable named `peopleServer`. Server will start on port 50060 by default.

Starting server on port 50012
```
peopleServer --port 50012
```
