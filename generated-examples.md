Document ID: `chat-logs/1410233`

<blockquote>

#### philipobi:
Your task is to generate **50 distinct examples** of common C++ coding mistakes that introduce **significant inefficiencies**. For each example, output the following, in order:

1. **A title** on its own line, e.g. `Example 1: Inefficient String Concatenation with std::string`

2. **Inefficient version** – a complete, compilable C++17 snippet (including `#include` directives and `int main()`), using only the standard library, that demonstrates the inefficiency. Make sure it **prints** its result to `stdout` so the compiler cannot optimize it away. Wrap it in a fenced code block tagged `cpp`:
   ```cpp
   // inefficient version
   #include <…>
   int main() {
       …
       std::cout << result << std::endl;
       return 0;
   }
   ```

3. Efficient version – another complete, compilable C++17 snippet that performs exactly the same task and produces the same output, but with the inefficiency removed. Also print its result:
    ```cpp
    // efficient version
    #include <…>
    int main() {
        …
        std::cout << result << std::endl;
        return 0;
    }
    ```

4. Description: One or two sentences explaining why the first version is inefficient (e.g. “Because it performs repeated reallocations” or “Because it uses O(n²) instead of O(n)”) and how the second version fixes it.

Additional requirements:

- Each pair must demonstrate the same observable behavior (same output).
- Use realistic but minimal examples.
- Cover 50 different inefficiencies (e.g. unnecessary copies, wrong container choice, unbounded recursion, missing reserve(), expensive virtual calls in hot loops, etc.).
- Label each section clearly and consistently.
- Do not use any third‑party libraries.
- All examples should compile under g++ -std=c++17.

Please produce the entire set of 50 examples in one response, numbered 1 through 50.


</blockquote>

<blockquote>

#### GitHub Copilot (claude-3.7-sonnet-thought):

# 50 Common C++ Inefficiency Examples

## Example 1: Inefficient String Concatenation in a Loop

```cpp
// inefficient version
#include <iostream>
#include <string>

int main() {
    std::string result;
    for (int i = 0; i < 10000; i++) {
        result = result + std::to_string(i) + " ";
    }
    std::cout << result.substr(0, 20) << "..." << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <string>

int main() {
    std::string result;
    result.reserve(70000);  // Approximate size needed
    for (int i = 0; i < 10000; i++) {
        result += std::to_string(i) + " ";
    }
    std::cout << result.substr(0, 20) << "..." << std::endl;
    return 0;
}
```

Description: The inefficient version causes multiple reallocations of the string as it grows. The efficient version pre-allocates memory using `reserve()` and uses `+=` operator instead of concatenation with `+`, which reduces allocations and copying operations.

## Example 2: Using push_back() Instead of Reserving Capacity

```cpp
// inefficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers;
    for (int i = 0; i < 100000; i++) {
        numbers.push_back(i);
    }
    std::cout << "Size: " << numbers.size() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers;
    numbers.reserve(100000);
    for (int i = 0; i < 100000; i++) {
        numbers.push_back(i);
    }
    std::cout << "Size: " << numbers.size() << std::endl;
    return 0;
}
```

Description: The inefficient version causes multiple reallocations and copies as the vector grows. The efficient version pre-allocates memory for the vector using `reserve()`, which eliminates most reallocations.

## Example 3: Unnecessary std::endl Usage

```cpp
// inefficient version
#include <iostream>
#include <string>
#include <fstream>

int main() {
    std::ofstream devnull("/dev/null");
    for (int i = 0; i < 10000; i++) {
        devnull << "Number: " << i << std::endl;
    }
    devnull << "Done" << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <string>
#include <fstream>

int main() {
    std::ofstream devnull("/dev/null");
    for (int i = 0; i < 10000; i++) {
        devnull << "Number: " << i << '\n';
    }
    devnull << "Done" << '\n';
    return 0;
}
```

Description: Using `std::endl` forces a flush of the output buffer every time, which is unnecessary and inefficient. Using `'\n'` character instead allows the buffer to be flushed only when needed.

## Example 4: Unnecessary Copy of Large Objects

```cpp
// inefficient version
#include <iostream>
#include <vector>

std::vector<int> createAndProcess(std::vector<int> data) {
    for (int i = 0; i < 1000; i++) {
        data.push_back(i);
    }
    return data;
}

int main() {
    std::vector<int> myData(10000, 42);
    std::vector<int> result = createAndProcess(myData);
    std::cout << "Size: " << result.size() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>

std::vector<int> createAndProcess(const std::vector<int>& data) {
    std::vector<int> result = data;
    for (int i = 0; i < 1000; i++) {
        result.push_back(i);
    }
    return result;
}

int main() {
    std::vector<int> myData(10000, 42);
    std::vector<int> result = createAndProcess(myData);
    std::cout << "Size: " << result.size() << std::endl;
    return 0;
}
```

Description: The inefficient version passes and returns large vectors by value, causing unnecessary copies. The efficient version passes by const reference to avoid one copy.

## Example 5: Using std::find Instead of std::unordered_set for Lookups

```cpp
// inefficient version
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> numbers;
    for (int i = 0; i < 10000; i++) {
        numbers.push_back(i);
    }
    
    int lookups = 0;
    for (int i = 0; i < 1000; i++) {
        if (std::find(numbers.begin(), numbers.end(), i * 5) != numbers.end()) {
            lookups++;
        }
    }
    
    std::cout << "Found: " << lookups << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <unordered_set>

int main() {
    std::vector<int> temp;
    for (int i = 0; i < 10000; i++) {
        temp.push_back(i);
    }
    
    std::unordered_set<int> numbers(temp.begin(), temp.end());
    
    int lookups = 0;
    for (int i = 0; i < 1000; i++) {
        if (numbers.find(i * 5) != numbers.end()) {
            lookups++;
        }
    }
    
    std::cout << "Found: " << lookups << std::endl;
    return 0;
}
```

Description: The inefficient version uses `std::find` which has O(n) complexity, resulting in O(n²) overall complexity. The efficient version uses `std::unordered_set` for O(1) lookups, resulting in O(n) overall complexity.

## Example 6: Inefficient String Splitting

```cpp
// inefficient version
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::string input = "apple,banana,orange,grape,pear,peach,kiwi";
    std::vector<std::string> tokens;
    
    size_t start = 0;
    size_t end = 0;
    while ((end = input.find(',', start)) != std::string::npos) {
        std::string token = input.substr(start, end - start);
        tokens.push_back(token);
        start = end + 1;
    }
    tokens.push_back(input.substr(start));
    
    std::cout << "Tokens: " << tokens.size() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <string>
#include <vector>
#include <string_view>

int main() {
    std::string input = "apple,banana,orange,grape,pear,peach,kiwi";
    std::vector<std::string> tokens;
    
    size_t start = 0;
    size_t end = 0;
    while ((end = input.find(',', start)) != std::string::npos) {
        tokens.emplace_back(input.substr(start, end - start));
        start = end + 1;
    }
    tokens.emplace_back(input.substr(start));
    
    std::cout << "Tokens: " << tokens.size() << std::endl;
    return 0;
}
```

