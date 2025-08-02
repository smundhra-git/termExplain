#!/usr/bin/env python3
"""
Test file for termExplain - generates various common errors
"""

import sys
import os

def test_import_error():
    """Test ModuleNotFoundError"""
    print("Testing ModuleNotFoundError...")
    try:
        import nonexistent_module
    except ImportError as e:
        print(f"Error: {e}")
        return str(e)

def test_syntax_error():
    """Test SyntaxError"""
    print("Testing SyntaxError...")
    try:
        exec("print('Hello' + )")
    except SyntaxError as e:
        print(f"Error: {e}")
        return str(e)

def test_name_error():
    """Test NameError"""
    print("Testing NameError...")
    try:
        print(undefined_variable)
    except NameError as e:
        print(f"Error: {e}")
        return str(e)

def test_type_error():
    """Test TypeError"""
    print("Testing TypeError...")
    try:
        result = "hello" + 123
    except TypeError as e:
        print(f"Error: {e}")
        return str(e)

def test_file_not_found():
    """Test FileNotFoundError"""
    print("Testing FileNotFoundError...")
    try:
        with open("nonexistent_file.txt", "r") as f:
            content = f.read()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return str(e)

def test_permission_error():
    """Test PermissionError"""
    print("Testing PermissionError...")
    try:
        # Try to write to a protected directory
        with open("/etc/test_file.txt", "w") as f:
            f.write("test")
    except PermissionError as e:
        print(f"Error: {e}")
        return str(e)

def test_attribute_error():
    """Test AttributeError"""
    print("Testing AttributeError...")
    try:
        text = "hello"
        text.nonexistent_method()
    except AttributeError as e:
        print(f"Error: {e}")
        return str(e)

def test_value_error():
    """Test ValueError"""
    print("Testing ValueError...")
    try:
        int("not_a_number")
    except ValueError as e:
        print(f"Error: {e}")
        return str(e)

def test_index_error():
    """Test IndexError"""
    print("Testing IndexError...")
    try:
        my_list = [1, 2, 3]
        print(my_list[10])
    except IndexError as e:
        print(f"Error: {e}")
        return str(e)

def test_key_error():
    """Test KeyError"""
    print("Testing KeyError...")
    try:
        my_dict = {"a": 1, "b": 2}
        print(my_dict["c"])
    except KeyError as e:
        print(f"Error: {e}")
        return str(e)

def main():
    """Run all error tests"""
    print("🧪 termExplain Error Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Error", test_import_error),
        ("Syntax Error", test_syntax_error),
        ("Name Error", test_name_error),
        ("Type Error", test_type_error),
        ("File Not Found", test_file_not_found),
        ("Permission Error", test_permission_error),
        ("Attribute Error", test_attribute_error),
        ("Value Error", test_value_error),
        ("Index Error", test_index_error),
        ("Key Error", test_key_error),
    ]
    
    errors = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            error = test_func()
            if error:
                errors.append((test_name, error))
        except Exception as e:
            print(f"Test failed: {e}")
    
    print("\n" + "=" * 50)
    print("📋 Generated Errors for termExplain Testing:")
    print("=" * 50)
    
    for i, (test_name, error) in enumerate(errors, 1):
        print(f"\n{i}. {test_name}:")
        print(f"   Error: {error}")
        print(f"   Command: explain \"{error}\"")
    
    print(f"\n✅ Generated {len(errors)} errors for testing!")
    print("\n💡 Copy any error message above and run:")
    print("   explain \"<error_message>\"")
    
    return errors

if __name__ == "__main__":
    main() 