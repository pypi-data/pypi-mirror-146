import requests


class Element:
    def __init__(self, name: str, options: dict, content):
        self.name = name
        self.options = options
        self.content = content

class Parse:
    def __init__(self, url: str):
        self.url = url
        self.res = requests.get(self.url)
        self.text = self.res.text
        self.lines = self.text.split("\n")
    
    def update(self, url: str = None):
        if url: self.url = url
        self.res = requests.get(self.url)
        self.text = self.res.text
        self.lines = self.text.split("\n")

    def get_title(self) -> str:
        for i in self.lines:
            if "title" in i:
                return i.split(">")[1].split("<")[0]
    
    def get_spaces(self, text: str) -> int:
        length = len(text.split("\n"))
        out = 0

        if length > 1 or length < 1: return

        for i in text.split("\n")[0]:
            if i == " ":
                out += 1
            if i == "<":
                break
        
        return out

    def get_options(self, line: str, element: str) -> dict:
        options = line.replace(" = ", "=").split("<")[1].split(">")[0].replace(element, "").split()

        out = {}

        for option in options:
            out[option.split("=")[0]] = option.split("=")[1].replace('"', '').replace("'", "")

        return out

    def find_elements(self, lines: list, element: str, spaces: int) -> list:
        if lines == []: return

        if f"</{element}>" in lines[0]:
            return lines[0].split(">")[1].split("<")[0]
        
        for i in range(len(lines)):
            _spaces = self.get_spaces(lines[i])

            if f"</{element}>" in lines[i] and spaces == _spaces:
                return lines[1:i]

    def find_by_element_name(self, element: str) -> list:
        elements = []
        
        for i in range(len(self.lines)):
            if f"<{element}" in self.lines[i]:
                spaces = self.get_spaces(self.lines[i])
                content = self.find_elements(self.lines[i:], element, spaces)
                options = self.get_options(self.lines[i], element)

                elements.append(Element(element, options, content))
        
        return elements

    def find_by_class(self, class_name: str) -> list:
        elements = []

        for i in range(len(self.lines)):
            if f"class='{class_name}'" in self.lines[i] or f'class="{class_name}"' in self.lines[i]:
                name = self.lines[i].split("<")[1].split()[0]
                spaces = self.get_spaces(self.lines[i])
                content = self.find_elements(self.lines[i:], name, spaces)
                options = self.get_options(self.lines[i], name)

                elements.append(Element(name, options, content))
                
        return elements
                
    def find_by_id(self, id: str) -> list:
        elements = []

        for i in range(len(self.lines)):
            if f"id='{id}'" in self.lines[i] or f'id="{id}"' in self.lines[i]:
                name = self.lines[i].split("<")[1].split()[0]
                spaces = self.get_spaces(self.lines[i])
                content = self.find_elements(self.lines[i:], name, spaces)
                options = self.get_options(self.lines[i], name)

                elements.append(Element(name, options, content))
                
        return elements

    def show_document(self) -> str:
        return self.text