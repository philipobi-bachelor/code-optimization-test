Document ID: `chat-logs/1764948`

<blockquote>

#### philipobi:
I have been using the following prompt to get a LLM to generate examples of common C++ coding mistages for me:

---

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

---

However, I have had mixed results with the generated examples. There have been examples which perform virtually the same task even though I asked for distinct examples. Also, a lot of the examples are too simple, e.g. there is a loop adding one to a sum variable for each iteration. The examples are to be used in a test and should therefore perform a little more complicated operations which are also not that easy to be optimized away by the compiler. How can I modify my prompt to achieve better results?

</blockquote>

<blockquote>

#### GitHub Copilot (claude-3.7-sonnet-thought):

# Improving Your C++ Inefficiency Examples Prompt

Your current prompt has good structure but needs refinement to generate more distinct, complex, and realistic examples. Here's how I'd modify it:

```markdown
Your task is to generate **50 distinct examples** of common C++ coding mistakes that introduce **significant inefficiencies**. For each example, output the following:

1. **A title** on its own line, e.g. `Example 1: Inefficient String Concatenation with std::string`

2. **Inefficient version** – a complete, compilable C++17 snippet (including `#include` directives and `int main()`), using only the standard library, that demonstrates the inefficiency. The code should:
   - Perform a realistic task of moderate complexity
   - Include enough work that performance differences are measurable
   - Contain input variables that cannot be optimized away at compile-time
   - Print its result to `stdout`
   
   ```cpp
   // inefficient version
   #include <…>
   int main() {
       …
       std::cout << result << std::endl;
       return 0;
   }
   ```

3. **Efficient version** – another complete, compilable C++17 snippet that performs exactly the same task and produces the same output, but with the inefficiency removed:
    ```cpp
    // efficient version
    #include <…>
    int main() {
        …
        std::cout << result << std::endl;
        return 0;
    }
    ```

4. **Description**: Explain why the first version is inefficient, including:
   - The performance complexity difference (e.g., O(n²) vs O(n))
   - Approximate performance impact (e.g., "5-10x slower for large inputs")
   - Why modern compilers might struggle to optimize this automatically

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
- Each example should be significantly different from others
- Include at least one example where the performance difference is 100x or greater

Please produce the entire set of 50 examples in one response, numbered 1 through 50.
```

This revised prompt should help you get:
1. More distinct examples across different categories
2. More complex operations that better represent real code
3. Examples that aren't easily optimized away
4. Clear explanations of performance impacts

Would you like me to suggest any further modifications to focus on specific aspects of C++ inefficiencies?

`(38.527 s)`

</blockquote>

<blockquote>

#### philipobi:
I tried my old prompt with different models and they all generated very similar examples, it seems that they are drawing from some set of examples in their training data. How can I get them to try and generate something different / unique?

</blockquote>

<blockquote>

#### GitHub Copilot (claude-3.7-sonnet-thought):

# Encouraging More Unique C++ Inefficiency Examples

You've identified a common issue with LLMs - they tend to reproduce similar examples from their training data. Here's how to modify your prompt to encourage more creative, unique examples:

```markdown
Your task is to generate **50 unique C++ inefficiency examples** that go beyond common textbook cases. I've already seen the standard examples (string concatenation in loops, missing vector::reserve(), using endl vs '\n', etc.), so please be creative.

For each example, provide:

1. **A title** that clearly describes the inefficiency

2. **Inefficient version**: A complete, compilable C++17 snippet that:
   - Demonstrates a non-obvious inefficiency pattern
   - Uses realistic, complex operations (not just trivial loops)
   - Incorporates randomized or user input values to prevent compile-time optimization
   - Includes sufficient computation to make performance impact measurable

3. **Efficient version**: The optimized equivalent with the same observable behavior

4. **Description**: Explain the inefficiency, why it's not obvious, and why compilers struggle to optimize it automatically

**Uniqueness requirements:**
- Create examples that combine multiple subtle inefficiencies
- Focus on less-discussed C++17 features (fold expressions, if constexpr, etc.)
- Include inefficiencies from specialized domains (graphics processing, networking, etc.)
- Demonstrate inefficiencies that only manifest under specific conditions
- Showcase counter-intuitive cases where the "obvious" optimization is actually worse
- Include at least 5 examples where a well-intentioned programmer following best practices might still introduce the inefficiency
- Demonstrate at least 8 inefficiency patterns not commonly discussed in C++ optimization articles

**Application domains to draw from:**
- Text processing beyond simple string manipulation
- Data serialization/deserialization
- Multi-threading communication patterns
- Complex data structure operations
- Numerical computation
- Resource management in exception-safe code
- Generic programming with templates
- Compile-time vs runtime computation tradeoffs

Before submitting your response, verify that each example differs significantly from the others and avoids duplicating common textbook examples.
```

This approach:

1. Explicitly asks for unique examples beyond what's commonly found in training data
2. Forces consideration of specialized domains and complex scenarios
3. Requires examples to incorporate features that make them harder to optimize away
4. Asks for counter-intuitive cases that break from conventional wisdom
5. Specifies diverse application domains to draw inspiration from

Would you like me to suggest any additional strategies to encourage uniqueness in the generated examples?

`(37.485 s)`

</blockquote>

