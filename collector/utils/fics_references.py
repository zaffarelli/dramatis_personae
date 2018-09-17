from django.db import models
from django.contrib import admin
from datetime import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import hashlib
from collector import fs_fics7
from .utils import write_pdf



