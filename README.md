# qszy Dataset Generation

This folder contains scripts to download audio and transcript files from v.xwcz.org, convert `.doc` transcripts to `.txt`, and generate derived datasets.

## Scripts

### `download_mp3.py`
Download MP3 files from the `14-004` series using numeric ranges and `a/b` suffixes.

Usage:
```powershell
python download_mp3.py --start 1 --end 22 --output mp3
```

This downloads files like:
- `14-004-0001a.mp3`
- `14-004-0001b.mp3`
- ...

Options:
- `--start`: starting numeric index
- `--end`: ending numeric index
- `--output`: directory for downloaded MP3s
- `--skip-existing`: skip files that already exist locally

### `download_doc.py`
Download `.doc` transcript files from the `14-004` series, optionally choosing Traditional Chinese (`CHT`) or Simplified Chinese (`CHS`).

Usage:
```powershell
python download_doc.py --start 1 --end 22 --output docs --lang cht
```

This downloads files like:
- `14-004-0001a.doc`
- `14-004-0001b.doc`

Options:
- `--start`: starting numeric index
- `--end`: ending numeric index
- `--output`: directory for downloaded DOCs
- `--lang`: `cht` or `chs`
- `--skip-existing`: skip files that already exist locally

### `doc_to_txt.py`
Convert `.doc` files into plain text `.txt` files.

Supported conversion modes:
- single `.doc` file
- entire directory
- recursive directory traversal
- numeric range conversion matching the `download_doc.py` pattern

Usage examples:
```powershell
python doc_to_txt.py --input txt/14-004-0001a.doc --output txt/14-004-0001a.txt
python doc_to_txt.py --input docs --output txt --recursive
python doc_to_txt.py --input docs --start 1 --end 22 --output txt --skip-existing
```

Options:
- `--input`, `-i`: input file or directory
- `--output`, `-o`: output file or directory
- `--recursive`, `-r`: convert all `.doc` files recursively in a directory
- `--start`: starting numeric index for range conversion
- `--end`: ending numeric index for range conversion
- `--method`, `-m`: conversion backend
- `--skip-existing`: skip files that already exist
- `--force`, `-f`: overwrite existing output files

Range mode expects the input directory to contain files named like `14-004-0001a.doc` and will generate `.txt` outputs with the same stem.

### `convert_vid.sh` and `run_convert_all.bat`
These helper scripts are used to process downloaded audio/video files and batch-run the conversion pipeline on Windows.

- `convert_vid.sh`: a shell script for converting media files using the local toolchain.
- `run_convert_all.bat`: a batch wrapper to execute the shell script for all matching files in a directory.

## Recommended dataset workflow

1. Download audio:
   ```powershell
   python download_mp3.py --start 1 --end 22 --output mp3
   ```
2. Download transcript DOCs:
   ```powershell
   python download_doc.py --start 1 --end 22 --output docs --lang cht
   ```
3. Convert DOCs to text:
   ```powershell
   python doc_to_txt.py --input docs --output txt --start 1 --end 22 --skip-existing
   ```
4. Generate transcripts with SDT:
   ```powershell
   cd ..\SDT
   python -m sdt --input txt --output transcripts
   ```
5. (Optional) Run media conversion if needed:
   ```powershell
   run_convert_all.bat
   ```

## Notes

- On Windows, `doc_to_txt.py` prefers Word automation via `win32com` when available.
- If Word automation is not available, the script falls back to other installed converters such as `antiword`, `wvText`, LibreOffice, or `textract`.
- Use `--skip-existing` when rerunning downloads or conversions to avoid repeating work.
