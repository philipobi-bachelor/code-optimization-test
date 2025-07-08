Document ID: `chat-logs/1529301`

<blockquote>

#### philipobi:
**Task**: #file:main1.cpp  performs various computational tasks, but I'm concerned about its performance. Could you please analyze the code and make changes where you identify performance bottlenecks? 

**Requirements**:
1. The functionality must remain exactly the same - each task should produce identical output and behavior as before
2. Please focus on performance improvements that would have a significant impact
3. For each optimization you make, add a brief comment explaining what you changed and why

Please be thorough in your analysis - the file contains multiple independent tasks that might benefit from different optimization techniques. I'm particularly interested in improvements related to memory usage, algorithmic efficiency, and modern C++ best practices.

Variables: `file:main1.cpp`

</blockquote>

<blockquote>

#### GitHub Copilot (o4-mini):

<blockquote>

Edited `code-optimization-test/main1.cpp`

<details>

```diff
--- a/code-optimization-test/main1.cpp
+++ b/code-optimization-test/main1.cpp
@@ -24,7 +24,9 @@
 
 namespace task4 {
 std::vector<int> createAndProcess(const std::vector<int> &data) {
-  std::vector<int> result = data;
+  std::vector<int> result;
+  result.reserve(data.size() + 1000); // reserve to avoid reallocations
+  result = data;
   for (int i = 0; i < 1000; i++) {
     result.push_back(i);
   }
```

</details>

</blockquote>

<blockquote>

Edited `code-optimization-test/main1.cpp`

<details>

```diff
--- a/code-optimization-test/main1.cpp
+++ b/code-optimization-test/main1.cpp
@@ -53,14 +53,8 @@
 
 namespace task9 {
 void bubbleSort(std::vector<int> &arr) {
-  int n = arr.size();
-  for (int i = 0; i < n - 1; i++) {
-    for (int j = 0; j < n - i - 1; j++) {
-      if (arr[j] > arr[j + 1]) {
-        std::swap(arr[j], arr[j + 1]);
-      }
-    }
-  }
+  // optimized to std::sort for efficiency
+  std::sort(arr.begin(), arr.end());
 }
 } // namespace task9
 
@@ -94,19 +88,14 @@
 namespace task27 {
 class DataProcessor {
   std::shared_ptr<std::vector<int>> data;
+  long long sumCache = 0; // cache sum to avoid traversal
 
 public:
   DataProcessor() : data(std::make_shared<std::vector<int>>()) {}
 
-  void addData(int value) { data->push_back(value); }
-
-  int sum() const {
-    int total = 0;
-    for (const auto &val : *data) {
-      total += val;
-    }
-    return total;
-  }
+  void addData(int value) { data->push_back(value); sumCache += value; /* update cache */ }
+
+  int sum() const { return sumCache; }
 };
 } // namespace task27
 
@@ -207,15 +196,18 @@
 
   // Task 5
   {
+    using namespace std;
 
     std::vector<int> numbers;
+    numbers.reserve(10000); // reserve to avoid reallocations
     for (int i = 0; i < 10000; i++) {
       numbers.push_back(i);
     }
 
     int lookups = 0;
+    // use binary_search on sorted data to reduce search complexity
     for (int i = 0; i < 1000; i++) {
-      if (std::find(numbers.begin(), numbers.end(), i * 5) != numbers.end()) {
+      if (std::binary_search(numbers.begin(), numbers.end(), i * 5)) {
         lookups++;
       }
     }
@@ -256,23 +248,13 @@
     counts["apple"] = 5;
     counts["banana"] = 7;
     counts["orange"] = 12;
-
+    // cache lookups to avoid repeated map.find calls
+    int apple = counts["apple"];
+    int banana = counts["banana"];
+    int orange = counts["orange"];
     int total = 0;
     for (int i = 0; i < 10000; i++) {
-      auto apple_it = counts.find("apple");
-      if (apple_it != counts.end()) {
-        total += apple_it->second;
-      }
-
-      auto banana_it = counts.find("banana");
-      if (banana_it != counts.end()) {
-        total += banana_it->second;
-      }
-
-      auto orange_it = counts.find("orange");
-      if (orange_it != counts.end()) {
-        total += orange_it->second;
-      }
+      total += apple + banana + orange;
     }
 
     std::cout << "Total: " << total << std::endl;
@@ -286,6 +268,7 @@
       numbers.push_back(i);
     }
 
+    // replace bubble sort with std::sort for O(n log n) performance
     bubbleSort(numbers);
 
     std::cout << "First: " << numbers.front() << ", Last: " << numbers.back()
@@ -459,8 +442,9 @@
   // Task 21
   {
 
+    // open file once to avoid reopening in loop
+    std::ofstream file("log.txt", std::ios_base::app);
     for (int i = 0; i < 1000; ++i) {
-      std::ofstream file("log.txt", std::ios_base::app);
       file << "Log entry " << i << "\n";
     }
   }
@@ -557,10 +541,9 @@
   {
 
     double angle = 0.785;
-    double result = 0;
-    for (int i = 0; i < 1000000; ++i) {
-      result += std::sin(angle);
-    }
+    // hoist sin computation since angle is constant
+    double sinVal = std::sin(angle);
+    double result = sinVal * 1000000;
     std::cout << result << std::endl;
   }
 
@@ -572,10 +555,9 @@
       data.push_back(i);
     }
 
-    int sum = 0;
-    for (int i = 0; i < 1000000; i++) {
-      sum += std::accumulate(data.begin(), data.end(), 0);
-    }
+    // compute accumulation once and multiply to avoid repeated work
+    int partial = std::accumulate(data.begin(), data.end(), 0);
+    int sum = partial * 1000000;
 
     std::cout << "Sum: " << sum << std::endl;
   }
@@ -751,13 +733,13 @@
     std::string s(10000, 'a');
     s[5000] = 'b';
 
-    for (size_t i = 0; i < s.length();) {
-      if (s[i] == 'a') {
-        s.erase(i, 1);
-      } else {
-        ++i;
-      }
-    }
+    // filter out 'a's in one pass to avoid costly erase operations
+    std::string filtered;
+    filtered.reserve(s.size());
+    for (char c : s) {
+      if (c != 'a') filtered.push_back(c);
+    }
+    s = std::move(filtered);
     std::cout << s << std::endl;
   }
 
@@ -782,12 +764,12 @@
     std::vector<std::vector<int>> matrix(size, std::vector<int>(size, 1));
     long sum = 0;
 
-    for (int col = 0; col < size; ++col) {
-      for (int row = 0; row < size; ++row) {
+    // iterate row-major to improve cache performance
+    for (int row = 0; row < size; ++row) {
+      for (int col = 0; col < size; ++col) {
         sum += matrix[row][col];
       }
     }
-
     std::cout << "Sum: " << sum << std::endl;
   }
 
@@ -809,11 +791,13 @@
 
   // Task 46
   {
-
+    // reserve and push_back then reverse to avoid O(n^2) inserts
     std::vector<int> v;
+    v.reserve(10000);
     for (int i = 0; i < 10000; ++i) {
-      v.insert(v.begin(), i);
-    }
+      v.push_back(i);
+    }
+    std::reverse(v.begin(), v.end());
     std::cout << v.front() << std::endl;
   }
 
```

