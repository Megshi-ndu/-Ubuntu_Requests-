import requests
import os
import hashlib
from urllib.parse import urlparse

def is_valid_image(response):
    content_type = response.headers.get('Content-Type', '')
    return content_type.startswith('image/')

def get_image_hash(content):
    return hashlib.md5(content).hexdigest()

def fetch_and_save_image(url, saved_hashes):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Check if it's an image
        if not is_valid_image(response):
            print(f"✗ Skipped (Not an image): {url}")
            return

        # Check for duplicates
        image_hash = get_image_hash(response.content)
        if image_hash in saved_hashes:
            print(f"✗ Skipped (Duplicate image): {url}")
            return
        saved_hashes.add(image_hash)

        # Extract filename
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path) or f"image_{image_hash[:8]}.jpg"
        filepath = os.path.join("Fetched_Images", filename)

        # Save image
        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"✓ Saved: {filename} → {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
    except Exception as e:
        print(f"✗ Error for {url}: {e}")

def main():
    print("🖼️ Ubuntu Image Fetcher – Multi-URL Edition")
    print("Mindfully collecting images with safety and care\n")

    # Create directory
    os.makedirs("Fetched_Images", exist_ok=True)

    # Get multiple URLs
    urls = input("https://www.pexels.com/photo/historic-neo-gothic-library-interior-in-scotland-33705332/, https://hotcore.info/act/kareff-092024p.html, https://www.gettyimages.com/detail/photo/choice-variation-concept-royalty-free-image/1475043801?adppopup=true:\n").split(',')

    # Track downloaded image hashes
    saved_hashes = set()

    for url in map(str.strip, urls):
        if url:
            fetch_and_save_image(url, saved_hashes)

    print("\n🌍 Connection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
