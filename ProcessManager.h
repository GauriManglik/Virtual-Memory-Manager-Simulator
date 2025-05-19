#ifndef PROCESS_MANAGER_H
#define PROCESS_MANAGER_H

#include <vector>
#include <unordered_map>
#include <iostream>
#include "MemoryManager.h"

struct PageTableEntry {
    int frameNumber;
    bool valid;
};

class ProcessManager {
private:
    std::unordered_map<int, std::vector<PageTableEntry>> pageTables;
    int nextPid;
    MemoryManager& memoryManager;

public:
    ProcessManager(MemoryManager& mm);
    int createProcess(int numPages);
    void deleteProcess(int pid);
    void accessPage(int pid, int pageNum);
    void printPageTable(int pid) const;
};

#endif

