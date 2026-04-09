class ContextFormatter:

    def __init__(self, necessary_props: list[str]=None):
        if necessary_props is None:
            self.necessary_props = ['ProductName', 'Brand', 'CategoryName', 'Price', 'Description', 'IsAvailable', 'StockQuantity', 'OrderID', 'Status', 'TotalAmount', 'OrderDate']
        else:
            self.necessary_props = necessary_props

    def format(self, results: dict) -> str:
        documents = results.get('documents', [[]])[0]
        if not documents:
            return 'No relevant documents found.'
        context_parts = []
        for doc in documents:
            lines = []
            if isinstance(doc, dict):
                for prop in self.necessary_props:
                    if prop in doc:
                        lines.append(f'{prop}: {doc[prop]}')
            else:
                for prop in self.necessary_props:
                    val = self._extract_prop(doc, prop)
                    if val != 'N/A':
                        lines.append(f'{prop}: {val}')
            if lines:
                context_parts.append('\n'.join(lines))
        return '\n\n'.join(context_parts)

    def _extract_prop(self, raw_text: str, prop: str) -> str:
        for segment in raw_text.split('\n'):
            if segment.strip().startswith(f'{prop}:'):
                return segment.split(f'{prop}:')[1].strip()
        return 'N/A'