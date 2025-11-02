from django.db import models

# Create your models here.
class XrplWallet(models.Model):
    """
    Represents a single XRPL wallet entry in the database.
    """
    # A character field for the user's name, with a max length of 100
    username = models.CharField(max_length=100)
    
    # A character field for the wallet address, max 35 chars.
    # We set unique=True to ensure no two entries have the same address.
    wallet_address = models.CharField(max_length=35, unique=True)
    
    # A fixed-precision decimal field for the balance.
    # This is much better for currency than a FloatField to avoid rounding errors.
    # max_digits allows 20 total numbers.
    # decimal_places stores up to 6 places, standard for XRP drops.
    balance = models.DecimalField(max_digits=20, decimal_places=6, default=0.0)

    def __str__(self):
        """
        Returns a human-readable string for the object.
        This is what will be shown in the Django admin list.
        """
        return f"{self.username} ({self.wallet_address})"