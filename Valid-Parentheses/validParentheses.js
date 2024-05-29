function isValid(s) {
    const stack = [];
    const hashMap = {
      ")": "(",
      "]": "[",
      "}": "{",
    };
    for (let char of s) {
      if (char === "(" || char === "[" || char == "{") {
        stack.push(char);
      } else if (char === ")" || char === "]" || char === "}") {
        if (stack.length === 0 || stack.pop() !== hashMap[char]) {
          return false;
        }
      }
    }
    return stack.length === 0;
  }
  
  console.log(isValid("()")); // true
  console.log(isValid("()[]{}")); // true
  console.log(isValid("(]")); // false
  console.log(isValid("([)]")); // false
  console.log(isValid("{[]}")); // true
  