Description: The inefficient version creates temporary strings before pushing them. The efficient version uses `emplace_back()` to construct strings directly in the vector, avoiding unnecessary copies.

## Example 7: Inefficient Use of emplace_back with Temporary Objects

```cpp
// inefficient version
#include <iostream>
#include <vector>
#include <string>

class Person {
public:
    Person(std::string n, int a) : name(std::move(n)), age(a) {}
    std::string name;
    int age;
};

int main() {
    std::vector<Person> people;
    std::string name = "John";
    
    for (int i = 0; i < 1000; i++) {
        Person temp(name + std::to_string(i), i);
        people.emplace_back(temp);  // Using emplace_back with a temporary
    }
    
    std::cout << "People: " << people.size() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <string>

class Person {
public:
    Person(std::string n, int a) : name(std::move(n)), age(a) {}
    std::string name;
    int age;
};

int main() {
    std::vector<Person> people;
    std::string name = "John";
    
    for (int i = 0; i < 1000; i++) {
        people.emplace_back(name + std::to_string(i), i);  // Passing constructor arguments directly
    }
    
    std::cout << "People: " << people.size() << std::endl;
    return 0;
}
```

Description: The inefficient version creates a temporary Person object and then moves it into the vector. The efficient version passes the constructor arguments directly to `emplace_back()`, which constructs the object in-place.

## Example 8: Inefficient Map Lookup

```cpp
// inefficient version
#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, int> counts;
    counts["apple"] = 5;
    counts["banana"] = 7;
    counts["orange"] = 12;
    
    int total = 0;
    for (int i = 0; i < 10000; i++) {
        if (counts.find("apple") != counts.end()) {
            total += counts["apple"];
        }
        if (counts.find("banana") != counts.end()) {
            total += counts["banana"];
        }
        if (counts.find("orange") != counts.end()) {
            total += counts["orange"];
        }
    }
    
    std::cout << "Total: " << total << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, int> counts;
    counts["apple"] = 5;
    counts["banana"] = 7;
    counts["orange"] = 12;
    
    int total = 0;
    for (int i = 0; i < 10000; i++) {
        auto apple_it = counts.find("apple");
        if (apple_it != counts.end()) {
            total += apple_it->second;
        }
        
        auto banana_it = counts.find("banana");
        if (banana_it != counts.end()) {
            total += banana_it->second;
        }
        
        auto orange_it = counts.find("orange");
        if (orange_it != counts.end()) {
            total += orange_it->second;
        }
    }
    
    std::cout << "Total: " << total << std::endl;
    return 0;
}
```

Description: The inefficient version performs duplicate lookups: one in `find()` and another when accessing with `operator[]`. The efficient version uses the iterator returned by `find()` to avoid duplicate lookups.

## Example 9: Using Bubble Sort Instead of std::sort

```cpp
// inefficient version
#include <iostream>
#include <vector>

void bubbleSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
            }
        }
    }
}

int main() {
    std::vector<int> numbers;
    for (int i = 10000; i > 0; i--) {
        numbers.push_back(i);
    }
    
    bubbleSort(numbers);
    
    std::cout << "First: " << numbers.front() << ", Last: " << numbers.back() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> numbers;
    for (int i = 10000; i > 0; i--) {
        numbers.push_back(i);
    }
    
    std::sort(numbers.begin(), numbers.end());
    
    std::cout << "First: " << numbers.front() << ", Last: " << numbers.back() << std::endl;
    return 0;
}
```

Description: Bubble sort has O(n²) time complexity, while `std::sort` uses introsort which typically has O(n log n) complexity. For large arrays, this makes a significant difference in performance.

## Example 10: Inefficient File Reading Line by Line

```cpp
// inefficient version
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

int main() {
    std::ofstream outfile("test.txt");
    for (int i = 0; i < 10000; i++) {
        outfile << "Line " << i << "\n";
    }
    outfile.close();
    
    std::vector<std::string> lines;
    std::ifstream file("test.txt");
    std::string line;
    
    while (file.good()) {
        std::getline(file, line);
        if (!file.eof()) {
            lines.push_back(line);
        }
    }
    
    std::cout << "Lines read: " << lines.size() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

int main() {
    std::ofstream outfile("test.txt");
    for (int i = 0; i < 10000; i++) {
        outfile << "Line " << i << "\n";
    }
    outfile.close();
    
    std::vector<std::string> lines;
    std::ifstream file("test.txt");
    std::string line;
    
    while (std::getline(file, line)) {
        lines.push_back(line);
    }
    
    std::cout << "Lines read: " << lines.size() << std::endl;
    return 0;
}
```

Description: The inefficient version checks `good()` before reading, which can lead to reading one extra line, and requires an extra check for `eof()`. The efficient version uses the return value of `getline()` directly in the while condition, which is more idiomatic and correct.

## Example 11: Inefficient Loop Variable Type

```cpp
// inefficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers(10000);
    for (int i = 0; i < numbers.size(); i++) {
        numbers[i] = i;
    }
    
    int sum = 0;
    for (int i = 0; i < numbers.size(); i++) {
        sum += numbers[i];
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers(10000);
    for (size_t i = 0; i < numbers.size(); i++) {
        numbers[i] = static_cast<int>(i);
    }
    
    int sum = 0;
    for (size_t i = 0; i < numbers.size(); i++) {
        sum += numbers[i];
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

Description: The inefficient version uses `int` for loop counters, which can cause signed/unsigned comparison warnings and potential overflow issues. The efficient version uses `size_t`, the appropriate type for container sizes and indices.

## Example 12: Inefficient Usage of std::vector::erase

```cpp
// inefficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers;
    for (int i = 0; i < 10000; i++) {
        numbers.push_back(i);
    }
    
    // Remove all even numbers
    for (size_t i = 0; i < numbers.size(); i++) {
        if (numbers[i] % 2 == 0) {
            numbers.erase(numbers.begin() + i);
            // Don't adjust i, which can lead to skipping elements
        }
    }
    
    std::cout << "Remaining elements: " << numbers.size() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> numbers;
    for (int i = 0; i < 10000; i++) {
        numbers.push_back(i);
    }
    
    // Remove all even numbers using the erase-remove idiom
    numbers.erase(
        std::remove_if(numbers.begin(), numbers.end(), 
            [](int n) { return n % 2 == 0; }),
        numbers.end()
    );
    
    std::cout << "Remaining elements: " << numbers.size() << std::endl;
    return 0;
}
```

Description: The inefficient version repeatedly calls `erase()` which has O(n) complexity, resulting in O(n²) overall, and doesn't properly adjust indices after removal. The efficient version uses the erase-remove idiom for O(n) complexity and correct removal.

## Example 13: Inefficient String to Integer Conversion

```cpp
// inefficient version
#include <iostream>
#include <string>
#include <sstream>
#include <vector>

