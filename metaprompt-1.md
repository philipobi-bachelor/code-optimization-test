---
Source: https://chatgpt.com/c/68646f4d-2fd0-8008-8a44-7a2c37174430
Model: o4-mini
Exported with: https://github.com/pionxzh/chatgpt-exporter
---

# Inefficient C++ Code Prompts

#### You:
How to structure an AI prompt that should generate around 100 examples of inefficient C++ code which should be used as exercises for students to find and fix the cause of the inefficiency

#### ChatGPT:
\[Unsupported Content]


#### ChatGPT:
\[Unsupported Content]


#### ChatGPT:
When you ask an LLM to generate a large batch (∼100) of “inefficient‐by‐design” C++ snippets, you want your prompt to be crystal­clear about:

1. **Scope & purpose** – students will identify and fix the inefficiency.
2. **Output format** – numbered list, each with code + brief description of what to look for.
3. **Variety & categories** – cover different inefficiency types (algorithms, data structures, language‑idioms, memory, I/O, etc.).
4. **Self‑containment** – each example is complete enough to compile, but clearly sub‑optimal.
5. **Meta data** – tag each snippet with the kind of inefficiency so instructors can group them.

---

### Prompt Outline

```text
You are a teaching assistant for a C++ programming course.  
Your task is to produce **100** standalone C++ code examples that are intentionally inefficient.  
Each example should be used as an exercise for students to **find and fix** the inefficiency.

**Requirements:**  
1. **Numbered list** from 1 to 100.  
2. **For each item**:  
   - A short **title** indicating the inefficiency type (e.g. “O(n²) algorithm”, “Unnecessary deep copy”, “Excessive I/O flush”).  
   - A **complete C++ snippet** (include `#include` and a `main()` if needed) that **compiles** but runs or uses resources poorly.  
   - A **1–2 sentence description** of *what* to look for (but do NOT reveal the fix).  
3. **Cover at least these categories** (and feel free to invent more):  
   - **Algorithmic** (quadratic vs. linear, naive recursion)  
   - **Data structures** (inefficient container choice, lack of reserve on vectors)  
   - **Memory** (unnecessary copies, misuse of pointers, not using move semantics)  
   - **I/O** (using `endl` inside loops, unbuffered I/O)  
   - **Language‑idioms** (manual loops instead of `std::transform`, C‑style casts)  
   - **Concurrency** (locking too often, false sharing)  
4. **Keep each snippet under 20 lines.**  
5. **Do not provide the solution**; students will analyze and refactor later.

**Example item** (but DO NOT generate just this one; it’s illustrative):

```

1. \[O(n²) loop]
   \#include <iostream>
   \#include <vector>
   int main() {
   std::vector<int> v;
   for (int i = 0; i < 10000; ++i)
   v.push\_back(i);
   int sum = 0;
   for (int i = 0; i < v.size(); ++i)
   for (int j = 0; j < v.size(); ++j)
   sum += v\[j];
   std::cout << sum << std::endl;
   return 0;
   }
   // Description: Nested loops over the same container cause O(n²) complexity.

````

---

### Full Prompt You Can Send to the AI

```text
You are a C++ teaching assistant.  
Generate **100** distinct, self‐contained C++ code examples that are intentionally inefficient.  
Students will use these as exercises to find and fix the inefficiencies—but do NOT include the fixes.

**Output format:**  
1. Number each example (1–100).  
2. Each example must have:
   - A short title in brackets indicating the inefficiency type.
   - A complete C++ snippet (with necessary includes and `main()` if needed).
   - A one‐sentence hint describing what is inefficient (no fix described).

**Constraints:**  
- Maximum 20 lines of code per snippet.  
- Cover these categories (and feel free to add more):
  1. Algorithmic complexity (e.g. O(n²) vs. O(n)).
  2. Data‐structure misuse (e.g. using list where vector is better).
  3. Memory inefficiency (e.g. unnecessary copies, missing move semantics).
  4. I/O inefficiency (e.g. flushing streams inside loops).
  5. Language‐idiom pitfalls (e.g. manual loops vs. standard algorithms).
  6. Concurrency mistakes (e.g. locking granularity issues).
- Do NOT reveal the solution.

Begin now.  
````

With a prompt like this, the AI will understand exactly how to format each exercise, what range of inefficiencies to include, and how to keep the output consistent and student‑friendly.
