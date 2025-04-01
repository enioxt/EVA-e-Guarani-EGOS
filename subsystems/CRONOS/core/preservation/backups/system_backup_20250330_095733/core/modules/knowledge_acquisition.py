#!/usr/bin/env python3
"""
# ========================================================================
# KNOWLEDGE ACQUISITION MODULE - EVA & GUARANI
# ========================================================================
#
# This module provides tools for acquiring knowledge from various sources
# including academic repositories, open access journals, and public domain
# libraries. It ensures all content is obtained legally and ethically.
#
# Features:
# 1. Integration with open repositories (arXiv, PLOS, etc.)
# 2. Processing and parsing of scientific text
# 3. Semantic indexing and categorization
# 4. Connection mapping between knowledge domains
# 5. API integration with Perplexity for research
# 
# ========================================================================
"""

import os
import sys
import json
import requests
import datetime
import re
import time
from pathlib import Path
from urllib.parse import quote_plus
import concurrent.futures

# Optional imports - graceful degradation if not available
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

try:
    import arxiv
    ARXIV_AVAILABLE = True
except ImportError:
    ARXIV_AVAILABLE = False

try:
    from scholarly import scholarly
    SCHOLARLY_AVAILABLE = True
except ImportError:
    SCHOLARLY_AVAILABLE = False

# Quantum Knowledge Integration - graceful degradation if not available
try:
    from modules.quantum.quantum_knowledge_hub import QuantumKnowledgeHub
    from modules.quantum.quantum_knowledge_integrator import QuantumKnowledgeIntegrator
    QUANTUM_KNOWLEDGE_AVAILABLE = True
except ImportError:
    QUANTUM_KNOWLEDGE_AVAILABLE = False

# Ensure we can import from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ========================================================================
# CONFIGURATION
# ========================================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(PROJECT_ROOT, "config", "knowledge_acquisition.json")
KNOWLEDGE_DIR = os.path.join(PROJECT_ROOT, "data", "knowledge")
SOURCES_FILE = os.path.join(KNOWLEDGE_DIR, "sources.json")
CACHE_DIR = os.path.join(PROJECT_ROOT, "data", "cache")
DOMAIN_MAPPING_FILE = os.path.join(KNOWLEDGE_DIR, "domain_mapping.json")
PERPLEXITY_CONFIG = os.path.join(PROJECT_ROOT, "config", "api_keys.json")

# Knowledge domains
KNOWLEDGE_DOMAINS = [
    "mathematics", "logic", "calculus",
    "nature", "biology", "ecology",
    "ethics", "philosophy", "morality",
    "art", "aesthetics", "beauty",
    "humanity", "humanism", "sociology",
    "quantum_computing", "physics", "consciousness",
    "data_science", "machine_learning", "ai",
    "psychology", "neuroscience", "cognitive_science",
    "medicine", "public_health", "biology",
    "astronomy", "quantum_physics", "cosmology",
    "linguistics", "communication", "semiotics",
    "cybersecurity", "privacy", "cryptography",
    "education", "pedagogy", "learning_science",
    "music", "musical_theory", "acoustics",
    "architecture", "design", "ergonomics",
    "sustainability", "environment", "ecology",
    "systems_engineering", "complexity", "chaos_theory",
    "religion", "spirituality", "comparative_religion",
    "formal_logic", "set_theory", "category_theory",
    "anthropology", "indigenous_knowledge", "cultural_studies",
    "iot", "xr", "biotechnology",
    "history", "archaeology", "anthropology",
    "visual_arts", "aesthetics", "art_theory",
    "geopolitics", "international_relations", "political_science",
    "futurism", "trend_analysis", "forecasting",
    "consciousness_studies", "altered_states", "perception",
    "quantum_computing", "quantum_algorithms", "quantum_information",
    "biomimicry", "natural_systems", "bionics",
    "programming_languages", "coding_paradigms", "software_philosophy",
    "simulation_theory", "virtual_reality", "digital_metaphysics",
    "decentralized_economy", "dao", "autonomous_systems"
]

