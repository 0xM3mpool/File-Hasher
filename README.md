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
git clone https://github.com/yourusername/file-hasher.git
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