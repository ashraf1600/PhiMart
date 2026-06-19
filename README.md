# PhiMart — Django REST API Backend

Lightweight e-commerce backend built with Django & Django REST Framework.

## Project structure (high level)
- `phi_mart/` — project settings and URLs
- `product/` — product catalog, serializers, views, filters
- `order/` — order models, serializers, services
- `users/` — custom user model and auth serializers
- `api/` — project-level API views, permissions, and routes
- `fixtures/` — sample data (`product_data.json`)
- `media/` — uploaded product images

## Features
- RESTful endpoints for products, categories, users, and orders
- Filtering, pagination, and custom permissions
- Fixtures for seeding product data

## Requirements
- Python 3.8+
- See `requirements.txt` for exact package versions

## Quickstart (local)
1. Create and activate a virtual environment:

```bash
python -m venv .env
# Windows
.env\Scripts\activate
# macOS / Linux
source .env/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables (example):

- `DJANGO_SECRET_KEY` — secret key for Django
- `DJANGO_DEBUG` — `True` or `False`
- `DATABASE_URL` — optional (if using a different DB)

You can also edit `phi_mart/settings.py` for local defaults.

4. Run migrations and load fixtures:

```bash
python manage.py migrate
python manage.py loaddata fixtures/product_data.json
```

5. Create a superuser (optional):

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## Media files
Uploaded product images are stored under the `media/` directory. During development, Django serves them when `DEBUG=True` and `MEDIA_URL`/`MEDIA_ROOT` are set in settings.

## Common management commands
- Run tests: `python manage.py test`
- Collect static: `python manage.py collectstatic --noinput`
- Load fixtures: `python manage.py loaddata fixtures/product_data.json`

## API overview
(Adjust paths if your project-level `urls.py` prefixes routes.) Typical endpoints:

- `GET /api/products/` — list products
- `GET /api/products/{id}/` — retrieve product
- `GET /api/categories/` — list categories
- `POST /api/orders/` — create order
- `POST /api/auth/` — authentication endpoints (login/register)

See the app `views.py` and `urls.py` modules for full details.

## Contributing
- Fork the repo, create a branch, and open a PR.
- Add tests for new behavior.
- Keep changes focused and well-documented.

## License
MIT License — see LICENSE file if present.

---

If you'd like, I can add more detailed API docs (endpoints, request/response examples) or a Postman/OpenAPI spec.
