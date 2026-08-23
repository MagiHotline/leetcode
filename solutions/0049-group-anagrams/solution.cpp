/*
 * Problem: 49. Group Anagrams
 * URL: https://leetcode.com/problems/group-anagrams/
 * Difficulty: Medium
 * Date: 23/08/2026
 */

#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

class Solution {
public:
  vector<vector<string>> groupAnagrams(vector<string> &strs) {

    // count the letters in a hashmap (letter , number_of_occurences)
    vector<unordered_map<char, int>> occs;
    unordered_map<char, int> occ;
    for (int i = 0; i < strs.size(); i++) {
      occ.clear();
      for (int j = 0; j < strs[i].size(); j++) {
        // if we found a letter that its already tracked, increment number of
        // occurences. or else insert the new word with an occurence of 1
        if (occ.contains(strs[i][j])) {
          occ[strs[i][j]]++;
        } else {
          occ.insert({strs[i][j], 1});
        }
      }
      occs.push_back(occ);
    }

    // occs.size() == strs.size()
    vector<vector<string>> res;

    while (!occs.empty()) {
      vector<string> temp_res;
      temp_res.clear();
      temp_res.push_back(strs[0]);
      for (int j = 1; j < strs.size(); j++) {
        if (occs[0] == occs[j]) {
          temp_res.push_back(strs[j]);
          strs.erase(strs.begin() + j);
          occs.erase(occs.begin() + j);
          j--;
        }
      }
      strs.erase(strs.begin());
      occs.erase(occs.begin());
      res.push_back(temp_res);
    }

    return res;
  }
};
