#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <deque>
#include <fstream>
#include <functional>
#include <iomanip>
#include <iostream>
#include <list>
#include <map>
#include <memory>
#include <numeric>
#include <queue>
#include <random>
#include <regex>
#include <sstream>
#include <string>
#include <thread>
#include <unordered_map>
#include <unordered_set>
#include <vector>

namespace task4 {
std::vector<int> createAndProcess(std::vector<int> data) {
  for (int i = 0; i < 1000; i++) {
    data.push_back(i);
  }
  return data;
}
} // namespace task4

namespace task6 {
void use_ptr(std::shared_ptr<int> p, int &counter) {
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

namespace task15 {
int calculateSum(std::vector<int> values) {
  return std::accumulate(values.begin(), values.end(), 0);
}
} // namespace task15

namespace task16 {
std::atomic<long long> counter{0};

void work() {
  for (int i = 0; i < 1000000; ++i) {
    counter++;
  }
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
  std::vector<int> data;

public:
  DataProcessor() {}

  void addData(int value) { data.push_back(value); }

  int sum() const {
    int total = 0;
    for (const auto &val : data) {
      total += val;
    }
    return total;
  }
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

LargeObject createObject() {
  LargeObject obj(10000);
  return obj;
}
} // namespace task37

namespace task41 {
enum Color { RED, GREEN, BLUE, YELLOW, PURPLE, COLOR_COUNT };
}

namespace task45 {
int transform(int x) { return x * x + 1; }
} // namespace task45

namespace task50 {
unsigned long long fibonacci(unsigned int n) {
  if (n <= 1)
    return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}
} // namespace task50

int main() {
  // Task 1
  {

    std::string result;
    for (int i = 0; i < 10000; i++) {
      result = result + std::to_string(i) + " ";
    }
    std::cout << result.substr(0, 20) << "..." << std::endl;
  }

  // Task 2
  {

    std::vector<int> numbers;
    for (int i = 0; i < 100000; i++) {
      numbers.push_back(i);
    }
    std::cout << "Size: " << numbers.size() << std::endl;
  }

  // Task 3
  {

    std::ofstream devnull("/dev/null");
    for (int i = 0; i < 10000; i++) {
      devnull << "Number: " << i << std::endl;
    }
    devnull << "Done" << std::endl;
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
    std::string name = "John";

    for (int i = 0; i < 1000; i++) {
      people.emplace_back(name + std::to_string(i), i);
    }

    std::cout << "People: " << people.size() << std::endl;
  }

  // Task 8
  {

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
  }

  // Task 9
  {

    std::vector<int> numbers;
    for (int i = 10000; i > 0; i--) {
      numbers.push_back(i);
    }

    std::sort(numbers.begin(), numbers.end());

    std::cout << "First: " << numbers.front() << ", Last: " << numbers.back()
              << std::endl;
  }

  // Task 10
  {

    std::ofstream("test.txt") << std::string(100000, 'x');
    std::ifstream file("test.txt");
    char c;
    long count = 0;
    while (file.get(c)) {
      count++;
    }
    std::cout << "Read " << count << " chars." << std::endl;
  }

  // Task 11
  {

    long long result = 0;
    for (int i = 0; i < 20; ++i) {
      result += std::pow(2, i);
    }
    std::cout << result << std::endl;
  }

  // Task 12
  {

    std::vector<int> numbers;
    for (int i = 0; i < 10000; i++) {
      numbers.push_back(i);
    }

    for (size_t i = 0; i < numbers.size(); i++) {
      if (numbers[i] % 2 == 0) {
        numbers.erase(numbers.begin() + i);
      }
    }

    std::cout << "Remaining elements: " << numbers.size() << std::endl;
  }

  // Task 13
  {

    std::vector<std::string> numbers = {"123", "456", "789", "101", "202"};
    int sum = 0;

    for (const auto &numStr : numbers) {
      std::stringstream ss(numStr);
      int num;
      ss >> num;
      sum += num;
    }

    std::cout << "Sum: " << sum << std::endl;
  }

  // Task 14
  {

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

    std::unordered_map<int, int> m;
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
        std::string temp = word;
        if (temp == target) {
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

    int total = 0;
    for (int i = 0; i < 100000; i++) {
      for (const auto &key : {"apple", "banana", "orange", "grape", "pear"}) {
        total += counts[key];
      }
    }

    std::cout << "Total: " << total << std::endl;
  }

  // Task 20
  {

    std::vector<std::string> names = {"John", "Alice", "Bob", "Carol", "Dave"};

    int totalLength = 0;
    for (int i = 0; i < 100000; i++) {
      for (auto name : names) {
        totalLength += name.length();
      }
    }

    std::cout << "Total length: " << totalLength << std::endl;
  }

  // Task 21
  {

    std::ofstream file("log.txt", std::ios_base::app);
    for (int i = 0; i < 1000; ++i) {
      file << "Log entry " << i << "\n";
    }
  }

  // Task 22
  {

    std::vector<int> numbers(1000, 5);

    std::string result = std::accumulate(
        numbers.begin(), numbers.end(), std::string(""),
        [](std::string a, int b) { return a + std::to_string(b) + ","; });

    std::cout << "Result length: " << result.size() << std::endl;
  }

  // Task 23
  {

    std::list<int> l;
    std::mt19937 rng(0);
    for (int i = 0; i < 100000; ++i)
      l.push_back(rng());

    l.sort();

    std::cout << l.front() << std::endl;
  }

  // Task 24
  {

    std::vector<int> v(1000000, 1);
    long long sum = std::accumulate(v.begin(), v.end(), 0LL);
    std::cout << sum << std::endl;
  }

  // Task 25
  {

    std::string result;

    for (int i = 0; i < 100000; i++) {
      result = result + ".";
    }

    std::cout << "Result length: " << result.length() << std::endl;
  }

  // Task 26
  {
    using namespace task26;
    std::unique_ptr<Derived> p = std::make_unique<Derived>();
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

    for (int i = 0; i < 10000; i++) {
      std::string name = "Person" + std::to_string(i);
      people.push_back(Person(name));
    }

    std::cout << "First person: " << people.front().name << std::endl;
  }

  // Task 29
  {

    double angle = 0.785;
    double result = 0;
    const double sin_val = std::sin(angle);
    for (int i = 0; i < 1000000; ++i) {
      result += sin_val;
    }
    std::cout << result << std::endl;
  }

  // Task 30
  {

    std::array<int, 5> data = {0, 1, 2, 3, 4};

    int sum = 0;
    for (int i = 0; i < 1000000; i++) {
      sum += std::accumulate(data.begin(), data.end(), 0);
    }

    std::cout << "Sum: " << sum << std::endl;
  }

  // Task 31
  {

    std::vector<int> v(1000000);
    for (size_t i = 0; i < v.size(); ++i) {
      v[i] = 42;
    }
    std::cout << v.back() << std::endl;
  }

  // Task 32
  {
    using namespace task32;
    int sum = 0;

    std::vector<int> values = getValues();
    for (int i = 0; i < 100000; i++) {
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

    for (int i = 0; i < 100000; i++) {
      std::ostringstream oss;
      oss << std::fixed << std::setprecision(4) << value;
      result = oss.str();
    }

    std::cout << "Result: " << result << std::endl;
  }

  // Task 34
  {

    std::unordered_set<std::string> words = {"apple", "banana", "orange",
                                             "grape", "pear"};

    std::string target = "orange";
    int count = 0;

    for (int i = 0; i < 1000000; i++) {
      if (words.find(target) != words.end()) {
        count++;
      }
    }

    std::cout << "Count: " << count << std::endl;
  }

  // Task 35
  {

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
  }

  // Task 36
  {

    std::vector<int> v(100000);
    std::iota(v.begin(), v.end(), 0);

    std::priority_queue<int> pq(v.begin(), v.end());
    std::cout << pq.top() << std::endl;
  }

  // Task 37
  {
    using namespace task37;
    int sum = 0;

    for (int i = 0; i < 100; i++) {
      LargeObject obj = createObject();
      for (const auto &val : obj.data) {
        sum += val;
      }
    }

    std::cout << "Sum: " << sum << std::endl;
  }

  // Task 38
  {

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
  }

  // Task 39
  {

    std::vector<int> data(10000, 1);
    int sum = 0;

    for (int i = 0; i < data.size(); i++) {
      sum += data[i];
    }

    std::cout << "Sum: " << sum << std::endl;
  }

  // Task 40
  {

    unsigned x = 123456;
    unsigned long sum = 0;
    for (int i = 0; i < 1000000; ++i) {
      sum += (x + i) >> 4;
      sum += (x + i) & 15;
    }
    std::cout << sum << std::endl;
  }

  // Task 41
  {
    using namespace task41;
    std::array<std::string, COLOR_COUNT> colorNames = {"Red", "Green", "Blue",
                                                       "Yellow", "Purple"};

    Color c = BLUE;
    std::cout << "Color name: " << colorNames[c] << std::endl;
  }

  // Task 42
  {

    std::string s(10000, 'a');
    s[5000] = 'b';
    s.erase(std::remove(s.begin(), s.end(), 'a'), s.end());
    std::cout << s << std::endl;
  }

  // Task 43
  {

    std::vector<int> v(10000);
    for (int i = 0; i < 10000; ++i) {
      v[i] = i * 2;
    }
    long long sum = 0;
    for (int i = 0; i < 10000; ++i) {
      sum += v[i];
    }
    std::cout << sum << std::endl;
  }

  // Task 44
  {

    const int size = 10000;
    std::vector<std::vector<int>> matrix(size, std::vector<int>(size, 1));
    long sum = 0;

    for (int row = 0; row < size; ++row) {
      for (int col = 0; col < size; ++col) {
        sum += matrix[row][col];
      }
    }

    std::cout << "Sum: " << sum << std::endl;
  }

  // Task 45
  {
    using namespace task45;
    const int size = 10000000;
    std::vector<int> numbers(size, 5);
    std::vector<int> results(size);

    std::function<int(int)> func = transform;

    for (int i = 0; i < size; ++i) {
      results[i] = func(numbers[i]);
    }

    std::cout << "Result sample: " << results[1000] << std::endl;
  }

  // Task 46
  {

    std::deque<int> d;
    for (int i = 0; i < 10000; ++i) {
      d.push_front(i);
    }
    std::cout << d.front() << std::endl;
  }

  // Task 47
  {

    std::vector<int> sortedData(10000);
    for (int i = 0; i < sortedData.size(); ++i) {
      sortedData[i] = i * 2;
    }

    int target = 19998;
    bool found = false;
    for (int num : sortedData) {
      if (num == target) {
        found = true;
        break;
      }
    }

    std::cout << "Found: " << std::boolalpha << found << std::endl;
  }

  // Task 48
  {

    std::vector<std::string> emails = {"user@example.com",
                                       "john.doe@company.org", "invalid-email",
                                       "another@email.co.uk"};

    int validCount = 0;

    for (const auto &email : emails) {

      std::regex emailRegex(
          R"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})");
      if (std::regex_match(email, emailRegex)) {
        validCount++;
      }
    }

    std::cout << "Valid emails: " << validCount << std::endl;
  }

  // Task 49
  {

    std::vector<int> values;

    for (int i = 0; i < 1000; ++i) {
      values.push_back(i);
    }

    int sum = 0;
    for (const auto &value : values) {
      sum += value;
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
