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

## Example 6: Passing `shared_ptr` by value

```cpp
// inefficient version
#include <iostream>
#include <memory>

void use_ptr(std::shared_ptr<int> p, int& counter) { // Copies shared_ptr, increments ref count
    if (p) {
        counter += *p % 2 ? 1 : -1;
    }
}

int main() {
    auto ptr = std::make_shared<int>(0);
    int counter = 0;
    for (int i = 0; i < 1000000; ++i) {
        *ptr = i;
        use_ptr(ptr, counter);
    }
    std::cout << counter << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <memory>

void use_ptr(const std::shared_ptr<int>& p, int& counter) { // No copy, no ref count change
    if (p) {
        counter += *p % 2 ? 1 : -1;
    }
}

int main() {
    auto ptr = std::make_shared<int>(0);
    int counter = 0;
    for (int i = 0; i < 1000000; ++i) {
        *ptr = i;
        use_ptr(ptr, counter);
    }
    std::cout << counter << std::endl;
    return 0;
}
```

Description: Passing a `shared_ptr` by value copies it and involves an atomic increment/decrement of the reference count. Pass by `const` reference if the function doesn't need to modify or store a copy of the `shared_ptr`.´

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

## Example 10: Reading a file character by character

```cpp
// inefficient version
#include <iostream>
#include <fstream>

int main() {
    std::ofstream("test.txt") << std::string(100000, 'x');
    std::ifstream file("test.txt");
    char c;
    long count = 0;
    while (file.get(c)) {
        count++;
    }
    std::cout << "Read " << count << " chars." << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <fstream>
#include <vector>

int main() {
    std::ofstream("test.txt") << std::string(100000, 'x');
    std::ifstream file("test.txt", std::ios::binary);
    const size_t buffer_size = 4096;
    std::vector<char> buffer(buffer_size);
    long count = 0;
    while (file.read(buffer.data(), buffer_size)) {
        count += file.gcount();
    }
    count += file.gcount(); // Add count from final partial read
    std::cout << "Read " << count << " chars." << std::endl;
    return 0;
}
```

Description: Reading a file one character at a time involves many system calls and is very slow. Read the file in larger chunks into a buffer.

## Example 11: Using `std::pow` for integer powers of 2

```cpp
// inefficient version
#include <iostream>
#include <cmath>

int main() {
    long long result = 0;
    for (int i = 0; i < 20; ++i) {
        result += std::pow(2, i);
    }
    std::cout << result << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>

int main() {
    long long result = 0;
    for (int i = 0; i < 20; ++i) {
        result += (1LL << i);
    }
    std::cout << result << std::endl;
    return 0;
}
```

Description: `std::pow` is a general-purpose floating-point function and is slow for integer powers. Use bit-shifting (`1LL << i`) for powers of 2.

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

## Example 16: High contention on a single atomic

```cpp
// inefficient version
#include <iostream>
#include <vector>
#include <thread>
#include <atomic>

std::atomic<long long> counter{0};

void work() {
    for (int i = 0; i < 1000000; ++i) {
        counter++; // High contention from all threads
    }
}

int main() {
    std::vector<std::thread> threads;
    for (int i = 0; i < 8; ++i) threads.emplace_back(work);
    for (auto& t : threads) t.join();
    std::cout << counter << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <thread>
#include <atomic>

std::atomic<long long> counter{0};

void work() {
    long long local_counter = 0; // Use a thread-local variable
    for (int i = 0; i < 1000000; ++i) {
        local_counter++;
    }
    counter += local_counter; // Update the shared atomic once
}

int main() {
    std::vector<std::thread> threads;
    for (int i = 0; i < 8; ++i) threads.emplace_back(work);
    for (auto& t : threads) t.join();
    std::cout << counter << std::endl;
    return 0;
}
```

Description: Having many threads frequently update a single atomic variable creates high contention. A more scalable approach is to use thread-local counters and sum the results at the end.

## Example 17: `std::map` for key lookups when order is not needed

```cpp
// inefficient version
#include <iostream>
#include <map>

int main() {
    std::map<int, int> m;
    for (int i = 0; i < 100000; ++i) {
        m[i] = i;
    }
    long long sum = 0;
    for (int i = 0; i < 100000; ++i) {
        sum += m.count(i);
    }
    std::cout << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <unordered_map>

int main() {
    std::unordered_map<int, int> m;
    for (int i = 0; i < 100000; ++i) {
        m[i] = i;
    }
    long long sum = 0;
    for (int i = 0; i < 100000; ++i) {
        sum += m.count(i);
    }
    std::cout << sum << std::endl;
    return 0;
}
```

