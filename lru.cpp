#include <bits/stdc++.h>
using namespace std;

void lru(int frames, int pg, vector<int> &pages, int &pageFaults)
{
    unordered_set<int> s;
    unordered_map<int, int> pgframe(frames);
    for (int i = 0; i < pages.size(); i++)
    {
        if (s.size() < frames)
        {
            if (s.find(pages[i]) == s.end())
            {
                s.insert(pages[i]);
                pageFaults++;
            }
            pgframe[pages[i]] = i;
        }
        else
        {
            if (s.find(pages[i]) == s.end())
            {
                int lru = INT_MAX, val;
                for (auto it : s)
                {
                    if (pgframe[it] < lru)
                    {
                        lru = pgframe[it];
                        val = it;
                    }
                }
                s.erase(val);
                s.insert(pages[i]);
                pageFaults++;
            }
            pgframe[pages[i]] = i;
        }
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
    lru(frames, numOfpages, pages, pageFaults);
    cout << "Number of page faults : " << pageFaults << endl;
    return 0;
}