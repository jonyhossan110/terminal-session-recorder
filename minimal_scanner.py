#!/usr/bin/env python3
"""
Minimal Web Security Testing Tool
"""

import json
import time
import requests
from colorama import init, Fore

init(autoreset=True)

class MinimalSecurityScanner:
    def __init__(self, url, output_file=None):
        self.url = url if url.startswith(('http://', 'https://')) else 'https://' + url
        self.output_file = output_file
        self.report = {
            'url': self.url,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'checks': {}
        }

    def log(self, message, color=Fore.WHITE):
        print(color + message)

    def check_https(self):
        """Check if the URL uses HTTPS."""
        from urllib.parse import urlparse
        parsed = urlparse(self.url)
        result = {'status': 'PASS' if parsed.scheme == 'https' else 'FAIL',
                  'message': 'HTTPS is enabled' if parsed.scheme == 'https' else 'HTTPS not used'}
        self.report['checks']['https'] = result
        color = Fore.GREEN if result['status'] == 'PASS' else Fore.RED
        self.log(f"🔒 HTTPS Check: {result['message']}", color)

    def check_response_time(self):
        """Check response time."""
        try:
            start = time.time()
            response = requests.get(self.url, timeout=10)
            end = time.time()
            response_time = round(end - start, 2)
            status = 'PASS' if response_time < 2 else 'WARN'
            result = {'time': response_time, 'status': status}
            self.report['checks']['response_time'] = result
            color = Fore.GREEN if status == 'PASS' else Fore.YELLOW
            self.log(f"⏱️  Response Time: {response_time}s", color)
        except Exception as e:
            self.log(f"⏱️  Response Time: Error - {str(e)}", Fore.RED)

    def generate_report(self):
        """Generate JSON report."""
        if self.output_file:
            with open(self.output_file, 'w') as f:
                json.dump(self.report, f, indent=2)
            self.log(f"📄 Report saved to {self.output_file}", Fore.GREEN)

    def run_scan(self):
        """Run basic security checks."""
        self.log(f"🔍 Starting basic security scan for: {self.url}", Fore.CYAN)
        self.log("=" * 50, Fore.CYAN)

        self.check_https()
        self.check_response_time()

        self.log("=" * 50, Fore.CYAN)
        self.log("📊 Scan Complete!", Fore.GREEN)
        self.generate_report()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Minimal Web Security Testing Tool")
    parser.add_argument("url", help="Target URL to scan")
    parser.add_argument("-o", "--output", help="Output report file (JSON)")
    args = parser.parse_args()

    scanner = MinimalSecurityScanner(args.url, args.output)
    scanner.run_scan()