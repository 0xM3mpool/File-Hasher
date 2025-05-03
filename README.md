# 🔐 File Hasher

A simple command-line tool for calculating and verifying file checksums using various hash algorithms.

## ✨ Features

- 🔒 Calculate file hashes with multiple algorithms (MD5, SHA1, SHA256, SHA384, SHA512)
- 📂 Hash entire directories recursively
- 🔄 Compare files for identity
- ✅ Verify files against hash files (like md5sum format)
- 💾 Cache hashes for faster repeated access
- 📊 Show file information (size, modification time)
- 🚀 Efficient processing of large files

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/0xM3mpool/file-hasher.git
cd file-hasher
```

2. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage

```bash
python main.py <mode> [options]
```

## ⚙️ Modes

- `file`: Hash a single file
- `dir`: Hash all files in a directory
- `compare`: Compare hashes of two files
- `verify`: Verify files against a hash file
- `clear-cache`: Clear the hash cache

## 📋 Command Options

### Hash a single file:
```bash
python main.py file <path> [options]
```

Options:

- `-a, --algorithm`: Hash algorithm (md5, sha1, sha256, sha384, sha512)
- `-i, --info`: Show file information
- `--no-cache`: Don't use cache

### Hash a directory:
```bash
python main.py dir <path> [options]
```

Options:

- `-a, --algorithm`: Hash algorithm
- `-n, --no-recursive`: Don't recurse into subdirectories
- `--no-cache`: Don't use cache

### Compare two files:
```bash
python main.py compare <file1> <file2> [options]
```

Options:

- `-a, --algorithm`: Hash algorithm
- `--no-cache`: Don't use cache

### Verify against a hash file:
```bash
python main.py verify <hashfile> [options]
```

Options:

- `-d, --directory`: Directory containing files
- `-a, --algorithm`: Algorithm to use (auto-detected if not specified)

### Clear cache:
```bash
python main.py clear-cache
```

## 📝 Examples

### Hash a single file:
```bash
# Default SHA256 hash
python main.py file document.pdf
```

```bash
# With MD5 algorithm
python main.py file image.jpg -a md5
```

```bash
# Show file info
python main.py file large_file.zip -i
```

### Hash a directory:
```bash
# Hash all files in a directory
python main.py dir ~/Downloads
```

```bash
# With specific algorithm
python main.py dir ~/Documents -a sha1
```

```bash
# Non-recursive
python main.py dir ~/Projects -n
```

### Compare files:
```bash
# Compare two files
python main.py compare file1.txt file2.txt
```

```bash
# With specific algorithm
python main.py compare photo1.jpg photo2.jpg -a md5
```

### Verify against a hash file:
```bash
# Verify files in current directory
python main.py verify checksums.md5
```

```bash
# Verify files in specified directory
python main.py verify hashes.sha256 -d ~/Downloads
```

```bash
# With specific algorithm
python main.py verify checksums.txt -a sha256
```

### Clear cache:
```bash
python main.py clear-cache
```

## 📄 Hash File Format

The tool accepts hash files in the standard format used by tools like md5sum:
hash  filename
hash  filename

For example:
d41d8cd98f00b204e9800998ecf8427e  empty.txt
5d41402abc4b2a76b9719d911017c592  hello.txt

Hash files can:
- Contain comments (lines starting with #)
- Have empty lines
- Use any supported hash algorithm (auto-detected by hash length)

## 💾 Cache Information

- Hash results are cached for faster repeated access
- Cache is stored in `~/.file_hasher_cache.json`
- Cache checks file modification time to detect changes
- Use `--no-cache` to bypass cache
- Use `clear-cache` to remove all cached hashes

## 💡 Tips

- Use SHA256 for general-purpose hashing (best security/speed balance)
- MD5 is fastest but least secure
- Use the cache for large directories to speed up repeated operations
- Verify important downloads with hash files from the source
- For identical file detection, any hash algorithm will work
- Use file info (-i) to see file details while hashing

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.