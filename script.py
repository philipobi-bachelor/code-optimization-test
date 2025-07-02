import re

def findMainBody(code:str) -> str:
    funcStart = code.find("int main")
    if funcStart < 0: return ""
    else: subs = code[funcStart:]
    
    bodyStart = funcStart
    bodyEnd = funcStart
    depth = 0
    for char in subs:
        if depth == 0: bodyStart += 1
        
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0: break
        
        bodyEnd += 1
    
    return {
        "funcStart" : funcStart,
        "funcEnd" : bodyEnd + 1,
        "bodyStart" : bodyStart,
        "bodyEnd" : bodyEnd
    }


#file structure
"""
1.  **Title**: ...
````cpp
...
````
**Fix**: ...
````cpp
...
````

2.  **Title**: ...
````cpp
...
````
**Fix**: ...
````cpp
...
````
"""   
exampleRegex = re.compile(
    r"\d+\.\s*\*\*Title\*\*:\s*(?P<title>[^\n]*)\s*"
    r"````cpp\s*(?P<code1>[^`]*)````\s*"
    r"\*\*Fix\*\*:\s*(?P<fixDescription>[^\n]*)\s*"
    r"````cpp\s*(?P<code2>[^`]*)````\s*"
)

commentRegex = re.compile(r"\/\/[^\n]*")
stripComments = lambda s : commentRegex.sub("", s)

includeRegex = re.compile(r"(#include[^\n]*)")  

if __name__ == "__main__":
    with open("generation.md", "r") as f:
        buffer = f.read()
    
    res = exampleRegex.finditer(buffer)
    print(len(list(res)))