int main() {
    std::vector<std::string> numbers = {"123", "456", "789", "101", "202"};
    int sum = 0;
    
    for (const auto& numStr : numbers) {
        std::stringstream ss(numStr);
        int num;
        ss >> num;
        sum += num;
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> numbers = {"123", "456", "789", "101", "202"};
    int sum = 0;
    
    for (const auto& numStr : numbers) {
        sum += std::stoi(numStr);
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

Description: The inefficient version creates a `stringstream` for each conversion, which has significant overhead. The efficient version uses `std::stoi()` which is specifically designed for string-to-integer conversion.

## Example 14: Using std::list for Random Access

```cpp
// inefficient version
#include <iostream>
#include <list>
#include <cstdlib>
#include <ctime>

int main() {
    std::list<int> numbers;
    for (int i = 0; i < 10000; i++) {
        numbers.push_back(i);
    }
    
    std::srand(static_cast<unsigned int>(std::time(nullptr)));
    int sum = 0;
    
    for (int i = 0; i < 1000; i++) {
        int index = std::rand() % numbers.size();
        auto it = numbers.begin();
        std::advance(it, index);
        sum += *it;
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>

int main() {
    std::vector<int> numbers;
    for (int i = 0; i < 10000; i++) {
        numbers.push_back(i);
    }
    
    std::srand(static_cast<unsigned int>(std::time(nullptr)));
    int sum = 0;
    
    for (int i = 0; i < 1000; i++) {
        int index = std::rand() % numbers.size();
        sum += numbers[index];
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

Description: The inefficient version uses `std::list` which has O(n) random access complexity. The efficient version uses `std::vector` which has O(1) random access complexity, making it much faster for this use case.

## Example 15: Passing Large Objects by Value to Functions

```cpp
// inefficient version
#include <iostream>
#include <vector>
#include <numeric>

int calculateSum(std::vector<int> values) {
    return std::accumulate(values.begin(), values.end(), 0);
}

int main() {
    std::vector<int> numbers(100000, 1);
    int sum = 0;
    
    for (int i = 0; i < 10; i++) {
        sum += calculateSum(numbers);
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <numeric>

int calculateSum(const std::vector<int>& values) {
    return std::accumulate(values.begin(), values.end(), 0);
}

int main() {
    std::vector<int> numbers(100000, 1);
    int sum = 0;
    
    for (int i = 0; i < 10; i++) {
        sum += calculateSum(numbers);
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

Description: The inefficient version passes a large vector by value, making an expensive copy each time. The efficient version passes by const reference, avoiding unnecessary copies.

## Example 16: Inefficient Loop Traversal with Iterator Increment

```cpp
// inefficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers(10000);
    for (int i = 0; i < 10000; i++) {
        numbers[i] = i;
    }
    
    int sum = 0;
    for (auto it = numbers.begin(); it != numbers.end(); it++) {
        sum += *it;
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers(10000);
    for (int i = 0; i < 10000; i++) {
        numbers[i] = i;
    }
    
    int sum = 0;
    for (auto it = numbers.begin(); it != numbers.end(); ++it) {
        sum += *it;
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

Description: The inefficient version uses post-increment `it++` which creates a temporary copy of the iterator before incrementing. The efficient version uses pre-increment `++it` which avoids the temporary copy.

## Example 17: Inefficient Use of std::find with Custom Comparison

```cpp
// inefficient version
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

struct Person {
    std::string name;
    int age;
    
    Person(const std::string& n, int a) : name(n), age(a) {}
};

int main() {
    std::vector<Person> people;
    for (int i = 0; i < 1000; i++) {
        people.push_back(Person("Person" + std::to_string(i), 20 + i % 50));
    }
    
    bool found = false;
    for (const auto& person : people) {
        if (person.name == "Person500") {
            found = true;
            break;
        }
    }
    
    std::cout << "Person500 found: " << (found ? "yes" : "no") << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

struct Person {
    std::string name;
    int age;
    
    Person(const std::string& n, int a) : name(n), age(a) {}
};

int main() {
    std::vector<Person> people;
    for (int i = 0; i < 1000; i++) {
        people.push_back(Person("Person" + std::to_string(i), 20 + i % 50));
    }
    
    auto it = std::find_if(people.begin(), people.end(),
                          [](const Person& p) { return p.name == "Person500"; });
    bool found = (it != people.end());
    
    std::cout << "Person500 found: " << (found ? "yes" : "no") << std::endl;
    return 0;
}
```

Description: The inefficient version manually iterates through the vector with a for loop. The efficient version uses `std::find_if()` with a lambda function, which better expresses the intent and may enable compiler optimizations.

## Example 18: Inefficient String Comparison

```cpp
// inefficient version
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> words = {"apple", "banana", "orange", "grape", "pear"};
    std::string target = "orange";
    
    int count = 0;
    for (int i = 0; i < 100000; i++) {
        for (const auto& word : words) {
            std::string temp = word;
            if (temp == target) {
                count++;
            }
        }
    }
    
    std::cout << "Count: " << count << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> words = {"apple", "banana", "orange", "grape", "pear"};
    std::string target = "orange";
    
    int count = 0;
    for (int i = 0; i < 100000; i++) {
        for (const auto& word : words) {
            if (word == target) {
                count++;
            }
        }
    }
    
    std::cout << "Count: " << count << std::endl;
    return 0;
}
```

Description: The inefficient version creates unnecessary temporary copies of strings before comparison. The efficient version compares strings directly without creating temporaries.

## Example 19: Inefficient Map Iteration

```cpp
// inefficient version
#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, int> counts;
    counts["apple"] = 5;
    counts["banana"] = 7;
    counts["orange"] = 12;
    counts["grape"] = 3;
    counts["pear"] = 9;
    
    int total = 0;
    for (int i = 0; i < 100000; i++) {
        for (const auto& key : {"apple", "banana", "orange", "grape", "pear"}) {
            total += counts[key];  // Using operator[] which checks and inserts
        }
    }
    
    std::cout << "Total: " << total << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, int> counts;
    counts["apple"] = 5;
    counts["banana"] = 7;
    counts["orange"] = 12;
    counts["grape"] = 3;
    counts["pear"] = 9;
    
    int total = 0;
    for (int i = 0; i < 100000; i++) {
        for (const auto& pair : counts) {
            total += pair.second;
        }
    }
    
    std::cout << "Total: " << total << std::endl;
    return 0;
}
```

Description: The inefficient version uses `operator[]` which performs lookups that might insert new elements if keys don't exist. The efficient version iterates directly over map entries, which is faster and avoids potential insertions.

## Example 20: Inefficient Use of auto for Iterating Complex Containers

```cpp
// inefficient version
#include <iostream>
#include <vector>
#include <string>

int main() {
    std::vector<std::string> names = {"John", "Alice", "Bob", "Carol", "Dave"};
    
    int totalLength = 0;
    for (int i = 0; i < 100000; i++) {
        for (auto name : names) {  // Copies each string
            totalLength += name.length();
        }
    }
    
    std::cout << "Total length: " << totalLength << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <string>

int main() {
    std::vector<std::string> names = {"John", "Alice", "Bob", "Carol", "Dave"};
    
    int totalLength = 0;
    for (int i = 0; i < 100000; i++) {
        for (const auto& name : names) {  // Uses references, no copying
            totalLength += name.length();
        }
    }
    
    std::cout << "Total length: " << totalLength << std::endl;
    return 0;
}
```

Description: The inefficient version uses `auto` without reference, creating copies of each string during iteration. The efficient version uses `const auto&` to avoid copying strings.

## Example 21: Inefficient Lambda Capture

```cpp
// inefficient version
#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>

int main() {
    std::vector<int> data(10000, 1);
    std::vector<int> multipliers(10000);
    for (int i = 0; i < 10000; i++) {
        multipliers[i] = i % 10 + 1;
    }
    
    std::vector<int> results;
    results.resize(data.size());
    
    // Capture entire vectors by value
    std::transform(data.begin(), data.end(), results.begin(),
        [multipliers](int val) {
            int sum = 0;
            for (size_t i = 0; i < multipliers.size(); i++) {
                sum += val * (i % 100 == 0 ? multipliers[i] : 1);
            }
            return sum;
        }
    );
    
    std::cout << "Result sum: " << std::accumulate(results.begin(), results.end(), 0) << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>

int main() {
    std::vector<int> data(10000, 1);
    std::vector<int> multipliers(10000);
    for (int i = 0; i < 10000; i++) {
        multipliers[i] = i % 10 + 1;
    }
    
    std::vector<int> results;
    results.resize(data.size());
    
    // Capture vector by reference
    std::transform(data.begin(), data.end(), results.begin(),
        [&multipliers](int val) {
            int sum = 0;
            for (size_t i = 0; i < multipliers.size(); i++) {
                sum += val * (i % 100 == 0 ? multipliers[i] : 1);
            }
            return sum;
        }
    );
    
    std::cout << "Result sum: " << std::accumulate(results.begin(), results.end(), 0) << std::endl;
    return 0;
}
```

Description: The inefficient version captures a large vector by value, creating an unnecessary copy. The efficient version captures by reference, avoiding the copy.

## Example 22: Using std::accumulate with Inefficient Operation

```cpp
// inefficient version
#include <iostream>
#include <vector>
#include <numeric>
#include <string>

int main() {
    std::vector<int> numbers(1000, 5);
    
    // Using string concatenation in accumulate
    std::string result = std::accumulate(numbers.begin(), numbers.end(), std::string(""),
        [](std::string a, int b) {
            return a + std::to_string(b) + ",";
        }
    );
    
    std::cout << "Result length: " << result.size() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <string>
#include <sstream>

int main() {
    std::vector<int> numbers(1000, 5);
    
    // Using stringstream instead
    std::ostringstream oss;
    for (const auto& num : numbers) {
        oss << num << ",";
    }
    std::string result = oss.str();
    
    std::cout << "Result length: " << result.size() << std::endl;
    return 0;
}
```

Description: The inefficient version uses `std::accumulate` with string concatenation, which creates multiple temporary strings and has O(n²) complexity. The efficient version uses `std::ostringstream` which has amortized O(n) complexity.

## Example 23: Inefficient Use of std::pow for Integer Powers

```cpp
// inefficient version
#include <iostream>
#include <vector>
#include <cmath>

int main() {
    std::vector<double> results;
    
    for (int i = 0; i < 1000000; i++) {
        double result = std::pow(2.0, 3.0);
        results.push_back(result);
    }
    
    std::cout << "Result: " << results.back() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<double> results;
    
    for (int i = 0; i < 1000000; i++) {
        double result = 2.0 * 2.0 * 2.0;
        results.push_back(result);
    }
    
    std::cout << "Result: " << results.back() << std::endl;
    return 0;
}
```

Description: The inefficient version calls `std::pow` for a constant power computation. The efficient version computes the result directly using multiplication, which is much faster for simple cases like integer powers.

## Example 24: Inefficient Recursive Fibonacci

```cpp
// inefficient version
#include <iostream>
#include <vector>

int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
    std::vector<int> results;
    
    for (int i = 0; i < 35; i++) {
        results.push_back(fibonacci(i));
    }
    
    std::cout << "Fibonacci(34): " << results.back() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> results = {0, 1};
    
    for (int i = 2; i < 35; i++) {
        results.push_back(results[i-1] + results[i-2]);
    }
    
    std::cout << "Fibonacci(34): " << results.back() << std::endl;
    return 0;
}
```

Description: The inefficient version uses recursive calls, recomputing the same values multiple times with exponential complexity O(2ⁿ). The efficient version uses dynamic programming to store intermediate results, reducing complexity to O(n).

## Example 25: Inefficient String Concatenation in Tight Loop

```cpp
// inefficient version
#include <iostream>
#include <string>

int main() {
    std::string result;
    
    for (int i = 0; i < 100000; i++) {
        result = result + ".";
    }
    
    std::cout << "Result length: " << result.length() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <string>

int main() {
    std::string result;
    result.reserve(100000);  // Pre-allocate space
    
    for (int i = 0; i < 100000; i++) {
        result += ".";
    }
    
    std::cout << "Result length: " << result.length() << std::endl;
    return 0;
}
```

Description: The inefficient version uses the `+` operator for concatenation, creating a new string each time. The efficient version uses `reserve()` to pre-allocate space and `+=` operator, which appends without creating a new string.

## Example 26: Using Unoptimized std::pair for Simple Structs

```cpp
// inefficient version
#include <iostream>
#include <vector>
#include <utility>
#include <string>

int main() {
    std::vector<std::pair<std::string, int>> people;
    
    for (int i = 0; i < 10000; i++) {
        people.push_back(std::make_pair("Person" + std::to_string(i), 20 + (i % 50)));
    }
    
    int sum = 0;
    for (const auto& person : people) {
        sum += person.second;
    }
    
    std::cout << "Sum of ages: " << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <string>

struct Person {
    std::string name;
    int age;
};

int main() {
    std::vector<Person> people;
    
    for (int i = 0; i < 10000; i++) {
        people.push_back({"Person" + std::to_string(i), 20 + (i % 50)});
    }
    
    int sum = 0;
    for (const auto& person : people) {
        sum += person.age;
    }
    
    std::cout << "Sum of ages: " << sum << std::endl;
    return 0;
}
```

Description: The inefficient version uses `std::pair` which has generic but less descriptive member names (first, second). The efficient version uses a custom struct with meaningful member names, improving readability and potentially allowing compiler optimizations.

## Example 27: Inefficient Use of std::shared_ptr for Internal Implementation

```cpp
// inefficient version
#include <iostream>
#include <memory>
#include <vector>

class DataProcessor {
    std::shared_ptr<std::vector<int>> data;
public:
    DataProcessor() : data(std::make_shared<std::vector<int>>()) {}
    
    void addData(int value) {
        data->push_back(value);
    }
    
    int sum() const {
        int total = 0;
        for (const auto& val : *data) {
            total += val;
        }
        return total;
    }
};

int main() {
    DataProcessor processor;
    for (int i = 0; i < 10000; i++) {
        processor.addData(i);
    }
    
    std::cout << "Sum: " << processor.sum() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>

class DataProcessor {
    std::vector<int> data;
public:
    DataProcessor() {}
    
    void addData(int value) {
        data.push_back(value);
    }
    
    int sum() const {
        int total = 0;
        for (const auto& val : data) {
            total += val;
        }
        return total;
    }
};

int main() {
    DataProcessor processor;
    for (int i = 0; i < 10000; i++) {
        processor.addData(i);
    }
    
    std::cout << "Sum: " << processor.sum() << std::endl;
    return 0;
}
```

Description: The inefficient version uses `std::shared_ptr` for internal data that doesn't need to be shared. The efficient version stores the data directly as a member variable, avoiding reference counting overhead and indirection.

## Example 28: Inefficient Object Construction with Temporary Objects

```cpp
// inefficient version
#include <iostream>
#include <vector>
#include <string>

class Person {
public:
    Person(std::string n) : name(std::move(n)) {}
    std::string name;
};

int main() {
    std::vector<Person> people;
    
    for (int i = 0; i < 10000; i++) {
        std::string name = "Person" + std::to_string(i);
        people.push_back(Person(name));
    }
    
    std::cout << "First person: " << people.front().name << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <string>

class Person {
public:
    Person(std::string n) : name(std::move(n)) {}
    std::string name;
};

int main() {
    std::vector<Person> people;
    people.reserve(10000);
    
    for (int i = 0; i < 10000; i++) {
        people.emplace_back("Person" + std::to_string(i));
    }
    
    std::cout << "First person: " << people.front().name << std::endl;
    return 0;
}
```

Description: The inefficient version creates a temporary `Person` object and then copies or moves it into the vector. The efficient version uses `emplace_back()` to construct the object directly in the vector, and also reserves memory to avoid reallocations.

## Example 29: Inefficient Dynamic Memory Management

```cpp
// inefficient version
#include <iostream>

int main() {
    int sum = 0;
    
    for (int i = 0; i < 1000000; i++) {
        int* ptr = new int(i);
        sum += *ptr;
        delete ptr;
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>

int main() {
    int sum = 0;
    
    for (int i = 0; i < 1000000; i++) {
        sum += i;
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

Description: The inefficient version allocates and deallocates memory in a tight loop, causing significant overhead. The efficient version avoids unnecessary heap allocations by using stack variables directly.

## Example 30: Inefficient Use of std::vector for Fixed-Size Arrays

```cpp
// inefficient version
#include <iostream>
#include <vector>
#include <numeric>

int main() {
    std::vector<int> data;
    for (int i = 0; i < 5; i++) {
        data.push_back(i);
    }
    
    int sum = 0;
    for (int i = 0; i < 1000000; i++) {
        sum += std::accumulate(data.begin(), data.end(), 0);
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <array>
#include <numeric>

int main() {
    std::array<int, 5> data = {0, 1, 2, 3, 4};
    
    int sum = 0;
    for (int i = 0; i < 1000000; i++) {
        sum += std::accumulate(data.begin(), data.end(), 0);
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

Description: The inefficient version uses `std::vector` for a small, fixed-size collection. The efficient version uses `std::array` which avoids heap allocation and has less overhead.

## Example 31: Inefficient String Comparison with find()

```cpp
// inefficient version
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> words = {
        "apple", "banana", "orange", "grape", "pear"
    };
    
    int count = 0;
    std::string prefix = "ap";
    
    for (int i = 0; i < 100000; i++) {
        for (const auto& word : words) {
            if (word.find(prefix) == 0) {
                count++;
            }
        }
    }
    
    std::cout << "Count: " << count << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> words = {
        "apple", "banana", "orange", "grape", "pear"
    };
    
    int count = 0;
    std::string prefix = "ap";
    
    for (int i = 0; i < 100000; i++) {
        for (const auto& word : words) {
            if (word.substr(0, prefix.length()) == prefix) {
                count++;
            }
        }
    }
    
    std::cout << "Count: " << count << std::endl;
    return 0;
}
```

Description: The inefficient version uses `find()` for prefix matching, but it's designed for substring search anywhere. The efficient version directly compares the prefix using `substr()`, which is clearer and potentially faster for this specific use case.

## Example 32: Inefficient Function Call Inside Loop

```cpp
// inefficient version
#include <iostream>
#include <vector>

std::vector<int> getValues() {
    std::vector<int> values(5, 42);
    return values;
}

int main() {
    int sum = 0;
    
    for (int i = 0; i < 100000; i++) {
        std::vector<int> values = getValues();
        for (const auto& val : values) {
            sum += val;
        }
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>

std::vector<int> getValues() {
    std::vector<int> values(5, 42);
    return values;
}

int main() {
    int sum = 0;
    
    std::vector<int> values = getValues();
    for (int i = 0; i < 100000; i++) {
        for (const auto& val : values) {
            sum += val;
        }
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

Description: The inefficient version repeatedly calls `getValues()` inside a loop, creating the same vector over and over. The efficient version calls it once outside the loop and reuses the result.

## Example 33: Inefficient Stream Formatting

```cpp
// inefficient version
#include <iostream>
#include <iomanip>
#include <sstream>

int main() {
    double value = 3.14159265358979;
    std::string result;
    
    for (int i = 0; i < 100000; i++) {
        std::ostringstream oss;
        oss << std::fixed << std::setprecision(4) << value;
        result = oss.str();
    }
    
    std::cout << "Result: " << result << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <iomanip>
#include <sstream>

int main() {
    double value = 3.14159265358979;
    std::string result;
    
    std::ostringstream oss;
    oss << std::fixed << std::setprecision(4);
    
    for (int i = 0; i < 100000; i++) {
        oss.str("");
        oss.clear();
        oss << value;
        result = oss.str();
    }
    
    std::cout << "Result: " << result << std::endl;
    return 0;
}
```

Description: The inefficient version creates a new `ostringstream` in each loop iteration. The efficient version reuses the same stream by clearing it, which avoids repeated stream creation and formatting setup.

## Example 34: Inefficient Use of Set for Simple Existence Checks

```cpp
// inefficient version
#include <iostream>
#include <set>
#include <string>

int main() {
    std::set<std::string> words = {
        "apple", "banana", "orange", "grape", "pear"
    };
    
    std::string target = "orange";
    int count = 0;
    
    for (int i = 0; i < 1000000; i++) {
        if (words.find(target) != words.end()) {
            count++;
        }
    }
    
    std::cout << "Count: " << count << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <unordered_set>
#include <string>

int main() {
    std::unordered_set<std::string> words = {
        "apple", "banana", "orange", "grape", "pear"
    };
    
    std::string target = "orange";
    int count = 0;
    
    for (int i = 0; i < 1000000; i++) {
        if (words.find(target) != words.end()) {
            count++;
        }
    }
    
    std::cout << "Count: " << count << std::endl;
    return 0;
}
```

Description: The inefficient version uses `std::set` which has O(log n) lookup complexity. The efficient version uses `std::unordered_set` which has O(1) average lookup complexity.

## Example 35: Inefficient String Splitting with istringstream

```cpp
// inefficient version
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int main() {
    std::string input = "apple,banana,orange,grape,pear";
    std::vector<std::string> tokens;
    
    for (int i = 0; i < 10000; i++) {
        tokens.clear();
        std::istringstream ss(input);
        std::string token;
        
        while (std::getline(ss, token, ',')) {
            tokens.push_back(token);
        }
    }
    
    std::cout << "Tokens: " << tokens.size() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::string input = "apple,banana,orange,grape,pear";
    std::vector<std::string> tokens;
    
    for (int i = 0; i < 10000; i++) {
        tokens.clear();
        
        size_t start = 0;
        size_t end = 0;
        while ((end = input.find(',', start)) != std::string::npos) {
            tokens.push_back(input.substr(start, end - start));
            start = end + 1;
        }
        tokens.push_back(input.substr(start));
    }
    
    std::cout << "Tokens: " << tokens.size() << std::endl;
    return 0;
}
```

Description: The inefficient version creates a new `istringstream` for each splitting operation, which has overhead. The efficient version uses direct string manipulation with `find()` and `substr()`, avoiding the stream overhead.

## Example 36: Inefficient Use of getline() for Reading Lines

```cpp
// inefficient version
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

int main() {
    // Create a test file
    std::ofstream outfile("test_lines.txt");
    for (int i = 0; i < 10000; i++) {
        outfile << "Line " << i << "\n";
    }
    outfile.close();
    
    std::vector<std::string> lines;
    std::ifstream file("test_lines.txt");
    std::string line;
    
    while (true) {
        std::getline(file, line);
        if (file.eof()) break;
        lines.push_back(line);
    }
    
    std::cout << "Lines read: " << lines.size() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

int main() {
    // Create a test file
    std::ofstream outfile("test_lines.txt");
    for (int i = 0; i < 10000; i++) {
        outfile << "Line " << i << "\n";
    }
    outfile.close();
    
    std::vector<std::string> lines;
    lines.reserve(10000);
    std::ifstream file("test_lines.txt");
    std::string line;
    
    while (std::getline(file, line)) {
        lines.push_back(line);
    }
    
    std::cout << "Lines read: " << lines.size() << std::endl;
    return 0;
}
```

Description: The inefficient version uses an explicit loop with `eof()` check after `getline()`, which can lead to reading one extra line. The efficient version uses the return value of `getline()` directly in the while condition and reserves memory for the vector.

## Example 37: Inefficient Value Copy in Function Return

```cpp
// inefficient version
#include <iostream>
#include <vector>

class LargeObject {
public:
    std::vector<int> data;
    
    LargeObject(int size) : data(size, 42) {}
};

LargeObject createObject() {
    LargeObject obj(10000);
    return obj;
}

int main() {
    int sum = 0;
    
    for (int i = 0; i < 100; i++) {
        LargeObject obj = createObject();
        for (const auto& val : obj.data) {
            sum += val;
        }
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>

class LargeObject {
public:
    std::vector<int> data;
    
    LargeObject(int size) : data(size, 42) {}
};

LargeObject&& createObject() {
    static LargeObject obj(10000);
    return std::move(obj);
}

int main() {
    int sum = 0;
    
    for (int i = 0; i < 100; i++) {
        const LargeObject& obj = createObject();
        for (const auto& val : obj.data) {
            sum += val;
        }
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

Description: The inefficient version returns a large object by value, potentially causing copy. The efficient version uses a static object and returns it by rvalue reference, avoiding copies (Note: this is safe only because we're just reading from the object).

## Example 38: Using std::map for Integer Keys

```cpp
// inefficient version
#include <iostream>
#include <map>

int main() {
    std::map<int, std::string> data;
    
    for (int i = 0; i < 10000; i++) {
        data[i] = "Value" + std::to_string(i);
    }
    
    int count = 0;
    for (int i = 0; i < 10000; i++) {
        if (data.find(i) != data.end()) {
            count++;
        }
    }
    
    std::cout << "Count: " << count << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <unordered_map>

int main() {
    std::unordered_map<int, std::string> data;
    
    for (int i = 0; i < 10000; i++) {
        data[i] = "Value" + std::to_string(i);
    }
    
    int count = 0;
    for (int i = 0; i < 10000; i++) {
        if (data.find(i) != data.end()) {
            count++;
        }
    }
    
    std::cout << "Count: " << count << std::endl;
    return 0;
}
```

Description: The inefficient version uses `std::map` which has O(log n) lookup complexity. The efficient version uses `std::unordered_map` which has O(1) average lookup complexity for integer keys.

## Example 39: Inefficient Loop Iteration with unnecessary boundary checks

```cpp
// inefficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> data(10000, 1);
    int sum = 0;
    
    for (int i = 0; i < 10000; i++) {
        if (i < data.size()) {
            sum += data[i];
        }
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> data(10000, 1);
    int sum = 0;
    
    for (int i = 0; i < data.size(); i++) {
        sum += data[i];
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

Description: The inefficient version unnecessarily checks if `i < data.size()` in every iteration, even though the loop condition already ensures this. The efficient version avoids this redundant check.

## Example 40: Inefficient Recursive Implementation for Factorials

```cpp
// inefficient version
#include <iostream>
#include <vector>

unsigned long factorial(unsigned int n) {
    if (n == 0 || n == 1)
        return 1;
    return n * factorial(n - 1);
}

int main() {
    std::vector<unsigned long> results;
    
    for (unsigned int i = 0; i < 13; i++) {
        results.push_back(factorial(i));
    }
    
    std::cout << "Factorial of 12: " << results.back() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<unsigned long> results = {1}; // 0! = 1
    
    for (unsigned int i = 1; i < 13; i++) {
        results.push_back(results.back() * i);
    }
    
    std::cout << "Factorial of 12: " << results.back() << std::endl;
    return 0;
}
```

Description: The inefficient version uses recursion, which has function call overhead and stack frame creation for each call. The efficient version uses iteration, which avoids function call overhead.

## Example 41: Inefficient Memory Management in Class

```cpp
// inefficient version
#include <iostream>
#include <string>

class Message {
    char* buffer;
    size_t size;
    
public:
    Message(const std::string& text) {
        size = text.length();
        buffer = new char[size + 1];
        std::copy(text.begin(), text.end(), buffer);
        buffer[size] = '\0';
    }
    
    ~Message() {
        delete[] buffer;
    }
    
    // Missing copy constructor and assignment operator
    
    std::string getText() const {
        return std::string(buffer, size);
    }
};

int main() {
    Message msg1("Hello, World!");
    Message msg2 = msg1;  // Shallow copy, will cause double-free
    
    std::cout << "Message 1: " << msg1.getText() << std::endl;
    std::cout << "Message 2: " << msg2.getText() << std::endl;
    
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <string>
#include <memory>

class Message {
    std::unique_ptr<char[]> buffer;
    size_t size;
    
public:
    Message(const std::string& text) {
        size = text.length();
        buffer = std::make_unique<char[]>(size + 1);
        std::copy(text.begin(), text.end(), buffer.get());
        buffer[size] = '\0';
    }
    
    // Copy constructor
    Message(const Message& other) {
        size = other.size;
        buffer = std::make_unique<char[]>(size + 1);
        std::copy(other.buffer.get(), other.buffer.get() + size + 1, buffer.get());
    }
    
    // Copy assignment operator
    Message& operator=(const Message& other) {
        if (this != &other) {
            size = other.size;
            buffer = std::make_unique<char[]>(size + 1);
            std::copy(other.buffer.get(), other.buffer.get() + size + 1, buffer.get());
        }
        return *this;
    }
    
    std::string getText() const {
        return std::string(buffer.get(), size);
    }
};

int main() {
    Message msg1("Hello, World!");
    Message msg2 = msg1;  // Deep copy
    
    std::cout << "Message 1: " << msg1.getText() << std::endl;
    std::cout << "Message 2: " // efficient version
#include <iostream>
#include <string>
#include <memory>

class Message {
    std::unique_ptr<char[]> buffer;
    size_t size;
    
public:
    Message(const std::string& text) {
        size = text.length();
        buffer = std::make_unique<char[]>(size + 1);
        std::copy(text.begin(), text.end(), buffer.get());
        buffer[size] = '\0';
    }
    
    // Copy constructor
    Message(const Message& other) {
        size = other.size;
        buffer = std::make_unique<char[]>(size + 1);
        std::copy(other.buffer.get(), other.buffer.get() + size + 1, buffer.get());
    }
    
    // Copy assignment operator
    Message& operator=(const Message& other) {
        if (this != &other) {
            size = other.size;
            buffer = std::make_unique<char[]>(size + 1);
            std::copy(other.buffer.get(), other.buffer.get() + size + 1, buffer.get());
        }
        return *this;
    }
    
    std::string getText() const {
        return std::string(buffer.get(), size);
    }
};

int main() {
    Message msg1("Hello, World!");
    Message msg2 = msg1;  // Deep copy
    
    std::cout << "Message 1: " << msg1.getText() << std::endl;
    std::cout << "Message 2: " 
```
<blockquote>

Error: Sorry, the response hit the length limit. Please rephrase your prompt.

</blockquote>

`(4 min, 40.927 s)`

</blockquote>

<blockquote>

#### philipobi:
Please also provide examples 41 - 50

</blockquote>

<blockquote>

#### GitHub Copilot (claude-3.7-sonnet-thought):

# C++ Efficiency Examples (41-50)

## Example 41: Inefficient Lookup with std::map for Known Enum Values

```cpp
// inefficient version
#include <iostream>
#include <map>
#include <string>

enum Color { RED, GREEN, BLUE, YELLOW, PURPLE };

int main() {
    std::map<Color, std::string> colorNames = {
        {RED, "Red"}, {GREEN, "Green"}, {BLUE, "Blue"}, 
        {YELLOW, "Yellow"}, {PURPLE, "Purple"}
    };
    
    Color c = BLUE;
    std::cout << "Color name: " << colorNames[c] << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <string>
#include <array>

enum Color { RED, GREEN, BLUE, YELLOW, PURPLE, COLOR_COUNT };

int main() {
    std::array<std::string, COLOR_COUNT> colorNames = {
        "Red", "Green", "Blue", "Yellow", "Purple"
    };
    
    Color c = BLUE;
    std::cout << "Color name: " << colorNames[c] << std::endl;
    return 0;
}
```

Description: Using `std::map` for small enum-based lookups is inefficient because it involves dynamic allocation and tree traversal operations. The efficient version uses a simple array with O(1) lookup, which is much faster for small enum-indexed data.

## Example 42: Unnecessary Exception Handling in Hot Loop

```cpp
// inefficient version
#include <iostream>
#include <vector>
#include <stdexcept>

int main() {
    std::vector<int> numbers(10000000, 5);
    int sum = 0;
    
    for (int i = 0; i < numbers.size(); ++i) {
        try {
            sum += numbers.at(i); // Uses bounds checking with exceptions
        } catch (const std::out_of_range&) {
            // Won't happen, but the try-catch machinery is still present
        }
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers(10000000, 5);
    int sum = 0;
    
    for (size_t i = 0; i < numbers.size(); ++i) {
        sum += numbers[i]; // No exception handling overhead
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

Description: Exception handling machinery adds significant overhead, especially in hot loops. The inefficient version uses `at()` which throws exceptions for bounds checking, while the efficient version uses operator `[]` which avoids this overhead when bounds checking isn't needed.

## Example 43: Using std::endl Instead of '\n'

```cpp
// inefficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers(10000, 42);
    
    for (int num : numbers) {
        std::cout << num << std::endl; // Flushes buffer on every iteration
    }
    
    std::cout << "Done" << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers(10000, 42);
    
    for (int num : numbers) {
        std::cout << num << '\n'; // No buffer flushing
    }
    
    std::cout << "Done" << std::endl; // Single flush at the end
    return 0;
}
```

Description: Using `std::endl` not only inserts a newline character but also flushes the output buffer, which is expensive when done repeatedly. The efficient version uses `'\n'` characters for line breaks and only flushes once at the end, improving output performance.

## Example 44: Cache-Unfriendly Memory Access Pattern

```cpp
// inefficient version
#include <iostream>
#include <vector>

int main() {
    const int size = 10000;
    std::vector<std::vector<int>> matrix(size, std::vector<int>(size, 1));
    long sum = 0;
    
    // Column-major traversal in a row-major storage system
    for (int col = 0; col < size; ++col) {
        for (int row = 0; row < size; ++row) {
            sum += matrix[row][col];
        }
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>

int main() {
    const int size = 10000;
    std::vector<std::vector<int>> matrix(size, std::vector<int>(size, 1));
    long sum = 0;
    
    // Row-major traversal matches storage layout
    for (int row = 0; row < size; ++row) {
        for (int col = 0; col < size; ++col) {
            sum += matrix[row][col];
        }
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

Description: The inefficient version uses column-major traversal on a row-major stored matrix, causing poor cache locality and frequent cache misses. The efficient version aligns the traversal pattern with the memory layout, improving cache utilization and performance.

## Example 45: Inefficient Use of std::function for Performance-Critical Callbacks

```cpp
// inefficient version
#include <iostream>
#include <functional>
#include <vector>
#include <chrono>

int transform(int x) {
    return x * x + 1;
}

int main() {
    const int size = 10000000;
    std::vector<int> numbers(size, 5);
    std::vector<int> results(size);
    
    std::function<int(int)> func = transform; // Extra overhead
    
    for (int i = 0; i < size; ++i) {
        results[i] = func(numbers[i]);
    }
    
    std::cout << "Result sample: " << results[1000] << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <chrono>

int transform(int x) {
    return x * x + 1;
}

int main() {
    const int size = 10000000;
    std::vector<int> numbers(size, 5);
    std::vector<int> results(size);
    
    // Direct function pointer, no std::function overhead
    int (*func)(int) = transform;
    
    for (int i = 0; i < size; ++i) {
        results[i] = func(numbers[i]);
    }
    
    std::cout << "Result sample: " << results[1000] << std::endl;
    return 0;
}
```

Description: `std::function` introduces type erasure overhead that can impact performance in tight loops. The efficient version uses a direct function pointer which avoids this overhead and allows better compiler optimizations.

## Example 46: Random Number Generation with Modulo Bias

```cpp
// inefficient version
#include <iostream>
#include <random>

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());
    
    const int dice_sides = 6;
    const int rolls = 1000000;
    int counts[dice_sides] = {0};
    
    // This creates modulo bias when RAND_MAX is not a multiple of dice_sides
    for (int i = 0; i < rolls; ++i) {
        int roll = gen() % dice_sides + 1;
        counts[roll-1]++;
    }
    
    for (int i = 0; i < dice_sides; ++i) {
        std::cout << "Side " << (i+1) << ": " << counts[i] << std::endl;
    }
    
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <random>

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dist(1, 6);
    
    const int dice_sides = 6;
    const int rolls = 1000000;
    int counts[dice_sides] = {0};
    
    for (int i = 0; i < rolls; ++i) {
        int roll = dist(gen); // Uses proper distribution
        counts[roll-1]++;
    }
    
    for (int i = 0; i < dice_sides; ++i) {
        std::cout << "Side " << (i+1) << ": " << counts[i] << std::endl;
    }
    
    return 0;
}
```

Description: Using modulo (`%`) on random numbers causes bias when the random number range isn't divisible by the desired range. The efficient version uses `std::uniform_int_distribution` which guarantees uniform distribution without bias.

## Example 47: Linear Search Instead of Binary Search on Sorted Data

```cpp
// inefficient version
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> sortedData(10000);
    for (int i = 0; i < sortedData.size(); ++i) {
        sortedData[i] = i * 2;
    }
    
    // Linear search - O(n)
    int target = 19998;
    bool found = false;
    for (int num : sortedData) {
        if (num == target) {
            found = true;
            break;
        }
    }
    
    std::cout << "Found: " << std::boolalpha << found << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> sortedData(10000);
    for (int i = 0; i < sortedData.size(); ++i) {
        sortedData[i] = i * 2;
    }
    
    // Binary search - O(log n)
    int target = 19998;
    bool found = std::binary_search(sortedData.begin(), sortedData.end(), target);
    
    std::cout << "Found: " << std::boolalpha << found << std::endl;
    return 0;
}
```

Description: The inefficient version uses linear search which is O(n) complexity, while the efficient version uses binary search which is O(log n). For sorted data, binary search provides exponentially better performance as data size increases.

## Example 48: Recompiling Regular Expressions Repeatedly

```cpp
// inefficient version
#include <iostream>
#include <regex>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> emails = {
        "user@example.com",
        "john.doe@company.org",
        "invalid-email",
        "another@email.co.uk"
    };
    
    int validCount = 0;
    
    for (const auto& email : emails) {
        // Recompiles the regex on each iteration
        std::regex emailRegex(R"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})");
        if (std::regex_match(email, emailRegex)) {
            validCount++;
        }
    }
    
    std::cout << "Valid emails: " << validCount << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <regex>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> emails = {
        "user@example.com",
        "john.doe@company.org",
        "invalid-email",
        "another@email.co.uk"
    };
    
    // Compile the regex once, outside the loop
    std::regex emailRegex(R"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})");
    
    int validCount = 0;
    for (const auto& email : emails) {
        if (std::regex_match(email, emailRegex)) {
            validCount++;
        }
    }
    
    std::cout << "Valid emails: " << validCount << std::endl;
    return 0;
}
```

Description: Regular expression compilation is an expensive operation. The inefficient version recompiles the same regex on each loop iteration, while the efficient version compiles it once and reuses it, significantly reducing overhead.

## Example 49: Inefficient Use of std::any When Type is Known

```cpp
// inefficient version
#include <iostream>
#include <any>
#include <vector>
#include <string>

int main() {
    std::vector<std::any> values;
    
    // Store integers in std::any
    for (int i = 0; i < 1000; ++i) {
        values.push_back(std::any(i));
    }
    
    int sum = 0;
    for (const auto& value : values) {
        sum += std::any_cast<int>(value); // Requires type checking and casting
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> values;
    
    // Store integers directly
    for (int i = 0; i < 1000; ++i) {
        values.push_back(i);
    }
    
    int sum = 0;
    for (const auto& value : values) {
        sum += value; // Direct access, no casting needed
    }
    
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

Description: Using `std::any` introduces overhead from type erasure, dynamic allocation, and runtime type checking. When the actual types are known at compile time, using direct types avoids this overhead and enables better compiler optimizations.

## Example 50: Inefficient Recursive Fibonacci Without Memoization

```cpp
// inefficient version
#include <iostream>

unsigned long long fibonacci(unsigned int n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2); // Exponential complexity
}

int main() {
    unsigned int n = 40;
    unsigned long long result = fibonacci(n);
    std::cout << "Fibonacci(" << n << ") = " << result << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>

unsigned long long fibonacci(unsigned int n) {
    if (n <= 1) return n;
    
    std::vector<unsigned long long> fib(n+1);
    fib[0] = 0;
    fib[1] = 1;
    
    for (unsigned int i = 2; i <= n; ++i) {
        fib[i] = fib[i-1] + fib[i-2];
    }
    
    return fib[n];
}

int main() {
    unsigned int n = 40;
    unsigned long long result = fibonacci(n);
    std::cout << "Fibonacci(" << n << ") = " << result << std::endl;
    return 0;
}
```

Description: The inefficient recursive version has exponential time complexity O(2^n) due to redundant recalculations. The efficient version uses dynamic programming with memoization to calculate each Fibonacci number only once, resulting in linear O(n) time complexity.

`(1 min, 14.113 s)`

</blockquote>

