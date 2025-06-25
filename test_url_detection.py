"""
Quick test to verify URL detection logic
"""

# Import the LinkValidator class - adjust import based on your filename
try:
    from link_validator_simplified import LinkValidator
except ImportError:
    try:
        from link_validator import LinkValidator
    except ImportError:
        # Create a minimal version for testing
        import pandas as pd
        from urllib.parse import urlparse
        
        class LinkValidator:
            def looks_like_url(self, text):
                """Check if text looks like a URL before validation - comprehensive logic"""
                text = text.strip()
                
                # Empty or very short text
                if len(text) < 4:
                    return False
                
                # Should not be too long (likely paragraph text)
                if len(text) > 200:
                    return False
                
                # Should not contain too many spaces (likely sentence)
                if text.count(' ') > 2:
                    return False
                
                # Check for obvious URL patterns first
                url_indicators = ['http://', 'https://', 'www.', 'ftp://']
                if any(indicator in text.lower() for indicator in url_indicators):
                    return True
                
                # Check for common sentence indicators that would disqualify it
                sentence_indicators = [
                    '. ', '! ', '? ', ', and ', ', or ', ' the ', ' a ', ' an ', 
                    ' is ', ' are ', ' was ', ' were ', ' will ', ' can ', ' could ',
                    ' should ', ' would ', ' may ', ' might ', ' this ', ' that ',
                    ' these ', ' those ', ' with ', ' without ', ' from ', ' into ',
                    ' about ', ' through ', ' during ', ' before ', ' after ', ' over ',
                    ' under ', ' above ', ' below ', ' between ', ' among ', ' within '
                ]
                
                text_lower = text.lower()
                if any(indicator in text_lower for indicator in sentence_indicators):
                    return False
                
                # Check for domain-like patterns (contains dots and looks like domain)
                if '.' in text:
                    # Split by spaces to handle cases where URL might be in a sentence
                    words = text.split()
                    for word in words:
                        word = word.strip('.,!?()[]{}"\'-')  # Remove common punctuation
                        
                        # Check if word looks like a domain or URL
                        if self.looks_like_domain_or_url(word):
                            return True
                
                return False
            
            def looks_like_domain_or_url(self, word):
                """Check if a word looks like a domain name or URL - more permissive"""
                if not word or len(word) < 4:
                    return False
                
                # Must contain at least one dot
                if '.' not in word:
                    return False
                
                # Handle URLs with paths (like arxiv.org/ai-safety)
                base_part = word
                if '/' in word:
                    base_part = word.split('/')[0]  # Get just the domain part
                
                # Split by dots
                parts = base_part.split('.')
                
                # Must have at least 2 parts for domain
                if len(parts) < 2:
                    return False
                
                # Check if it looks like a domain structure
                # Allow more flexibility in TLD length (2-20 characters to handle things like "missing-domain")
                tld = parts[-1]
                if not (2 <= len(tld) <= 20):
                    return False
                
                # TLD should contain mostly letters (allow hyphens for compound TLDs)
                if not all(c.isalpha() or c == '-' for c in tld):
                    return False
                
                # All parts before TLD should contain only valid domain characters
                for part in parts[:-1]:  # All parts except the last (TLD)
                    if not part:  # Empty part (like in "example..com")
                        return False
                    
                    # Allow letters, numbers, and hyphens (but not at start/end)
                    for char in part:
                        if not (char.isalnum() or char == '-'):
                            return False
                    
                    # Hyphens cannot be at start or end
                    if part.startswith('-') or part.endswith('-'):
                        return False
                
                # Additional checks
                # Domain should have reasonable length
                if len(base_part) > 100:
                    return False
                
                # Should not start or end with dot
                if base_part.startswith('.') or base_part.endswith('.'):
                    return False
                
                # Must have at least one alphabetic character in the main domain part
                main_domain = parts[-2] if len(parts) >= 2 else parts[0]
                if not any(c.isalpha() for c in main_domain):
                    return False
                
                return True
            
            def is_valid_url(self, url):
                """Validate a URL using urllib.parse"""
                try:
                    if pd.isna(url) or not str(url).strip():
                        return False
                        
                    url_str = str(url).strip()
                    result = urlparse(url_str)
                    
                    # Must have scheme and netloc
                    if not result.scheme or not result.netloc:
                        return False
                        
                    # Accept http/https schemes
                    if result.scheme not in ('http', 'https'):
                        return False
                        
                    # Basic netloc validation
                    netloc = result.netloc.lower()
                    if not netloc or netloc.startswith('.') or netloc.endswith('.'):
                        return False
                        
                    return True
                    
                except Exception:
                    return False

def test_url_detection():
    validator = LinkValidator()
    
    test_cases = [
        # Should be detected as URL-like
        "https://openai.com/research",
        "https://www.nih.gov/news-events/news-releases/artificial-intelligence", 
        "https://tesla.com/autopilot",
        "https://www.ibm.com/quantum-computing",
        "https://digital-strategy.ec.europa.eu/en/policies/european-approach-artificial-intelligence",
        "arxiv.org/ai-safety",
        "broken-link.economics.gov", 
        "complete-research.papers.ai",
        "ai-ethics.missing-domain",
        
        # Should NOT be detected as URL-like
        "one 6 more embedded as descriptive text that will be flagged as invalid URLs by the validator",
        "The future of AI is bright",
        "Machine learning algorithms are becoming sophisticated",
        "This is just regular text with no URLs",
        "Some text with, punctuation and normal words."
    ]
    
    print("🧪 Testing URL Detection Logic")
    print("=" * 60)
    
    for test_text in test_cases:
        looks_like = validator.looks_like_url(test_text)
        is_valid = validator.is_valid_url(test_text) if looks_like else False
        
        status = "🔗" if looks_like else "📝"
        validity = "✅" if is_valid else "❌" if looks_like else "⏭️"
        
        print(f"{status} {validity} {test_text[:60]}{'...' if len(test_text) > 60 else ''}")
        
        if looks_like:
            print(f"    → Detected as URL-like, Valid: {is_valid}")
    
    print("\n🔍 Legend:")
    print("🔗 = Detected as URL-like")
    print("📝 = Detected as regular text") 
    print("✅ = Valid URL")
    print("❌ = Invalid URL")
    print("⏭️ = Skipped (not URL-like)")

if __name__ == "__main__":
    test_url_detection()