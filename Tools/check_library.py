import sys

def check_libraries():
    required_libs = ['numpy', 'pyopenms']
    missing = []
    
    for lib in required_libs:
        try:
            __import__(lib)
            print(f"{lib} is installed")
        except ImportError:
            missing.append(lib)
            print(f"{lib} is missing")
    
    if missing:
        print(f"Missing libraries: {', '.join(missing)}")
        sys.exit(1)
    else:
        print("All required libraries are installed.")

if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    check_libraries()