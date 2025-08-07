Your task is to generate **50 distinct examples** of common C++ coding mistakes that introduce **significant inefficiencies**. For each example, output the following:

1. **A short title** on its own line, e.g. `Example 1: Inefficient String Concatenation`

2. **Inefficient version** – a complete, compilable C++17 snippet (including `#include` directives and `int main()`), using only the standard library, that demonstrates the inefficiency. The code should:
   - Perform a realistic task of moderate complexity
   - Include enough work that performance differences are measurable
   - Print its final result to `stdout` so that it is not optimized away by the compiler
   
   ```cpp
   #include <…>
   int main() {
       …
       std::cout << result << std::endl;
       return 0;
   }
   ```

3. **Efficient version** – another complete, compilable C++17 snippet that performs exactly the same task and produces the same output, but with the inefficiency removed:
    ```cpp
    #include <…>
    int main() {
        …
        std::cout << result << std::endl;
        return 0;
    }
    ```

4. **Description**: One or two sentences explaining why the first version is inefficient (e.g. “Because it performs repeated reallocations” or “Because it uses O(n²) instead of O(n)”) and how the second version fixes it.

Ensure examples cover these categories with at least 3-5 examples from each:
- Container selection and usage (std::vector vs std::list vs std::map, etc.)
- Memory management (allocation patterns, move semantics, etc.)
- Algorithm complexity (using appropriate STL algorithms)
- String handling operations
- I/O and file operations
- Concurrency patterns
- Class design and inheritance
- Lambda usage and capture
- Template metaprogramming inefficiencies
- Modern C++17 feature usage

Additional requirements:
- Use realistic variable names and scenarios that mimic actual programming situations
- Incorporate non-trivial computations that resist compiler optimization
- Where appropriate, use realistic data sizes (e.g., processing 10000+ elements)

Before submitting your response, verify that each example differs significantly from the others and avoids duplicating common textbook examples.
