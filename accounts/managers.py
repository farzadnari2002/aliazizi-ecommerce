from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, number=None, email=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not number and not email:
            raise ValueError("Users must have an phone number or a email address")

        if email:
            email = self.normalize_email(email)
        if number:
            number = number.strip()

        user = self.model(
            number=number if number else None,
            email=email if email else None
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, number=None, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            number,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
