#!/usr/bin/env python3

import argparse
import hashlib
import os
import sys
import json
from datetime import datetime

# Constants
SUPPORTED_ALGORITHMS = ['md5', 'sha1', 'sha256', 'sha384', 'sha512']
DEFAULT_ALGORITHM = 'sha256'
BUFFER_SIZE = 65536  # 64kb chunks
CACHE_FILE = os.path.expanduser("~/.file_hasher_cache.json")

def get_file_hash(file_path, algorithm='sha256', use_cache=True):
    """Calculate hash of a file using specified algorithm"""
    try:
        # Check cache first
        if use_cache:
            cached_hash = get_cached_hash(file_path, algorithm)
            if cached_hash:
                return cached_hash
        
        # Create hash object based on algorithm
        hash_obj = hashlib.new(algorithm)
        
        # Read file in chunks to handle large files
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                hash_obj.update(data)
        
        # Get final hash
        file_hash = hash_obj.hexdigest()
        
        # Cache the result
        if use_cache:
            save_to_cache(file_path, algorithm, file_hash)
        
        return file_hash
    
    except Exception as e:
        print(f"Error hashing file {file_path}: {e}")
        return None

def get_cached_hash(file_path, algorithm):
    """Get cached hash for a file if it exists and file hasn't changed"""
    if not os.path.exists(CACHE_FILE):
        return None
    
    try:
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
        
        cache_key = file_path
        if cache_key in cache:
            entry = cache[cache_key]
            
            # Check if file has been modified since cache
            if os.path.getmtime(file_path) == entry.get('mtime'):
                if algorithm in entry.get('hashes', {}):
                    print(f"Using cached {algorithm} hash for {os.path.basename(file_path)}")
                    return entry['hashes'][algorithm]
    except:
        pass
    
    return None

def save_to_cache(file_path, algorithm, file_hash):
    """Save hash to cache"""
    cache = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                cache = json.load(f)
        except:
            pass
    
    cache_key = file_path
    if cache_key not in cache:
        cache[cache_key] = {'hashes': {}}
    
    cache[cache_key]['hashes'][algorithm] = file_hash
    cache[cache_key]['mtime'] = os.path.getmtime(file_path)
    
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=2)
    except:
        pass

def hash_file(file_path, algorithm=DEFAULT_ALGORITHM, show_info=False, no_cache=False):
    """Display hash for a single file"""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist")
        return False
    
    if not os.path.isfile(file_path):
        print(f"Error: '{file_path}' is not a file")
        return False
    
    file_hash = get_file_hash(file_path, algorithm, not no_cache)
    if file_hash is None:
        return False
    
    # Show file info if requested
    if show_info:
        file_size = os.path.getsize(file_path)
        file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
        
        print(f"\nFile: {file_path}")
        print(f"Size: {format_size(file_size)}")
        print(f"Modified: {file_mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{algorithm.upper()}: {file_hash}")
    else:
        print(f"{file_hash}  {os.path.basename(file_path)}")
    
    return True

