import os
import re
import datetime

class PostManager:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.posts_dir = os.path.join(repo_path, 'content', 'posts')

    def get_posts(self):
        if not os.path.exists(self.posts_dir):
            return []
        
        posts = []
        for f in os.listdir(self.posts_dir):
            if f.endswith('.md'):
                path = os.path.join(self.posts_dir, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    meta = self._parse_frontmatter(content)
                    posts.append({
                        'filename': f,
                        'path': path,
                        'title': meta.get('title', f),
                        'date': meta.get('date', ''),
                        'content': content
                    })
        # Sort by date descending
        posts.sort(key=lambda x: x['date'], reverse=True)
        return posts

    def _parse_frontmatter(self, content):
        meta = {}
        if content.startswith('---'):
            end = content.find('\n---', 3)
            if end != -1:
                yaml_block = content[3:end]
                for line in yaml_block.split('\n'):
                    if ':' in line:
                        key, val = line.split(':', 1)
                        meta[key.strip()] = val.strip()
        return meta

    def save_post(self, filename, content):
        path = os.path.join(self.posts_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    def create_post(self, title):
        slug = title.lower().replace(' ', '-').replace('[^a-z0-9-]', '')
        filename = f"{slug}.md"
        today = datetime.date.today().isoformat()
        
        content = f"""---
title: {title}
date: {today}
excerpt: 
tags: 
---

Write your content here...
"""
        path = os.path.join(self.posts_dir, filename)
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        return filename
