#ifndef MEMORY_MANAGER_H
#define MEMORY_MANAGER_H

#include <vector>
#include <queue>
#include <iostream>

class MemoryManager {
private:
    int totalFrames;
    std::vector<int> frameTable;
    std::queue<int> freeFrames;

public:
    MemoryManager(int numFrames);
    int allocateFrame(int pid);
    void deallocateFrames(int pid);
    void printFrameTable() const;
};

#endif
