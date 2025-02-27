import os
import re
import pandas as pd

def count_loc(file_path):
    with open(file_path, 'r') as file:
        code = file.readlines()
    loc = 0
    for line in code:
        if line.strip() and not line.strip().startswith('//') and not line.strip().startswith('/*'):
            loc += 1
    return loc

def count_method_invocations(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    methods_invoked = len(re.findall(r'\b\w+\(.*\)\s*;', code))  # Simple method invocation pattern
    return methods_invoked

def count_coupling(file_path, class_name):
    with open(file_path, 'r') as file:
        code = file.read()
    dependencies = re.findall(r'\b\w+\s+\w+\s*=\s*new\s+(\w+)\(', code)  # Detect class instantiation
    method_calls = re.findall(r'\b\w+\.(\w+)\(', code)  # Method calls to other classes
    combined_dependencies = dependencies + method_calls
    combined_dependencies = list(set(combined_dependencies))  # Remove duplicates
    combined_dependencies = [dep for dep in combined_dependencies if dep != class_name]
    return len(combined_dependencies)

def count_complexity(file_path):
    complexity = 0
    with open(file_path, 'r') as file:
        code = file.read()
    complexity += len(re.findall(r'\b(if|for|while|switch)\b', code))
    return complexity

def count_fan_in_out(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    fan_out = len(re.findall(r'\b\w+\.(\w+)\(', code))  # Method calls to other classes
    fan_in = len(re.findall(r'\b' + re.escape(file_path.split("/")[-1].split(".")[0]) + r'\.([A-Za-z0-9_]+)\(', code))
    return fan_in, fan_out

def count_loops_and_comparisons(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    loops = len(re.findall(r'\b(for|while|foreach)\b', code))
    comparisons = len(re.findall(r'\b(if|else|switch|case)\b', code))
    return loops, comparisons

def count_assignments_and_math_operations(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    assignments = len(re.findall(r'\b\w+\s*=\s*', code))  # Basic assignment pattern
    math_operations = len(re.findall(r'\+|-|\*|/|\%', code))  # Simple math operations
    return assignments, math_operations

def count_return_statements(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return len(re.findall(r'\breturn\b', code))

def count_variables(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return len(re.findall(r'\b\w+\s+\w+\s*;', code))

def count_methods(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return len(re.findall(r'\b\w+\s+\w+\s*\(.*\)\s*{', code))

def count_classes(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return len(re.findall(r'\bclass\s+\w+', code))

def count_comments(file_path):
    with open(file_path, 'r') as file:
        code = file.readlines()
    comment_lines = 0
    in_comment_block = False
    for line in code:
        if in_comment_block:
            comment_lines += 1
            if '*/' in line:
                in_comment_block = False
        elif '/*' in line:
            in_comment_block = True
            comment_lines += 1
        elif '//' in line:
            comment_lines += 1
    return comment_lines

def count_strings(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return len(re.findall(r'"([^"]*)"', code))

def count_numeric_literals(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return len(re.findall(r'\b\d+(\.\d+)?\b', code))

def count_method_parameters(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return len(re.findall(r'\b\w+\s+\w+\s*[,)]', code))

def count_anonymous_classes(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return len(re.findall(r'\bnew\s+(\w+)\s*\{', code))

def count_lambdas(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return len(re.findall(r'\(\w+\)\s*=>', code))

def count_inner_classes(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return len(re.findall(r'\bclass\s+\w+\s*{', code))

def analyze_csharp_project(directory):
    data = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.cs'):  # Process only C# files
                file_path = os.path.join(root, file)
                class_name = file.split('.')[0]  # Assume class name is the same as the file name
                
                loc = count_loc(file_path)
                methods_invoked = count_method_invocations(file_path)
                cbo = count_coupling(file_path, class_name)
                wmc = count_complexity(file_path)
                fan_in, fan_out = count_fan_in_out(file_path)
                loops, comparisons = count_loops_and_comparisons(file_path)
                assignments, math_operations = count_assignments_and_math_operations(file_path)
                return_statements = count_return_statements(file_path)
                variables = count_variables(file_path)
                methods = count_methods(file_path)
                classes = count_classes(file_path)
                comments = count_comments(file_path)
                strings = count_strings(file_path)
                numeric_literals = count_numeric_literals(file_path)
                method_params = count_method_parameters(file_path)
                anonymous_classes = count_anonymous_classes(file_path)
                lambdas = count_lambdas(file_path)
                inner_classes = count_inner_classes(file_path)

                data.append({
                    'File Name': file,
                    'LOC': loc,
                    'Methods Invoked': methods_invoked,
                    'CBO': cbo,
                    'WMC': wmc,
                    'Fan-In': fan_in,
                    'Fan-Out': fan_out,
                    'Loops': loops,
                    'Comparisons': comparisons,
                    'Assignments': assignments,
                    'Math Operations': math_operations,
                    'Return Statements': return_statements,
                    'Variables': variables,
                    'Methods': methods,
                    'Classes': classes,
                    'Comments': comments,
                    'Strings': strings,
                    'Numeric Literals': numeric_literals,
                    'Method Parameters': method_params,
                    'Anonymous Classes': anonymous_classes,
                    'Lambdas': lambdas,
                    'Inner Classes': inner_classes
                })
    
    df = pd.DataFrame(data)

    total_row = df.sum(numeric_only=True)
    total_row['File Name'] = 'Total'
    df = pd.concat([df, total_row.to_frame().T], ignore_index=True)
    return df

project_directory = '/Users/suraviakhter/Documents/event-management-system-main'
metrics_df = analyze_csharp_project(project_directory)

metrics_df.to_csv('csharp_project_metrics.csv', index=False)

print(metrics_df)
