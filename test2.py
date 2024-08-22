import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import locale

# Définir la locale française
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

def parse_date(date_str):
    date_formats = ["%d %b %Y", "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Format de date non reconnu : {date_str}")

def csv_to_wordpress_xml(csv_file, xml_file):
    rss = ET.Element("rss", version="2.0",
                     attrib={"xmlns:excerpt": "http://wordpress.org/export/1.2/excerpt/",
                             "xmlns:content": "http://purl.org/rss/1.0/modules/content/",
                             "xmlns:wfw": "http://wellformedweb.org/CommentAPI/",
                             "xmlns:dc": "http://purl.org/dc/elements/1.1/",
                             "xmlns:wp": "http://wordpress.org/export/1.2/"})
    
    channel = ET.SubElement(rss, "channel")
    
    ET.SubElement(channel, "title").text = "Ziegler & Associés"
    ET.SubElement(channel, "link").text = "https://www.ziegler-associes.com"
    ET.SubElement(channel, "description").text = "Cabinet d'avocats spécialisés Paris 16"
    ET.SubElement(channel, "pubDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
    ET.SubElement(channel, "language").text = "fr-FR"
    ET.SubElement(channel, "wp:wxr_version").text = "1.2"
    ET.SubElement(channel, "wp:base_site_url").text = "https://www.ziegler-associes.com"
    ET.SubElement(channel, "wp:base_blog_url").text = "https://www.ziegler-associes.com"

    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        
        for row in csv_reader:
            item = ET.SubElement(channel, "item")
            
            ET.SubElement(item, "title").text = row['title']
            ET.SubElement(item, "link").text = f"https://www.ziegler-associes.com/{row['title'].lower().replace(' ', '-')}"
            
            try:
                date_obj = parse_date(row['date'])
                formatted_date = date_obj.strftime("%a, %d %b %Y %H:%M:%S +0000")
                ET.SubElement(item, "pubDate").text = formatted_date
                ET.SubElement(item, "wp:post_date").text = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                ET.SubElement(item, "wp:post_date_gmt").text = date_obj.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError as e:
                print(f"Erreur de date pour l'article '{row['title']}': {e}")
                continue

            ET.SubElement(item, "dc:creator").text = row['author']
            ET.SubElement(item, "guid", isPermaLink="false").text = f"https://www.ziegler-associes.com/?p={csv_reader.line_num}"
            
            content = ET.SubElement(item, "content:encoded")
            content.text = ET.CDATA(row['content'])
            
            ET.SubElement(item, "wp:comment_status").text = "open"
            ET.SubElement(item, "wp:ping_status").text = "open"
            ET.SubElement(item, "wp:post_name").text = row['title'].lower().replace(' ', '-')
            ET.SubElement(item, "wp:status").text = "publish"
            ET.SubElement(item, "wp:post_parent").text = "0"
            ET.SubElement(item, "wp:menu_order").text = "0"
            ET.SubElement(item, "wp:post_type").text = "post"
            ET.SubElement(item, "wp:post_password").text = ""
            ET.SubElement(item, "wp:is_sticky").text = "0"
            
            category = ET.SubElement(item, "category", domain="category", nicename=row['category'].lower().replace(' ', '-'))
            category.text = row['category']
            
            for tag in row['tags'].split(','):
                tag_elem = ET.SubElement(item, "category", domain="post_tag", nicename=tag.strip().lower().replace(' ', '-'))
                tag_elem.text = tag.strip()

    xml_str = minidom.parseString(ET.tostring(rss)).toprettyxml(indent="  ")
    
    with open(xml_file, 'w', encoding='utf-8') as file:
        file.write(xml_str)

# Utilisation du script
csv_to_wordpress_xml('articles2.csv', 'wordpress_export.xml')