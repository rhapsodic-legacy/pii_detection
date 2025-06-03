import re
import spacy
from typing import List, Dict, Set
import os
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

class PIIDetector:
    """Base class for PII detection methods."""
    def detect(self, text: str) -> Set[str]:
        raise NotImplementedError("Detect method must be implemented.")

class RegexPIIDetector(PIIDetector):
    """Detects PII using regular expressions."""
    def __init__(self):
        self.patterns = {
            "Email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "Phone": r'\b(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
            "SSN": r'\b\d{3}-\d{2}-\d{4}\b',
            "Credit Card": r'\b(?:\d[ -]*?){13,16}\b',  # Simplified for Visa, MC, etc.
            "Passport": r'\b[A-Z0-9]{6,9}\b',  # Basic passport number pattern
            "Canadian SIN": r'\b\d{3}-\d{3}-\d{3}\b'  # Canadian Social Insurance Number
        }

    def detect(self, text: str) -> Set[str]:
        findings = set()
        for pii_type, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                findings.add(f"{pii_type}: {match}")
        return findings

class SpacyPIIDetector(PIIDetector):
    """Detects PII using spaCy's NER model."""
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise RuntimeError("spaCy model 'en_core_web_sm' not found. Run 'python -m spacy download en_core_web_sm'.")

    def detect(self, text: str) -> Set[str]:
        findings = set()
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "GPE", "ORG"]:
                findings.add(f"{ent.label_}: {ent.text}")
        return findings

class PresidioPIIDetector(PIIDetector):
    """Detects PII using Presidio's analyzer."""
    def __init__(self):
        provider = NlpEngineProvider(nlp_configuration={
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}]
        })
        self.analyzer = AnalyzerEngine(nlp_engine=provider.create_engine())

    def detect(self, text: str) -> Set[str]:
        findings = set()
        results = self.analyzer.analyze(text=text, entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "CREDIT_CARD", "US_SSN", "US_PASSPORT", "CA_SIN"], language="en")
        for result in results:
            findings.add(f"{result.entity_type}: {text[result.start:result.end]}")
        return findings

class PIIDetectionManager:
    """Manages multiple PII detection methods and user interaction."""
    def __init__(self):
        self.detectors: Dict[str, PIIDetector] = {
            "regex": RegexPIIDetector(),
            "spacy": SpacyPIIDetector(),
            "presidio": PresidioPIIDetector()
        }
        self.available_methods = list(self.detectors.keys())

    def select_methods(self) -> List[str]:
        """Prompts user to select PII detection methods."""
        print("\nSelect PII Detection Methods (like checkboxes):")
        for i, method in enumerate(self.available_methods, 1):
            print(f"{i}. {method.capitalize()}")
        print("Enter the numbers of the methods to use (e.g., '1 2 3' for all, or '1 3'), or 'all':")
        
        while True:
            try:
                user_input = input("> ").strip().lower()
                if user_input == "all":
                    return self.available_methods
                selected = [int(x) - 1 for x in user_input.split()]
                if all(0 <= x < len(self.available_methods) for x in selected):
                    return [self.available_methods[i] for i in selected]
                else:
                    print("Invalid selection. Please enter valid numbers.")
            except ValueError:
                print("Invalid input. Please enter numbers separated by spaces or 'all'.")

    def read_corpus(self, file_path: str) -> str:
        """Reads the input corpus from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return ""
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""

    def detect_pii(self, text: str, methods: List[str]) -> Dict[str, Set[str]]:
        """Runs selected PII detection methods on the text."""
        results = {}
        for method in methods:
            if method in self.detectors:
                try:
                    findings = self.detectors[method].detect(text)
                    results[method] = findings
                except Exception as e:
                    print(f"Error with {method} detector: {e}")
                    results[method] = set()
        return results

    def display_results(self, results: Dict[str, Set[str]]):
        """Displays the PII detection results."""
        print("\n=== PII Detection Results ===")
        for method, findings in results.items():
            print(f"\n{method.capitalize()} Detector:")
            if findings:
                for finding in sorted(findings):  # Sort for consistent output
                    print(f"  - {finding}")
            else:
                print("  No PII detected.")
        print("\n============================")

def main():
    # Initialize the PII detection manager
    try:
        manager = PIIDetectionManager()
    except Exception as e:
        print(f"Error initializing detectors: {e}")
        return

    # Specify the input file (user can modify this path)
    corpus_file = "input_corpus.txt"
    
    # Read the corpus
    corpus = manager.read_corpus(corpus_file)
    if not corpus:
        print("Exiting due to corpus read error.")
        return

    # Select detection methods
    selected_methods = manager.select_methods()
    if not selected_methods:
        print("No methods selected. Exiting.")
        return

    # Detect PII
    results = manager.detect_pii(corpus, selected_methods)

    # Display results
    manager.display_results(results)

if __name__ == "__main__":
    main()