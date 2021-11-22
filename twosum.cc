class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        vector<int> result;
        int length = nums.size();
        cout << length;
        if(length >= 2 && length <= 10000){
            //cout << "\nenter length \n";
            if((target >= -1000000000) && (target <= 1000000000)){
                //cout << "enter target \n";
                for( int i = 0; i < length; i++){
                    cout << "nums.at(i) = " << nums.at(i) << "\n";
                    for(int j = i+1; j < length; j++){
                        if((nums.at(i) >= -1000000000) && (nums.at(i) <= 1000000000)){
                            cout << "nums.at(j) = " << nums.at(j) << "\n";
                            if((nums.at(j) >= -1000000000) && (nums.at(j) <= 1000000000)){
                                //cout << "calculate result\n";
                                int res = nums.at(i) + nums.at(j);
                                cout << "result = " << res;
                                if(res == target) {
                                    result.push_back(i);
                                    result.push_back(j);
                                    cout << "\nreturn result\n";
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
