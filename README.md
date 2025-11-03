# Automation Tools to Reverse Engineering

<p align="center">
  <img src="https://user-images.githubusercontent.com/26800596/168480566-89c9c935-20e3-4745-ba34-0a5a8236489d.png" width="600" height="400">
</p>

In this repository, I will store my scripts that I create to automate some processes during some Reverse Engineering tasks.

Some scripts are just code exercises, the main topic of which is reverse engineering.

## Tools

For now, this repository contains the following tools:

- **Malware Deobfuscation Tools**: Python scripts for deobfuscating malware (or config extractors) that I analyzed and posted on my blog. These scripts are for mixed use! Some are for use in Binary Ninja, others in IDA Pro, and others as standalone Python scripts.
- **hashdb_automated**: Yes, there are plugins for *Binary Ninja*, for *IDA Pro*, which already performs this action. However, thinking about Reverse Engineers who are still starting out, and cannot afford the pro version of *IDA* and *Binary Ninja* (and don't want to depend on ***Ghidra's terrible UI***), this script can save several hours when the analyst encounters **Hashed API** calls. In a new update, I gave the ability to accept several Hashes separated by commas, with the aim of the reverse engineer being able to perform the lookup of several Hashed APIs at once. And I gave a new functionality to the script to perform lookups of Hashed APIs using a specific algorithm and containing an XOR key. You obtain this information during your analysis in the disassembler.
- **malware_triage**: A Python script that automates the first stage of screening malicious binaries, such as identifying verdicts through public Threat Intelligence, correlating different names seen in the wild, entropy of sections of the PE artifact (to identify possible Shellcode or packed binaries), import table, Yara and Sigma rule match identification, among other useful information, which are part of the first phase of the malware sample analysis process. Today this script collects this information, only through VirusTotal, however, with free time I will add more platforms with different useful information.
