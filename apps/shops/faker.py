from faker import Faker
from apps.shop.models import Categories, Straps, Watches, CustomWatch
from apps.users.models import User
from decimal import Decimal

# Initialize Faker instance
fake = Faker()

# Create fake categories
def create_fake_categories():
    for _ in range(5):  # Generate 5 fake categories
        category_name = fake.word()
        Categories.objects.create(name=category_name)

# Create fake straps
def create_fake_straps():
    categories = Categories.objects.all()  # Get all categories
    for _ in range(10):  # Generate 10 fake straps
        strap_name = fake.word()
        category = fake.random_element(categories)
        Straps.objects.create(name=strap_name, category=category)

# Create fake watches
def create_fake_watches():
    categories = Categories.objects.all()  # Get all categories
    straps = Straps.objects.all()  # Get all straps
    for _ in range(20):  # Generate 20 fake watches
        watch_name = fake.company()
        category = fake.random_element(categories)
        strap = fake.random_element(straps)
        about = fake.text()
        price = Decimal(fake.random_number(digits=3))
        case_color = fake.color_name()
        dial_design = fake.word()
        strap_design = fake.word()
        image = fake.image_url()
        specification = {
            'keys': fake.word(),
            'coating': fake.word(),
            'glass': fake.word(),
            'straps': strap.name,
            'case_size': fake.word(),
            'case_color': case_color,
            'dial_color': fake.color_name(),
            'water_resistance': fake.word(),
            'straps_type': fake.word(),
            'movement': fake.word(),
            'instantaneous_rate': fake.word(),
            'standard_battery_life': fake.word()
        }
        Watches.objects.create(
            name=watch_name,
            category=category,
            about=about,
            price=price,
            case_color=case_color,
            dial_design=dial_design,
            strap_design=strap_design,
            image=image,
            specification=specification
        )

# Create fake custom watches
def create_fake_custom_watches():
    users = User.objects.all()  # Get all users
    for _ in range(10):  # Generate 10 fake custom watches
        user = fake.random_element(users)
        case_color = fake.color_name()
        strap_color = fake.color_name()
        dial_design = fake.word()
        extra_strap = fake.boolean()
        laser_engraving = fake.boolean()
        price = Decimal(fake.random_number(digits=3))
        image = fake.image_url()
        CustomWatch.objects.create(
            user=user,
            case_color=case_color,
            strap_color=strap_color,
            dial_design=dial_design,
            extra_strap=extra_strap,
            laser_engraving=laser_engraving,
            price=price,
            image=image
        )

# Run the fake data creation functions
if __name__ == "__main__":
    create_fake_categories()
    create_fake_straps()
    create_fake_watches()
    create_fake_custom_watches()
    print("Fake data has been successfully created.")