Description: `std::map` is a balanced binary search tree with O(log n) lookups. If element order is not required, `std::unordered_map` provides average O(1) lookups.

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

## Example 21: Opening/closing file in a loop

```cpp
// inefficient version
#include <iostream>
#include <fstream>
#include <string>

int main() {
    for (int i = 0; i < 1000; ++i) {
        std::ofstream file("log.txt", std::ios_base::app); // Open and close file handle
        file << "Log entry " << i << "\n";
    }
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <fstream>
#include <string>

int main() {
    std::ofstream file("log.txt", std::ios_base::app); // Open once
    for (int i = 0; i < 1000; ++i) {
        file << "Log entry " << i << "\n";
    }
    // File is closed automatically by destructor
    return 0;
}
```

Description: Opening and closing a file is a slow operation that involves system calls. Open the file once before the loop and close it after the loop finishes.

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

## Example 23: `std::list::sort`

```cpp
// inefficient version
#include <iostream>
#include <list>
#include <random>

int main() {
    std::list<int> l;
    std::mt19937 rng(0);
    for (int i = 0; i < 100000; ++i) l.push_back(rng());
    
    l.sort(); // list::sort has poor cache locality
    
    std::cout << l.front() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <list>
#include <vector>
#include <random>
#include <algorithm>

int main() {
    std::list<int> l;
    std::mt19937 rng(0);
    for (int i = 0; i < 100000; ++i) l.push_back(rng());
    
    std::vector<int> v(l.begin(), l.end());
    std::sort(v.begin(), v.end()); // vector sort is cache-friendly
    l.assign(v.begin(), v.end());
    
    std::cout << l.front() << std::endl;
    return 0;
}
```

Description: `std::list::sort` cannot take advantage of cache locality because list nodes are not contiguous in memory. For sorting large amounts of data, it's often faster to copy the data to a `std::vector`, sort it, and then rebuild the list if necessary.

## Example 24: Manual loop instead of `std::accumulate`

```cpp
// inefficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v(1000000, 1);
    long long sum = 0;
    for (size_t i = 0; i < v.size(); ++i) {
        sum += v[i];
    }
    std::cout << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <numeric>

int main() {
    std::vector<int> v(1000000, 1);
    long long sum = std::accumulate(v.begin(), v.end(), 0LL);
    std::cout << sum << std::endl;
    return 0;
}
```

Description: Standard library algorithms like std::accumulate are often more expressive, less error-prone, and can be better optimized by the compiler.

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

## Example 26: Virtual function call in a hot loop

```cpp
// inefficient version
#include <iostream>
#include <memory>

struct Base { virtual int val(int i) = 0; };
struct Derived : Base { int val(int i) override { return i%2; } };

int main() {
    std::unique_ptr<Base> p = std::make_unique<Derived>();
    long long sum = 0;
    for (int i = 0; i < 10000000; ++i) {
        sum += p->val(i); // Virtual call can inhibit inlining
    }
    std::cout << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <memory>

struct Base { virtual int val(int i) = 0; };
struct Derived : Base { int val(int i) override { return i%2; } };

int main() {
    std::unique_ptr<Derived> p = std::make_unique<Derived>();
    long long sum = 0;
    for (int i = 0; i < 10000000; ++i) {
        sum += p->val(i); // Direct call can be inlined
    }
    std::cout << sum << std::endl;
    return 0;
}
```

Description: Virtual function calls can be slower than direct calls due to vtable lookups and can prevent compiler optimizations like inlining. If the derived type is known within a scope, cast the pointer and call the function directly.

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

## Example 29: Re-calculating a value in a loop

```cpp
// inefficient version
#include <iostream>
#include <cmath>

int main() {
    double angle = 0.785; // pi/4
    double result = 0;
    for (int i = 0; i < 1000000; ++i) {
        result += std::sin(angle); // sin() is calculated every time
    }
    std::cout << result << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <cmath>

int main() {
    double angle = 0.785; // pi/4
    double result = 0;
    const double sin_val = std::sin(angle); // Calculate once
    for (int i = 0; i < 1000000; ++i) {
        result += sin_val;
    }
    std::cout << result << std::endl;
    return 0;
}
```

Description: If a calculation inside a loop uses variables that don't change during the loop (loop-invariant), perform the calculation once before the loop.

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

## Example 31: Manual loop instead of `std::fill`

