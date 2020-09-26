import re

class categorizer:
    def __init__(self):
        self.samples = {
            "name": r'^[А-ЯЁ][а-яё\-]+\s([А-ЯЁ][а-яё\-]+)(\.|\s)\s*([А-ЯЁ][а-яё\-\.]+)$',
            "inn": r'^[\d+]{10,12}$',
			"phone_number": r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$',
            "post_index": r'\d{6}',
            "email": r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',
            "website": r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"
        }

    def get_category(self, data):
        categorized = {}

        for d in data.items():
            categorized[self.define_category(d[1])] = d[0]

        return categorized

    def define_category(self, data):
        for sample in self.samples.items():
            for d in data:
                match = re.search(sample[1], str(d))
                if match:
                    return sample[0]
