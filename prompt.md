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
