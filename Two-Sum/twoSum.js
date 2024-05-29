let nums = [1, 2, 3 , 7, 11, 15];
let target = 9;

function twoSum(nums, target){
    let nums_to_index = {};
    for (i=0; i< nums.length; i++) {
        let complement = target - nums[i]
        if(nums_to_index[complement] !== undefined) {
            return [nums_to_index[complement], i];
        }
        nums_to_index[nums[i]] = i
    }
    return []
}
console.log(twoSum(nums, target))
