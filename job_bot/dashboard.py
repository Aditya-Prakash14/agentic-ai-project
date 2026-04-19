import json
import os
from pathlib import Path
from tracker import Tracker

def generate_dashboard():
    """Generate static HTML dashboard from output files and tracker"""
    tracker = Tracker()
    output_dir = Path('output')
    
    # Collect all cover letters
    cards = []
    if output_dir.exists():
        for filepath in sorted(output_dir.glob('*.txt'), reverse=True):
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Parse metadata header
                lines = content.split('\n')
                metadata = {}
                cover_letter = content
                
                for i, line in enumerate(lines):
                    if line.startswith('Job Title:'):
                        metadata['title'] = line.replace('Job Title:', '').strip()
                    elif line.startswith('URL:'):
                        metadata['url'] = line.replace('URL:', '').strip()
                    elif line.startswith('Fit Score:'):
                        score_str = line.replace('Fit Score:', '').strip()
                        metadata['fit_score'] = int(score_str.split('/')[0]) if '/' in score_str else 0
                    elif line.startswith('Strengths:'):
                        strengths = line.replace('Strengths:', '').strip()
                        metadata['strengths'] = [s.strip() for s in strengths.split(',') if s.strip()]
                    elif line.startswith('Gaps:'):
                        gaps = line.replace('Gaps:', '').strip()
                        metadata['gaps'] = [g.strip() for g in gaps.split(',') if g.strip()]
                    elif '--- COVER LETTER ---' in line:
                        cover_letter = '\n'.join(lines[i+2:])
                        break
                
                metadata['cover_letter'] = cover_letter.strip()
                cards.append(metadata)
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
    
    # Sort by fit score
    cards.sort(key=lambda x: x.get('fit_score', 0), reverse=True)
    
    # Generate HTML
    html = generate_html(cards)
    
    # Save dashboard
    with open('dashboard.html', 'w') as f:
        f.write(html)

def generate_html(cards: list) -> str:
    """Generate HTML dashboard content"""
    
    html_cards = ''
    for card in cards:
        score = card.get('fit_score', 0)
        title = card.get('title', 'Unknown')
        url = card.get('url', '#')
        strengths = card.get('strengths', [])
        gaps = card.get('gaps', [])
        cover_letter = card.get('cover_letter', '')
        
        # Color based on score
        if score >= 80:
            color = '#10b981'  # green
        elif score >= 65:
            color = '#f59e0b'  # amber
        else:
            color = '#ef4444'  # red
        
        strengths_html = ''.join([f'<span class="tag tag-strength">{s}</span>' for s in strengths])
        gaps_html = ''.join([f'<span class="tag tag-gap">{g}</span>' for g in gaps])
        
        letter_id = f"letter_{len(html_cards)}"
        
        html_cards += f'''
        <div class="card">
            <div class="card-header">
                <div class="score-badge" style="background-color: {color};">{score}</div>
                <div class="card-title">{title}</div>
            </div>
            <a href="{url}" target="_blank" class="card-url">{url}</a>
            <div class="tags">
                {strengths_html}
                {gaps_html}
            </div>
            <button class="toggle-btn" onclick="toggleLetter('{letter_id}')">Show Cover Letter</button>
            <div id="{letter_id}" class="cover-letter" style="display: none;">
                <pre>{cover_letter}</pre>
            </div>
        </div>
        '''
    
    if not html_cards:
        html_cards = '<p style="text-align: center; color: #999;">No jobs processed yet. Run main.py to generate results.</p>'
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Bot Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            color: #1f2937;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 8px;
        }}
        
        .header p {{
            font-size: 1rem;
            color: #666;
        }}
        
        .cards {{
            display: grid;
            gap: 20px;
        }}
        
        .card {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.15);
        }}
        
        .card-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 12px;
        }}
        
        .score-badge {{
            font-size: 1.5rem;
            font-weight: bold;
            color: white;
            width: 60px;
            height: 60px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}
        
        .card-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: #1f2937;
        }}
        
        .card-url {{
            display: block;
            color: #3b82f6;
            text-decoration: none;
            font-size: 0.9rem;
            margin-bottom: 12px;
            word-break: break-all;
        }}
        
        .card-url:hover {{
            text-decoration: underline;
        }}
        
        .tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }}
        
        .tag {{
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        
        .tag-strength {{
            background-color: #d1fae5;
            color: #065f46;
        }}
        
        .tag-gap {{
            background-color: #fee2e2;
            color: #991b1b;
        }}
        
        .toggle-btn {{
            background-color: #3b82f6;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 500;
            transition: background-color 0.2s;
        }}
        
        .toggle-btn:hover {{
            background-color: #2563eb;
        }}
        
        .cover-letter {{
            margin-top: 15px;
            padding: 15px;
            background-color: #f9fafb;
            border-radius: 6px;
            border-left: 4px solid #3b82f6;
        }}
        
        .cover-letter pre {{
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.9rem;
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1.5;
            color: #374151;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #666;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Job Bot Dashboard</h1>
            <p>AI-scored job matches with draft cover letters</p>
        </div>
        
        <div class="cards">
            {html_cards}
        </div>
        
        <div class="footer">
            <p>Generated by Job Bot • Sort by fit score (highest first)</p>
        </div>
    </div>
    
    <script>
        function toggleLetter(id) {{
            const element = document.getElementById(id);
            const btn = event.target;
            if (element.style.display === 'none') {{
                element.style.display = 'block';
                btn.textContent = 'Hide Cover Letter';
            }} else {{
                element.style.display = 'none';
                btn.textContent = 'Show Cover Letter';
            }}
        }}
    </script>
</body>
</html>
'''
    
    return html
