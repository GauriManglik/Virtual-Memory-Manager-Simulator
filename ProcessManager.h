#pragma once
#include <unordered_map>
#include <vector>
#include <iostream>

struct PageTableEntry {
    int frameNumber;
    bool valid;
};

class MemoryManager;

class ProcessManager {
    MemoryManager& memoryManager;
    int nextPid;
    std::unordered_map<int, std::vector<PageTableEntry>> pageTables;

public:
    ProcessManager(MemoryManager &mm);

    int createProcess(int numPages);
    void deleteProcess(int pid);

    void accessPage(int pid, int pageNum);

    void printPageTable(int pid) const;

    void invalidatePage(int pid, int pageNum);  // Called by MemoryManager on eviction
};
