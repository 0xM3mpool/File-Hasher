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

