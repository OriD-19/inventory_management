from flask import Blueprint, render_template, redirect, url_for, flash, request

from inventory_app import db

from inventory_app.alerts.models import Alert


