from django.db import models
from api.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

class Category(models.Model):

    """
    Purpose: To organize products into hierarchical categories for easier navigation and filtering.
    Example: "Dog Food" category might contain subcategories like "Dry Food", "Wet Food", and "Treats".
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name

class Brand(models.Model):

    """
    Purpose: To represent the manufacturers or labels of products, allowing customers to filter by brand preference.
    Example: "Pedigree" or "Royal Canin" would be brands of dog food.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brand_logos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    
    """
    Purpose: To define the core details of a product, including its name, description, brand, category, price, and availability.
    Example: "Pedigree Adult Chicken & Rice Dog Food" would be a product.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    """
    Purpose: To represent different variations of a product, such as different sizes, weights,
    or flavors.
    Example: "Pedigree Adult Chicken & Rice Dog Food" might have variants of 1kg, 2kg, and 5kg.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=50)  # e.g., "8gm", "20gm"
    weight = models.DecimalField(max_digits=10, decimal_places=2)  # in grams
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    sku = models.CharField(max_length=100, unique=True)

    def update_stock(self, quantity_change, action, reason, user):
        self.stock += quantity_change
        self.save()
        InventoryLog.objects.create(
            product_variant=self,
            quantity_change=quantity_change,
            action=action,
            reason=reason,
            performed_by=user
        )
        
        # Check if stock alert should be triggered
        stock_alert = StockAlert.objects.filter(product_variant=self).first()
        if stock_alert:
            stock_alert.check_stock()

    def add_stock(self, quantity, reason, user):
        self.update_stock(quantity, 'add', reason, user)

    def remove_stock(self, quantity, reason, user):
        self.update_stock(-quantity, 'remove', reason, user)

    def __str__(self):
        return f"{self.product.name} - {self.size}"

class ProductImage(models.Model):
    """
    Purpose: To provide visual representation of products, enhancing the shopping experience.
    Example: Images of a dog food bag from different angles.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"

class PetType(models.Model):
    """
    Purpose: To categorize pets into broad types, such as "Dog", "Cat", or "Bird", for product filtering and recommendations.
    Example: "Dog" would be a pet type.
    """
    name = models.CharField(max_length=50)  # e.g., "Dog", "Cat", "Bird"

    def __str__(self):
        return self.name

class Breed(models.Model):
    """
    Purpose: To specify the specific breed of a pet, allowing for more targeted product recommendations.
    Example: "Golden Retriever" or "Persian" or "Husky" would be breeds.
    """

    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE, related_name='breeds')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.pet_type.name} - {self.name}"

class ProductPetCompatibility(models.Model):
    """
    Purpose: To indicate which products are suitable for different pet types, breeds, or life stages.
    Example: A "Puppy" life stage might have recommendations for specific dog food formulas.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pet_compatibilities')
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE)
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True, blank=True)
    life_stage = models.CharField(max_length=50, blank=True)  # e.g., "Puppy", "Adult", "Senior"

    class Meta:
        unique_together = ('product', 'pet_type', 'breed', 'life_stage')

    def __str__(self):
        return f"{self.product.name} - {self.pet_type.name}"

class Order(models.Model):

    """
    Purpose: To store information about customer orders, including the items purchased, total amount, and status.
    Example: An order might include multiple products, quantities, and shipping details.
    """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')  # e.g., "Pending", "Shipped", "Delivered"

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):

    """
    Purpose: To detail the specific items included in an order, including quantity and price.
    Example: A single order might contain two items: 1kg of dog food and 1 cat toy.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product_variant.product.name} ({self.product_variant.size}) in Order {self.order.id}"


class Wishlist(models.Model):

    """
    Purpose: To allow customers to save products they're interested in for later purchase.
    Example: A customer might add a premium dog bed to their wishlist.
    """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.user.username
    
class WishlistItem(models.Model):

    """
    Purpose: To represent individual items added to a wishlist.
    Example: A specific dog bed added to a wishlist.
    """

    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product

class Review(models.Model):

    """
    Purpose: To collect customer feedback on products, helping potential buyers make informed decisions.
    Example: A customer might leave a positive review for a dog food product.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified_purchase = models.BooleanField(default=False)
    helpfulness_votes = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.user.username}'s review of {self.product.name}"

class Discount(models.Model):
    
    """
    Purpose: To offer promotional discounts or coupons to customers.
    Example: A "20% OFF" discount code for all dog food purchases.
    """

    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]

    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def get_discount_amount(self, total_amount):
        if self.discount_type == 'percentage':
            discount_amount = (self.value / 100) * total_amount
        else:
            discount_amount = min(self.value, total_amount)
        return discount_amount
    
    def get_discount_type_display(self):
        if self.discount_type == 'percentage':
            return f"{self.value}%"
        elif self.discount_type == 'fixed':
            return f"₹{self.value}"
        return None

    def __str__(self):
        return f"{self.code} - {self.get_discount_type_display()}"

    def is_valid(self):
        now = timezone.now()
        return (
            self.is_active and
            self.start_date <= now <= self.end_date and
            (self.usage_limit is None or self.usage_limit > 0)
        )

class Promotion(models.Model):
    
    """
    Purpose:To create marketing campaigns and promotions for specific products or categories.
    Example: A "Summer Sale" promotion offering discounts on all pet accessories.
    """

    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    banner_image = models.ImageField(upload_to='promotion_banners/', null=True, blank=True)
    products = models.ManyToManyField(Product, related_name='promotions', blank=True)
    categories = models.ManyToManyField(Category, related_name='promotions', blank=True)

    def __str__(self):
        return self.name

class PetProfile(models.Model):
    
    """
    Purpose: To allow users to create profiles for their pets, storing information like breed, age, and dietary preferences.
    Example: A user might create a profile for their "Golden Retriever" dog.
    """

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='pet_profiles')
    name = models.CharField(max_length=100)
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE)
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in kg
    allergies = models.TextField(blank=True)
    medical_conditions = models.TextField(blank=True)
    dietary_preferences = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='pet_profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.pet_type.name})"

    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return (today - self.date_of_birth).days // 365
        return None

class InventoryLog(models.Model):
    """
    Purpose: To track changes in product stock levels, including additions, removals, and adjustments.
    Example: A log entry recording the addition of 100 bags of dog food to the inventory.
    """
    ACTION_CHOICES = [
        ('add', 'Stock Added'),
        ('remove', 'Stock Removed'),
        ('adjust', 'Stock Adjusted'),
    ]

    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='inventory_logs')
    quantity_change = models.IntegerField()
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    reason = models.TextField()
    performed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_action_display()} for {self.product_variant} ({self.quantity_change})"

class StockAlert(models.Model):
    """
    Purpose: To monitor stock levels for products and trigger alerts when they fall below a specified threshold.
    Example: An alert might be triggered when the stock of a popular cat food brand drops below 10 units.
    """
    product_variant = models.OneToOneField(ProductVariant, on_delete=models.CASCADE, related_name='stock_alert')
    low_stock_threshold = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    last_triggered = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Stock Alert for {self.product_variant}"

    def check_stock(self):
        if self.is_active and self.product_variant.stock <= self.low_stock_threshold:
            self.last_triggered = timezone.now()
            self.save()
            return True
        return False
