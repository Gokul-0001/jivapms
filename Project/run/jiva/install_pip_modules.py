import subprocess, sys

def extract_modules(requirements_file):
    modules = []
    with open(requirements_file, 'r') as file:
        for line in file:
            # Remove comments and strip whitespace
            line = line.strip()
            if line and not line.startswith('#'):
                # Extract module name by splitting at the first '==' or any versioning symbols
                module_name = line.split('==')[0]
                modules.append(module_name)
    return modules

def install_modules(modules):
    for module in modules:
        print(f"Installing {module}...")
        subprocess.run([sys.executable, "-m", "pip", "install", module])

def main():
    requirements_file = 'requirements.txt'  # Modify this if your file has a different name
    modules = extract_modules(requirements_file)
    install_modules(modules)

if __name__ == "__main__":
    main()
