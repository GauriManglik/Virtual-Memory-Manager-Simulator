#include "MemoryManager.h"
#include "ProcessManager.h"
#include <iostream>

int main() {
    int numFrames;
    std::cout << "Enter total number of physical frames: " << std::flush;

    std::cin >> numFrames;

    MemoryManager mm(numFrames);
    ProcessManager pm(mm);

    int choice;
    do {
        std::cout << "\n1. Create Process\n2. Access Page\n3. Delete Process\n4. Show Page Table\n5. Show Frame Table\n0. Exit\nChoice: ";
        std::cin >> choice;

        if (choice == 1) {
            int pages;
            std::cout << "Enter number of pages for new process: ";
            std::cin >> pages;
            pm.createProcess(pages);
        } else if (choice == 2) {
            int pid, page;
            std::cout << "Enter PID and Page Number to access: ";
            std::cin >> pid >> page;
            pm.accessPage(pid, page);
        } else if (choice == 3) {
            int pid;
            std::cout << "Enter PID to delete: ";
            std::cin >> pid;
            pm.deleteProcess(pid);
        } else if (choice == 4) {
            int pid;
            std::cout << "Enter PID to show page table: ";
            std::cin >> pid;
            pm.printPageTable(pid);
        } else if (choice == 5) {
            mm.printFrameTable();
        }

    } while (choice != 0);

    return 0;
}
