# Step 1: Install frontend dependencies
npm install

# Step 2: Build Tailwind CSS with pruning and minification
npx tailwindcss -i ./dashboard/static/dashboard/css/input.css -o ./dashboard/static/dashboard/css/min-tailwind.css --minify

# step3: installing requirements
pip install -r requirements.txt

# Step 4: Collect static files for Django
python manage.py collectstatic --no-input