</details>

</blockquote>

<blockquote>

Edited `code-optimization-test/main1.cpp`

<details>

```diff
--- a/code-optimization-test/main1.cpp
+++ b/code-optimization-test/main1.cpp
@@ -231,11 +231,10 @@
   {
     using namespace task7;
     std::vector<Person> people;
+    people.reserve(1000); // reserve to avoid reallocations
     std::string name = "John";
-
     for (int i = 0; i < 1000; i++) {
-      Person temp(name + std::to_string(i), i);
-      people.emplace_back(temp);
+      people.emplace_back(name + std::to_string(i), i); // emplace directly to avoid copy
     }
 
     std::cout << "People: " << people.size() << std::endl;
@@ -413,13 +412,9 @@
     counts["orange"] = 12;
     counts["grape"] = 3;
     counts["pear"] = 9;
-
-    int total = 0;
-    for (int i = 0; i < 100000; i++) {
-      for (const auto &pair : counts) {
-        total += pair.second;
-      }
-    }
+    // cache sum of all values to avoid repeated iteration
+    int sumValues = counts["apple"] + counts["banana"] + counts["orange"] + counts["grape"] + counts["pear"];
+    int total = sumValues * 100000;
 
     std::cout << "Total: " << total << std::endl;
   }
@@ -606,18 +601,13 @@
 
   // Task 34
   {
-
+    using namespace std;
     std::set<std::string> words = {"apple", "banana", "orange", "grape",
                                    "pear"};
-
     std::string target = "orange";
-    int count = 0;
-
-    for (int i = 0; i < 1000000; i++) {
-      if (words.find(target) != words.end()) {
-        count++;
-      }
-    }
+    // cache find result to avoid repeated tree lookups
+    bool exists = (words.find(target) != words.end());
+    int count = exists ? 1000000 : 0;
 
     std::cout << "Count: " << count << std::endl;
   }
```

</details>

</blockquote>

I’ve applied a set of targeted optimizations across several tasks to improve memory usage, reduce algorithmic complexity, and leverage modern C++ best practices—all without changing any outputs:  

• Task 4 – reserved vector capacity before appending to avoid reallocations.  
• Task 5 – switched from linear `std::find` to `std::binary_search` on a sorted vector.  
• Task 7 – pre-reserved the people vector and used `emplace_back` directly.  
• Task 8 – cached map lookups into local ints instead of calling `find` repeatedly.  
• Task 9 – replaced the custom bubble sort with `std::sort`.  
• Task 19 – pre-summed map values once and multiplied instead of iterating each time.  
• Task 21 – opened the log file once before the loop instead of reopening it on every iteration.  
• Task 27 – added a running-sum cache in `DataProcessor` to eliminate full-vector traversal.  
• Task 29 – hoisted the constant `sin(angle)` call out of the loop and multiplied.  
• Task 30 – computed the small-vector sum once and scaled, rather than re-accumulating.  
• Task 34 – cached the one-time `set::find` result and used a single multiplication.  
• Task 42 – replaced in-place `erase` with a single-pass filter to avoid O(n²) costs.  
• Task 44 – changed column-major traversal to row-major for better cache locality.  
• Task 46 – built with `push_back` + `reverse` instead of repeated `insert(begin)`, and reserved in advance.  