# Default configuration
DEFAULT_CONFIG = {
    "repositories": {
        "arxiv": {
            "enabled": True,
            "max_results": 100,
            "query_limit_per_day": 1000
        },
        "plos": {
            "enabled": True,
            "max_results": 100,
            "api_key": ""
        },
        "pubmed": {
            "enabled": True,
            "max_results": 100,
            "api_key": ""
        },
        "scielo": {
            "enabled": True,
            "max_results": 100
        },
        "doaj": {
            "enabled": True,
            "max_results": 100
        },
        "gutenberg": {
            "enabled": True,
            "max_results": 50
        }
    },
    "perplexity": {
        "enabled": False,
        "api_key": "",
        "max_queries_per_day": 50,
        "research_mode": "thorough"
    },
    "processing": {
        "extract_metadata": True,
        "parse_latex": False,
        "extract_citations": True,
        "extract_references": True,
        "semantic_analysis": True
    },
    "storage": {
        "compression": True,
        "database_indexing": True,
        "vector_embeddings": False,
        "max_storage_gb": 50
    },
    "integration": {
        "mycelium_connection": True,
        "bios_q_registration": True,
        "quantum_analysis": True
    }
}

# ========================================================================
# HELPER FUNCTIONS
# ========================================================================

def load_config():
    """Load configuration from file or use defaults"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Ensure all default keys are present
                for category, settings in DEFAULT_CONFIG.items():
                    if category not in config:
                        config[category] = settings
                    elif isinstance(settings, dict):
                        for key, value in settings.items():
                            if key not in config[category]:
                                config[category][key] = value
                return config
        except Exception as e:
            print(f"Error loading config: {str(e)}")
    
    # Create default config file if it doesn't exist
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    
    return DEFAULT_CONFIG

def load_perplexity_api_key():
    """Load Perplexity API key from config file"""
    if os.path.exists(PERPLEXITY_CONFIG):
        try:
            with open(PERPLEXITY_CONFIG, 'r', encoding='utf-8') as f:
                keys = json.load(f)
                return keys.get("perplexity_api_key", "")
        except Exception as e:
            print(f"Error loading API keys: {str(e)}")
    
    return ""

def ensure_knowledge_directories():
    """Ensure all required directories exist"""
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    # Create subdirectories for each domain
    for domain in KNOWLEDGE_DOMAINS:
        os.makedirs(os.path.join(KNOWLEDGE_DIR, domain.replace("_", "-")), exist_ok=True)
    
    return True

def save_source_metadata(source_id, metadata):
    """Save metadata for a knowledge source"""
    if not os.path.exists(SOURCES_FILE):
        with open(SOURCES_FILE, 'w', encoding='utf-8') as f:
            json.dump({"sources": {}}, f, indent=2)
    
    try:
        with open(SOURCES_FILE, 'r', encoding='utf-8') as f:
            sources_data = json.load(f)
    except:
        sources_data = {"sources": {}}
    
    # Add/update source metadata
    sources_data["sources"][source_id] = metadata
    sources_data["last_updated"] = datetime.datetime.now().isoformat()
    
    with open(SOURCES_FILE, 'w', encoding='utf-8') as f:
        json.dump(sources_data, f, indent=2)
    
    return True

def generate_source_id(title, source_type, domain):
    """Generate a unique ID for a knowledge source"""
    import hashlib
    
    # Create slug from title
    slug = re.sub(r'[^a-zA-Z0-9]', '_', title.lower())
    slug = re.sub(r'_+', '_', slug)
    slug = slug[:30]  # Limit length
    
    # Create hash from title and domain
    content_hash = hashlib.md5(f"{title}_{domain}".encode('utf-8')).hexdigest()[:8]
    
    # Get timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    
    return f"{domain}_{source_type}_{slug}_{timestamp}_{content_hash}"

# ========================================================================
# DOMAIN MAPPING
# ========================================================================

def load_domain_mapping():
    """Load domain mapping from file or create default"""
    if os.path.exists(DOMAIN_MAPPING_FILE):
        try:
            with open(DOMAIN_MAPPING_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading domain mapping: {str(e)}")
    
    # Create default domain mapping
    default_mapping = {
        "domains": KNOWLEDGE_DOMAINS,
        "connections": [],
        "last_updated": datetime.datetime.now().isoformat()
    }
    
    # Add some basic connections between related domains
    connections = [
        {"source": "mathematics", "target": "logic", "strength": 0.9},
        {"source": "mathematics", "target": "calculus", "strength": 0.95},
        {"source": "mathematics", "target": "quantum_physics", "strength": 0.8},
        {"source": "nature", "target": "biology", "strength": 0.9},
        {"source": "nature", "target": "ecology", "strength": 0.9},
        {"source": "ethics", "target": "philosophy", "strength": 0.9},
        {"source": "ethics", "target": "morality", "strength": 0.95},
        {"source": "art", "target": "aesthetics", "strength": 0.9},
        {"source": "art", "target": "beauty", "strength": 0.85},
        {"source": "humanity", "target": "humanism", "strength": 0.9},
        {"source": "humanity", "target": "sociology", "strength": 0.75},
        {"source": "quantum_computing", "target": "quantum_physics", "strength": 0.9},
        {"source": "quantum_computing", "target": "quantum_algorithms", "strength": 0.95}
    ]
    
    default_mapping["connections"] = connections
    
    os.makedirs(os.path.dirname(DOMAIN_MAPPING_FILE), exist_ok=True)
    with open(DOMAIN_MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_mapping, f, indent=2)
    
    return default_mapping

def update_domain_mapping(new_connections):
    """Update domain mapping with new connections"""
    mapping = load_domain_mapping()
    
    # Add new connections
    for connection in new_connections:
        # Check if connection already exists
        exists = False
        for existing in mapping["connections"]:
            if (existing["source"] == connection["source"] and 
                existing["target"] == connection["target"]):
                # Update strength if it's stronger
                if connection["strength"] > existing["strength"]:
                    existing["strength"] = connection["strength"]
                exists = True
                break
        
        if not exists:
            mapping["connections"].append(connection)
    
    mapping["last_updated"] = datetime.datetime.now().isoformat()
    
    with open(DOMAIN_MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2)
    
    return True

def calculate_domain_similarity(domain1, domain2):
    """Calculate similarity between two domains based on their connections"""
    mapping = load_domain_mapping()
    
    # Direct connection
    for connection in mapping["connections"]:
        if ((connection["source"] == domain1 and connection["target"] == domain2) or
            (connection["source"] == domain2 and connection["target"] == domain1)):
            return connection["strength"]
    
    # Second-order connection (through a common domain)
    domain1_connections = [c for c in mapping["connections"] 
                          if c["source"] == domain1 or c["target"] == domain1]
    domain2_connections = [c for c in mapping["connections"] 
                          if c["source"] == domain2 or c["target"] == domain2]
    
    common_domains = set()
    for c1 in domain1_connections:
        d1 = c1["target"] if c1["source"] == domain1 else c1["source"]
        for c2 in domain2_connections:
            d2 = c2["target"] if c2["source"] == domain2 else c2["source"]
            if d1 == d2:
                common_domains.add(d1)
    
    if common_domains:
        # Average the connection strengths through common domains
        total_strength = 0
        for common in common_domains:
            strength1 = next(c["strength"] for c in domain1_connections 
                           if (c["source"] == common or c["target"] == common))
            strength2 = next(c["strength"] for c in domain2_connections 
                           if (c["source"] == common or c["target"] == common))
            total_strength += strength1 * strength2
        
        return total_strength / len(common_domains)
    
    return 0.1  # Default low similarity

# ========================================================================
# REPOSITORY INTERFACES
# ========================================================================

def search_arxiv(query, max_results=50, categories=None):
    """Search arXiv repository for papers"""
    if not ARXIV_AVAILABLE:
        print("⚠️ arxiv module not available. Install with: pip install arxiv")
        return []
    
    try:
        # Build the search query
        search_query = query
        if categories:
            for category in categories:
                search_query += f" AND cat:{category}"
        
        # Search arXiv
        search = arxiv.Search(
            query=search_query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = []
        for paper in search.results():
            # Extract information
            paper_data = {
                "title": paper.title,
                "authors": [author.name for author in paper.authors],
                "summary": paper.summary,
                "published": paper.published.isoformat() if paper.published else None,
                "updated": paper.updated.isoformat() if paper.updated else None,
                "doi": paper.doi,
                "arxiv_id": paper.entry_id,
                "pdf_url": paper.pdf_url,
                "categories": paper.categories,
                "source": "arxiv"
            }
            results.append(paper_data)
        
        return results
    except Exception as e:
        print(f"⚠️ Error searching arXiv: {str(e)}")
        return []

def search_pubmed(query, max_results=50, api_key=None):
    """Search PubMed for papers"""
    if not BS4_AVAILABLE:
        print("⚠️ BeautifulSoup not available. Install with: pip install beautifulsoup4")
        return []
    
    try:
        # Set up parameters
        params = {
            "term": query,
            "retmax": max_results,
            "retmode": "json"
        }
        
        if api_key:
            params["api_key"] = api_key
        
        # Search PubMed
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        search_data = response.json()
        id_list = search_data.get("esearchresult", {}).get("idlist", [])
        
        if not id_list:
            return []
        
        # Fetch details for each ID
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        id_param = ",".join(id_list)
        fetch_params = {
            "db": "pubmed",
            "id": id_param,
            "retmode": "xml"
        }
        
        if api_key:
            fetch_params["api_key"] = api_key
        
        fetch_response = requests.get(fetch_url, params=fetch_params)
        fetch_response.raise_for_status()
        
        # Parse XML
        soup = BeautifulSoup(fetch_response.content, "xml")
        articles = soup.find_all("PubmedArticle")
        
        results = []
        for article in articles:
            # Extract information
            title_elem = article.find("ArticleTitle")
            title = title_elem.text if title_elem else "No title"
            
            abstract_elem = article.find("AbstractText")
            abstract = abstract_elem.text if abstract_elem else "No abstract"
            
            authors = []
            author_list = article.find("AuthorList")
            if author_list:
                for author in author_list.find_all("Author"):
                    last_name = author.find("LastName")
                    first_name = author.find("ForeName")
                    if last_name and first_name:
                        authors.append(f"{first_name.text} {last_name.text}")
                    elif last_name:
                        authors.append(last_name.text)
            
            # Find PMID
            pmid_elem = article.find("PMID")
            pmid = pmid_elem.text if pmid_elem else "Unknown"
            
            # Find DOI
            doi = None
            article_id_list = article.find("ArticleIdList")
            if article_id_list:
                for article_id in article_id_list.find_all("ArticleId"):
                    if article_id.get("IdType") == "doi":
                        doi = article_id.text
            
            paper_data = {
                "title": title,
                "authors": authors,
                "summary": abstract,
                "pmid": pmid,
                "doi": doi,
                "source": "pubmed"
            }
            results.append(paper_data)
        
        return results
    except Exception as e:
        print(f"⚠️ Error searching PubMed: {str(e)}")
        return []

def search_open_access(query, source="doaj", max_results=50):
    """Search open access repositories"""
    if not BS4_AVAILABLE:
        print("⚠️ BeautifulSoup not available. Install with: pip install beautifulsoup4")
        return []
    
    try:
        if source == "doaj":
            # Directory of Open Access Journals
            url = f"https://doaj.org/search/articles?source=%7B%22query%22%3A%7B%22query_string%22%3A%7B%22query%22%3A%22{quote_plus(query)}%22%7D%7D%7D"
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.select(".search-results .article-item")
            
            results = []
            for article in articles[:max_results]:
                title_elem = article.select_one(".title a")
                title = title_elem.text.strip() if title_elem else "No title"
                
                link = title_elem["href"] if title_elem else None
                
                abstract_elem = article.select_one(".abstract")
                abstract = abstract_elem.text.strip() if abstract_elem else "No abstract"
                
                authors_elem = article.select_one(".authors")
                authors = [a.strip() for a in authors_elem.text.split(",")] if authors_elem else []
                
                journal_elem = article.select_one(".journal")
                journal = journal_elem.text.strip() if journal_elem else "Unknown"
                
                paper_data = {
                    "title": title,
                    "authors": authors,
                    "summary": abstract,
                    "journal": journal,
                    "url": link,
                    "source": "doaj"
                }
                results.append(paper_data)
            
            return results
        
        elif source == "scielo":
            # SciELO
            url = f"https://search.scielo.org/?q={quote_plus(query)}&lang=en"
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.select(".results .item")
            
            results = []
            for article in articles[:max_results]:
                title_elem = article.select_one(".title")
                title = title_elem.text.strip() if title_elem else "No title"
                
                link_elem = article.select_one(".title a")
                link = link_elem["href"] if link_elem else None
                
                authors_elem = article.select_one(".authors")
                authors = [a.strip() for a in authors_elem.text.split(";")] if authors_elem else []
                
                journal_elem = article.select_one(".journal")
                journal = journal_elem.text.strip() if journal_elem else "Unknown"
                
                paper_data = {
                    "title": title,
                    "authors": authors,
                    "journal": journal,
                    "url": link,
                    "source": "scielo"
                }
                results.append(paper_data)
            
            return results
        
        else:
            print(f"⚠️ Unsupported open access source: {source}")
            return []
    except Exception as e:
        print(f"⚠️ Error searching {source}: {str(e)}")
        return []

def search_gutenberg(query, max_results=50):
    """Search Project Gutenberg for books"""
    if not BS4_AVAILABLE:
        print("⚠️ BeautifulSoup not available. Install with: pip install beautifulsoup4")
        return []
    
    try:
        url = f"https://www.gutenberg.org/ebooks/search/?query={quote_plus(query)}"
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        books = soup.select(".booklink")
        
        results = []
        for book in books[:max_results]:
            title_elem = book.select_one(".title")
            title = title_elem.text.strip() if title_elem else "No title"
            
            author_elem = book.select_one(".subtitle")
            author = author_elem.text.strip() if author_elem else "Unknown"
            
            link_elem = book.select_one("a.link")
            book_id = link_elem["href"].split("/")[-1] if link_elem else None
            
            if book_id:
                book_data = {
                    "title": title,
                    "authors": [author],
                    "book_id": book_id,
                    "url": f"https://www.gutenberg.org/ebooks/{book_id}",
                    "download_url": f"https://www.gutenberg.org/ebooks/{book_id}.kindle.noimages",
                    "source": "gutenberg"
                }
                results.append(book_data)
        
        return results
    except Exception as e:
        print(f"⚠️ Error searching Project Gutenberg: {str(e)}")
        return []

# ========================================================================
# PERPLEXITY API INTEGRATION
# ========================================================================

def perplexity_api_search(query, mode="thorough"):
    """Search using Perplexity API"""
    api_key = load_perplexity_api_key()
    if not api_key:
        print("⚠️ Perplexity API key not available")
        return None
    
    try:
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Set up the prompt
        system_prompt = """You are a research assistant helping with an EVA & GUARANI knowledge acquisition project.
        Your task is to provide detailed, accurate information with credible sources about the query.
        Focus on academic sources, books, and reliable publications.
        Include direct links to any papers, books, or resources mentioned.
        Format your response as JSON with the following structure:
        {
          "summary": "Brief overview of the topic",
          "key_points": ["Point 1", "Point 2", ...],
          "academic_sources": [
            {"title": "Source title", "authors": ["Author names"], "year": "Year", "url": "URL if available", "type": "paper/book/website"}
          ],
          "books": [
            {"title": "Book title", "authors": ["Author names"], "year": "Year", "description": "Brief description"}
          ],
          "connections": [
            {"domain": "Related domain", "relationship": "How it connects to the query"}
          ]
        }"""
        
        data = {
            "model": "llama-3-sonar-large-32k-online" if mode == "thorough" else "llama-3-sonar-large-online",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # Extract JSON from content
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON without code blocks
            json_match = re.search(r'(\{.*\})', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                return None
        
        try:
            parsed_content = json.loads(json_str)
            return parsed_content
        except json.JSONDecodeError:
            print("⚠️ Failed to parse JSON from Perplexity response")
            return None
    except Exception as e:
        print(f"⚠️ Error using Perplexity API: {str(e)}")
        return None

# ========================================================================
# KNOWLEDGE ACQUISITION FUNCTIONS
# ========================================================================

def search_knowledge(query, domain=None, sources=None, max_results=100):
    """Search for knowledge across multiple sources"""
    config = load_config()
    results = []
    
    if not sources:
        # Use all enabled sources
        sources = [s for s, cfg in config["repositories"].items() if cfg["enabled"]]
    
    # Define categories based on domain
    arxiv_categories = None
    if domain:
        # Map domains to arXiv categories
        domain_to_arxiv = {
            "mathematics": ["math", "math-ph"],
            "physics": ["physics", "quant-ph"],
            "computer_science": ["cs"],
            "astronomy": ["astro-ph"],
            "quantum_computing": ["quant-ph", "cs.ET"],
            "quantum_physics": ["quant-ph"],
            "ai": ["cs.AI", "cs.LG", "stat.ML"],
            "machine_learning": ["cs.LG", "stat.ML"],
            "neuroscience": ["q-bio.NC"],
            "biology": ["q-bio"],
            "ecology": ["q-bio.PE"]
        }
        arxiv_categories = domain_to_arxiv.get(domain, None)
    
    # Adjust query based on domain
    if domain:
        domain_terms = domain.replace("_", " ")
        query = f"{query} {domain_terms}"
    
    # Search in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(sources)) as executor:
        # Set up search tasks
        search_tasks = {}
        
        for source in sources:
            if source == "arxiv" and config["repositories"]["arxiv"]["enabled"]:
                max_arxiv = min(config["repositories"]["arxiv"]["max_results"], max_results)
                search_tasks[executor.submit(search_arxiv, query, max_arxiv, arxiv_categories)] = "arxiv"
            
            elif source == "pubmed" and config["repositories"]["pubmed"]["enabled"]:
                max_pubmed = min(config["repositories"]["pubmed"]["max_results"], max_results)
                api_key = config["repositories"]["pubmed"].get("api_key")
                search_tasks[executor.submit(search_pubmed, query, max_pubmed, api_key)] = "pubmed"
            
            elif source == "doaj" and config["repositories"]["doaj"]["enabled"]:
                max_doaj = min(config["repositories"]["doaj"]["max_results"], max_results)
                search_tasks[executor.submit(search_open_access, query, "doaj", max_doaj)] = "doaj"
            
            elif source == "scielo" and config["repositories"]["scielo"]["enabled"]:
                max_scielo = min(config["repositories"]["scielo"]["max_results"], max_results)
                search_tasks[executor.submit(search_open_access, query, "scielo", max_scielo)] = "scielo"
            
            elif source == "gutenberg" and config["repositories"]["gutenberg"]["enabled"]:
                max_gutenberg = min(config["repositories"]["gutenberg"]["max_results"], max_results)
                search_tasks[executor.submit(search_gutenberg, query, max_gutenberg)] = "gutenberg"
        
        # Collect results
        for future in concurrent.futures.as_completed(search_tasks):
            source_name = search_tasks[future]
            try:
                source_results = future.result()
                print(f"✅ Found {len(source_results)} results from {source_name}")
                
                # Add source and domain information
                for result in source_results:
                    result["domain"] = domain
                    result["acquisition_date"] = datetime.datetime.now().isoformat()
                
                results.extend(source_results)
            except Exception as e:
                print(f"⚠️ Error in {source_name} search: {str(e)}")
    
    # Add Perplexity results if enabled
    if "perplexity" in sources and config["perplexity"]["enabled"]:
        try:
            perplexity_result = perplexity_api_search(
                query, 
                mode=config["perplexity"]["research_mode"]
            )
            
            if perplexity_result:
                # Convert to standard format
                if "academic_sources" in perplexity_result:
                    for source in perplexity_result["academic_sources"]:
                        results.append({
                            "title": source.get("title", "Unknown"),
                            "authors": source.get("authors", []),
                            "year": source.get("year"),
                            "url": source.get("url"),
                            "source_type": source.get("type"),
                            "domain": domain,
                            "source": "perplexity",
                            "acquisition_date": datetime.datetime.now().isoformat()
                        })
                
                if "books" in perplexity_result:
                    for book in perplexity_result["books"]:
                        results.append({
                            "title": book.get("title", "Unknown"),
                            "authors": book.get("authors", []),
                            "year": book.get("year"),
                            "summary": book.get("description"),
                            "source_type": "book",
                            "domain": domain,
                            "source": "perplexity",
                            "acquisition_date": datetime.datetime.now().isoformat()
                        })
                
                # Add domain connections if available
                if "connections" in perplexity_result:
                    new_connections = []
                    for connection in perplexity_result["connections"]:
                        conn_domain = connection.get("domain", "").lower().replace(" ", "_")
                        if conn_domain in KNOWLEDGE_DOMAINS and domain:
                            new_connections.append({
                                "source": domain,
                                "target": conn_domain,
                                "strength": 0.7,  # Default medium-high strength
                                "description": connection.get("relationship", "")
                            })
                    
                    if new_connections:
                        update_domain_mapping(new_connections)
        except Exception as e:
            print(f"⚠️ Error processing Perplexity results: {str(e)}")
    
    return results

def save_knowledge_source(source_data, content=None, file_path=None):
    """Save a knowledge source to the appropriate directory"""
    domain = source_data.get("domain")
    if not domain:
        domain = "general"
    
    # Generate ID if not present
    source_id = source_data.get("source_id")
    if not source_id:
        title = source_data.get("title", "Untitled")
        source_type = source_data.get("source_type", source_data.get("source", "unknown"))
        source_id = generate_source_id(title, source_type, domain)
        source_data["source_id"] = source_id
    
    # Determine the file path
    if not file_path:
        domain_dir = os.path.join(KNOWLEDGE_DIR, domain.replace("_", "-"))
        os.makedirs(domain_dir, exist_ok=True)
        
        file_name = f"{source_id}.json"
        file_path = os.path.join(domain_dir, file_name)
    
    # Save metadata
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(source_data, f, indent=2)
    
    # Save content if provided
    if content:
        content_file = file_path.replace(".json", ".txt")
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # Update sources index
    save_source_metadata(source_id, {
        "title": source_data.get("title", "Untitled"),
        "authors": source_data.get("authors", []),
        "domain": domain,
        "source": source_data.get("source", "unknown"),
        "source_type": source_data.get("source_type", "unknown"),
        "file_path": file_path,
        "has_content": content is not None,
        "acquisition_date": source_data.get("acquisition_date", datetime.datetime.now().isoformat())
    })
    
    return file_path

def acquire_knowledge(query, domain=None, sources=None, save_results=True):
    """
    Acquire knowledge on a topic from multiple sources
    
    This is the main function to use for knowledge acquisition.
    It combines external searches with internal quantum knowledge.
    """
    ensure_knowledge_directories()
    
    print(f"🔍 Searching for knowledge on: {query}")
    if domain:
        print(f"📚 Domain: {domain}")
    
    # First, try the quantum knowledge system if available
    quantum_results = []
    if QUANTUM_KNOWLEDGE_AVAILABLE:
        try:
            # Use asyncio.run to run the async function
            import asyncio
            quantum_results = asyncio.run(search_quantum_knowledge(query, domain))
            print(f"✅ Found {len(quantum_results)} quantum knowledge sources")
        except Exception as e:
            print(f"⚠️ Error with quantum knowledge: {str(e)}")
    
    # Then search external knowledge sources
    external_results = search_knowledge(query, domain, sources)
    print(f"✅ Found {len(external_results)} external knowledge sources")
    
    # Combine results with quantum results first
    combined_results = quantum_results + external_results
    
    if not combined_results:
        print("⚠️ No results found")
        return []
    
    # Save results if requested
    if save_results:
        saved_paths = []
        for result in combined_results:
            file_path = save_knowledge_source(result)
            saved_paths.append(file_path)
        
        print(f"✅ Saved {len(saved_paths)} knowledge sources")
    
    return combined_results

async def search_quantum_knowledge(query, domain=None):
    """
    Search for knowledge in the quantum knowledge system
    
    Args:
        query (str): The search query
        domain (str, optional): Knowledge domain to search in
    
    Returns:
        list: List of knowledge source dictionaries
    """
    results = []
    
    if not QUANTUM_KNOWLEDGE_AVAILABLE:
        return results
    
    try:
        # Initialize the knowledge hub
        hub = QuantumKnowledgeHub()
        
        # Modify query based on domain if provided
        search_query = query
        if domain:
            search_query = f"{query} {domain.replace('_', ' ')}"
        
        # Search the knowledge base
        type_filter = domain if domain else None
        quantum_results = await hub.search_knowledge_base(search_query, type_=type_filter)
        
        # Convert to standard format
        for item in quantum_results:
            source_data = {
                "title": item.get("title", "Quantum Knowledge"),
                "source": "quantum_knowledge",
                "source_id": item.get("id", ""),
                "url": item.get("url", ""),
                "authors": item.get("authors", []),
                "date": item.get("date", datetime.datetime.now().isoformat()),
                "summary": item.get("summary", ""),
                "domain": domain or item.get("type", "general"),
                "content": item.get("content", ""),
                "metadata": {
                    "quantum_confidence": item.get("score", 0.0),
                    "source_type": "internal"
                }
            }
            results.append(source_data)
    
    except Exception as e:
        print(f"Error accessing quantum knowledge: {str(e)}")
    
    return results

def download_source_content(source_data):
    """Download content for a knowledge source"""
    source = source_data.get("source")
    
    if source == "arxiv":
        # Download PDF from arXiv
        pdf_url = source_data.get("pdf_url")
        if not pdf_url:
            return None
        
        try:
            response = requests.get(pdf_url)
            response.raise_for_status()
            
            # Save PDF
            source_id = source_data.get("source_id")
            if not source_id:
                source_id = generate_source_id(
                    source_data.get("title", "Untitled"),
                    "arxiv",
                    source_data.get("domain", "general")
                )
            
            pdf_path = os.path.join(CACHE_DIR, f"{source_id}.pdf")
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            
            return pdf_path
        except Exception as e:
            print(f"⚠️ Error downloading arXiv PDF: {str(e)}")
            return None
    
    elif source == "gutenberg":
        # Download ebook from Project Gutenberg
        download_url = source_data.get("download_url")
        if not download_url:
            return None
        
        try:
            response = requests.get(download_url)
            response.raise_for_status()
            
            # Save ebook
            source_id = source_data.get("source_id")
            if not source_id:
                source_id = generate_source_id(
                    source_data.get("title", "Untitled"),
                    "gutenberg",
                    source_data.get("domain", "general")
                )
            
            ebook_path = os.path.join(CACHE_DIR, f"{source_id}.txt")
            with open(ebook_path, 'wb') as f:
                f.write(response.content)
            
            return ebook_path
        except Exception as e:
            print(f"⚠️ Error downloading Gutenberg ebook: {str(e)}")
            return None
    
    else:
        print(f"⚠️ Content download not supported for source: {source}")
        return None

# ========================================================================
# MAIN FUNCTIONS
# ========================================================================

def initialize_knowledge_system():
    """Initialize the knowledge acquisition system"""
    config = load_config()
    ensure_knowledge_directories()
    load_domain_mapping()
    
    print("\n✧༺❀༻∞ EVA & GUARANI - Knowledge Acquisition ∞༺❀༻✧\n")
    print("System initialized with the following settings:")
    
    # Check available repositories
    available_repos = []
    for repo, settings in config["repositories"].items():
        if settings["enabled"]:
            available_repos.append(repo)
    
    print(f"📚 Active repositories: {', '.join(available_repos)}")
    
    # Check Perplexity
    if config["perplexity"]["enabled"]:
        api_key = load_perplexity_api_key()
        if api_key:
            print("🔍 Perplexity API: Enabled")
        else:
            print("⚠️ Perplexity API: Key missing")
    else:
        print("ℹ️ Perplexity API: Disabled")
    
    # Check knowledge domains
    print(f"🌐 Available knowledge domains: {len(KNOWLEDGE_DOMAINS)}")
    
    # Check processing capabilities
    if not ARXIV_AVAILABLE:
        print("⚠️ arXiv module not available - Install with: pip install arxiv")
    
    if not BS4_AVAILABLE:
        print("⚠️ BeautifulSoup not available - Install with: pip install beautifulsoup4")
    
    if not SCHOLARLY_AVAILABLE:
        print("⚠️ Scholarly module not available - Install with: pip install scholarly")
    
    print("\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")
    
    return True

def search_by_domain_list(query, domains=None, max_per_domain=10):
    """Search for knowledge across multiple domains"""
    if not domains:
        # Use a subset of domains
        domains = [
            "mathematics", "ethics", "art", "humanity", 
            "quantum_computing", "data_science", "psychology", 
            "philosophy", "sustainability", "complexity"
        ]
    
    results_by_domain = {}
    total_results = 0
    
    print(f"🔍 Searching for '{query}' across {len(domains)} domains")
    
    for domain in domains:
        print(f"📚 Searching in domain: {domain}")
        domain_results = search_knowledge(query, domain=domain, max_results=max_per_domain)
        results_by_domain[domain] = domain_results
        total_results += len(domain_results)
        
        # Save results
        for result in domain_results:
            save_knowledge_source(result)
        
        # Avoid rate limiting
        time.sleep(1)
    
    print(f"✅ Search complete - Found {total_results} results across {len(domains)} domains")
    
    return results_by_domain

def main():
    """Main function for demonstrating knowledge acquisition"""
    initialize_knowledge_system()
    
    # Display a simple menu
    print("EVA & GUARANI - Knowledge Acquisition System\n")
    print("1. Search for knowledge on a topic")
    print("2. Search across multiple domains")
    print("3. Display knowledge domains")
    print("4. Update domain mapping")
    print("5. Exit")
    
    choice = input("\nChoose an option (1-5): ")
    
    if choice == "1":
        query = input("Enter search query: ")
        domain = input("Enter domain (optional): ")
        
        domain = domain.strip().lower().replace(" ", "_") if domain else None
        if domain and domain not in KNOWLEDGE_DOMAINS:
            print(f"⚠️ Unknown domain: {domain}")
            print(f"Available domains: {', '.join(KNOWLEDGE_DOMAINS[:10])}...")
            print("Using 'general' domain instead")
            domain = None
        
        results = acquire_knowledge(query, domain)
        
        if results:
            print("\nTop results:")
            for i, result in enumerate(results[:5]):
                print(f"{i+1}. {result.get('title')} - {', '.join(result.get('authors', []))}")
                print(f"   Source: {result.get('source')}")
                print()
    
    elif choice == "2":
        query = input("Enter search query: ")
        results = search_by_domain_list(query)
        
        print("\nResults summary by domain:")
        for domain, domain_results in results.items():
            print(f"{domain}: {len(domain_results)} results")
    
    elif choice == "3":
        print("\nAvailable knowledge domains:")
        # Display in columns
        col_width = 25
        num_cols = 3
        domains = sorted(KNOWLEDGE_DOMAINS)
        
        for i in range(0, len(domains), num_cols):
            row = domains[i:i+num_cols]
            print("  ".join(domain.ljust(col_width) for domain in row))
    
    elif choice == "4":
        print("\nUpdating domain mapping...")
        mapping = load_domain_mapping()
        print(f"Current connections: {len(mapping['connections'])}")
        
        # Example new connections
        new_connections = [
            {"source": "mathematics", "target": "quantum_computing", "strength": 0.75},
            {"source": "ethics", "target": "artificial_intelligence", "strength": 0.8},
            {"source": "humanity", "target": "ethics", "strength": 0.9}
        ]
        
        update_domain_mapping(new_connections)
        print(f"Updated with {len(new_connections)} new connections")
    
    print("\nThank you for using the EVA & GUARANI Knowledge Acquisition System!")
    print("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧")

if __name__ == "__main__":
    main() 