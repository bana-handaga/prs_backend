from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Departemen'
        verbose_name_plural = 'Departemen'

    def __str__(self):
        return f'{self.code} - {self.name}'


class UserManager(BaseUserManager):
    def create_user(self, email, employee_id, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Email wajib diisi')
        if not employee_id:
            raise ValueError('ID Pegawai wajib diisi')
        email = self.normalize_email(email)
        user = self.model(email=email, employee_id=employee_id, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, employee_id, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)
        return self.create_user(email, employee_id, full_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        SUPERVISOR = 'supervisor', 'Supervisor'
        STAFF = 'staff', 'Staff'

    employee_id = models.CharField(max_length=20, unique=True, verbose_name='NIP/ID Pegawai')
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, verbose_name='Nama Lengkap')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='No. HP')
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='staff', verbose_name='Departemen'
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STAFF, verbose_name='Peran')
    photo_profile = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name='Foto Profil')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['employee_id', 'full_name']

    class Meta:
        ordering = ['full_name']
        verbose_name = 'Pengguna'
        verbose_name_plural = 'Pengguna'

    def __str__(self):
        return f'{self.employee_id} - {self.full_name}'

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_supervisor(self):
        return self.role in (self.Role.ADMIN, self.Role.SUPERVISOR)
