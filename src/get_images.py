import requests
from PIL import Image

__url_images = (
    "https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg",
    "https://i.ytimg.com/vi/FSHUxZTsPwU/maxresdefault.jpg",
    "https://content.api.news/v3/images/bin/ac8ca11a6b694e57a4b9730a1f58defc",
    "https://img.freepik.com/premium-photo/caught-camera-car-thief-mask-breaking-into-vehicle-concept-crime-car-theft-surveillance-video-security-footage-criminal-investigation_864588-158259.jpg",
    "https://www.shutterstock.com/image-photo/teenager-girl-aiming-gun-camera-260nw-554655208.jpg",
    "https://media.istockphoto.com/id/1207364112/photo/cctv-view-of-thief-standing-in-dark-alley.jpg?s=612x612&w=0&k=20&c=PUnaoKfegsFarQ-kY19T56Zet69Pk0NzLuwM1QPIxQ8=",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSH2qRfTqvRALFwAb2lneFLFnIMYeZ5dSXlIT8ua_sEtrwIhEB7nEBmQVAtR6EzWY8qAYM",
)


def __get_raw_image(url: str) -> Image.Image:
    return Image.open(requests.get(url, stream=True).raw).convert("RGB")


raw_images = tuple(__get_raw_image(url) for url in __url_images)
