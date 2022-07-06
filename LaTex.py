import urllib.parse
import requests

def save_image_from_latex(latex):
    if latex == "":
        raise Exception("Empty input!")

    compiled_image = open("images/compiled_latex.png", "wb+")
    encoded = urllib.parse.quote(latex)

    compiled_image.write(requests.get(f"https://chart.apis.google.com/chart?cht=tx&chl={urllib.parse.quote(latex)}").content)

    compiled_image.close()
