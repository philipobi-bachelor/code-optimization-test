---
Source: https://chatgpt.com/c/68695aeb-bfe8-8008-8e9b-2b31ad4355c4
Model: o4-mini
Exported with: https://github.com/pionxzh/chatgpt-exporter
---

# C++ Inefficiency Examples

#### You:
Please help me to compose an AI prompt which should produce 20 examples of common C++ mistakes that significant inefficiencies. For each example I need two compilable snippets of code with includes and main function, one for the inefficient version and one with the inefficiency removed as well as a short description of the cause of the inefficiency. Both should perform the same general task, i.e. have the same outcome / output. Also, it is important that the code will not be optimized away. To avoid this, it might be useful for the result of the operations to be printed

#### ChatGPT:
\[Unsupported Content]


#### ChatGPT:
\[Unsupported Content]


#### ChatGPT:
Here’s a ready-to-use meta‑prompt you can feed into an LLM to get exactly what you asked for. You can tweak wording or formatting to match the style of your target model, but this covers all requirements:

````
You are an expert C++ developer and technical writer. Your task is to generate **20 distinct examples** of common C++ coding mistakes that introduce **significant inefficiencies**. For each example, output the following, in order:

1. **A title** on its own line, e.g.  
   `Example 1: Inefficient String Concatenation with std::string`

2. **Inefficient version** – a complete, compilable C++17 snippet (including `#include` directives and `int main()`), using only the standard library, that demonstrates the inefficiency. Make sure it **prints** its result to `stdout` so the compiler cannot optimize it away. Wrap it in a fenced code block tagged `cpp`:
   ```cpp
   // inefficient version
   #include <…>
   int main() {
       …
       std::cout << result << std::endl;
       return 0;
   }
````

3. **Efficient version** – another complete, compilable C++17 snippet that performs exactly the same task and produces the same output, but with the inefficiency removed. Also print its result:
   ```cpp
   // efficient version
   #include <…>
   int main() {
       …
       std::cout << result << std::endl;
       return 0;
   }
   ```

4. **Description:** One or two sentences explaining **why** the first version is inefficient (e.g. “Because it performs repeated reallocations” or “Because it uses O(n²) instead of O(n)”) and **how** the second version fixes it.

Additional requirements:

- Each pair must demonstrate **the same observable behavior** (same output).
- Use realistic but minimal examples.
- Cover 20 *different* inefficiencies (e.g. unnecessary copies, wrong container choice, unbounded recursion, missing `reserve()`, expensive virtual calls in hot loops, etc.).
- Label each section clearly and consistently.
- Do **not** use any third‑party libraries.
- All examples should compile under `g++ -std=c++17`.

Please produce the entire set of 20 examples in one response, numbered 1 through 20.

```

**How to use:** Paste this prompt into your LLM interface. It will then emit 20 examples, each with two compilable snippets and a short description of the inefficiency and its fix.

```
