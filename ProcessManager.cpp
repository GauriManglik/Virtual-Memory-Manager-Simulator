#include "ProcessManager.h"
#include <iostream>

ProcessManager::ProcessManager(MemoryManager &mm) : memoryManager(mm), nextPid(0) {}

int ProcessManager::createProcess(int numPages) {
    std::vector<PageTableEntry> table(numPages, {-1, false});
    int pid = nextPid++;
    pageTables[pid] = table;
    std::cout << "Created process with PID: " << pid << " and " << numPages << " pages.\n";
    return pid;
}

void ProcessManager::deleteProcess(int pid) {
    if (pageTables.find(pid) != pageTables.end()) {
        pageTables.erase(pid);
        memoryManager.deallocateFrames(pid);
        std::cout << "Deleted process PID: " << pid << "\n";
    } else {
        std::cout << "Process not found.\n";
    }
}

void ProcessManager::accessPage(int pid, int pageNum) {
    if (pageTables.find(pid) == pageTables.end()) {
        std::cout << "Process not found.\n";
        return;
    }
    auto &table = pageTables[pid];
    if (pageNum < 0 || pageNum >= static_cast<int>(table.size())) {
        std::cout << "Invalid page number.\n";
        return;
    }

    PageTableEntry &entry = table[pageNum];
    if (!entry.valid) {
        std::cout << "Page fault on PID " << pid << ", Page " << pageNum << ".\n";
        int frame = memoryManager.allocateFrame(pid);
        if (frame != -1) {
            entry.frameNumber = frame;
            entry.valid = true;
        }
    } else {
        std::cout << "Page already in memory at frame " << entry.frameNumber << ".\n";
    }
}

void ProcessManager::printPageTable(int pid) const {
    if (pageTables.find(pid) == pageTables.end()) {
        std::cout << "Process not found.\n";
        return;
    }
    const auto &table = pageTables.at(pid);
    std::cout << "\n[Page Table for PID " << pid << "]\n";
    for (size_t i = 0; i < table.size(); ++i) {
        const auto &entry = table[i];
        std::cout << "Page " << i << ": ";
        if (entry.valid)
            std::cout << "Frame " << entry.frameNumber << "\n";
        else
            std::cout << "Not Loaded\n";
    }
}
