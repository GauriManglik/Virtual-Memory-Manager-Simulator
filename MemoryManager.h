#pragma once
#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>

enum ReplacementPolicy { FIFO, LRU, LFU };

class ProcessManager;  // Forward declaration

class MemoryManager {
    int totalFrames;
    std::vector<int> frameTable;              // PID owning each frame or -1 if free
    std::queue<int> freeFrames;               

    // For replacement policies
    ReplacementPolicy policy;
    std::queue<int> fifoQueue;                 // For FIFO
    std::unordered_map<int, int> lastUsed;    // For LRU: frame -> last used time
    std::unordered_map<int, int> freq;        // For LFU: frame -> frequency count
    int currentTime = 0;                       // Time stamp for LRU

    // Map frame to (PID, pageNum)
    std::vector<std::pair<int, int>> frameToPage;

    ProcessManager* processManager = nullptr;  // Back reference to notify evictions

public:
    MemoryManager(int numFrames, ReplacementPolicy rp);

    void setProcessManager(ProcessManager* pm);

    int allocateFrame(int pid, int pageNum);
    void deallocateFrames(int pid);

    void updateOnAccess(int frame);

    void printFrameTable() const;

private:
    int selectVictimFrame();
};
