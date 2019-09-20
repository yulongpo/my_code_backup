# cmake_minimum_required(VERSION 3.0 FATAL_ERROR) project(custom_ops)

# find_package(Torch REQUIRED)

# add_executable(example-app example-app.cpp)
# target_link_libraries(example-app ${TORCH_LIBRARIES})
# set_property(TARGET example-app PROPERTY CXX_STANDARD 11)

cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(CarrierDetectDLL)

find_package(Torch REQUIRED)
# find_package(OpenCV REQUIRED)

if(NOT Torch_FOUND)
    message(FATAL_ERROR "Pytorch Not Found!")
endif(NOT Torch_FOUND)

message(STATUS "Pytorch status:")
message(STATUS "    libraries: ${TORCH_LIBRARIES}")

# message(STATUS "OpenCV library status:")
# message(STATUS "    version: ${OpenCV_VERSION}")
# message(STATUS "    libraries: ${OpenCV_LIBS}")
# message(STATUS "    include path: ${OpenCV_INCLUDE_DIRS}")


# add_executable(demo example.cpp)
include_directories(./include)
add_definitions(-D_CRT_SECURE_NO_WARNINGS)

SET(LIBWAVE_SRC ./include/CarrierDetect.h ./src/CarrierDetect.cpp ./include/waveBandDetect.h ./src/waveBandDetect.cpp ./include/myLog.hpp)
ADD_LIBRARY(CarrierDetectDLL SHARED ${LIBWAVE_SRC})

target_link_libraries(CarrierDetectDLL ${TORCH_LIBRARIES})

# add_executable(API_test ./API_test/api_test.cpp ./include/CarrierDetect.h ./src/waveCapture.cpp ./include/waveCapture.h)  
# target_link_libraries(API_test CarrierDetectDLL)  

set_property(TARGET CarrierDetectDLL PROPERTY CXX_STANDARD 11)

