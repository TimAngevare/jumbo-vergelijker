class Product:
    def __init__(self, name : str, url : str, image_url : str, id : int) -> None:
        self.id = id
        self.name = name
        self.url = url
        self.image_url = image_url