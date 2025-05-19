#include "MemoryManager.h"
#include "ProcessManager.h"

MemoryManager::MemoryManager(int numFrames, ReplacementPolicy rp)
    : totalFrames(numFrames), policy(rp)
{
    frameTable.resize(totalFrames, -1);
    frameToPage.resize(totalFrames, {-1, -1});
    for (int i = 0; i < totalFrames; ++i) {
        freeFrames.push(i);
    }
}

void MemoryManager::setProcessManager(ProcessManager* pm) {
    processManager = pm;
}

int MemoryManager::allocateFrame(int pid, int pageNum) {
    currentTime++;

    if (!freeFrames.empty()) {
        int frame = freeFrames.front();
        freeFrames.pop();

        frameTable[frame] = pid;
        frameToPage[frame] = {pid, pageNum};

        // Track for replacement policy
        if (policy == FIFO) {
            fifoQueue.push(frame);
        } 
        if (policy == LRU) {
            lastUsed[frame] = currentTime;
        }
        if (policy == LFU) {
            freq[frame] = 1;
        }

        return frame;
    } else {
        int victim = selectVictimFrame();
        if (victim == -1) {
            std::cout << "No frame available for replacement!\n";
            return -1;
        }

        auto [victimPid, victimPage] = frameToPage[victim];

        // Notify ProcessManager to invalidate victim page
        if (processManager) {
            processManager->invalidatePage(victimPid, victimPage);
        }

        // Replace
        frameTable[victim] = pid;
        frameToPage[victim] = {pid, pageNum};

        // Update replacement policy trackers
        if (policy == FIFO) {
            fifoQueue.pop();
            fifoQueue.push(victim);
        }
        if (policy == LRU) {
            lastUsed[victim] = currentTime;
        }
        if (policy == LFU) {
            freq[victim] = 1;
        }

        std::cout << "Replaced frame " << victim << " held by PID " << victimPid << ", Page " << victimPage << "\n";

        return victim;
    }
}

int MemoryManager::selectVictimFrame() {
    if (policy == FIFO) {
        if (fifoQueue.empty()) return -1;
        return fifoQueue.front();
    } 
    else if (policy == LRU) {
        int lruFrame = -1;
        int minTime = INT_MAX;
        for (int i = 0; i < totalFrames; ++i) {
            if (frameTable[i] != -1 && lastUsed[i] < minTime) {
                minTime = lastUsed[i];
                lruFrame = i;
            }
        }
        return lruFrame;
    } 
    else if (policy == LFU) {
        int lfuFrame = -1;
        int minFreq = INT_MAX;
        for (int i = 0; i < totalFrames; ++i) {
            if (frameTable[i] != -1 && freq[i] < minFreq) {
                minFreq = freq[i];
                lfuFrame = i;
            }
        }
        return lfuFrame;
    }
    return -1;
}

void MemoryManager::deallocateFrames(int pid) {
    for (int i = 0; i < totalFrames; ++i) {
        if (frameTable[i] == pid) {
            frameTable[i] = -1;
            frameToPage[i] = {-1, -1};
            freeFrames.push(i);

            if (policy == FIFO) {
                // Remove from fifoQueue is tricky, we can rebuild fifoQueue here if needed,
                // but for simplicity, we skip strict removal from FIFO queue on deallocation.
            }
            if (policy == LRU) {
                lastUsed.erase(i);
            }
            if (policy == LFU) {
                freq.erase(i);
            }
        }
    }
}

void MemoryManager::updateOnAccess(int frame) {
    currentTime++;
    if (policy == LRU) {
        lastUsed[frame] = currentTime;
    }
    if (policy == LFU) {
        freq[frame]++;
    }
}

void MemoryManager::printFrameTable() const {
    std::cout << "\n[Frame Table]\n";
    for (int i = 0; i < totalFrames; ++i) {
        std::cout << "Frame " << i << ": ";
        if (frameTable[i] == -1)
            std::cout << "Free\n";
        else
            std::cout << "PID " << frameTable[i] << ", Page " << frameToPage[i].second << "\n";
    }
}
