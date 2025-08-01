import os
import re
import shutil

# Paths
posts_dir = "C:\\Projects\\tempus-blowfish\\content\\"
attachments_dir = "Z:\\documents\\obsidian\\Mark\\99 - Meta\\assets"
static_images_dir = "C:\\Projects\\tempus-blowfish\\static\\images\\"

# Step 1: Process each markdown file in the posts directory (recursively)
for root, dirs, files in os.walk(posts_dir):
    for filename in files:
        if filename.endswith(".md"):
            filepath = os.path.join(root, filename)
            
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
            
            # Step 2: Find all image links in the format ![[image.png]] or ![[image.png|size]]
            images = re.findall(r'!\[\[([^]]*\.(jpe?g|png|gif|bmp|webp))(\|[^\]]*)?\]\]', content)
            
            # Step 3: Replace image links and ensure URLs are correctly formatted
            for image_tuple in images:
                # Extract the filename and size specification from the tuple
                image = image_tuple[0]
                size_spec = image_tuple[2] if len(image_tuple) > 2 else ""
                
                # Create the original obsidian format to search for
                original_obsidian = f"![[{image}{size_spec}]]"
                
                # Prepare the Markdown-compatible link with %20 replacing spaces
                markdown_image = f"![{image}](/images/{image.replace(' ', '%20')})"
                content = content.replace(original_obsidian, markdown_image)
                print("Processing: " + filename)
                print("  -> Image: " + image)
                # Step 4: Copy the image to the Hugo static/images directory if it exists
                image_source = os.path.join(attachments_dir, image)
                if os.path.exists(image_source):
                    shutil.copy(image_source, static_images_dir)
    
            # Step 5: Write the updated content back to the markdown file
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)

print("Markdown files processed and images copied successfully.")
