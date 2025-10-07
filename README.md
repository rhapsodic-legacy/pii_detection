# Modular PII Detection Toolkit

### This repository contains much of the PII detection toolkit that was used for the corpus of text for the Hugging Face / BigScience 176 Billion Parameter BLOOM LLM released in 2022.

This repository provides a modular Personally Identifiable Information (PII) detection toolkit designed to identify and flag sensitive data in text. The toolkit supports multiple detection methods, including regular expressions (regex), spaCy, and Presidio, which can be used in any combination for flexible and robust PII detection.
 
##### Importance
This toolkit mirrors the approach used to screen the training corpus for the BLOOM large language model, a 176-billion-parameter model developed by Hugging Face and BigScience. By identifying and mitigating PII in training data, this tool helps ensure privacy compliance and reduces the risk of sensitive information leakage in large-scale language models.  
  
##### Repository Contents   
The repository contains a single folder, pii_detection_tools, with the following five files:         
     
pii_detection.py: The main program that executes the PII detection pipeline.      
    
input_corpus.txt: A sample text file containing PII for testing the toolkit.   
   
prerequisites.txt: A list of dependencies required to run the program.          
 
walkthrough.txt: A detailed guide explaining the code's structure, functionality, and design rationale. 

BLOOM_LLM_history.txt: A detail rich memoire of the largest LLM of its day, as well as the first international open source LLM. 
 

##### MIT License
Copyright (c) 2025 rhapsodic-legacy
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