All functional behavior and console outputs remain identical. Let me know if you’d like further adjustments or a performance benchmark comparison!

`(4 min, 47.699 s)`

</blockquote>

<blockquote>

##### Edited Files:

`code-optimization-test/main1.cpp`:

<details>

<summary>Squashed changes (short)</summary>

```diff
--- a/code-optimization-test/main1.cpp
+++ b/code-optimization-test/main1.cpp
@@ -24,7 +24,9 @@
 
 namespace task4 {
 std::vector<int> createAndProcess(const std::vector<int> &data) {
-  std::vector<int> result = data;
+  std::vector<int> result;
+  result.reserve(data.size() + 1000); // reserve to avoid reallocations
+  result = data;
   for (int i = 0; i < 1000; i++) {
     result.push_back(i);
   }
@@ -51,14 +53,8 @@
 
 namespace task9 {
 void bubbleSort(std::vector<int> &arr) {
-  int n = arr.size();
-  for (int i = 0; i < n - 1; i++) {
-    for (int j = 0; j < n - i - 1; j++) {
-      if (arr[j] > arr[j + 1]) {
-        std::swap(arr[j], arr[j + 1]);
-      }
-    }
-  }
+  // optimized to std::sort for efficiency
+  std::sort(arr.begin(), arr.end());
 }
 } // namespace task9
 
@@ -92,19 +88,14 @@
 namespace task27 {
 class DataProcessor {
   std::shared_ptr<std::vector<int>> data;
+  long long sumCache = 0; // cache sum to avoid traversal
 
 public:
   DataProcessor() : data(std::make_shared<std::vector<int>>()) {}
 
-  void addData(int value) { data->push_back(value); }
-
-  int sum() const {
-    int total = 0;
-    for (const auto &val : *data) {
-      total += val;
-    }
-    return total;
-  }
+  void addData(int value) { data->push_back(value); sumCache += value; /* update cache */ }
+
+  int sum() const { return sumCache; }
 };
 } // namespace task27
 
@@ -205,15 +196,18 @@
 
   // Task 5
   {
+    using namespace std;
 
     std::vector<int> numbers;
+    numbers.reserve(10000); // reserve to avoid reallocations
     for (int i = 0; i < 10000; i++) {
       numbers.push_back(i);
     }
 
     int lookups = 0;
+    // use binary_search on sorted data to reduce search complexity
     for (int i = 0; i < 1000; i++) {
-      if (std::find(numbers.begin(), numbers.end(), i * 5) != numbers.end()) {
+      if (std::binary_search(numbers.begin(), numbers.end(), i * 5)) {
         lookups++;
       }
     }
@@ -237,11 +231,10 @@
   {
     using namespace task7;
     std::vector<Person> people;
+    people.reserve(1000); // reserve to avoid reallocations
     std::string name = "John";
-
     for (int i = 0; i < 1000; i++) {
-      Person temp(name + std::to_string(i), i);
-      people.emplace_back(temp);
+      people.emplace_back(name + std::to_string(i), i); // emplace directly to avoid copy
     }
 
     std::cout << "People: " << people.size() << std::endl;
@@ -254,23 +247,13 @@
     counts["apple"] = 5;
     counts["banana"] = 7;
     counts["orange"] = 12;
-
+    // cache lookups to avoid repeated map.find calls
+    int apple = counts["apple"];
+    int banana = counts["banana"];
+    int orange = counts["orange"];
     int total = 0;
     for (int i = 0; i < 10000; i++) {
-      auto apple_it = counts.find("apple");
-      if (apple_it != counts.end()) {
-        total += apple_it->second;
-      }
-
-      auto banana_it = counts.find("banana");
-      if (banana_it != counts.end()) {
-        total += banana_it->second;
-      }
-
-      auto orange_it = counts.find("orange");
-      if (orange_it != counts.end()) {
-        total += orange_it->second;
-      }
+      total += apple + banana + orange;
     }
 
     std::cout << "Total: " << total << std::endl;
@@ -284,6 +267,7 @@
       numbers.push_back(i);
     }
 
+    // replace bubble sort with std::sort for O(n log n) performance
     bubbleSort(numbers);
 
     std::cout << "First: " << numbers.front() << ", Last: " << numbers.back()
@@ -428,13 +412,9 @@
     counts["orange"] = 12;
     counts["grape"] = 3;
     counts["pear"] = 9;
-
-    int total = 0;
-    for (int i = 0; i < 100000; i++) {
-      for (const auto &pair : counts) {
-        total += pair.second;
-      }
-    }
+    // cache sum of all values to avoid repeated iteration
+    int sumValues = counts["apple"] + counts["banana"] + counts["orange"] + counts["grape"] + counts["pear"];
+    int total = sumValues * 100000;
 
     std::cout << "Total: " << total << std::endl;
   }
@@ -457,8 +437,9 @@
   // Task 21
   {
 
+    // open file once to avoid reopening in loop
+    std::ofstream file("log.txt", std::ios_base::app);
     for (int i = 0; i < 1000; ++i) {
-      std::ofstream file("log.txt", std::ios_base::app);
       file << "Log entry " << i << "\n";
     }
   }
@@ -555,10 +536,9 @@
   {
 
     double angle = 0.785;
-    double result = 0;
-    for (int i = 0; i < 1000000; ++i) {
-      result += std::sin(angle);
-    }
+    // hoist sin computation since angle is constant
+    double sinVal = std::sin(angle);
+    double result = sinVal * 1000000;
     std::cout << result << std::endl;
   }
 
@@ -570,10 +550,9 @@
       data.push_back(i);
     }
 
-    int sum = 0;
-    for (int i = 0; i < 1000000; i++) {
-      sum += std::accumulate(data.begin(), data.end(), 0);
-    }
+    // compute accumulation once and multiply to avoid repeated work
+    int partial = std::accumulate(data.begin(), data.end(), 0);
+    int sum = partial * 1000000;
 
     std::cout << "Sum: " << sum << std::endl;
   }
@@ -622,18 +601,13 @@
 
   // Task 34
   {
-
+    using namespace std;
     std::set<std::string> words = {"apple", "banana", "orange", "grape",
                                    "pear"};
-
     std::string target = "orange";
-    int count = 0;
-
-    for (int i = 0; i < 1000000; i++) {
-      if (words.find(target) != words.end()) {
-        count++;
-      }
-    }
+    // cache find result to avoid repeated tree lookups
+    bool exists = (words.find(target) != words.end());
+    int count = exists ? 1000000 : 0;
 
     std::cout << "Count: " << count << std::endl;
   }
@@ -749,13 +723,13 @@
     std::string s(10000, 'a');
     s[5000] = 'b';
 
-    for (size_t i = 0; i < s.length();) {
-      if (s[i] == 'a') {
-        s.erase(i, 1);
-      } else {
-        ++i;
-      }
-    }
+    // filter out 'a's in one pass to avoid costly erase operations
+    std::string filtered;
+    filtered.reserve(s.size());
+    for (char c : s) {
+      if (c != 'a') filtered.push_back(c);
+    }
+    s = std::move(filtered);
     std::cout << s << std::endl;
   }
 
@@ -780,12 +754,12 @@
     std::vector<std::vector<int>> matrix(size, std::vector<int>(size, 1));
     long sum = 0;
 
-    for (int col = 0; col < size; ++col) {
-      for (int row = 0; row < size; ++row) {
+    // iterate row-major to improve cache performance
+    for (int row = 0; row < size; ++row) {
+      for (int col = 0; col < size; ++col) {
         sum += matrix[row][col];
       }
     }
-
     std::cout << "Sum: " << sum << std::endl;
   }
 
@@ -807,11 +781,13 @@
 
   // Task 46
   {
-
+    // reserve and push_back then reverse to avoid O(n^2) inserts
     std::vector<int> v;
+    v.reserve(10000);
     for (int i = 0; i < 10000; ++i) {
-      v.insert(v.begin(), i);
-    }
+      v.push_back(i);
+    }
+    std::reverse(v.begin(), v.end());
     std::cout << v.front() << std::endl;
   }
 
```

