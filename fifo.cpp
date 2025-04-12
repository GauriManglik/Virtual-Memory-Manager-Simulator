#include <bits/stdc++.h>
using namespace std;

void printFrame(queue<int> q)
{
    vector<int> temp;
    while (!q.empty())
    {
        temp.push_back(q.front());
        q.pop();
    }

    for (int i = 0; i < temp.size(); i++)
    {
        cout << temp[i] << " ";
        q.push(temp[i]);
    }
    cout << endl;
}

bool find(int pgToFind, queue<int> q)
{
    while (!q.empty())
    {
        if (q.front() == pgToFind)
        {
            return true;
        }
        q.pop();
    }
    return false;
}

void fifo(int frames, int pg, vector<int> &pages, int &pageFaults)
{
    queue<int> currPages;
    for (int i = 0; i < pg; i++)
    {
        cout << "Accessing page : " << pages[i] << " - ";
        if (!find(pages[i], currPages))
        {
            if (currPages.size() == frames)
            {
                currPages.pop();
            }
            currPages.push(pages[i]);
            pageFaults++;

            cout << "Page Fault (Inserted) : ";
        }
        else
        {
            cout << "Page Hit (Already in Frame) : ";
        }
        printFrame(currPages);
    }
}

int main()
{
    int numOfpages, frames, pageFaults = 0;
    cout << "Enter number of pages : ";
    cin >> numOfpages;
    cout << "Enter number of frames : ";
    cin >> frames;
    vector<int> pages;
    int page;
    cout << "Enter the reference string of pages : ";
    for (int i = 0; i < numOfpages; i++)
    {
        cin >> page;
        pages.push_back(page);
    }
    fifo(frames, numOfpages, pages, pageFaults);
    cout << "Number of page faults : " << pageFaults << endl;
    return 0;
}