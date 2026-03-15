#!/usr/bin/env python3
"""Smart Command Classifier for Pentesting Tools and Techniques"""

import re
from typing import List, Dict, Tuple
from enum import Enum


class CommandCategory(Enum):
    """Command categories based on pentesting methodology"""
    RECONNAISSANCE = "reconnaissance"
    SCANNING = "scanning"
    ENUMERATION = "enumeration"
    EXPLOITATION = "exploitation"
    POST_EXPLOITATION = "post_exploitation"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    LATERAL_MOVEMENT = "lateral_movement"
    DATA_EXFILTRATION = "data_exfiltration"
    PERSISTENCE = "persistence"
    DEFENSE_EVASION = "defense_evasion"
    CREDENTIAL_ACCESS = "credential_access"
    DISCOVERY = "discovery"
    COLLECTION = "collection"
    NETWORK_ANALYSIS = "network_analysis"
    WEB_SECURITY = "web_security"
    SYSTEM_ADMIN = "system_admin"
    UNKNOWN = "unknown"


class CommandClassifier:
    """Intelligent command classifier for pentesting workflows"""

    # Tool patterns and their categories
    TOOL_PATTERNS = {
        CommandCategory.RECONNAISSANCE: [
            r'\b(whois|dig|nslookup|host|dnsrecon|dnsenum|fierce|sublist3r|amass)\b',
            r'\b(shodan|censys|theharvester|recon-ng|maltego)\b',
            r'\b(osint|google\s+dork|inurl|intitle)\b',
        ],
        CommandCategory.SCANNING: [
            r'\b(nmap|masscan|zmap|unicornscan|hping3)\b',
            r'\b(nessus|openvas|nexpose|nikto|wapiti)\b',
            r'\b(nuclei|httpx|subfinder)\b',
        ],
        CommandCategory.ENUMERATION: [
            r'\b(enum4linux|smbclient|rpcclient|nbtscan|snmpwalk)\b',
            r'\b(ldapsearch|ldapdomaindump|bloodhound|sharphound)\b',
            r'\b(gobuster|dirb|dirbuster|ffuf|feroxbuster|wfuzz)\b',
        ],
        CommandCategory.EXPLOITATION: [
            r'\b(metasploit|msfconsole|msfvenom|exploit|payload)\b',
            r'\b(sqlmap|commix|xsser|beef)\b',
            r'\b(hydra|medusa|ncrack|john|hashcat)\b',
            r'\b(exploit-db|searchsploit)\b',
        ],
        CommandCategory.WEB_SECURITY: [
            r'\b(burp|burpsuite|zap|owasp|zaproxy)\b',
            r'\b(sqlmap|xsstrike|commix|nosqlmap)\b',
            r'\b(wpscan|joomscan|droopescan)\b',
            r'\b(curl|wget|httpie).*(-H|--header|--cookie)',
        ],
        CommandCategory.POST_EXPLOITATION: [
            r'\b(empire|covenant|koadic|pupy|sliver)\b',
            r'\b(mimikatz|lazagne|secretsdump|samdump|lsadump)\b',
            r'\b(winpeas|linpeas|linux-exploit-suggester)\b',
        ],
        CommandCategory.PRIVILEGE_ESCALATION: [
            r'\b(sudo|su|pkexec|getsystem)\b',
            r'\b(uac|bypass|elevate|privilege)\b',
            r'\b(pspy|linux-smart-enumeration|sudo\s+-l)\b',
        ],
        CommandCategory.LATERAL_MOVEMENT: [
            r'\b(psexec|wmiexec|smbexec|atexec)\b',
            r'\b(ssh|scp|rsync|rdp|rdesktop|xfreerdp)\b',
            r'\b(impacket|crackmapexec|evil-winrm)\b',
        ],
        CommandCategory.CREDENTIAL_ACCESS: [
            r'\b(mimikatz|secretsdump|lsadump|hashdump)\b',
            r'\b(john|hashcat|ophcrack|rainbow\s+table)\b',
            r'\b(responder|mitm6|ntlmrelayx)\b',
        ],
        CommandCategory.NETWORK_ANALYSIS: [
            r'\b(wireshark|tshark|tcpdump|tcpflow|ettercap)\b',
            r'\b(arpspoof|arping|bettercap|mitmproxy)\b',
            r'\b(netcat|nc|socat|ncat|cryptcat)\b',
        ],
        CommandCategory.PERSISTENCE: [
            r'\b(cron|crontab|systemd|service|rc\.local)\b',
            r'\b(startup|registry|run\s+key|scheduled\s+task)\b',
            r'\b(backdoor|webshell|rootkit)\b',
        ],
        CommandCategory.DEFENSE_EVASION: [
            r'\b(obfuscate|encode|encrypt|pack|upx)\b',
            r'\b(disable.*defender|disable.*firewall|disable.*av)\b',
            r'\b(clear.*log|wevtutil|shred|srm)\b',
        ],
        CommandCategory.DATA_EXFILTRATION: [
            r'\b(exfil|upload|download|transfer)\b',
            r'\b(base64|gzip|tar|zip).*\|.*(curl|wget|nc)',
            r'\b(scp|sftp|ftp).*put',
        ],
        CommandCategory.DISCOVERY: [
            r'\b(ipconfig|ifconfig|ip\s+addr|netstat|ss)\b',
            r'\b(ps|tasklist|systeminfo|uname|whoami|id)\b',
            r'\b(find|locate|ls|dir|tree)\b',
        ],
    }

    # Technique indicators (MITRE ATT&CK-like)
    TECHNIQUE_PATTERNS = {
        'T1595': r'\b(whois|nslookup|dig)\b',  # Active Scanning
        'T1590': r'\b(shodan|censys|google\s+dork)\b',  # Gather Victim Network Information
        'T1046': r'\bnmap\b',  # Network Service Scanning
        'T1087': r'\b(enum4linux|ldapsearch|net\s+user)\b',  # Account Discovery
        'T1110': r'\b(hydra|medusa|john|hashcat)\b',  # Brute Force
        'T1190': r'\b(sqlmap|metasploit|exploit)\b',  # Exploit Public-Facing Application
        'T1003': r'\b(mimikatz|secretsdump|lsadump)\b',  # OS Credential Dumping
        'T1021': r'\b(psexec|wmiexec|ssh)\b',  # Remote Services
        'T1071': r'\b(curl|wget|http).*(-H|--header)',  # Application Layer Protocol
        'T1048': r'\b(exfil|upload|transfer)\b',  # Exfiltration Over Alternative Protocol
    }

    def __init__(self):
        # Compile regex patterns for performance
        self.compiled_patterns = {}
        for category, patterns in self.TOOL_PATTERNS.items():
            self.compiled_patterns[category] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]
        
        self.compiled_techniques = {
            tech_id: re.compile(pattern, re.IGNORECASE)
            for tech_id, pattern in self.TECHNIQUE_PATTERNS.items()
        }

    def classify(self, command: str) -> Tuple[CommandCategory, List[str], float]:
        """
        Classify a command and return category, tags, and confidence score
        
        Returns:
            Tuple of (category, tags, confidence)
        """
        if not command or not command.strip():
            return CommandCategory.UNKNOWN, [], 0.0

        command = command.strip()
        scores = {category: 0.0 for category in CommandCategory}
        tags = []

        # Check tool patterns
        for category, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(command):
                    scores[category] += 1.0
                    # Extract matched tool name as tag
                    match = pattern.search(command)
                    if match:
                        tool = match.group(0).strip()
                        if tool and tool not in tags:
                            tags.append(tool)

        # Check technique patterns
        for tech_id, pattern in self.compiled_techniques.items():
            if pattern.search(command):
                tags.append(tech_id)

        # Determine primary category
        max_score = max(scores.values())
        if max_score == 0:
            category = self._fallback_classification(command)
            confidence = 0.3
        else:
            category = max(scores, key=scores.get)
            # Confidence based on how many patterns matched
            confidence = min(1.0, max_score / 3.0)

        # Add context-based tags
        context_tags = self._extract_context_tags(command)
        tags.extend(context_tags)

        # Remove duplicates while preserving order
        tags = list(dict.fromkeys(tags))

        return category, tags, confidence

    def _fallback_classification(self, command: str) -> CommandCategory:
        """Fallback classification for unknown commands"""
        # Common system commands
        system_keywords = ['ls', 'cd', 'pwd', 'cat', 'echo', 'mkdir', 'rm', 'cp', 'mv']
        if any(cmd in command.lower().split() for cmd in system_keywords):
            return CommandCategory.SYSTEM_ADMIN

        # Check for common discovery patterns
        if re.search(r'\b(ps|top|htop|who|w)\b', command, re.IGNORECASE):
            return CommandCategory.DISCOVERY

        return CommandCategory.UNKNOWN

    def _extract_context_tags(self, command: str) -> List[str]:
        """Extract contextual tags from command"""
        tags = []

        # File operations
        if re.search(r'\.(txt|log|conf|config|xml|json|yaml)', command):
            tags.append('file-access')

        # Network operations
        if re.search(r'(https?://|ftp://|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', command):
            tags.append('network')

        # Sudo/privilege
        if re.search(r'\b(sudo|su)\b', command):
            tags.append('elevated-privilege')

        # Piping/chaining
        if '|' in command or '&&' in command or ';' in command:
            tags.append('chained-command')

        # Output redirection
        if '>' in command or '>>' in command:
            tags.append('file-write')

        return tags

    def get_category_name(self, category: CommandCategory) -> str:
        """Get human-readable category name"""
        return category.value.replace('_', ' ').title()

    def get_risk_level(self, category: CommandCategory) -> str:
        """Assess risk level based on category"""
        high_risk = [
            CommandCategory.EXPLOITATION,
            CommandCategory.PRIVILEGE_ESCALATION,
            CommandCategory.CREDENTIAL_ACCESS,
            CommandCategory.DATA_EXFILTRATION,
            CommandCategory.DEFENSE_EVASION,
        ]
        
        medium_risk = [
            CommandCategory.POST_EXPLOITATION,
            CommandCategory.LATERAL_MOVEMENT,
            CommandCategory.PERSISTENCE,
        ]

        if category in high_risk:
            return "HIGH"
        elif category in medium_risk:
            return "MEDIUM"
        else:
            return "LOW"


# Singleton instance
_classifier_instance = None


def get_classifier() -> CommandClassifier:
    """Get global classifier instance"""
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = CommandClassifier()
    return _classifier_instance
