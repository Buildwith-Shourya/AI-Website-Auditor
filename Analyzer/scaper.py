
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def scrape_website(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; WebsiteAuditor/1.0)"
    }

    try:
        response = requests.get(
            url,
            timeout=15,
            headers=headers
        )
        response.raise_for_status()

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

        # 4. Images and ALT Text
        images = soup.find_all("img")
        total_images = len(images)

        images_without_alt = sum(
            1 for img in images
            if not img.get("alt", "").strip()
        )

        # 5. HTTPS Check
        https = urlparse(response.url).scheme == "https"

        # 6. Mobile Viewport
        viewport = soup.find(
            "meta",
            attrs={"name": "viewport"}
        )
        mobile_viewport = viewport is not None

        # 7. Broken Links Check
        # Check a maximum of 10 unique links to reduce scan time.
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

        links_to_check = list(unique_links)[:10]

        broken_links = 0
        unverified_links = 0

        for link_url in links_to_check:
            try:
                # GET is used because many sites restrict HEAD requests.
                result = requests.get(
                    link_url,
                    timeout=5,
                    allow_redirects=True,
                    headers=headers,
                    stream=True
                )

                status = result.status_code
                result.close()

                # Count only clear "not found" responses as broken.
                # 403, 429 and server errors may be temporary or blocked.
                if status in (404, 410):
                    broken_links += 1
                elif status >= 400:
                    unverified_links += 1

            except requests.RequestException:
                # A timeout or connection failure does not prove
                # that a link is broken.
                unverified_links += 1

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
            "checked_links": len(links_to_check),
            "broken_links": broken_links,
            "unverified_links": unverified_links
        }

        return audit_data

    except requests.RequestException as error:
        print("Website access karne mein problem:", error)
        return None
