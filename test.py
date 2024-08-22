import csv
import re

def extract_content(text, start_tag, end_tag):
    pattern = f"{re.escape(start_tag)}(.*?){re.escape(end_tag)}"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""

def parse_article(article_text):
    title = extract_content(article_text, "Title : ", "\n")
    date = extract_content(article_text, "Date: ", "\n")
    author = extract_content(article_text, "Author: ", "\n")
    category = extract_content(article_text, "Category: ", "\n")
    reading_time = extract_content(article_text, "Reading Time: ", "\n")
    views = extract_content(article_text, "Vues: ", "\n")
    tags = extract_content(article_text, "Tags: ", "\n")
    image = extract_content(article_text, "Image: ", "\n")
    content = extract_content(article_text, "<content>", "</content>")
    
    # Nettoyer le contenu
    content = re.sub(r'\*\*h1\*\*', '', content)
    content = re.sub(r'\*\*h2\*\*', '', content)
    
    return {
        "title": title,
        "date": date,
        "author": author,
        "category": category,
        "reading_time": reading_time,
        "views": views,
        "tags": tags,
        "image": image,
        "content": content
    }

def main():
    input_file = "articles.txt"
    output_file = "wordpress_import.csv"
    
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    articles = content.split("_________________________________________________________")
    
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ["title", "date", "author", "category", "reading_time", "views", "tags", "image", "content"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for article in articles:
            if article.strip():
                parsed_article = parse_article(article)
                writer.writerow(parsed_article)
    
    print(f"Fichier CSV '{output_file}' créé avec succès.")

if __name__ == "__main__":
    main()