```cpp
// inefficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v(1000000);
    for (size_t i = 0; i < v.size(); ++i) {
        v[i] = 42;
    }
    std::cout << v.back() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v(1000000);
    std::fill(v.begin(), v.end(), 42);
    std::cout << v.back() << std::endl;
    return 0;
}
```

Description: Use standard library algorithms like `std::fill` when they fit the task. They are more expressive and can be heavily optimized by the compiler (e.g., using `memset` for trivial types).

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

## Example 36: Inefficient `std::priority_queue` usage

```cpp
// inefficient version
#include <iostream>
#include <vector>
#include <queue>
#include <numeric>

int main() {
    std::vector<int> v(100000);
    std::iota(v.begin(), v.end(), 0);
    std::priority_queue<int> pq;
    for (int x : v) {
        pq.push(x); // O(log n) for each push
    }
    std::cout << pq.top() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>
#include <queue>
#include <numeric>

int main() {
    std::vector<int> v(100000);
    std::iota(v.begin(), v.end(), 0);
    // O(n) construction from a range
    std::priority_queue<int> pq(v.begin(), v.end());
    std::cout << pq.top() << std::endl;
    return 0;
}
```

Description: Pushing elements one-by-one into a priority queue is less efficient than initializing it from a range. The range constructor can build the heap in linear time (O(n)).

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

## Example 40: Division and Modulo with powers of two

```cpp
// inefficient version
#include <iostream>

int main() {
    unsigned x = 123456;
    unsigned long sum = 0;
    for (int i = 0; i < 1000000; ++i) {
        sum += (x + i) / 16;
        sum += (x + i) % 16;
    }
    std::cout << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>

int main() {
    unsigned x = 123456;
    unsigned long sum = 0;
    for (int i = 0; i < 1000000; ++i) {
        sum += (x + i) >> 4;
        sum += (x + i) & 15;
    }
    std::cout << sum << std::endl;
    return 0;
}
```

Description: Integer division and modulo are much slower than bitwise operations. For powers of two, use bit-shifting (`>>`) for division and bitwise AND (`&`) for modulo.


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

## Example 42: Inefficient `std::string::erase`

```cpp
// inefficient version
#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s(10000, 'a');
    s[5000] = 'b';
    // Repeatedly calling erase is O(n^2) because it shifts elements each time
    for (size_t i = 0; i < s.length(); ) {
        if (s[i] == 'a') {
            s.erase(i, 1);
        } else {
            ++i;
        }
    }
    std::cout << s << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s(10000, 'a');
    s[5000] = 'b';
    s.erase(std::remove(s.begin(), s.end(), 'a'), s.end());
    std::cout << s << std::endl;
    return 0;
}
```

Description: Repeatedly erasing single characters from a string is very inefficient. Use the erase-remove idiom, which moves all elements to be kept to the front in a single pass and then performs one erase operation.

## Example 43: `std::map` for dense integer keys

```cpp
// inefficient version
#include <iostream>
#include <map>

int main() {
    std::map<int, int> m;
    for (int i = 0; i < 10000; ++i) {
        m[i] = i * 2; // Using map for keys 0, 1, 2, ...
    }
    long long sum = 0;
    for (int i = 0; i < 10000; ++i) {
        sum += m[i];
    }
    std::cout << sum << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v(10000);
    for (int i = 0; i < 10000; ++i) {
        v[i] = i * 2; // Using vector index for keys 0, 1, 2, ...
    }
    long long sum = 0;
    for (int i = 0; i < 10000; ++i) {
        sum += v[i];
    }
    std::cout << sum << std::endl;
    return 0;
}
```

Description: A `std::map` has significant memory and performance overhead compared to a vector. If you have dense, zero-based integer keys, use a `std::vector` where the key is the index.

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

## Example 46: Using `std::vector` for front insertions/deletions

```cpp
// inefficient version
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v;
    for (int i = 0; i < 10000; ++i) {
        v.insert(v.begin(), i);
    }
    std::cout << v.front() << std::endl;
    return 0;
}
```

```cpp
// efficient version
#include <iostream>
#include <deque>

int main() {
    std::deque<int> d;
    for (int i = 0; i < 10000; ++i) {
        d.push_front(i);
    }
    std::cout << d.front() << std::endl;
    return 0;
}
```

Description: Inserting at the beginning of a `std::vector` is an O(n) operation as all subsequent elements must be shifted. Use `std::deque` for efficient O(1) insertions at both ends.

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
