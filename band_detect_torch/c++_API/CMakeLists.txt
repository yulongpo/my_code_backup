# cmake_minimum_required(VERSION 3.0 FATAL_ERROR) project(custom_ops)

# find_package(Torch REQUIRED)

# add_executable(example-app example-app.cpp)
# target_link_libraries(example-app ${TORCH_LIBRARIES})
# set_property(TARGET example-app PROPERTY CXX_STANDARD 11)

cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(wave_band_api)

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

SET(LIBWAVE_SRC CarrierDetect.h CarrierDetect.cpp waveBandDetect.h waveBandDetect.cpp)
ADD_LIBRARY(wave_band_api SHARED ${LIBWAVE_SRC})

target_link_libraries(wave_band_api ${TORCH_LIBRARIES})
set_property(TARGET wave_band_api PROPERTY CXX_STANDARD 11)