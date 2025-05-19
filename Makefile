# Makefile

# Compiler and flags
CXX = g++
CXXFLAGS = -std=c++17 -Wall

# Executable name
TARGET = memory_simulator

# Source files
SRCS = main.cpp MemoryManager.cpp ProcessManager.cpp

# Header files
HEADERS = MemoryManager.h ProcessManager.h

# Object files (optional in this case)
OBJS = $(SRCS:.cpp=.o)

all: $(TARGET)

$(TARGET): $(SRCS) $(HEADERS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRCS)

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET) *.o
