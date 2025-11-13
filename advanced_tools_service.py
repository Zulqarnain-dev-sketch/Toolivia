#!/usr/bin/env python3
"""
Advanced Tools Service
Provides AI-powered tools for SEO, text analysis, and data processing
"""

import re
import requests
import json
import hashlib
import base64
from datetime import datetime
from urllib.parse import urlparse
from textstat import flesch_reading_ease, flesch_kincaid_grade
from collections import Counter
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/readability', methods=['POST'])
def analyze_readability():
    """Advanced readability analysis"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Basic metrics
        words = len(text.split())
        sentences = len(re.split(r'[.!?]+', text))
        paragraphs = len([p for p in text.split('\n\n') if p.strip()])
        
        # Advanced readability scores
        flesch_score = flesch_reading_ease(text)
        fk_grade = flesch_kincaid_grade(text)
        
        # Reading level
        if flesch_score >= 90:
            level = "Very Easy"
        elif flesch_score >= 80:
            level = "Easy"
        elif flesch_score >= 70:
            level = "Fairly Easy"
        elif flesch_score >= 60:
            level = "Standard"
        elif flesch_score >= 50:
            level = "Fairly Difficult"
        elif flesch_score >= 30:
            level = "Difficult"
        else:
            level = "Very Difficult"
        
        # Keyword density
        word_freq = Counter(re.findall(r'\b\w+\b', text.lower()))
        total_words = sum(word_freq.values())
        top_keywords = [(word, count, round(count/total_words*100, 2)) 
                       for word, count in word_freq.most_common(10)]
        
        return jsonify({
            'flesch_score': round(flesch_score, 1),
            'grade_level': round(fk_grade, 1),
            'reading_level': level,
            'word_count': words,
            'sentence_count': sentences,
            'paragraph_count': paragraphs,
            'avg_words_per_sentence': round(words/sentences if sentences > 0 else 0, 1),
            'top_keywords': top_keywords
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/keywords', methods=['POST'])
def analyze_keywords():
    """Advanced keyword analysis"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Extract keywords
        words = re.findall(r'\b\w{3,}\b', text.lower())
        word_freq = Counter(words)
        
        # Filter common stop words
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}
        filtered_words = {word: count for word, count in word_freq.items() if word not in stop_words}
        
        # Calculate keyword metrics
        total_words = len(words)
        keywords = []
        
        for word, count in Counter(filtered_words).most_common(20):
            density = round(count / total_words * 100, 2)
            keywords.append({
                'keyword': word,
                'count': count,
                'density': density,
                'prominence': 'High' if density > 2 else 'Medium' if density > 1 else 'Low'
            })
        
        return jsonify({
            'total_words': total_words,
            'unique_words': len(filtered_words),
            'keywords': keywords
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sitemap', methods=['POST'])
def generate_sitemap():
    """Generate XML sitemap"""
    try:
        data = request.json
        urls = data.get('urls', [])
        domain = data.get('domain', '')
        
        if not urls:
            return jsonify({'error': 'No URLs provided'}), 400
        
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        for url_data in urls:
            url = url_data.get('url', '')
            priority = url_data.get('priority', '0.5')
            changefreq = url_data.get('changefreq', 'monthly')
            
            if not url.startswith('http'):
                url = f"{domain.rstrip('/')}/{url.lstrip('/')}"
            
            sitemap += f'  <url>\n'
            sitemap += f'    <loc>{url}</loc>\n'
            sitemap += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
            sitemap += f'    <changefreq>{changefreq}</changefreq>\n'
            sitemap += f'    <priority>{priority}</priority>\n'
            sitemap += f'  </url>\n'
        
        sitemap += '</urlset>'
        
        return jsonify({'sitemap': sitemap})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/schema', methods=['POST'])
def generate_schema():
    """Generate schema markup"""
    try:
        data = request.json
        schema_type = data.get('type', 'Organization')
        schema_data = data.get('data', {})
        
        if schema_type == 'Organization':
            schema = {
                "@context": "https://schema.org",
                "@type": "Organization",
                "name": schema_data.get('name', ''),
                "url": schema_data.get('url', ''),
                "logo": schema_data.get('logo', ''),
                "description": schema_data.get('description', ''),
                "contactPoint": {
                    "@type": "ContactPoint",
                    "telephone": schema_data.get('phone', ''),
                    "contactType": "customer service"
                }
            }
        elif schema_type == 'Article':
            schema = {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": schema_data.get('title', ''),
                "description": schema_data.get('description', ''),
                "author": {
                    "@type": "Person",
                    "name": schema_data.get('author', '')
                },
                "datePublished": schema_data.get('date', datetime.now().isoformat()),
                "image": schema_data.get('image', '')
            }
        else:
            return jsonify({'error': 'Unsupported schema type'}), 400
        
        return jsonify({'schema': json.dumps(schema, indent=2)})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/text-diff', methods=['POST'])
def compare_texts():
    """Advanced text comparison"""
    try:
        data = request.json
        text1 = data.get('text1', '').splitlines()
        text2 = data.get('text2', '').splitlines()
        
        import difflib
        
        diff = list(difflib.unified_diff(text1, text2, lineterm=''))
        
        changes = []
        for line in diff:
            if line.startswith('+++') or line.startswith('---') or line.startswith('@@'):
                continue
            elif line.startswith('+'):
                changes.append({'type': 'added', 'content': line[1:]})
            elif line.startswith('-'):
                changes.append({'type': 'removed', 'content': line[1:]})
            else:
                changes.append({'type': 'unchanged', 'content': line[1:] if line.startswith(' ') else line})
        
        # Calculate similarity
        similarity = difflib.SequenceMatcher(None, ' '.join(text1), ' '.join(text2)).ratio()
        
        return jsonify({
            'changes': changes,
            'similarity': round(similarity * 100, 1)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/hash', methods=['POST'])
def generate_hash():
    """Generate multiple hash types"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        text_bytes = text.encode('utf-8')
        
        hashes = {
            'md5': hashlib.md5(text_bytes).hexdigest(),
            'sha1': hashlib.sha1(text_bytes).hexdigest(),
            'sha256': hashlib.sha256(text_bytes).hexdigest(),
            'sha512': hashlib.sha512(text_bytes).hexdigest()
        }
        
        return jsonify(hashes)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)