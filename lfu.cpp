#include<bits/stdc++.h>
using namespace std;

void lfu(int frames, int pg, vector<int> &pages, int &pageFaults){
    
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