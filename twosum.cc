class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        vector<int> result;
        vector<int> smallInd;
        vector<int> largeInd;
        int length = nums.size();
        cout << length;
        if(length >= 2 && length <= 10000){
            //cout << "\nenter length \n";
            if((target >= -1000000000) && (target <= 1000000000)){
                //cout << "enter target \n";
                int half = target / 2;
                for (int i = 0; i < length; i++) {
                  if (nums.at(i) < half) {
                    smallInd.push_back(i);
                  }
                  else
                    largeInd.push_back(i);
                }

                for( int i = 0; i < smallInd.size(); i++){
                    //cout << "nums.at(i) = " << smallInd.at(i) << "\n";

                    for(int j = i+1; j < largeInd.size(); j++){
                        if((nums.at(smallInd.at(i)) >= -1000000000) && (nums.at(smallInd.at(i)) <= 1000000000)){
                            //cout << "nums.at(j) = " << nums.at(j) << "\n";
                            if(nums.at((largeInd.at(j)) >= -1000000000) && (nums.at(largeInd.at(j)) <= 1000000000)){
                                //cout << "calculate result\n";
                                int res = nums.at(smallInd.at(i)) + nums.at(largeInd.at(j));
                                cout << "result = " << res;
                                if(res == target) {
                                    result.push_back(smallInd.at(i));
                                    result.push_back(largeInd.at(j));
                                    //cout << "\nreturn result\n";
                                    return result;
                                }
                            }
                        }
                    }
                }

            }

        }
        return result;
    }
};
