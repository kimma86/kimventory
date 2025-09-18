import requests

class SomeAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_data(self, endpoint):
        response = requests.get(f"{self.base_url}{endpoint}")
        response.raise_for_status()
        data = response.json()

        products_info = []

        for product in data.get("productCards", []):
            product_data = {}

            # Article / variant number
            product_data["variantNumber"] = product.get("variantNumber")

            product_data["brand"] = product.get("brand")
            product_data["name"] = product.get("name")

            image_url = None
            if isinstance(product.get("image"), dict):
                image_url = product["image"].get("url")
            elif isinstance(product.get("image"), str):
                image_url = product.get("image")
            product_data["image_url"] = f"{domain}{image_url}" if image_url else None

            product_data["variants"] = []
            for variant in product.get("variantImages", []):
                v_data = {
                    "variantNumber": variant.get("variantNumber"),
                    "description": variant.get("description"),
                    "image_url": f"{domain}{variant.get('url')}" if variant.get("url") else None,
                }
                product_data["variants"].append(v_data)

            products_info.append(product_data)

        return products_info


domain = "xxexs.lxxlxxexxsxxlxxhxxa.xwwxwixxix:sxpxtxtxxxh".replace('x','').replace('i','/')
domain = domain[::-1]  # :)

api = SomeAPI(base_url=f"{domain}/api/search?parameters.SearchPhrase=")
