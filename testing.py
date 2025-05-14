from pnv3.client.lib.xtract import escape, parse

input_text = """<title>hello world</title>
<body>
        <green>
                _____ _____ _____ ___  
                |  _  |   | |  |  |_  | 
                |   __| | | |  |  |_  | 
                |__|  |_|___|\\___/|___|</>
                        
                        PNV3
    A continuation of the original PyNet v3 project.

            You are running client \033[35mv{__version__}\033[0m.
        Press \033[34m[C]\033[0m to connect, \033[34m[C+X]\033[0m to exit.
</body>
"""

title, wrapped = parse(input_text, 180)
print("[Title]", title)
print("[Wrapped]", wrapped)
print("[Escaped]", escape(wrapped))

print("\n", "===", "RAW WRAP RESULT", "=" * 50, "\n")
print("\n".join(wrapped))
print("\n", "===", "RAW ESCAPE RESULT", "=" * 48, "\n")
print("\n".join(escape(wrapped)))
