import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_pos.settings')
django.setup()

from inventory.models import Category, Product, Batch

# Data
categories = ['Analgesic', 'Antibiotic', 'Antihistamine', 'Antacid', 'Vitamin', 'Supplements']
medicines = [
    ('Paracetamol 500mg', 'Analgesic', 5.00, 8.00),
    ('Biogesic 500mg', 'Analgesic', 6.00, 9.00),
    ('Ibuprofen 200mg', 'Analgesic', 8.00, 12.00),
    ('Amoxicillin 500mg', 'Antibiotic', 15.00, 25.00, True),
    ('Augmentin 625mg', 'Antibiotic', 45.00, 60.00, True),
    ('Cephalexin 500mg', 'Antibiotic', 20.00, 30.00, True),
    ('Cetirizine 10mg', 'Antihistamine', 10.00, 15.00),
    ('Loratadine 10mg', 'Antihistamine', 12.00, 18.00),
    ('Kremil-S', 'Antacid', 8.00, 11.00),
    ('Gaviscon Double Action', 'Antacid', 25.00, 35.00),
    ('Vitamin C (Ascorbic Acid)', 'Vitamin', 5.00, 8.00),
    ('Fern-C', 'Vitamin', 8.00, 12.00),
    ('Centrum Silver', 'Vitamin', 15.00, 20.00),
    ('Enervon-C', 'Vitamin', 7.00, 10.00),
    ('Poten-Cee', 'Vitamin', 6.00, 9.00),
    ('Solmux 500mg', 'Supplements', 10.00, 15.00),
    ('Neozep Forte', 'Analgesic', 7.00, 10.00),
    ('Bioflu', 'Analgesic', 7.50, 11.00),
    ('Diatabs', 'Supplements', 6.00, 10.00),
    ('Imodium', 'Supplements', 15.00, 20.00),
]

# Create Categories
cat_objs = {}
for name in categories:
    cat, created = Category.objects.get_or_create(name=name)
    cat_objs[name] = cat
    if created:
        print(f"Created Category: {name}")

# Create Products & Batches
for item in medicines:
    name = item[0]
    cat_name = item[1]
    cost = item[2]
    sell = item[3]
    prescription = item[4] if len(item) > 4 else False
    
    prod, created = Product.objects.get_or_create(
        name=name,
        defaults={
            'category': cat_objs[cat_name],
            'description': f'Generic {cat_name}',
            'requires_prescription': prescription
        }
    )
    
    if created:
        print(f"Created Product: {name}")
        # Add Batch
        Batch.objects.create(
            product=prod,
            batch_number=f"BATCH-2027-{prod.id}",
            expiry_date=date(2027, 12, 31),
            quantity=100,
            cost_price=cost,
            selling_price=sell
        )
        print(f"  > Added Batch: 100 units, Exp 2027")
    else:
        print(f"Skipped {name} (Already exists)")

print("\nDone! Added 20 medicines with stock.")