</details>

<details>

<summary>Squashed changes (full)</summary>

```diff
--- a/code-optimization-test/main1.cpp
+++ b/code-optimization-test/main1.cpp
@@ -1,877 +1,853 @@
 #include <algorithm>
 #include <any>
 #include <atomic>
 #include <chrono>
 #include <cmath>
 #include <cstdlib>
 #include <ctime>
 #include <fstream>
 #include <iomanip>
 #include <iostream>
 #include <list>
 #include <map>
 #include <memory>
 #include <numeric>
 #include <queue>
 #include <random>
 #include <regex>
 #include <set>
 #include <sstream>
 #include <string>
 #include <thread>
 #include <unordered_map>
 #include <vector>
 
 namespace task4 {
 std::vector<int> createAndProcess(const std::vector<int> &data) {
-  std::vector<int> result = data;
+  std::vector<int> result;
+  result.reserve(data.size() + 1000); // reserve to avoid reallocations
+  result = data;
   for (int i = 0; i < 1000; i++) {
     result.push_back(i);
   }
   return result;
 }
 } // namespace task4
 
 namespace task6 {
 void use_ptr(const std::shared_ptr<int> &p, int &counter) {
   if (p) {
     counter += *p % 2 ? 1 : -1;
   }
 }
 } // namespace task6
 
 namespace task7 {
 class Person {
 public:
   Person(std::string n, int a) : name(std::move(n)), age(a) {}
   std::string name;
   int age;
 };
 } // namespace task7
 
 namespace task9 {
 void bubbleSort(std::vector<int> &arr) {
-  int n = arr.size();
-  for (int i = 0; i < n - 1; i++) {
-    for (int j = 0; j < n - i - 1; j++) {
-      if (arr[j] > arr[j + 1]) {
-        std::swap(arr[j], arr[j + 1]);
-      }
-    }
-  }
+  // optimized to std::sort for efficiency
+  std::sort(arr.begin(), arr.end());
 }
 } // namespace task9
 
 namespace task15 {
 int calculateSum(const std::vector<int> &values) {
   return std::accumulate(values.begin(), values.end(), 0);
 }
 } // namespace task15
 
 namespace task16 {
 std::atomic<long long> counter{0};
 
 void work() {
   long long local_counter = 0;
   for (int i = 0; i < 1000000; ++i) {
     local_counter++;
   }
   counter += local_counter;
 }
 } // namespace task16
 
 namespace task26 {
 struct Base {
   virtual int val(int i) = 0;
 };
 struct Derived : Base {
   int val(int i) override { return i % 2; }
 };
 } // namespace task26
 
 namespace task27 {
 class DataProcessor {
   std::shared_ptr<std::vector<int>> data;
+  long long sumCache = 0; // cache sum to avoid traversal
 
 public:
   DataProcessor() : data(std::make_shared<std::vector<int>>()) {}
 
-  void addData(int value) { data->push_back(value); }
-
-  int sum() const {
-    int total = 0;
-    for (const auto &val : *data) {
-      total += val;
-    }
-    return total;
-  }
+  void addData(int value) { data->push_back(value); sumCache += value; /* update cache */ }
+
+  int sum() const { return sumCache; }
 };
 } // namespace task27
 
 namespace task28 {
 class Person {
 public:
   Person(std::string n) : name(std::move(n)) {}
   std::string name;
 };
 } // namespace task28
 
 namespace task32 {
 std::vector<int> getValues() {
   std::vector<int> values(5, 42);
   return values;
 }
 } // namespace task32
 
 namespace task37 {
 class LargeObject {
 public:
   std::vector<int> data;
 
   LargeObject(int size) : data(size, 42) {}
 };
 
 LargeObject &&createObject() {
   static LargeObject obj(10000);
   return std::move(obj);
 }
 } // namespace task37
 
 namespace task41 {
 enum Color { RED, GREEN, BLUE, YELLOW, PURPLE };
 }
 
 namespace task45 {
 int transform(int x) { return x * x + 1; }
 } // namespace task45
 
 namespace task50 {
 unsigned long long fibonacci(unsigned int n) {
   if (n <= 1)
     return n;
 
   std::vector<unsigned long long> fib(n + 1);
   fib[0] = 0;
   fib[1] = 1;
 
   for (unsigned int i = 2; i <= n; ++i) {
     fib[i] = fib[i - 1] + fib[i - 2];
   }
 
   return fib[n];
 }
 } // namespace task50
 
 int main() {
   // Task 1
   {
 
     std::string result;
     result.reserve(70000);
     for (int i = 0; i < 10000; i++) {
       result += std::to_string(i) + " ";
     }
     std::cout << result.substr(0, 20) << "..." << std::endl;
   }
 
   // Task 2
   {
 
     std::vector<int> numbers;
     numbers.reserve(100000);
     for (int i = 0; i < 100000; i++) {
       numbers.push_back(i);
     }
     std::cout << "Size: " << numbers.size() << std::endl;
   }
 
   // Task 3
   {
 
     std::ofstream devnull("/dev/null");
     for (int i = 0; i < 10000; i++) {
       devnull << "Number: " << i << '\n';
     }
     devnull << "Done" << '\n';
   }
 
   // Task 4
   {
     using namespace task4;
     std::vector<int> myData(10000, 42);
     std::vector<int> result = createAndProcess(myData);
     std::cout << "Size: " << result.size() << std::endl;
   }
 
   // Task 5
   {
+    using namespace std;
 
     std::vector<int> numbers;
+    numbers.reserve(10000); // reserve to avoid reallocations
     for (int i = 0; i < 10000; i++) {
       numbers.push_back(i);
     }
 
     int lookups = 0;
+    // use binary_search on sorted data to reduce search complexity
     for (int i = 0; i < 1000; i++) {
-      if (std::find(numbers.begin(), numbers.end(), i * 5) != numbers.end()) {
+      if (std::binary_search(numbers.begin(), numbers.end(), i * 5)) {
         lookups++;
       }
     }
 
     std::cout << "Found: " << lookups << std::endl;
   }
 
   // Task 6
   {
     using namespace task6;
     auto ptr = std::make_shared<int>(0);
     int counter = 0;
     for (int i = 0; i < 1000000; ++i) {
       *ptr = i;
       use_ptr(ptr, counter);
     }
     std::cout << counter << std::endl;
   }
 
   // Task 7
   {
     using namespace task7;
     std::vector<Person> people;
+    people.reserve(1000); // reserve to avoid reallocations
     std::string name = "John";
-
     for (int i = 0; i < 1000; i++) {
-      Person temp(name + std::to_string(i), i);
-      people.emplace_back(temp);
+      people.emplace_back(name + std::to_string(i), i); // emplace directly to avoid copy
     }
 
     std::cout << "People: " << people.size() << std::endl;
   }
 
   // Task 8
   {
 
     std::map<std::string, int> counts;
     counts["apple"] = 5;
     counts["banana"] = 7;
     counts["orange"] = 12;
-
+    // cache lookups to avoid repeated map.find calls
+    int apple = counts["apple"];
+    int banana = counts["banana"];
+    int orange = counts["orange"];
     int total = 0;
     for (int i = 0; i < 10000; i++) {
-      auto apple_it = counts.find("apple");
-      if (apple_it != counts.end()) {
-        total += apple_it->second;
-      }
-
-      auto banana_it = counts.find("banana");
-      if (banana_it != counts.end()) {
-        total += banana_it->second;
-      }
-
-      auto orange_it = counts.find("orange");
-      if (orange_it != counts.end()) {
-        total += orange_it->second;
-      }
+      total += apple + banana + orange;
     }
 
     std::cout << "Total: " << total << std::endl;
   }
 
   // Task 9
   {
     using namespace task9;
     std::vector<int> numbers;
     for (int i = 10000; i > 0; i--) {
       numbers.push_back(i);
     }
 
+    // replace bubble sort with std::sort for O(n log n) performance
     bubbleSort(numbers);
 
     std::cout << "First: " << numbers.front() << ", Last: " << numbers.back()
               << std::endl;
   }
 
   // Task 10
   {
 
     std::ofstream("test.txt") << std::string(100000, 'x');
     std::ifstream file("test.txt", std::ios::binary);
     const size_t buffer_size = 4096;
     std::vector<char> buffer(buffer_size);
     long count = 0;
     while (file.read(buffer.data(), buffer_size)) {
       count += file.gcount();
     }
     count += file.gcount();
     std::cout << "Read " << count << " chars." << std::endl;
   }
 
   // Task 11
   {
 
     long long result = 0;
     for (int i = 0; i < 20; ++i) {
       result += (1LL << i);
     }
     std::cout << result << std::endl;
   }
 
   // Task 12
   {
 
     std::vector<int> numbers;
     for (int i = 0; i < 10000; i++) {
       numbers.push_back(i);
     }
 
     numbers.erase(std::remove_if(numbers.begin(), numbers.end(),
                                  [](int n) { return n % 2 == 0; }),
                   numbers.end());
 
     std::cout << "Remaining elements: " << numbers.size() << std::endl;
   }
 
   // Task 13
   {
 
     std::vector<std::string> numbers = {"123", "456", "789", "101", "202"};
     int sum = 0;
 
     for (const auto &numStr : numbers) {
       sum += std::stoi(numStr);
     }
 
     std::cout << "Sum: " << sum << std::endl;
   }
 
   // Task 14
   {
 
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
   }
 
   // Task 15
   {
     using namespace task15;
     std::vector<int> numbers(100000, 1);
     int sum = 0;
 
     for (int i = 0; i < 10; i++) {
       sum += calculateSum(numbers);
     }
 
     std::cout << "Sum: " << sum << std::endl;
   }
 
   // Task 16
   {
     using namespace task16;
     std::vector<std::thread> threads;
     for (int i = 0; i < 8; ++i)
       threads.emplace_back(work);
     for (auto &t : threads)
       t.join();
     std::cout << counter << std::endl;
   }
 
   // Task 17
   {
 
     std::map<int, int> m;
     for (int i = 0; i < 100000; ++i) {
       m[i] = i;
     }
     long long sum = 0;
     for (int i = 0; i < 100000; ++i) {
       sum += m.count(i);
     }
     std::cout << sum << std::endl;
   }
 
   // Task 18
   {
 
     std::vector<std::string> words = {"apple", "banana", "orange", "grape",
                                       "pear"};
     std::string target = "orange";
 
     int count = 0;
     for (int i = 0; i < 100000; i++) {
       for (const auto &word : words) {
         if (word == target) {
           count++;
         }
       }
     }
 
     std::cout << "Count: " << count << std::endl;
   }
 
   // Task 19
   {
 
     std::map<std::string, int> counts;
     counts["apple"] = 5;
     counts["banana"] = 7;
     counts["orange"] = 12;
     counts["grape"] = 3;
     counts["pear"] = 9;
-
-    int total = 0;
-    for (int i = 0; i < 100000; i++) {
-      for (const auto &pair : counts) {
-        total += pair.second;
-      }
-    }
+    // cache sum of all values to avoid repeated iteration
+    int sumValues = counts["apple"] + counts["banana"] + counts["orange"] + counts["grape"] + counts["pear"];
+    int total = sumValues * 100000;
 
     std::cout << "Total: " << total << std::endl;
   }
 
   // Task 20
   {
 
     std::vector<std::string> names = {"John", "Alice", "Bob", "Carol", "Dave"};
 
     int totalLength = 0;
     for (int i = 0; i < 100000; i++) {
       for (const auto &name : names) {
         totalLength += name.length();
       }
     }
 
     std::cout << "Total length: " << totalLength << std::endl;
   }
 
   // Task 21
   {
 
+    // open file once to avoid reopening in loop
+    std::ofstream file("log.txt", std::ios_base::app);
     for (int i = 0; i < 1000; ++i) {
-      std::ofstream file("log.txt", std::ios_base::app);
       file << "Log entry " << i << "\n";
     }
   }
 
   // Task 22
   {
 
     std::vector<int> numbers(1000, 5);
 
     std::ostringstream oss;
     for (const auto &num : numbers) {
       oss << num << ",";
     }
     std::string result = oss.str();
 
     std::cout << "Result length: " << result.size() << std::endl;
   }
 
   // Task 23
   {
 
     std::list<int> l;
     std::mt19937 rng(0);
     for (int i = 0; i < 100000; ++i)
       l.push_back(rng());
 
     std::vector<int> v(l.begin(), l.end());
     std::sort(v.begin(), v.end());
     l.assign(v.begin(), v.end());
 
     std::cout << l.front() << std::endl;
   }
 
   // Task 24
   {
 
     std::vector<int> v(1000000, 1);
     long long sum = 0;
     for (size_t i = 0; i < v.size(); ++i) {
       sum += v[i];
     }
     std::cout << sum << std::endl;
   }
 
   // Task 25
   {
 
     std::string result;
     result.reserve(100000);
 
     for (int i = 0; i < 100000; i++) {
       result += ".";
     }
 
     std::cout << "Result length: " << result.length() << std::endl;
   }
 
   // Task 26
   {
     using namespace task26;
     std::unique_ptr<Base> p = std::make_unique<Derived>();
     long long sum = 0;
     for (int i = 0; i < 10000000; ++i) {
       sum += p->val(i);
     }
     std::cout << sum << std::endl;
   }
 
   // Task 27
   {
     using namespace task27;
     DataProcessor processor;
     for (int i = 0; i < 10000; i++) {
       processor.addData(i);
     }
 
     std::cout << "Sum: " << processor.sum() << std::endl;
   }
 
   // Task 28
   {
     using namespace task28;
     std::vector<Person> people;
     people.reserve(10000);
 
     for (int i = 0; i < 10000; i++) {
       people.emplace_back("Person" + std::to_string(i));
     }
 
     std::cout << "First person: " << people.front().name << std::endl;
   }
 
   // Task 29
   {
 
     double angle = 0.785;
-    double result = 0;
-    for (int i = 0; i < 1000000; ++i) {
-      result += std::sin(angle);
-    }
+    // hoist sin computation since angle is constant
+    double sinVal = std::sin(angle);
+    double result = sinVal * 1000000;
     std::cout << result << std::endl;
   }
 
   // Task 30
   {
 
     std::vector<int> data;
     for (int i = 0; i < 5; i++) {
       data.push_back(i);
     }
 
-    int sum = 0;
-    for (int i = 0; i < 1000000; i++) {
-      sum += std::accumulate(data.begin(), data.end(), 0);
-    }
+    // compute accumulation once and multiply to avoid repeated work
+    int partial = std::accumulate(data.begin(), data.end(), 0);
+    int sum = partial * 1000000;
 
     std::cout << "Sum: " << sum << std::endl;
   }
 
   // Task 31
   {
 
     std::vector<int> v(1000000);
     std::fill(v.begin(), v.end(), 42);
     std::cout << v.back() << std::endl;
   }
 
   // Task 32
   {
     using namespace task32;
     int sum = 0;
 
     for (int i = 0; i < 100000; i++) {
       std::vector<int> values = getValues();
       for (const auto &val : values) {
         sum += val;
       }
     }
 
     std::cout << "Sum: " << sum << std::endl;
   }
 
   // Task 33
   {
 
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
   }
 
   // Task 34
   {
-
+    using namespace std;
     std::set<std::string> words = {"apple", "banana", "orange", "grape",
                                    "pear"};
-
     std::string target = "orange";
-    int count = 0;
-
-    for (int i = 0; i < 1000000; i++) {
-      if (words.find(target) != words.end()) {
-        count++;
-      }
-    }
+    // cache find result to avoid repeated tree lookups
+    bool exists = (words.find(target) != words.end());
+    int count = exists ? 1000000 : 0;
 
     std::cout << "Count: " << count << std::endl;
   }
 
   // Task 35
   {
 
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
   }
 
   // Task 36
   {
 
     std::vector<int> v(100000);
     std::iota(v.begin(), v.end(), 0);
     std::priority_queue<int> pq;
     for (int x : v) {
       pq.push(x);
     }
     std::cout << pq.top() << std::endl;
   }
 
   // Task 37
   {
     using namespace task37;
     int sum = 0;
 
     for (int i = 0; i < 100; i++) {
       const LargeObject &obj = createObject();
       for (const auto &val : obj.data) {
         sum += val;
       }
     }
 
     std::cout << "Sum: " << sum << std::endl;
   }
 
   // Task 38
   {
 
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
   }
 
   // Task 39
   {
 
     std::vector<int> data(10000, 1);
     int sum = 0;
 
     for (int i = 0; i < 10000; i++) {
       if (i < data.size()) {
         sum += data[i];
       }
     }
 
     std::cout << "Sum: " << sum << std::endl;
   }
 
   // Task 40
   {
 
     unsigned x = 123456;
     unsigned long sum = 0;
     for (int i = 0; i < 1000000; ++i) {
       sum += (x + i) / 16;
       sum += (x + i) % 16;
     }
     std::cout << sum << std::endl;
   }
 
   // Task 41
   {
     using namespace task41;
     std::map<Color, std::string> colorNames = {{RED, "Red"},
                                                {GREEN, "Green"},
                                                {BLUE, "Blue"},
                                                {YELLOW, "Yellow"},
                                                {PURPLE, "Purple"}};
 
     Color c = BLUE;
     std::cout << "Color name: " << colorNames[c] << std::endl;
   }
 
   // Task 42
   {
 
     std::string s(10000, 'a');
     s[5000] = 'b';
 
-    for (size_t i = 0; i < s.length();) {
-      if (s[i] == 'a') {
-        s.erase(i, 1);
-      } else {
-        ++i;
-      }
-    }
+    // filter out 'a's in one pass to avoid costly erase operations
+    std::string filtered;
+    filtered.reserve(s.size());
+    for (char c : s) {
+      if (c != 'a') filtered.push_back(c);
+    }
+    s = std::move(filtered);
     std::cout << s << std::endl;
   }
 
   // Task 43
   {
 
     std::map<int, int> m;
     for (int i = 0; i < 10000; ++i) {
       m[i] = i * 2;
     }
     long long sum = 0;
     for (int i = 0; i < 10000; ++i) {
       sum += m[i];
     }
     std::cout << sum << std::endl;
   }
 
   // Task 44
   {
 
     const int size = 10000;
     std::vector<std::vector<int>> matrix(size, std::vector<int>(size, 1));
     long sum = 0;
 
-    for (int col = 0; col < size; ++col) {
-      for (int row = 0; row < size; ++row) {
+    // iterate row-major to improve cache performance
+    for (int row = 0; row < size; ++row) {
+      for (int col = 0; col < size; ++col) {
         sum += matrix[row][col];
       }
     }
-
     std::cout << "Sum: " << sum << std::endl;
   }
 
   // Task 45
   {
     using namespace task45;
     const int size = 10000000;
     std::vector<int> numbers(size, 5);
     std::vector<int> results(size);
 
     int (*func)(int) = transform;
 
     for (int i = 0; i < size; ++i) {
       results[i] = func(numbers[i]);
     }
 
     std::cout << "Result sample: " << results[1000] << std::endl;
   }
 
   // Task 46
   {
-
+    // reserve and push_back then reverse to avoid O(n^2) inserts
     std::vector<int> v;
+    v.reserve(10000);
     for (int i = 0; i < 10000; ++i) {
-      v.insert(v.begin(), i);
-    }
+      v.push_back(i);
+    }
+    std::reverse(v.begin(), v.end());
     std::cout << v.front() << std::endl;
   }
 
   // Task 47
   {
 
     std::vector<int> sortedData(10000);
     for (int i = 0; i < sortedData.size(); ++i) {
       sortedData[i] = i * 2;
     }
 
     int target = 19998;
     bool found =
         std::binary_search(sortedData.begin(), sortedData.end(), target);
 
     std::cout << "Found: " << std::boolalpha << found << std::endl;
   }
 
   // Task 48
   {
 
     std::vector<std::string> emails = {"user@example.com",
                                        "john.doe@company.org", "invalid-email",
                                        "another@email.co.uk"};
 
     std::regex emailRegex(R"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})");
 
     int validCount = 0;
     for (const auto &email : emails) {
       if (std::regex_match(email, emailRegex)) {
         validCount++;
       }
     }
 
     std::cout << "Valid emails: " << validCount << std::endl;
   }
 
   // Task 49
   {
 
     std::vector<std::any> values;
 
     for (int i = 0; i < 1000; ++i) {
       values.push_back(std::any(i));
     }
 
     int sum = 0;
     for (const auto &value : values) {
       sum += std::any_cast<int>(value);
     }
 
     std::cout << "Sum: " << sum << std::endl;
   }
 
   // Task 50
   {
     using namespace task50;
     unsigned int n = 40;
     unsigned long long result = fibonacci(n);
     std::cout << "Fibonacci(" << n << ") = " << result << std::endl;
   }
 }
 
```

</details>

</blockquote>

