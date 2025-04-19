#include<bits/stdc++.h>
using namespace std;

void lfu(int frames, int pg, vector<int> &pages, int &pageFaults)
{
    unordered_set<int> s;
    unordered_map<int, int> freq;

    for (int i = 0; i < pages.size(); i++)
    {
        int currPage = pages[i];

        if (s.size() < frames)
        {
            if (s.find(currPage) == s.end())
            {
                s.insert(currPage);
                pageFaults++;
                freq[currPage] = 1;
            }
            else
            {
                freq[currPage]++;
            }
        }
        else
        {
            if (s.find(currPage) == s.end())
            {
                int minFreq = INT_MAX, val = -1;
                for (auto it : s)
                {
                    if (freq[it] < minFreq)
                    {
                        minFreq = freq[it];
                        val = it;
                    }
                }
                s.erase(val);
                freq.erase(val);
                s.insert(currPage);
                pageFaults++;
                freq[currPage] = 1;
            }
            else
            {
                freq[currPage]++;
            }
        }
    }
}


int main(){
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
    lfu(frames, numOfpages, pages, pageFaults);
    cout << "Number of page faults : " << pageFaults << endl;
    return 0;
}