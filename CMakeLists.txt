cmake_minimum_required (VERSION 2.6)

PROJECT(Hackathon)

# Requires OpenCV
FIND_PACKAGE( OpenCV REQUIRED )

SET(SRC
    main_desktop.cpp
    mode.cpp
)

ADD_EXECUTABLE( ${PROJECT_NAME} ${SRC} )
TARGET_LINK_LIBRARIES( ${PROJECT_NAME}  ${OpenCV_LIBS} )
