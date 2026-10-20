import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def scrape_website(url):

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        soup = BeautifulSoup(response.text, "html.parser")

        # 1. Website Title
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else ""

        # 2. Meta Description
        meta_tag = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        meta_description = (
            meta_tag.get("content", "").strip()
            if meta_tag else ""
        )

        # 3. H1 Count
        h1_count = len(soup.find_all("h1"))

        # 4. Images
        images = soup.find_all("img")
        total_images = len(images)

        images_without_alt = sum(
            1 for img in images
            if not img.get("alt", "").strip()
        )

        # 5. HTTPS Check
        https = urlparse(response.url).scheme == "https"

        # 6. Mobile Viewport Check
        viewport = soup.find(
            "meta",
            attrs={"name": "viewport"}
        )

        mobile_viewport = viewport is not None

        # 7. Broken Links Check
        links = soup.find_all("a", href=True)

        unique_links = set()

        for link in links:
            href = link["href"].strip()

            if not href:
                continue

            if href.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue

            full_url = urljoin(response.url, href)
            parsed_url = urlparse(full_url)

            if parsed_url.scheme in ("http", "https"):
                unique_links.add(full_url)

        broken_links = 0

        for link_url in unique_links:

            try:
                result = requests.head(
                    link_url,
                    timeout=5,
                    allow_redirects=True,
                    headers={"User-Agent": "Mozilla/5.0"}
                )

                # Some websites do not support HEAD requests.
                if result.status_code in (403, 405):
                    result = requests.get(
                        link_url,
                        timeout=5,
                        allow_redirects=True,
                        headers={"User-Agent": "Mozilla/5.0"},
                        stream=True
                    )

                if result.status_code >= 400:
                    broken_links += 1

            except requests.RequestException:
                broken_links += 1

        # 8. Return Audit Data
        audit_data = {
            "url": response.url,
            "status_code": response.status_code,
            "title": title,
            "meta_description": meta_description,
            "h1_count": h1_count,
            "total_images": total_images,
            "images_without_alt": images_without_alt,
            "https": https,
            "mobile_viewport": mobile_viewport,
            "total_links": len(unique_links),
            "broken_links": broken_links
        }

        return audit_data

    except requests.RequestException as error:
        print("Website access karne mein problem:", error)
        return None