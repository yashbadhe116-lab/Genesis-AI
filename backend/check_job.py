from replicate.client import Client
from app.core.config import settings
c = Client(api_token=settings.REPLICATE_API_TOKEN)
p = c.predictions.get('k0e2whtbksrmw0cz13qv1sqvew')
print(f'Status: {p.status}')
print(f'Output: {p.output}')

