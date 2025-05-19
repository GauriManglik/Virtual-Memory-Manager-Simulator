#include "MemoryManager.h"

MemoryManager::MemoryManager(int numFrames) : totalFrames(numFrames) {
    frameTable.resize(totalFrames, -1);
    for (int i = 0; i < totalFrames; ++i)
        freeFrames.push(i);
}

int MemoryManager::allocateFrame(int pid) {
    if (freeFrames.empty()) {
        std::cout << "No free frames available.\n";
        return -1;
    }
    int frame = freeFrames.front();
    freeFrames.pop();
    frameTable[frame] = pid;
    return frame;
}

void MemoryManager::deallocateFrames(int pid) {
    for (int i = 0; i < totalFrames; ++i) {
        if (frameTable[i] == pid) {
            frameTable[i] = -1;
            freeFrames.push(i);
        }
    }
}

void MemoryManager::printFrameTable() const {
    std::cout << "\n[Frame Table]\n";
    for (int i = 0; i < totalFrames; ++i) {
        std::cout << "Frame " << i << ": ";
        if (frameTable[i] == -1)
            std::cout << "Free\n";
        else
            std::cout << "PID " << frameTable[i] << "\n";
    }
}
