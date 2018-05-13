# Virtual Memory System
This is a practice project written in Python that implements a virtual memory system using segmentation and paging. It uses a translation look-aside buffer to improve the translation process.

## I/O format
Two input files are necessary. The first file specifies the starting addresses of all page tables, with each 2-tuple `s f` in the first line specifying segment `s` starting at address `f`. Each 3-tuple `p s f` in the second line specifies that page `p` of segment `s` starts at address `f`. If `f` is -1, the corresponding page table or page is not in physical memory. 

The second file specifies the read/write operations, with each pair `o VA` specifying an operation `o` - 0 (read) or 1 (write), and `VA` being the virtual address to operate on.

## Usage
```py
cat input1.txt <(echo) input2.txt | python3 vm_sys.py
```