def format_size(size_bytes):
    """Format file size in human-readable form"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"

def hash_directory(directory, algorithm=DEFAULT_ALGORITHM, recursive=True, no_cache=False):
    """Hash all files in a directory"""
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist")
        return False
    
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a directory")
        return False
    
    results = []
    
    if recursive:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = get_file_hash(file_path, algorithm, not no_cache)
                if file_hash:
                    results.append((file_path, file_hash))
    else:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        for file in files:
            file_path = os.path.join(directory, file)
            file_hash = get_file_hash(file_path, algorithm, not no_cache)
            if file_hash:
                results.append((file_path, file_hash))
    
    # Sort by file path for consistent output
    results.sort(key=lambda x: x[0])
    
    print(f"\n{algorithm.upper()} hashes for {directory}:")
    print("-" * (len(directory) + 20))
    
    for file_path, file_hash in results:
        rel_path = os.path.relpath(file_path, directory)
        print(f"{file_hash}  {rel_path}")
    
    print(f"\nTotal files processed: {len(results)}")
    return True

def compare_hashes(file1, file2, algorithm=DEFAULT_ALGORITHM, no_cache=False):
    """Compare hashes of two files"""
    hash1 = get_file_hash(file1, algorithm, not no_cache)
    hash2 = get_file_hash(file2, algorithm, not no_cache)
    
    if hash1 and hash2:
        print(f"{algorithm.upper()} Comparison:")
        print(f"File 1: {file1}")
        print(f"  Hash: {hash1}")
        print(f"File 2: {file2}")
        print(f"  Hash: {hash2}")
        
        if hash1 == hash2:
            print("\n✓ The files are identical (hashes match)")
            return True
        else:
            print("\n✗ The files are different (hashes don't match)")
            return False
    
    return False

def verify_hashfile(hashfile_path, directory=".", algorithm=None):
    """Verify files against a hash file (like md5sum format)"""
    if not os.path.exists(hashfile_path):
        print(f"Error: Hash file '{hashfile_path}' does not exist")
        return False
    
    errors = 0
    verified = 0
    
    print(f"Verifying files against {hashfile_path}:")
    print("-" * 60)
    
    with open(hashfile_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Parse hash format: "hash  filename"
            parts = line.split(None, 1)
            if len(parts) != 2:
                continue
            
            expected_hash, filename = parts
            
            # Determine algorithm from hash length if not specified
            if algorithm is None:
                hash_length = len(expected_hash)
                algo_guess = {
                    32: 'md5',
                    40: 'sha1',
                    64: 'sha256',
                    96: 'sha384',
                    128: 'sha512'
                }.get(hash_length, DEFAULT_ALGORITHM)
            else:
                algo_guess = algorithm
            
            file_path = os.path.join(directory, filename)
            
            if not os.path.exists(file_path):
                print(f"✗ {filename}: FILE NOT FOUND")
                errors += 1
                continue
            
            actual_hash = get_file_hash(file_path, algo_guess)
            
            if actual_hash and actual_hash.lower() == expected_hash.lower():
                print(f"✓ {filename}: OK")
                verified += 1
            else:
                print(f"✗ {filename}: FAILED")
                errors += 1
    
    print("-" * 60)
    print(f"Verification complete: {verified} OK, {errors} failed")
    
    return errors == 0

def clear_cache():
    """Clear the hash cache"""
    if os.path.exists(CACHE_FILE):
        try:
            os.remove(CACHE_FILE)
            print("Cache cleared successfully")
            return True
        except Exception as e:
            print(f"Error clearing cache: {e}")
            return False
    else:
        print("Cache is already empty")
        return True

def main():
    parser = argparse.ArgumentParser(description="File Hasher - Calculate and verify file checksums")
    
    # Main mode selection
    subparsers = parser.add_subparsers(dest="mode", help="Operation mode")
    
    # Hash single file
    file_parser = subparsers.add_parser("file", help="Hash a single file")
    file_parser.add_argument("path", help="File path")
    file_parser.add_argument("-a", "--algorithm", choices=SUPPORTED_ALGORITHMS, default=DEFAULT_ALGORITHM,
                           help=f"Hash algorithm (default: {DEFAULT_ALGORITHM})")
    file_parser.add_argument("-i", "--info", action="store_true", help="Show file information")
    file_parser.add_argument("--no-cache", action="store_true", help="Don't use cache")
    
    # Hash directory
    dir_parser = subparsers.add_parser("dir", help="Hash all files in a directory")
    dir_parser.add_argument("path", help="Directory path")
    dir_parser.add_argument("-a", "--algorithm", choices=SUPPORTED_ALGORITHMS, default=DEFAULT_ALGORITHM,
                          help=f"Hash algorithm (default: {DEFAULT_ALGORITHM})")
    dir_parser.add_argument("-n", "--no-recursive", action="store_true", help="Don't recurse into subdirectories")
    dir_parser.add_argument("--no-cache", action="store_true", help="Don't use cache")
    
    # Compare files
    comp_parser = subparsers.add_parser("compare", help="Compare hashes of two files")
    comp_parser.add_argument("file1", help="First file")
    comp_parser.add_argument("file2", help="Second file")
    comp_parser.add_argument("-a", "--algorithm", choices=SUPPORTED_ALGORITHMS, default=DEFAULT_ALGORITHM,
                           help=f"Hash algorithm (default: {DEFAULT_ALGORITHM})")
    comp_parser.add_argument("--no-cache", action="store_true", help="Don't use cache")
    
    # Verify hash file
    verify_parser = subparsers.add_parser("verify", help="Verify files against a hash file")
    verify_parser.add_argument("hashfile", help="Hash file path")
    verify_parser.add_argument("-d", "--directory", default=".", help="Directory containing files (default: current)")
    verify_parser.add_argument("-a", "--algorithm", choices=SUPPORTED_ALGORITHMS,
                             help="Algorithm to use (default: auto-detect from hash length)")
    
    # Clear cache
    cache_parser = subparsers.add_parser("clear-cache", help="Clear the hash cache")
    
    args = parser.parse_args()
    
    if args.mode == "file":
        sys.exit(0 if hash_file(args.path, args.algorithm, args.info, args.no_cache) else 1)
    
    elif args.mode == "dir":
        sys.exit(0 if hash_directory(args.path, args.algorithm, not args.no_recursive, args.no_cache) else 1)
    
    elif args.mode == "compare":
        sys.exit(0 if compare_hashes(args.file1, args.file2, args.algorithm, args.no_cache) else 1)
    
    elif args.mode == "verify":
        sys.exit(0 if verify_hashfile(args.hashfile, args.directory, args.algorithm) else 1)
    
    elif args.mode == "clear-cache":
        clear_cache()
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
